use std::net::TcpListener;
use std::io::{Read, Write, BufReader};
use std::sync::Arc;
use std::thread;
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::collections::HashMap;

use rustls::pki_types::{CertificateDer, PrivateKeyDer};
use rustls::{ServerConfig, ServerConnection, StreamOwned};

#[derive(Debug, Clone)]
pub struct HttpRequest {
    pub method: String,
    pub path: String,
    pub body: String,
}

#[derive(Debug, Clone)]
pub struct HttpResponse {
    pub status: u16,
    pub content_type: String,
    pub body: String,
}

impl HttpResponse {
    pub fn json(status: u16, body: &str) -> Self {
        Self {
            status,
            content_type: "application/json; charset=utf-8".to_string(),
            body: body.to_string(),
        }
    }

    pub fn html(status: u16, body: &str) -> Self {
        Self {
            status,
            content_type: "text/html; charset=utf-8".to_string(),
            body: body.to_string(),
        }
    }

    pub fn text(status: u16, body: &str) -> Self {
        Self {
            status,
            content_type: "text/plain; charset=utf-8".to_string(),
            body: body.to_string(),
        }
    }
}

pub struct HttpServer {
    pub port: u16,
    pub is_tls: bool,
    pub tls_cert: Option<String>,
    pub tls_key: Option<String>,
}

impl HttpServer {
    pub fn new(port: u16) -> Self {
        Self { 
            port,
            is_tls: false,
            tls_cert: None,
            tls_key: None,
        }
    }

    pub fn new_https(port: u16, cert: Option<String>, key: Option<String>) -> Self {
        Self {
            port,
            is_tls: true,
            tls_cert: cert,
            tls_key: key,
        }
    }

    pub fn listen<F>(&self, handler: F) 
    where F: Fn(HttpRequest) -> HttpResponse + Send + Sync + 'static {
        let bind_addr = format!("0.0.0.0:{}", self.port);
        let listener = match TcpListener::bind(&bind_addr) {
            Ok(l) => l,
            Err(e) => {
                eprintln!("\n[AAYU Server Error] Could not bind to port {}: {}", self.port, e);
                eprintln!("  -> Reason: {}", e);
                eprintln!("  -> Fix: Either terminate the existing process or use '--port <ANOTHER_PORT>'\n");
                std::process::exit(1);
            }
        };

        let protocol = if self.is_tls { "https" } else { "http" };
        println!("==================================================");
        println!("AAYU Native Web Server running on port {}", self.port);
        println!("Accepting connections at {}://localhost:{}", protocol, self.port);
        if self.is_tls {
            println!("Security: Native TLS 1.3 / HTTPS Encryption ACTIVE");
            if self.tls_cert.is_none() {
                println!("TLS Mode: Auto-generated ephemeral dev certificate (localhost)");
            } else {
                println!("TLS Mode: Custom PEM Certificate & Private Key");
            }
        }
        println!("==================================================");

        let tls_config: Option<Arc<ServerConfig>> = if self.is_tls {
            Some(Arc::new(self.init_tls_config()))
        } else {
            None
        };

        let handler = Arc::new(handler);

        for stream in listener.incoming() {
            match stream {
                Ok(mut stream) => {
                    let _ = stream.set_nodelay(true);
                    let handler_clone = Arc::clone(&handler);
                    let tls_config_clone = tls_config.clone();

                    thread::spawn(move || {
                        let _ = catch_unwind(AssertUnwindSafe(|| {
                            if let Some(tls_cfg) = tls_config_clone {
                                if let Ok(conn) = ServerConnection::new(tls_cfg) {
                                    let mut tls_stream = StreamOwned::new(conn, stream);
                                    Self::handle_connection(&mut tls_stream, &handler_clone);
                                }
                            } else {
                                Self::handle_connection(&mut stream, &handler_clone);
                            }
                        }));
                    });
                }
                Err(e) => {
                    eprintln!("[AAYU Server] TCP accept error: {}", e);
                }
            }
        }
    }

    fn init_tls_config(&self) -> ServerConfig {
        let provider = Arc::new(rustls::crypto::ring::default_provider());
        let builder = ServerConfig::builder_with_provider(provider)
            .with_safe_default_protocol_versions()
            .expect("Failed to initialize safe TLS protocol versions");

        if let (Some(cert_path), Some(key_path)) = (&self.tls_cert, &self.tls_key) {
            let cert_file = std::fs::File::open(cert_path)
                .unwrap_or_else(|e| panic!("Cannot open TLS certificate file '{}': {}", cert_path, e));
            let mut cert_reader = BufReader::new(cert_file);
            let certs: Vec<CertificateDer<'static>> = rustls_pemfile::certs(&mut cert_reader)
                .collect::<Result<Vec<_>, _>>()
                .unwrap_or_else(|e| panic!("Failed to parse TLS certificate '{}': {}", cert_path, e));

            let key_file = std::fs::File::open(key_path)
                .unwrap_or_else(|e| panic!("Cannot open TLS private key file '{}': {}", key_path, e));
            let mut key_reader = BufReader::new(key_file);
            let key: PrivateKeyDer<'static> = rustls_pemfile::private_key(&mut key_reader)
                .unwrap_or_else(|e| panic!("Failed to read private key from '{}': {}", key_path, e))
                .unwrap_or_else(|| panic!("No valid private key found in '{}'", key_path));

            builder
                .with_no_client_auth()
                .with_single_cert(certs, key)
                .expect("Failed to configure custom TLS certificate")
        } else {
            let subject_alt_names = vec!["localhost".to_string(), "127.0.0.1".to_string()];
            let certified_key = rcgen::generate_simple_self_signed(subject_alt_names)
                .expect("Failed to generate ephemeral dev TLS certificate");

            let cert_der = certified_key.cert.der().to_vec();
            let key_der = certified_key.signing_key.serialize_der();

            let certs = vec![CertificateDer::from(cert_der)];
            let private_key = PrivateKeyDer::Pkcs8(key_der.into());

            builder
                .with_no_client_auth()
                .with_single_cert(certs, private_key)
                .expect("Failed to configure ephemeral dev TLS certificate")
        }
    }

    fn handle_connection<S: Read + Write>(stream: &mut S, handler: &Arc<impl Fn(HttpRequest) -> HttpResponse>) {
        let mut buffer = [0u8; 8192];
        if let Ok(bytes_read) = stream.read(&mut buffer) {
            if bytes_read == 0 { return; }
            let raw_request = String::from_utf8_lossy(&buffer[..bytes_read]);

            let req = Self::parse_request(&raw_request);

            let res = if req.method == "OPTIONS" {
                HttpResponse {
                    status: 204,
                    content_type: "text/plain".to_string(),
                    body: String::new(),
                }
            } else {
                handler(req)
            };

            let status_text = match res.status {
                200 => "OK",
                201 => "Created",
                204 => "No Content",
                400 => "Bad Request",
                404 => "Not Found",
                500 => "Internal Server Error",
                _ => "Unknown",
            };

            let body_bytes = res.body.as_bytes();
            let response = format!(
                "HTTP/1.1 {} {}\r\nContent-Type: {}\r\nContent-Length: {}\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS\r\nAccess-Control-Allow-Headers: *\r\nConnection: close\r\n\r\n{}",
                res.status,
                status_text,
                res.content_type,
                body_bytes.len(),
                res.body
            );

            let _ = stream.write_all(response.as_bytes());
            let _ = stream.flush();
        }
    }

    fn parse_request(raw: &str) -> HttpRequest {
        let mut lines = raw.lines();
        let first_line = lines.next().unwrap_or("GET / HTTP/1.1");
        let mut parts = first_line.split_whitespace();
        let method = parts.next().unwrap_or("GET").to_string();
        let path = parts.next().unwrap_or("/").to_string();

        let mut body = String::new();
        let mut in_body = false;
        for line in lines {
            if in_body {
                body.push_str(line);
                body.push('\n');
            } else if line.trim().is_empty() {
                in_body = true;
            }
        }

        HttpRequest { 
            method, 
            path, 
            body: body.trim_end().to_string() 
        }
    }
}

/// Dynamically extracts routes and their corresponding response payloads from an AAYU source file.
pub fn extract_routes_from_source(source: &str) -> HashMap<String, (String, String)> {
    let mut routes: HashMap<String, (String, String)> = HashMap::new();
    let lines: Vec<&str> = source.lines().collect();
    let mut i = 0;

    while i < lines.len() {
        let trimmed = lines[i].trim();
        if trimmed.starts_with("route ") || trimmed.starts_with("route\"") || trimmed.starts_with("route'") {
            let path_part = trimmed.trim_start_matches("route").trim();
            let path = if (path_part.starts_with('"') && path_part.ends_with('"')) ||
                          (path_part.starts_with('\'') && path_part.ends_with('\'')) {
                path_part[1..path_part.len()-1].to_string()
            } else {
                let p = path_part.split_whitespace().next().unwrap_or("/");
                p.trim_matches('"').trim_matches('\'').to_string()
            };

            let mut block_lines: Vec<String> = Vec::new();
            i += 1;
            let mut depth = 1;
            while i < lines.len() && depth > 0 {
                let l = lines[i].trim();
                if l == "end" {
                    depth -= 1;
                    if depth == 0 { break; }
                } else if l.starts_with("route ") || l == "get" || l == "post" || l == "put" || l == "delete" || l.starts_with("action ") {
                    depth += 1;
                }
                block_lines.push(lines[i].to_string());
                i += 1;
            }

            let block_str = block_lines.join("\n");
            let mut vars: HashMap<String, String> = HashMap::new();
            let mut respond_arg = String::new();

            for line in &block_lines {
                let l = line.trim();
                if l.starts_with("let ") {
                    if let Some(eq_pos) = l.find('=') {
                        let var_name = l[4..eq_pos].trim().to_string();
                        let mut val = l[eq_pos+1..].trim().to_string();
                        if (val.starts_with('"') && val.ends_with('"')) || (val.starts_with('\'') && val.ends_with('\'')) {
                            val = val[1..val.len()-1].to_string();
                        }
                        vars.insert(var_name, val);
                    }
                }
            }

            if let Some(pos) = block_str.find("respond(") {
                let after = &block_str[pos + 8..];
                let mut paren_depth = 1;
                let mut end_pos = None;
                let mut in_str = false;
                let mut str_char = '"';
                let mut escaped = false;

                for (idx, ch) in after.char_indices() {
                    if escaped {
                        escaped = false;
                        continue;
                    }
                    if ch == '\\' {
                        escaped = true;
                        continue;
                    }
                    if in_str {
                        if ch == str_char {
                            in_str = false;
                        }
                        continue;
                    }
                    if ch == '"' || ch == '\'' {
                        in_str = true;
                        str_char = ch;
                        continue;
                    }
                    if ch == '(' {
                        paren_depth += 1;
                    } else if ch == ')' {
                        paren_depth -= 1;
                        if paren_depth == 0 {
                            end_pos = Some(idx);
                            break;
                        }
                    }
                }

                if let Some(ep) = end_pos {
                    respond_arg = after[..ep].trim().to_string();
                }
            } else if let Some(pos) = block_str.find("respond ") {
                let after = &block_str[pos + 8..];
                respond_arg = after.lines().next().unwrap_or("").trim().to_string();
            }


            let mut final_body = if let Some(resolved) = vars.get(&respond_arg) {
                resolved.clone()
            } else if (respond_arg.starts_with('"') && respond_arg.ends_with('"')) ||
                      (respond_arg.starts_with('\'') && respond_arg.ends_with('\'')) {
                respond_arg[1..respond_arg.len()-1].to_string()
            } else if !respond_arg.is_empty() {
                respond_arg.clone()
            } else {
                r#"{"status":"OK","engine":"AAYU Silicon"}"#.to_string()
            };

            // Fix Python-dict style syntax if dictionary was used in respond({ ... })
            if final_body.starts_with('{') && final_body.ends_with('}') {
                // Ensure double quotes for JSON compliance
                final_body = final_body.replace('\'', "\"");
            }

            // Content-Type detection
            let content_type = if final_body.trim().starts_with('<') || final_body.contains("<html>") || final_body.contains("<!DOCTYPE") || final_body.contains("</div>") {
                "text/html; charset=utf-8".to_string()
            } else if final_body.trim().starts_with('{') || final_body.trim().starts_with('[') {
                "application/json; charset=utf-8".to_string()
            } else {
                "text/plain; charset=utf-8".to_string()
            };

            routes.insert(path, (content_type, final_body));
        }
        i += 1;
    }

    routes
}

/// Native Outbound HTTPS / TLS Client
pub fn fetch_https(url: &str) -> Result<String, String> {
    ureq::get(url)
        .call()
        .map_err(|e| format!("HTTPS request failed: {}", e))?
        .into_string()
        .map_err(|e| format!("Failed to read HTTPS body: {}", e))
}
