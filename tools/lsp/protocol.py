import json
import sys

class LSPProtocol:
    """Handles JSON-RPC 2.0 serialization/deserialization."""
    def __init__(self, reader, writer):
        # Always use binary buffer to avoid Windows newline translation
        self.reader = reader.buffer if hasattr(reader, "buffer") else reader
        self.writer = writer.buffer if hasattr(writer, "buffer") else writer
        
    def read_message(self):
        content_length = 0
        while True:
            line_bytes = self.reader.readline()
            if not line_bytes:
                return None
            line = line_bytes.decode('utf-8')
            if line in ('\r\n', '\n'):
                break
            if line.startswith('Content-Length:'):
                content_length = int(line.split(':')[1].strip())
                
        if content_length == 0:
            return None
            
        body = self.reader.read(content_length)
        try:
            return json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            return None

    def write_message(self, message):
        body = json.dumps(message).encode('utf-8')
        response = f"Content-Length: {len(body)}\r\n\r\n".encode('utf-8') + body
        self.writer.write(response)
        self.writer.flush()
