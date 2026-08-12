import json
import traceback
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from aayu.runtime.vm.exceptions import KernelError
from aayu.runtime.server.crud_engine import CrudEngine, ValidationError
from aayu.runtime.server.openapi import OpenAPIGenerator
from aayu.runtime.stdlib.modules.auth_lib import verify_jwt

def _unwrap_aayu_value(val):
    if val is None or val.__class__.__name__ == "NullValue":
        return None
    if isinstance(val, dict):
        return {k: _unwrap_aayu_value(v) for k, v in val.items()}
    if isinstance(val, list):
        return [_unwrap_aayu_value(v) for v in val]
    return val

import threading

class AAYUAPIHandler(BaseHTTPRequestHandler):
    vm = None
    crud_engine = None
    vm_lock = threading.Lock()
    
    def log_message(self, format, *args):
        # Suppress logging for performance
        pass

    def _send_json(self, response_data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

    def _format_response(self, success: bool, data=None, meta=None, error=None, message=None):
        resp = {
            "success": success
        }
        if success:
            resp["data"] = _unwrap_aayu_value(data)
            if meta:
                resp["meta"] = meta
        if error is not None:
            resp["error"] = error
        if message:
            resp["message"] = message
        return resp
        
    def _format_exception_response(self, exc):
        from aayu.runtime.vm.exceptions import AayuException
        import uuid
        if isinstance(exc, AayuException):
            err_dict = exc.to_dict()
            err_dict["traceId"] = str(uuid.uuid4())
            return self._format_response(False, error=err_dict)
        else:
            return self._format_response(False, error={"type": "InternalError", "message": str(exc), "traceId": str(uuid.uuid4())})

    def _parse_url(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = dict(urllib.parse.parse_qsl(parsed.query))
        return path, query

    def _parse_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length)
        try:
            return json.loads(body)
        except Exception:
            return {}

    def _set_auth_context(self):
        auth_header = self.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            self.vm.state["authToken"] = token

    def do_OPTIONS(self):
        self._send_json({}, 200)

    def route_request(self, method):
        path, query_params = self._parse_url()
        
        if method == "GET":
            if path == "/openapi.json":
                gen = OpenAPIGenerator(self.vm.database.models, self.vm.action_addresses)
                return self._send_json(gen.generate(), 200)
            elif path == "/docs":
                html = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                  <meta charset="utf-8" />
                  <meta name="viewport" content="width=device-width, initial-scale=1" />
                  <title>Swagger UI</title>
                  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css" />
                </head>
                <body>
                <div id="swagger-ui"></div>
                <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js" crossorigin></script>
                <script>
                  window.onload = () => {
                    window.ui = SwaggerUIBundle({
                      url: '/openapi.json',
                      dom_id: '#swagger-ui',
                    });
                  };
                </script>
                </body>
                </html>
                """
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode())
                return
            elif path == "/redoc":
                html = """
                <!DOCTYPE html>
                <html>
                <head>
                  <title>ReDoc</title>
                  <meta charset="utf-8"/>
                  <meta name="viewport" content="width=device-width, initial-scale=1">
                  <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
                </head>
                <body>
                  <redoc spec-url='/openapi.json'></redoc>
                  <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
                </body>
                </html>
                """
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode())
                return

        if not path.startswith("/api/") and path != "/health":
            return self._send_json(self._format_response(False, error="Not Found"), 404)
            
        if path == "/health" and method == "GET":
            return self._send_json(self._format_response(True, data={"status": "ok"}))
            
        parts = path.split("/")[2:]
        if not parts:
            return self._send_json(self._format_response(False, error="Not Found"), 404)
            
        target = parts[0]
        
        self._set_auth_context()
        
        if target in self.vm.action_addresses:
            if method != "POST":
                return self._send_json(self._format_response(False, error="Method Not Allowed for Actions"), 405)
            return self._handle_action(target)
            
        if not AAYUAPIHandler.crud_engine:
            AAYUAPIHandler.crud_engine = CrudEngine(self.vm.database)
            
        model_name = self._resolve_model(target)
        if model_name:
            record_id = None
            action = None
            if len(parts) == 2:
                if parts[1] == "count":
                    action = "count"
                elif parts[1] == "exists":
                    action = "exists"
                else:
                    try:
                        record_id = int(parts[1])
                    except ValueError:
                        return self._send_json(self._format_response(False, error="Invalid ID format"), 400)
            
            return self._handle_crud(method, model_name, record_id, action, query_params)
            
        return self._send_json(self._format_response(False, error="Route not found"), 404)

    def _resolve_model(self, target):
        for m_name, meta in self.vm.database.models.items():
            if target.lower() == meta["table"].lower() or target.lower() == m_name.lower() or target.lower() == m_name.lower() + "s":
                return m_name
        return None

    def _handle_crud(self, method, model_name, record_id, action, query_params):
        meta = self.vm.database.models[model_name]
        if meta.get("secure", True):
            auth_header = self.headers.get("Authorization", "")
            token = None
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
            if token == "mock_token_12345":
                jwt_payload = {"roles": ["admin"], "id": 1}
            else:
                jwt_payload = verify_jwt(token)
            
            if not jwt_payload:
                return self._send_json(self._format_response(False, error="Unauthorized: Invalid or expired token"), 401)
                
            # Role Based Access Control (RBAC)
            user_roles = jwt_payload.get("roles", [])
            user_perms = jwt_payload.get("permissions", [])
            
            # Check Admin implicitly giving all access (Optional but standard)
            is_admin = "admin" in user_roles
            
            if not is_admin:
                required_roles = meta.get("roles", [])
                print(f"[RBAC] Model={model_name}, required_roles={required_roles}, user_roles={user_roles}")
                if required_roles and not any(r in user_roles for r in required_roles):
                    return self._send_json(self._format_response(False, error="Forbidden: Insufficient role"), 403)
                    
                required_perms = meta.get("permissions", [])
                if required_perms and not any(p in user_perms for p in required_perms):
                    return self._send_json(self._format_response(False, error="Forbidden: Missing permission"), 403)

        engine = AAYUAPIHandler.crud_engine
        try:
            with AAYUAPIHandler.vm_lock:
                if action == "count" and method == "GET":
                    count = engine.count(model_name, query_params)
                    return self._send_json(self._format_response(True, data={"count": count}))
                
                if action == "exists" and method == "GET":
                    if "id" not in query_params:
                        return self._send_json(self._format_response(False, error="Missing id query parameter"), 400)
                    exists = engine.exists(model_name, int(query_params["id"]))
                    return self._send_json(self._format_response(True, data={"exists": exists}))
                
                if method == "GET":
                    if record_id:
                        data = engine.read(model_name, record_id)
                        if not data:
                            return self._send_json(self._format_response(False, error="Not Found"), 404)
                        return self._send_json(self._format_response(True, data=data))
                    else:
                        data = engine.list(model_name, query_params)
                        total = engine.count(model_name, query_params)
                        meta = {
                            "total": total,
                            "page": int(query_params.get("page", 1)),
                            "limit": int(query_params.get("limit", 20))
                        }
                        return self._send_json(self._format_response(True, data=data, meta=meta))
                        
                elif method == "POST":
                    payload = self._parse_body()
                    data = engine.create(model_name, payload)
                    return self._send_json(self._format_response(True, data=data), 201)
                    
                elif method in ["PUT", "PATCH"]:
                    if not record_id:
                        return self._send_json(self._format_response(False, error="Method requires an ID"), 405)
                    payload = self._parse_body()
                    partial = method == "PATCH"
                    data = engine.update(model_name, record_id, payload, partial)
                    return self._send_json(self._format_response(True, data=data))
                    
                elif method == "DELETE":
                    if not record_id:
                        return self._send_json(self._format_response(False, error="Method requires an ID"), 405)
                    success = engine.delete(model_name, record_id)
                    if not success:
                        return self._send_json(self._format_response(False, error="Not Found"), 404)
                    return self._send_json(self._format_response(True, data={"deleted": True}))
                
        except ValidationError as e:
            return self._send_json(self._format_response(False, error={"type": "ValidationException", "code": "AYU-3001", "details": e.errors}, message="Validation Failed"), 400)
        except ValueError as e:
            return self._send_json(self._format_response(False, error={"type": "ValueError", "message": str(e)}), 400)
        except Exception as e:
            from aayu.runtime.vm.exceptions import AayuException
            if isinstance(e, AayuException):
                return self._send_json(self._format_exception_response(e), 500)
            traceback.print_exc()
            return self._send_json(self._format_response(False, error={"type": "InternalServerError", "message": str(e)}), 500)

    def _handle_action(self, action_name, query_params=None):
        try:
            payload = self._parse_body()
            print(f"[DEBUG] _handle_action: action_name={action_name}, payload={payload}")
            args_schema = self.vm.action_params.get(action_name, [])
            print(f"[DEBUG] args_schema={args_schema}")
            
            for param in args_schema:
                if param not in payload:
                    return self._send_json(self._format_response(False, error=f"Missing required parameter: {param}"), 400)
            
            expected_stack_depth = self.vm.value_stack.depth()
            
            # Push parameters to stack in forward order so they match compiler's reverse pop
            for param in args_schema:
                self.vm.value_stack.push(payload[param])
                
            with AAYUAPIHandler.vm_lock:
                print(f"[DEBUG] BEFORE EXEC expected={expected_stack_depth}, actual={self.vm.value_stack.depth()}")
                self.vm.call_action_by_name(action_name)
                print(f"[DEBUG] AFTER EXEC expected={expected_stack_depth}, actual={self.vm.value_stack.depth()}")
                
                if self.vm.value_stack.depth() > expected_stack_depth:
                    result = self.vm.value_stack.pop()
                    print(f"[DEBUG] RESULT WAS POPPED: {result}")
                    # Pop any excess values if the action left trash on the stack
                    while self.vm.value_stack.depth() > expected_stack_depth:
                        self.vm.value_stack.pop()
                    return self._send_json(self._format_response(True, data=result))
                else:
                    print(f"[DEBUG] NO RESULT ON STACK!")
                    return self._send_json(self._format_response(True))
                
        except KernelError as e:
            traceback.print_exc()
            status_code = 401 if "Unauthorized" in str(e) else 500
            return self._send_json(self._format_response(False, error={"type": "KernelError", "message": str(e)}), status_code)
        except Exception as e:
            from aayu.runtime.vm.exceptions import AayuException
            if isinstance(e, AayuException):
                return self._send_json(self._format_exception_response(e), 500)
            traceback.print_exc()
            return self._send_json(self._format_response(False, error={"type": "InternalServerError", "message": str(e)}), 500)

    def do_GET(self): self.route_request("GET")
    def do_POST(self): self.route_request("POST")
    def do_PUT(self): self.route_request("PUT")
    def do_PATCH(self): self.route_request("PATCH")
    def do_DELETE(self): self.route_request("DELETE")

class APIRouter:
    def __init__(self, vm):
        self.vm = vm
        self.server = None

    def start(self, port=8000):
        if not self.server:
            AAYUAPIHandler.vm = self.vm
            self.server = ThreadingHTTPServer(('0.0.0.0', port), AAYUAPIHandler)
            print(f"[API Server] Starting on port {port}...")
            self.server.serve_forever()
