import os
import datetime
import sqlite3
import json
import re
import uuid
import hashlib
import hmac

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return f"{salt.hex()}:{hashed.hex()}"

def verify_password(stored_hash: str, password: str) -> bool:
    if ":" in stored_hash:
        try:
            salt_hex, hash_hex = stored_hash.split(":", 1)
            salt = bytes.fromhex(salt_hex)
            hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
            return hmac.compare_digest(hashed.hex(), hash_hex)
        except Exception:
            return False
    # Fallback to legacy sha256 with "aayu_salty"
    legacy_salt = "aayu_salty"
    legacy_hash = hashlib.sha256((password + legacy_salt).encode()).hexdigest()
    return hmac.compare_digest(stored_hash, legacy_hash)

# Import response types from interpreter if needed, or define them locally
try:
    from interpreter import AayuJSONResponse, AayuHTMLResponse, AayuTextResponse
except ImportError:
    class AayuJSONResponse:
        def __init__(self, data_str):
            self.data_str = data_str

    class AayuHTMLResponse:
        def __init__(self, data_str):
            self.data_str = data_str

    class AayuTextResponse:
        def __init__(self, data_str):
            self.data_str = data_str

class StdLib:
    def __init__(self, vm):
        self.vm = vm

    def _profiled_db(self, fn):
        import time
        t_wait = time.perf_counter()
        with self.vm.db_lock:
            self.vm.telemetry["db_wait_time"] += (time.perf_counter() - t_wait)
            t_exec = time.perf_counter()
            try:
                result = fn()
            finally:
                self.vm.telemetry["db_exec_time"] += (time.perf_counter() - t_exec)
            return result

    def db_register_entity(self, name: str, fields: list):
        """Creates table and stores schema metadata in SQLite."""
        def _exec():
            # 1. Create metadata table and insert schema rows
            self.vm.db_cursor.execute(
                "CREATE TABLE IF NOT EXISTS _aayu_schema (entity_name TEXT, field_name TEXT, field_type TEXT)"
            )
            self.vm.db_cursor.execute(
                "DELETE FROM _aayu_schema WHERE entity_name = ?", (name,)
            )
            for field in fields:
                field_name = field["name"]
                field_type = field["type"]
                self.vm.db_cursor.execute(
                    "INSERT INTO _aayu_schema (entity_name, field_name, field_type) VALUES (?, ?, ?)",
                    (name, field_name, field_type)
                )

            # 2. Create the actual entity table
            columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
            for field in fields:
                field_name = field["name"]
                field_type = field["type"]
                if field_type == "text":
                    columns.append(f"{field_name} TEXT")
                elif field_type == "number":
                    columns.append(f"{field_name} REAL")
                else:
                    columns.append(f"{field_name} TEXT")
            columns.append("created_at TEXT")
            columns.append("updated_at TEXT")
            
            sql = f"CREATE TABLE IF NOT EXISTS {name} ({', '.join(columns)})"
            self.vm.db_cursor.execute(sql)
            self.vm.db_conn.commit()

        self._profiled_db(_exec)

    def db_register_relation(self, entity1: str, rel_type: str, entity2: str):
        """Creates relationship schema (join tables or foreign keys)"""
        def _exec():
            if rel_type == "many_to_many":
                table_name = f"{entity1}_{entity2}"
                sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {entity1.lower()}_id INTEGER NOT NULL,
                    {entity2.lower()}_id INTEGER NOT NULL,
                    created_at TEXT,
                    updated_at TEXT
                )"""
                self.vm.db_cursor.execute(sql)
            elif rel_type == "one_to_many":
                fk_col = f"{entity1.lower()}_id"
                try:
                    self.vm.db_cursor.execute(f"ALTER TABLE {entity2} ADD COLUMN {fk_col} INTEGER")
                except Exception:
                    pass
            elif rel_type == "many_to_one":
                fk_col = f"{entity2.lower()}_id"
                try:
                    self.vm.db_cursor.execute(f"ALTER TABLE {entity1} ADD COLUMN {fk_col} INTEGER")
                except Exception:
                    pass
            elif rel_type == "one_to_one":
                fk_col = f"{entity1.lower()}_id"
                try:
                    self.vm.db_cursor.execute(f"ALTER TABLE {entity2} ADD COLUMN {fk_col} INTEGER")
                    self.vm.db_cursor.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{entity2}_{fk_col} ON {entity2}({fk_col})")
                except Exception:
                    pass
                    
            self.vm.db_conn.commit()
        self._profiled_db(_exec)
    def db_register_role(self, role_name: str):
        """Registers a role in the database."""
        def _exec():
            try:
                self.vm.db_cursor.execute("INSERT OR IGNORE INTO Role (name) VALUES (?)", (role_name,))
                self.vm.db_conn.commit()
            except Exception:
                pass
        self._profiled_db(_exec)

    def db_register_permission(self, role_name: str, action: str, target_entity: str):
        """Registers a permission for a role in the database."""
        def _exec():
            try:
                # Resolve role ID
                self.vm.db_cursor.execute("SELECT id FROM Role WHERE name = ?", (role_name,))
                row = self.vm.db_cursor.fetchone()
                if row:
                    role_id = row['id']
                    # Insert permission
                    self.vm.db_cursor.execute(
                        "INSERT INTO Permission (role_id, action, resource_name) VALUES (?, ?, ?)",
                        (role_id, action, target_entity)
                    )
                    self.vm.db_conn.commit()
            except Exception:
                pass
        self._profiled_db(_exec)

    def db_register_workflow(self, name: str, entity_name: str, steps_str: str):
        """Registers a workflow and its sequential steps."""
        def _exec():
            try:
                # Insert Workflow
                self.vm.db_cursor.execute(
                    "INSERT OR IGNORE INTO Workflow (name, entity_name) VALUES (?, ?)", 
                    (name, entity_name)
                )
                self.vm.db_cursor.execute("SELECT id FROM Workflow WHERE name = ?", (name,))
                row = self.vm.db_cursor.fetchone()
                if not row:
                    return
                workflow_id = row['id']
                
                # Insert Steps
                steps = [s.strip() for s in steps_str.split(",") if s.strip()]
                for idx, step_name in enumerate(steps):
                    self.vm.db_cursor.execute(
                        "INSERT INTO WorkflowStep (workflow_id, name, order_index) VALUES (?, ?, ?)",
                        (workflow_id, step_name, idx)
                    )
                self.vm.db_conn.commit()
            except Exception:
                pass
        self._profiled_db(_exec)

    def db_create(self, entity_name: str, data_map: dict):
        """Inserts a new record into the database table."""
        if not isinstance(data_map, dict):
            raise Exception(f"Create target must be a map, got: {type(data_map)}")
            
        now = datetime.datetime.now().isoformat()
        
        insert_data = dict(data_map)
        insert_data["created_at"] = now
        insert_data["updated_at"] = now
        
        columns = list(insert_data.keys())
        placeholders = ["?"] * len(columns)
        values = list(insert_data.values())
        sql = f"INSERT INTO {entity_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        
        def _exec():
            self.vm.db_cursor.execute(sql, values)
            self.vm.db_conn.commit()
        self._profiled_db(_exec)

    def db_find(self, entity_name: str, condition_field: str = None, condition_value = None) -> list:
        """Selects records matching condition, or all if no condition."""
        def _exec():
            if condition_field:
                sql = f"SELECT * FROM {entity_name} WHERE {condition_field} = ?"
                self.vm.db_cursor.execute(sql, [condition_value])
            else:
                sql = f"SELECT * FROM {entity_name}"
                self.vm.db_cursor.execute(sql)
                
            rows = self.vm.db_cursor.fetchall()
            result = []
            for row in rows:
                result.append(dict(row))
            return result
            
        return self._profiled_db(_exec)

    def db_update(self, entity_name: str, condition_field: str, condition_value, data_map: dict):
        """Updates records matching condition."""
        if not isinstance(data_map, dict):
            raise Exception(f"Update payload must be a map, got: {type(data_map)}")
            
        now = datetime.datetime.now().isoformat()
        update_data = dict(data_map)
        update_data["updated_at"] = now
        
        set_clauses = [f"{k} = ?" for k in update_data.keys()]
        values = list(update_data.values())
        values.append(condition_value)
        
        sql = f"UPDATE {entity_name} SET {', '.join(set_clauses)} WHERE {condition_field} = ?"
        def _exec():
            self.vm.db_cursor.execute(sql, values)
            self.vm.db_conn.commit()
        self._profiled_db(_exec)

    def db_delete(self, entity_name: str, condition_field: str, condition_value):
        """Deletes records matching condition."""
        sql = f"DELETE FROM {entity_name} WHERE {condition_field} = ?"
        def _exec():
            self.vm.db_cursor.execute(sql, [condition_value])
            self.vm.db_conn.commit()
        self._profiled_db(_exec)

    def json_serialize(self, data) -> AayuJSONResponse:
        """Serializes data to JSON response."""
        try:
            json_str = json.dumps(data)
            return AayuJSONResponse(json_str)
        except TypeError:
            raise Exception("Cannot serialize data to JSON.")

    def render_template(self, template_path: str, context_map: dict = None) -> str:
        """Loads and renders template file using context map variables."""
        import time
        t_start = time.perf_counter()
        try:
            print("RENDER TEMPLATE:", template_path, "CWD:", os.getcwd(), flush=True)
            if not os.path.exists(template_path):
                # Fallback to views directory
                views_path = os.path.join("views", template_path)
                print("VIEWS PATH:", views_path, "EXISTS:", os.path.exists(views_path), flush=True)
                if os.path.exists(views_path):
                    template_path = views_path
                elif template_path.startswith("library_demo/"):
                    fallback_path = template_path.replace("library_demo/", "examples/library-system/")
                    if os.path.exists(fallback_path):
                        template_path = fallback_path
                        
            if not os.path.exists(template_path):
                raise Exception(f"Template file '{template_path}' not found.")
                
            with open(template_path, 'r', encoding='utf-8') as f:
                template_str = f.read()
                
            if context_map and isinstance(context_map, dict):
                # Handle loops: {% for item in list_var %} ... {% endfor %}
                def loop_replacer(match):
                    item_name = match.group(1)
                    list_var_name = match.group(2)
                    inner_content = match.group(3)
                    
                    if list_var_name in context_map and isinstance(context_map[list_var_name], list):
                        items = context_map[list_var_name]
                        result = ""
                        for item in items:
                            if isinstance(item, dict):
                                curr_str = inner_content
                                for k, v in item.items():
                                    pattern = r'\{\{\s*' + re.escape(item_name) + r'\.' + re.escape(k) + r'\s*\}\}'
                                    curr_str = re.sub(pattern, str(v), curr_str)
                                result += curr_str
                        return result
                    return ""
                
                template_str = re.sub(r'\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}', loop_replacer, template_str, flags=re.DOTALL)
                
                # Handle simple variables
                for key, val in context_map.items():
                    pattern = r'\{\{\s*' + re.escape(key) + r'\s*\}\}'
                    template_str = re.sub(pattern, str(val), template_str)
                    
            # Strip missing variables placeholders
            template_str = re.sub(r'\{\{\s*[\w_\.]+\s*\}\}', '', template_str)
            return template_str
        finally:
            self.vm.telemetry["template_render_time"] += (time.perf_counter() - t_start)


    def http_route(self, path: str, arg2: str, arg3: str = None):
        if arg3 is None:
            method = "GET"
            handler_name = arg2
        else:
            method = arg2
            handler_name = arg3
        if path not in self.vm.routes:
            self.vm.routes[path] = {}
        self.vm.routes[path][method] = handler_name

    def http_form_get(self, key: str, req: dict) -> str:
        if not isinstance(req, dict):
            raise Exception("Request parameter must be a map.")
        values = req.get("_form_data", {}).get(key)
        if not values:
            return ""
        if isinstance(values, list):
            return values[0]
        return values

    def http_serve(self, port: int, handler_name: str = None):
        """Starts HTTP server and dispatches incoming requests to VM tasks."""
        from http.server import BaseHTTPRequestHandler, HTTPServer
        import urllib.parse
        from interpreter import AayuJSONResponse, AayuHTMLResponse, AayuTextResponse
        
        vm_instance = self.vm
        port = int(port)

        class AayuVMHTTPRequestHandler(BaseHTTPRequestHandler):
            def handle_request(self):
                import time
                req_start_time = time.perf_counter()
                
                # Request path normalization (split on ? to strip query params)
                clean_path = self.path.split('?')[0]
                
                # Create a map for the request
                req_map = {
                    "path": self.path,
                    "method": self.command,
                    "_form_data": {},
                    "cookies": {}
                }

                # Parse URL query parameters if present
                if '?' in self.path:
                    query_str = self.path.split('?', 1)[1]
                    req_map["_form_data"] = urllib.parse.parse_qs(query_str)
                
                # Parse request cookies
                cookie_header = self.headers.get('Cookie')
                if cookie_header:
                    from http import cookies
                    try:
                        C = cookies.SimpleCookie(cookie_header)
                        for key, morsel in C.items():
                            req_map["cookies"][key] = morsel.value
                    except Exception:
                        pass
                
                # Parse form data for POST, PUT, DELETE
                if self.command in ("POST", "PUT", "DELETE"):
                    content_length = int(self.headers.get('Content-Length', 0))
                    if content_length > 0:
                        post_data = self.rfile.read(content_length).decode('utf-8')
                        post_params = urllib.parse.parse_qs(post_data)
                        req_map["_form_data"].update(post_params)

                # Match route
                print(f"[DEBUG] self.vm.routes: {vm_instance.routes}")
                target_handler_name = handler_name
                if target_handler_name is None:
                    if clean_path in vm_instance.routes:
                        route_info = vm_instance.routes[clean_path]
                        if self.command not in route_info:
                            self.send_response(405)
                            self.send_header("Content-type", "text/html; charset=utf-8")
                            self.end_headers()
                            self.wfile.write(bytes(f"<h1>405 Method Not Allowed</h1><p>Method '{self.command}' not allowed for route '{clean_path}'.</p>", "utf8"))
                            return
                        target_handler_name = route_info[self.command]

                if target_handler_name is None:
                    self.send_response(404)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(bytes("<h1>404 Not Found</h1>", "utf8"))
                    return

                if target_handler_name not in vm_instance.globals:
                    self.send_response(500)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(bytes(f"<h1>500 Internal Server Error</h1><p>Handler '{target_handler_name}' not found.</p>", "utf8"))
                    return

                handler_bc = vm_instance.globals[target_handler_name]

                req_cursor = None
                try:
                    # Instantiate fresh thread-local cursor for this request
                    req_cursor = vm_instance.db_conn.cursor()
                    # Dynamically instantiate VirtualMachine of same class to avoid circular imports, sharing the db_lock
                    sub_vm = vm_instance.__class__(
                        db_conn=vm_instance.db_conn,
                        db_cursor=req_cursor,
                        db_lock=vm_instance.db_lock
                    )
                    sub_vm.globals = dict(vm_instance.globals)
                    sub_vm._register_stdlib()
                    sub_vm.routes = vm_instance.routes
                    sub_vm.current_request = req_map
                    
                    param_name = handler_bc.parameters[0] if handler_bc.parameters else "req"
                    sub_vm.run(handler_bc, initial_locals={param_name: req_map})
                    val = sub_vm.return_value

                    if isinstance(val, AayuJSONResponse):
                        result = val.data_str
                        content_type = "application/json"
                        status_code = 200
                    elif isinstance(val, AayuHTMLResponse):
                        result = val.data_str
                        content_type = "text/html; charset=utf-8"
                        status_code = 200
                    elif isinstance(val, AayuTextResponse):
                        result = val.data_str
                        content_type = "text/plain; charset=utf-8"
                        status_code = 200
                    else:
                        result = str(val)
                        content_type = "text/html; charset=utf-8"
                        status_code = 200
                except Exception as e:
                    if "unauthorized" in str(e).lower():
                        result = f"<h1>401 Unauthorized</h1><p>{str(e)}</p>"
                        content_type = "text/html; charset=utf-8"
                        status_code = 401
                    else:
                        result = f"<h1>500 Internal Server Error</h1><p>{str(e)}</p>"
                        content_type = "text/html; charset=utf-8"
                        status_code = 500
                finally:
                    if req_cursor:
                        req_cursor.close()

                # Get telemetry values
                total_ms = (time.perf_counter() - req_start_time) * 1000
                db_wait_ms = 0.0
                db_exec_ms = 0.0
                template_ms = 0.0
                vm_ms = 0.0
                
                if 'sub_vm' in locals() and hasattr(sub_vm, 'telemetry'):
                    db_wait_ms = sub_vm.telemetry["db_wait_time"] * 1000
                    db_exec_ms = sub_vm.telemetry["db_exec_time"] * 1000
                    template_ms = sub_vm.telemetry["template_render_time"] * 1000
                    vm_ms = sub_vm.telemetry["vm_exec_time"] * 1000

                self.send_response(status_code)
                self.send_header("Content-type", content_type)
                
                # Check for cookies to set in sub_vm
                if 'sub_vm' in locals() and hasattr(sub_vm, 'cookies_to_set'):
                    for cookie_val in sub_vm.cookies_to_set:
                        self.send_header("Set-Cookie", cookie_val)
                
                # Expose profiling headers
                self.send_header("X-Profiling-Total", f"{total_ms:.2f}")
                self.send_header("X-Profiling-Db-Wait", f"{db_wait_ms:.2f}")
                self.send_header("X-Profiling-Db-Exec", f"{db_exec_ms:.2f}")
                self.send_header("X-Profiling-Template", f"{template_ms:.2f}")
                self.send_header("X-Profiling-Vm", f"{vm_ms:.2f}")
                
                self.end_headers()
                self.wfile.write(bytes(result, "utf8"))

            def do_GET(self):
                self.handle_request()

            def do_POST(self):
                self.handle_request()

            def do_PUT(self):
                self.handle_request()

            def do_DELETE(self):
                self.handle_request()

            # Prevent logging every test request to keep stdout clean
            def log_message(self, format, *args):
                pass

        try:
            from http.server import ThreadingHTTPServer as HTTPServerClass
        except ImportError:
            from http.server import HTTPServer as HTTPServerClass
        HTTPServerClass.request_queue_size = 256
        server = HTTPServerClass(("", port), AayuVMHTTPRequestHandler)
        # Store http_server on the VM so tests can shutdown programmatically
        vm_instance.http_server = server
        
        print(f"Starting Aayu VM HTTP Server on port {port}...")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            server.server_close()

    def collection_len(self, coll) -> int:
        if not isinstance(coll, (list, dict)):
            raise Exception("Cannot get length of a non-collection object.")
        return len(coll)

    def string_contains(self, s: str, sub: str) -> float:
        if not isinstance(s, str) or not isinstance(sub, str):
            return 0.0
        return 1.0 if sub.lower() in s.lower() else 0.0

    def auth_create_account(self, data):
        if not isinstance(data, dict):
            raise Exception("Create account data must be a map.")
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            raise Exception("Account map must contain 'email' and 'password'.")

        hashed = hash_password(password)
        now = datetime.datetime.utcnow().isoformat()

        def _exec():
            # Check if email already exists
            self.vm.db_cursor.execute("SELECT id FROM Account WHERE email = ?", (email,))
            if self.vm.db_cursor.fetchone():
                raise Exception(f"Account with email {email} already exists.")
            self.vm.db_cursor.execute(
                "INSERT INTO Account (email, password_hash, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (email, hashed, now, now)
            )
            self.vm.db_conn.commit()
            return "Success"

        return self._profiled_db(_exec)

    def auth_login(self, data):
        if not isinstance(data, dict):
            raise Exception("Login credentials must be a map.")
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            raise Exception("Login credentials must contain 'email' and 'password'.")

        def _exec():
            self.vm.db_cursor.execute("SELECT id, password_hash FROM Account WHERE email = ?", (email,))
            row = self.vm.db_cursor.fetchone()
            if not row:
                raise Exception("Unauthorized: Invalid email or password.")
            
            stored_hash = row["password_hash"]
            if not verify_password(stored_hash, password):
                raise Exception("Unauthorized: Invalid email or password.")

            account_id = row["id"]
            token = str(uuid.uuid4())
            now = datetime.datetime.utcnow().isoformat()
            expires_at = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat()

            self.vm.db_cursor.execute(
                "INSERT INTO Session (account_id, token, expires_at, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (account_id, token, expires_at, now, now)
            )
            self.vm.db_conn.commit()
            return token

        token = self._profiled_db(_exec)
        self.vm.cookies_to_set.append(f"AAYU_SESSION={token}; Path=/; HttpOnly")
        return "Success"

    def auth_logout(self, req):
        if not isinstance(req, dict):
            raise Exception("Request parameter must be a map.")
        
        cookies_dict = req.get("cookies", {})
        token = cookies_dict.get("AAYU_SESSION")
        
        if token:
            def _exec():
                self.vm.db_cursor.execute("DELETE FROM Session WHERE token = ?", (token,))
                self.vm.db_conn.commit()
            self._profiled_db(_exec)
            
        self.vm.cookies_to_set.append("AAYU_SESSION=; Path=/; HttpOnly; Expires=Thu, 01 Jan 1970 00:00:00 GMT")
        return "Success"

    def auth_guard_session(self):
        req = getattr(self.vm, "current_request", None)
        if not req or not isinstance(req, dict):
            raise Exception("Unauthorized: No active HTTP request context.")
            
        if req.get("dispatch_context"):
            return 1
            
        cookies_dict = req.get("cookies", {})
        token = cookies_dict.get("AAYU_SESSION")
        if not token:
            raise Exception("Unauthorized: No session token found.")

        def _exec():
            now = datetime.datetime.utcnow().isoformat()
            self.vm.db_cursor.execute(
                "SELECT account_id, expires_at FROM Session WHERE token = ?",
                (token,)
            )
            row = self.vm.db_cursor.fetchone()
            if not row:
                raise Exception("Unauthorized: Invalid session token.")
            
            # Check expiration
            expires_at = row["expires_at"]
            if expires_at and expires_at < now:
                # Session expired, delete it
                self.vm.db_cursor.execute("DELETE FROM Session WHERE token = ?", (token,))
                self.vm.db_conn.commit()
                raise Exception("Unauthorized: Session has expired.")
                
            return row["account_id"]

        account_id = self._profiled_db(_exec)
        return account_id




    def http_request(self, options: dict) -> dict:
        import urllib.request
        import urllib.error
        import json
        
        url = options.get("url")
        method = options.get("method", "GET").upper()
        headers = options.get("headers", {})
        body = options.get("body")
        
        if not url:
            raise Exception("http_request requires a 'url'")
            
        req_data = None
        if body is not None:
            if isinstance(body, dict) or isinstance(body, list):
                req_data = json.dumps(body).encode("utf-8")
                if "Content-Type" not in headers:
                    headers["Content-Type"] = "application/json"
            else:
                req_data = str(body).encode("utf-8")
                
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        
        status_code = 500
        res_body = ""
        
        try:
            with urllib.request.urlopen(req) as response:
                status_code = response.getcode()
                res_body = response.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            status_code = e.code
            res_body = e.read().decode("utf-8")
        except Exception as e:
            raise Exception(f"HTTP Request failed: {e}")
            
        # Try parse JSON
        parsed_body = res_body
        try:
            parsed_body = json.loads(res_body)
        except:
            pass
            
        return {
            "status": status_code,
            "body": parsed_body
        }

    def dataframe_read_csv(self, file_path: str) -> list:
        import csv
        import os
        if not os.path.exists(file_path):
            raise Exception(f"File not found: {file_path}")
        data = []
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(dict(row))
            return data
        except Exception as e:
            raise Exception(f"Failed to read CSV: {str(e)}")


    def rag_add_document(self, text: str):
        if not hasattr(self, 'rag_docs'):
            self.rag_docs = []
        self.rag_docs.append(text)
        return text

    def rag_search(self, query: str) -> str:
        if not hasattr(self, 'rag_docs') or not self.rag_docs:
            return ""
        import math
        from collections import Counter
        
        def get_words(s):
            return s.lower().split()
        
        query_words = get_words(query)
        best_doc = ""
        best_score = -1
        
        for doc in self.rag_docs:
            doc_words = get_words(doc)
            doc_counts = Counter(doc_words)
            score = 0
            for w in query_words:
                if w in doc_counts:
                    score += doc_counts[w]
            if score > best_score:
                best_score = score
                best_doc = doc
        
        return best_doc

