import json
import os

class Response:
    def __init__(self, handler):
        self.handler = handler
        self._status_code = 200
        self._headers = {}
        self._body = b""
        self.is_sent = False

    def status(self, code: int):
        self._status_code = code
        return self

    def set_header(self, key: str, value: str):
        self._headers[key] = value
        return self

    def _send(self, content_type: str, body: bytes):
        if self.is_sent:
            return
        self.set_header("Content-Type", content_type)
        self.set_header("Content-Length", str(len(body)))
        
        self.handler.send_response(self._status_code)
        for k, v in self._headers.items():
            self.handler.send_header(k, v)
        self.handler.end_headers()
        
        self.handler.wfile.write(body)
        self.is_sent = True

    def json(self, data: dict):
        body = json.dumps(data).encode('utf-8')
        self._send("application/json", body)

    def text(self, data: str):
        body = data.encode('utf-8')
        self._send("text/plain", body)

    def html(self, data: str):
        body = data.encode('utf-8')
        self._send("text/html", body)

    def file(self, filepath: str):
        if not os.path.exists(filepath):
            self.status(404).text("File not found")
            return
        
        # Extremely basic mime type guessing for MVP
        content_type = "application/octet-stream"
        if filepath.endswith(".html"): content_type = "text/html"
        elif filepath.endswith(".js"): content_type = "application/javascript"
        elif filepath.endswith(".css"): content_type = "text/css"
        elif filepath.endswith(".png"): content_type = "image/png"
        
        with open(filepath, 'rb') as f:
            body = f.read()
        self._send(content_type, body)

    def redirect(self, location: str, status_code: int = 302):
        self.status(status_code)
        self.set_header("Location", location)
        self._send("text/plain", b"")
