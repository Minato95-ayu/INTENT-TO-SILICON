import time
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from typing import Any, Dict, Callable, List
from runtime.kernel.interface import RuntimeInterface, RuntimeMetadata, DispatchResult

logger = logging.getLogger("aayu.kernel.web")

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    daemon_threads = True

class WebRuntime(RuntimeInterface):
    """
    AAYU OS - Web Runtime Plugin.
    Provides inbound HTTP server, router, and middleware processing.
    """
    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        self.host = host
        self.port = port
        self.kernel = None
        self.server = None
        self.server_thread = None
        
        # Router mapping: Method -> Path -> Handler
        self.routes = {
            "GET": {},
            "POST": {},
            "PUT": {},
            "DELETE": {},
            "PATCH": {}
        }
        self.middlewares: List[Callable] = []

    def metadata(self) -> RuntimeMetadata:
        return RuntimeMetadata(
            name="web",
            version="1.0",
            dependencies=[],
            author="AAYU Core",
            priority=30
        )

    def initialize(self, kernel) -> None:
        self.kernel = kernel

    def boot(self) -> None:
        handler_class = self._create_handler_class()
        self.server = ThreadingHTTPServer((self.host, self.port), handler_class)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        logger.info(f"Web Runtime booted, listening on {self.host}:{self.port}")

    def _create_handler_class(self):
        # We define the handler dynamically to capture `self`
        runtime_self = self
        
        class RequestHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass # Suppress default logging
                
            def _handle_request(self):
                req_obj = {
                    "method": self.command,
                    "path": self.path.split('?')[0],
                    "headers": dict(self.headers),
                    "body": None
                }
                
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    req_obj["body"] = self.rfile.read(content_length).decode('utf-8')
                    
                res_obj = {
                    "status": 404,
                    "headers": {"Content-Type": "text/plain"},
                    "body": "Not Found"
                }
                
                try:
                    # Execute middleware chain + handler
                    self._execute_chain(req_obj, res_obj)
                except Exception as e:
                    logger.error(f"Web Handler crashed: {e}", exc_info=True)
                    res_obj["status"] = 500
                    res_obj["body"] = "Internal Server Error"
                    
                # Send response
                self.send_response(res_obj["status"])
                for k, v in res_obj["headers"].items():
                    self.send_header(k, v)
                self.end_headers()
                
                if res_obj["body"]:
                    self.wfile.write(str(res_obj["body"]).encode('utf-8'))

            def _execute_chain(self, req, res):
                # Chain structure: middlewares -> handler
                idx = -1
                
                def next_func():
                    nonlocal idx
                    idx += 1
                    
                    if idx < len(runtime_self.middlewares):
                        mid = runtime_self.middlewares[idx]
                        mid(req, res, next_func)
                    else:
                        # Reached the end of middleware, call actual handler
                        routes_for_method = runtime_self.routes.get(req["method"], {})
                        handler = routes_for_method.get(req["path"])
                        if handler:
                            handler(req, res)
                        else:
                            res["status"] = 404
                            res["body"] = "Not Found"

                # Start chain
                next_func()

            def do_GET(self): self._handle_request()
            def do_POST(self): self._handle_request()
            def do_PUT(self): self._handle_request()
            def do_DELETE(self): self._handle_request()
            def do_PATCH(self): self._handle_request()
            
        return RequestHandler

    def start(self) -> None:
        pass

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def handle(self, action: str, payload: Dict[str, Any]) -> DispatchResult:
        start_ms = time.time()
        try:
            if action == "route":
                method = payload.get("method", "GET").upper()
                path = payload["path"]
                handler = payload["handler"]
                
                if method not in self.routes:
                    self.routes[method] = {}
                self.routes[method][path] = handler
                
                return DispatchResult(success=True, time=time.time() - start_ms)

            elif action == "middleware":
                handler = payload["handler"]
                self.middlewares.append(handler)
                return DispatchResult(success=True, time=time.time() - start_ms)
                
            elif action == "listen":
                # For Phase 2, server starts in boot(). This is for dynamic port binding if needed later.
                return DispatchResult(success=True, time=time.time() - start_ms)
                
            elif action == "stop":
                self.stop()
                return DispatchResult(success=True, time=time.time() - start_ms)

            else:
                raise ValueError(f"Unknown Web action: {action}")

        except Exception as e:
            return DispatchResult(success=False, error=str(e), time=time.time() - start_ms)

    def stop(self) -> None:
        if self.server:
            self.server.shutdown()
            self.server.server_close()

    def shutdown(self) -> None:
        self.stop()
        if self.server_thread:
            self.server_thread.join(timeout=1.0)

    def health(self) -> dict:
        return {"status": "healthy"}

    def capabilities(self) -> dict:
        return {"actions": ["route", "middleware", "listen", "stop"]}
    
    def diagnostics(self) -> dict:
        return {
            "routes_count": sum(len(r) for r in self.routes.values()),
            "middlewares_count": len(self.middlewares)
        }
