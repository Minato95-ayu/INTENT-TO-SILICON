import json

class DAPProtocol:
    """Handles Debug Adapter Protocol JSON serialization."""
    
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.seq = 1
        
    def read_message(self):
        content_length = 0
        while True:
            line = self.reader.readline()
            if not line:
                return None
            if line == '\r\n':
                break
            if line.startswith('Content-Length: '):
                content_length = int(line[16:].strip())
                
        if content_length == 0:
            return None
            
        body = self.reader.read(content_length)
        return json.loads(body)
        
    def send_response(self, request, body=None):
        msg = {
            "type": "response",
            "seq": self.seq,
            "request_seq": request["seq"],
            "command": request["command"],
            "success": True,
        }
        if body is not None:
            msg["body"] = body
        self._write(msg)
        
    def send_event(self, event, body=None):
        msg = {
            "type": "event",
            "seq": self.seq,
            "event": event,
        }
        if body is not None:
            msg["body"] = body
        self._write(msg)
        
    def _write(self, msg):
        self.seq += 1
        payload = json.dumps(msg)
        raw = f"Content-Length: {len(payload)}\r\n\r\n{payload}"
        self.writer.write(raw)
        self.writer.flush()
