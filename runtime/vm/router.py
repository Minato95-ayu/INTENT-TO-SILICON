import time
import threading
import uuid
import logging
from dataclasses import dataclass, field
import json
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlsplit


logger = logging.getLogger("aayu.http")

@dataclass
class Route:
    name: str
    path: str
    params: dict = field(default_factory=dict)
    query: dict = field(default_factory=dict)
    state: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

class UIRouter:
    def __init__(self, vm):
        self.vm = vm
        self.history = []
        self.current_route = None

    def navigate(self, target: str, params: dict):
        path = "/" + target.lower()
        if target.lower() == "home":
            path = "/"
            
        route = Route(name=target, path=path, params=params)
        self.history.append(route)
        self.current_route = route
        
        print(f"[UIRouter] Navigated to {target} with {params}")
        
        # Pass params to VM state for the page
        self.vm.state["props"] = params
        self.vm.state["route"] = {"params": params, "name": target, "path": path, "query": {}}
        
        # Execute the page in the VM
        self.vm.call_action_by_name(target)
        
        # Dispatch event to Renderer
        if self.vm.interpreter and hasattr(self.vm.interpreter, 'render_tree') and self.vm.interpreter.render_tree:
            self.vm.interpreter.render_tree.dispatch_navigation(route)

    def back(self):
        if len(self.history) > 1:
            self.history.pop()
            self.current_route = self.history[-1]
            print(f"[UIRouter] Back to {self.current_route.name}")
            
            # Pass params and re-execute
            self.vm.state["props"] = self.current_route.params
            self.vm.state["route"] = {"params": self.current_route.params, "name": self.current_route.name, "path": self.current_route.path, "query": self.current_route.query}
            self.vm.call_action_by_name(f"__PAGE_START_{self.current_route.name}")
            
            if self.vm.interpreter and hasattr(self.vm.interpreter, 'render_tree') and self.vm.interpreter.render_tree:
                self.vm.interpreter.render_tree.dispatch_navigation(self.current_route)
            
class APIRouter:
    def __init__(
        self,
        vm,
        host="127.0.0.1",
        port=8080,
        max_body_bytes=1_048_576,
        rate_limit=120,
        rate_window_seconds=60,
        require_auth=False,
        auth_verifier=None,
        request_timeout_seconds=30,
    ):
        self.vm = vm
        self.host = host
        self.port = port
        self.max_body_bytes = max_body_bytes
        self.rate_limit = rate_limit
        self.rate_window_seconds = rate_window_seconds
        self.require_auth = require_auth
        self.auth_verifier = auth_verifier
        self.request_timeout_seconds = request_timeout_seconds
        self.routes = {} # { "/api/login": { "post": bytecode_address } }
        self.server = None
        self.thread = None
        self._vm_lock = threading.RLock()
        self._rate_lock = threading.Lock()
        self._rate_buckets = {}
        self._metrics_lock = threading.Lock()
        self._metrics = {
            "started_at": time.time(),
            "requests_total": 0,
            "responses_2xx": 0,
            "responses_4xx": 0,
            "responses_5xx": 0,
        }

    def metrics_snapshot(self):
        """Return process-local operational counters safe for health reporting."""
        with self._metrics_lock:
            snapshot = dict(self._metrics)
        snapshot["uptime_seconds"] = max(0, time.time() - snapshot["started_at"])
        snapshot["rate_limit_clients"] = len(self._rate_buckets)
        return snapshot

    def _record_response(self, status):
        with self._metrics_lock:
            self._metrics["requests_total"] += 1
            if 200 <= status < 300:
                self._metrics["responses_2xx"] += 1
            elif 400 <= status < 500:
                self._metrics["responses_4xx"] += 1
            elif status >= 500:
                self._metrics["responses_5xx"] += 1

    def _allow_request(self, client_address):
        if self.rate_limit <= 0:
            return True
        now = time.monotonic()
        client = client_address[0]
        with self._rate_lock:
            bucket = self._rate_buckets.setdefault(client, [])
            cutoff = now - self.rate_window_seconds
            bucket[:] = [timestamp for timestamp in bucket if timestamp > cutoff]
            if len(bucket) >= self.rate_limit:
                return False
            bucket.append(now)
            return True

    def register_route(self, path: str, methods_meta: list):
        if path not in self.routes:
            self.routes[path] = {}
        for meta in methods_meta:
            method = meta["method"].lower()
            addr = meta["target_address"]
            self.routes[path][method] = addr
            if getattr(getattr(self.vm, "config", None), "debug_mode", False):
                print(f"[Router] Registered route {method.upper()} {path} -> addr 0x{addr:04X}")

    def start(self):
        if self.server is not None:
            return

        router = self

        class RequestHandler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def setup(self):
                super().setup()
                # Slow clients must not hold a worker thread indefinitely.
                self.connection.settimeout(router.request_timeout_seconds)

            def _security_headers(self, request_id):
                self.send_header("X-Request-ID", request_id)
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_header("X-Frame-Options", "DENY")
                self.send_header("Referrer-Policy", "no-referrer")
                self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
                self.send_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'; base-uri 'none'")
                self.send_header("Cache-Control", "no-store")

            def _write(self, status, payload, content_type, request_id, extra_headers=None):
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(payload)))
                self._security_headers(request_id)
                for name, value in (extra_headers or {}).items():
                    self.send_header(name, value)
                self.end_headers()
                self.wfile.write(payload)
                router._record_response(status)
                logger.info(
                    "aayu_http_request method=%s path=%s status=%s request_id=%s client=%s",
                    self.command, urlsplit(self.path).path, status, request_id, self.client_address[0],
                )

            def _send_error(self, status, message, request_id, extra_headers=None):
                payload = json.dumps({
                    "error": message,
                    "requestId": request_id,
                }).encode("utf-8")
                self._write(status, payload, "application/json; charset=utf-8", request_id, extra_headers)

            def _handle(self):
                request_id = uuid.uuid4().hex
                if not router._allow_request(self.client_address):
                    self._send_error(429, "Rate limit exceeded", request_id, {"Retry-After": str(router.rate_window_seconds)})
                    return
                request = urlsplit(self.path)
                methods = router.routes.get(request.path)
                route = (methods or {}).get(self.command.lower())
                if route is None:
                    if methods:
                        allow = ", ".join(sorted(method.upper() for method in methods))
                        self._send_error(405, "Method not allowed", request_id, {"Allow": allow})
                        return
                    self._send_error(404, "AAYU route not found", request_id)
                    return

                if router.require_auth:
                    authorization = self.headers.get("Authorization", "")
                    if not authorization.startswith("Bearer ") or router.auth_verifier is None:
                        self._send_error(401, "Authentication required", request_id)
                        return
                    if not router.auth_verifier(authorization[7:].strip()):
                        self._send_error(401, "Invalid or expired token", request_id)
                        return

                body = None
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                except ValueError:
                    self._send_error(400, "Invalid Content-Length", request_id)
                    return
                if length < 0 or length > router.max_body_bytes:
                    self._send_error(413, "Request body too large", request_id)
                    return
                if length:
                    try:
                        raw = self.rfile.read(length).decode("utf-8")
                    except UnicodeDecodeError:
                        self._send_error(400, "Request body must be UTF-8", request_id)
                        return
                    try:
                        body = json.loads(raw)
                    except json.JSONDecodeError:
                        body = raw

                try:
                    with router._vm_lock:
                        router.vm.state["request"] = {
                            "method": self.command,
                            "path": request.path,
                            "query": {key: values[-1] for key, values in parse_qs(request.query).items()},
                            "body": body,
                        }
                        result = router.vm.execute_subroutine(route)
                except Exception:
                    self._send_error(500, "AAYU route execution failed", request_id)
                    return
                if isinstance(result, (dict, list)):
                    payload = json.dumps(result).encode("utf-8")
                    content_type = "application/json"
                else:
                    payload = str(result if result is not None else "").encode("utf-8")
                    content_type = "text/plain; charset=utf-8"

                self._write(200, payload, content_type, request_id)

            def do_GET(self):
                self._handle()

            def do_POST(self):
                self._handle()

            def do_PUT(self):
                self._handle()

            def do_PATCH(self):
                self._handle()

            def do_DELETE(self):
                self._handle()

            def log_message(self, *_args):
                return

        self.server = ThreadingHTTPServer((self.host, self.port), RequestHandler)
        self.port = self.server.server_address[1]
        import threading
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True, name="aayu-api-router")
        self.thread.start()

    def stop(self):
        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()
            if self.thread is not None and self.thread.is_alive():
                self.thread.join(timeout=self.request_timeout_seconds + 1)
            self.server = None
            self.thread = None
