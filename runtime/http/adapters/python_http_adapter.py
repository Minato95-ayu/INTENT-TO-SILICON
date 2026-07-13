import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Callable

class NativeHTTPHandler(BaseHTTPRequestHandler):
    routes: Dict[str, Dict[str, Any]] = {}

    def do_GET(self):
        self._handle_request("GET")

    def do_POST(self):
        self._handle_request("POST")
        
    def do_PUT(self):
        self._handle_request("PUT")
        
    def do_DELETE(self):
        self._handle_request("DELETE")

    def _handle_request(self, method: str):
        path = self.path.split('?')[0]
        
        # Simple exact routing for now
        matched_endpoint = None
        for endpoint in self.routes.get(method, []):
            # Check simple match or dynamic routing mapping
            # Ex: /users/{id}
            regex_path = re.sub(r'\{([^}]+)\}', r'([^/]+)', endpoint["path"])
            if re.match(f"^{regex_path}$", path):
                matched_endpoint = endpoint
                break
                
        if matched_endpoint:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Here we would normally hook back into the AAYU VM to execute the endpoint action block.
            # For now, return a placeholder JSON response.
            response = {"status": "success", "message": f"AAYU Native execution for {method} {path}"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())


class PythonHTTPAdapter:
    def __init__(self, port: int, services: list):
        self.port = port
        self.services = services
        self.server = None

    def initialize(self):
        routes = {"GET": [], "POST": [], "PUT": [], "DELETE": []}
        
        for service in self.services:
            for endpoint in service.get("endpoints", []):
                method = endpoint["method"]
                routes[method].append(endpoint)
                
        NativeHTTPHandler.routes = routes
        self.server = HTTPServer(('localhost', self.port), NativeHTTPHandler)

    def start(self):
        print(f"[AAYU Native] HTTP Server listening on port {self.port}.")
        self.server.serve_forever()
