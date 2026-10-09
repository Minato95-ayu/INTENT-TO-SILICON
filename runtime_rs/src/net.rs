use std::net::{TcpListener};
use std::io::{Read, Write};

pub struct HttpRequest {
    pub method: String,
    pub path: String,
    pub body: String,
}

pub struct HttpResponse {
    pub status: u16,
    pub content_type: String,
    pub body: String,
}

impl HttpResponse {
    pub fn json(status: u16, body: &str) -> Self {
        Self {
            status,
            content_type: "application/json".to_string(),
            body: body.to_string(),
        }
    }
}

pub struct HttpServer {
    port: u16,
}

impl HttpServer {
    pub fn new(port: u16) -> Self {
        Self { port }
    }

    pub fn listen<F>(&self, mut handler: F) 
    where F: FnMut(HttpRequest) -> HttpResponse {
        let listener = TcpListener::bind(format!("127.0.0.1:{}", self.port)).unwrap();
        println!("AAYU Native Server running on port {}", self.port);
        
        for mut stream in listener.incoming().flatten() {
            let mut buffer = [0; 4096];
            if let Ok(bytes_read) = stream.read(&mut buffer) {
                if bytes_read == 0 { continue; }
                let raw_request = String::from_utf8_lossy(&buffer[..bytes_read]);
                
                let req = Self::parse_request(&raw_request);
                let res = handler(req);
                
                let status_text = match res.status {
                    200 => "OK",
                    201 => "Created",
                    400 => "Bad Request",
                    404 => "Not Found",
                    500 => "Internal Server Error",
                    _ => "Unknown",
                };

                let response = format!(
                    "HTTP/1.1 {} {}\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n{}",
                    res.status,
                    status_text,
                    res.content_type,
                    res.body.len(),
                    res.body
                );
                
                let _ = stream.write_all(response.as_bytes());
            }
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
