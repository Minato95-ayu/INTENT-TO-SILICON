import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

class NativeUIHandler(BaseHTTPRequestHandler):
    ui_ir: Dict[str, Any] = {}
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # runtime/ui/

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_content = self._get_index_html()
            self.wfile.write(html_content.encode('utf-8'))
            
        elif self.path == "/_ir":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.ui_ir).encode('utf-8'))
            
        elif self.path.startswith("/renderer/"):
            file_path = os.path.join(self.base_dir, self.path.lstrip('/'))
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def _get_index_html(self) -> str:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>AAYU UI Runtime</title>
            <meta charset="utf-8">
            <style>
                body { margin: 0; padding: 0; font-family: sans-serif; }
                #aayu-root { width: 100vw; height: 100vh; overflow: auto; }
            </style>
        </head>
        <body>
            <div id="aayu-root"></div>
            <script type="module" src="/renderer/main.js"></script>
        </body>
        </html>
        """
        
    def _render_element(self, element: Dict[str, Any]) -> str:
        el_type = element.get("type", "div")
        props = element.get("properties", {})
        children = element.get("children", [])
        
        child_html = "".join([self._render_element(c) for c in children])
        
        if el_type == "heading":
            return f"<h1>{props.get('text', '')}</h1>"
        elif el_type == "button":
            return f"<button>{props.get('text', '')}</button>"
        elif el_type == "text":
            return f"<p>{props.get('text', '')}</p>"
        else:
            return f"<div>{child_html}</div>"


class NativeUIAdapter:
    def __init__(self, port: int, ui_ir: Dict[str, Any]):
        self.port = port
        self.ui_ir = ui_ir
        self.server = None

    def initialize(self):
        NativeUIHandler.ui_ir = self.ui_ir
        self.server = HTTPServer(('localhost', self.port), NativeUIHandler)

    def start(self):
        print(f"[AAYU Native] UI Server running on http://localhost:{self.port}/")
        self.server.serve_forever()
