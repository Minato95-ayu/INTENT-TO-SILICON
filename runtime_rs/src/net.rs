use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};

pub struct HttpServer {
    port: u16,
}

impl HttpServer {
    pub fn new(port: u16) -> Self {
        Self { port }
    }

    pub fn listen<F>(&self, mut handler: F) 
    where F: FnMut(String) -> String {
        let listener = TcpListener::bind(format!("127.0.0.1:{}", self.port)).unwrap();
        println!("AAYU Native Server running on port {}", self.port);
        
        for stream in listener.incoming() {
            match stream {
                Ok(mut stream) => {
                    let mut buffer = [0; 1024];
                    stream.read(&mut buffer).unwrap();
                    let request = String::from_utf8_lossy(&buffer[..]);
                    
                    let response_body = handler(request.to_string());
                    
                    let response = format!(
                        "HTTP/1.1 200 OK\r\nContent-Length: {}\r\n\r\n{}",
                        response_body.len(),
                        response_body
                    );
                    
                    stream.write_all(response.as_bytes()).unwrap();
                }
                Err(_) => {}
            }
        }
    }
}
