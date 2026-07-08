import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from runtime.http.request import Request
from runtime.http.response import Response
from runtime.http.context import HttpContext

class AAYUHTTPRequestHandler(BaseHTTPRequestHandler):
    def handle_one_request(self):
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                return
            
            # 1. Build Abstractions
            req = Request(self)
            res = Response(self)
            ctx = HttpContext(req, res)
            
            # 2. Hand off to AAYU HTTP Engine Pipeline (attached to server)
            self.server.engine.handle_request(ctx)
            
            self.wfile.flush()
        except Exception as e:
            # Fallback error trap
            print(f"[HTTP Server Error] {e}")
            if not getattr(self, '_headers_sent', False):
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Internal Server Error")

class HTTPServerEngine:
    def __init__(self, port, router, middleware_pipeline, error_engine):
        self.port = port
        self.router = router
        self.middlewares = middleware_pipeline
        self.error_engine = error_engine
        
        self.server = ThreadingHTTPServer(('0.0.0.0', self.port), AAYUHTTPRequestHandler)
        self.server.engine = self

    def start(self):
        print(f"[AAYU HTTP Runtime] Starting native server on port {self.port}")
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def handle_request(self, ctx: HttpContext):
        try:
            # 1. Execute Middleware Pipeline
            for mw in self.middlewares:
                mw.process(ctx)
                if ctx.response.is_sent:
                    return # Middleware short-circuited (e.g. auth failed)

            # 2. Find Route
            handler, params = self.router.find_route(ctx.request.method, ctx.request.path)
            
            if handler:
                ctx.request.params = params
                handler(ctx)
            else:
                self.error_engine.handle_404(ctx)
                
        except Exception as e:
            self.error_engine.handle_500(ctx, e)
