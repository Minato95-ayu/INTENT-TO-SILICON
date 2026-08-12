from urllib.parse import urlparse, parse_qs
import json

class Request:
    def __init__(self, handler):
        self.method = handler.command
        parsed_url = urlparse(handler.path)
        self.path = parsed_url.path
        
        # Parse Query Params
        self.query = {}
        for k, v in parse_qs(parsed_url.query).items():
            self.query[k] = v[0] if len(v) == 1 else v
            
        self.headers = dict(handler.headers)
        
        # Parse Cookies
        self.cookies = {}
        if 'Cookie' in self.headers:
            cookie_header = self.headers['Cookie']
            for item in cookie_header.split(';'):
                if '=' in item:
                    k, v = item.strip().split('=', 1)
                    self.cookies[k] = v

        # Path params (populated by router)
        self.params = {}

        # Parse Body
        self.body = None
        self.raw_body = None
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            self.raw_body = handler.rfile.read(content_length)
            content_type = self.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                try:
                    self.body = json.loads(self.raw_body.decode('utf-8'))
                except:
                    self.body = {}
            else:
                self.body = self.raw_body.decode('utf-8')
