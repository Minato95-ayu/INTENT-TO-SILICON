import sqlite3
from ir import Opcode, Bytecode
from errors import (
    AAYUError,
    AAYURuntimeError,
    UndefinedVariableError,
    DivisionByZeroError,
    IndexOutOfBoundsError,
    InvalidCallError,
    DatabaseError
)

from dataclasses import dataclass

@dataclass
class CallStackEntry:
    task: str
    file: str
    line: int

class CallFrame:
    def __init__(self, bytecode: Bytecode, locals_dict: dict, frame_name: str = "main"):
        self.bytecode = bytecode
        self.locals = locals_dict
        self.ip = 0
        self.stack = []
        self.frame_name = frame_name
        self.source_file = getattr(bytecode, 'file', '')

class VirtualMachine:
    def __init__(self, db_conn=None, db_cursor=None, db_lock=None):
        self.frames = []
        self.globals = {}
        self.output = []
        self.instruction_count = 0
        self.return_value = None
        self.telemetry = {
            "db_wait_time": 0.0,
            "db_exec_time": 0.0,
            "template_render_time": 0.0,
            "vm_exec_time": 0.0
        }
        
        import threading
        if db_lock is not None:
            self.db_lock = db_lock
        else:
            self.db_lock = threading.RLock()
            
        # Connect to SQLite for database functions or use injected connection
        if db_conn is not None:
            self.db_conn = db_conn
            self.db_cursor = db_cursor
        else:
            import sqlite3
            self.db_conn = sqlite3.connect("aayu_db.sqlite", check_same_thread=False, timeout=30.0)
            self.db_conn.row_factory = sqlite3.Row
            self.db_cursor = self.db_conn.cursor()
            try:
                self.db_cursor.execute("PRAGMA journal_mode=WAL;")
                self.db_cursor.execute("PRAGMA synchronous=NORMAL;")
            except Exception:
                pass
            
            # Bootstrap Auth Tables in VM
            try:
                self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS Account (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    password_hash TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )''')
                self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS Session (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER,
                    token TEXT UNIQUE,
                    expires_at TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )''')
                self.db_conn.commit()
            except Exception:
                pass
            
        self.routes = {}
        self.current_request = None
        self.cookies_to_set = []
        
        # Register standard library functions
        from runtime.stdlib import StdLib
        self.stdlib = StdLib(self)
        self._register_stdlib()
        
    def _register_stdlib(self):
        self.globals["db_register_entity"] = self.stdlib.db_register_entity
        self.globals["db_create"] = self.stdlib.db_create
        self.globals["db_find"] = self.stdlib.db_find
        self.globals["db_update"] = self.stdlib.db_update
        self.globals["db_delete"] = self.stdlib.db_delete
        self.globals["json_serialize"] = self.stdlib.json_serialize
        self.globals["render_template"] = self.stdlib.render_template
        self.globals["http_route"] = self.stdlib.http_route
        self.globals["http_form_get"] = self.stdlib.http_form_get
        self.globals["http_serve"] = self.stdlib.http_serve
        self.globals["collection_len"] = self.stdlib.collection_len
        self.globals["string_contains"] = self.stdlib.string_contains
        self.globals["auth_create_account"] = self.stdlib.auth_create_account
        self.globals["auth_login"] = self.stdlib.auth_login
        self.globals["auth_logout"] = self.stdlib.auth_logout
        self.globals["auth_guard_session"] = self.stdlib.auth_guard_session

    def _get_line_and_file(self, frame, ip):
        if ip < len(frame.bytecode.instructions):
            inst = frame.bytecode.instructions[ip]
            if inst.line is not None:
                return inst.line, inst.file
            for idx in range(ip - 1, -1, -1):
                i = frame.bytecode.instructions[idx]
                if i.line is not None:
                    return i.line, i.file
        return 1, frame.source_file

    def _raise_runtime_error(self, message, hint="", cls=AAYURuntimeError):
        if self.frames:
            current_frame = self.frames[-1]
            line, _ = self._get_line_and_file(current_frame, current_frame.ip)
        else:
            line = 1
        raise cls(message, line, hint)

    def close(self):
        if hasattr(self, 'db_conn') and self.db_conn:
            self.db_conn.close()

    def dispatch(self, path: str, method: str = "GET", form_data: dict = None):
        clean_path = path.split('?')[0]
        route_info = self.routes.get(clean_path)
        
        if not route_info:
            raise Exception(f"Route '{clean_path}' not found.")
            
        if route_info["method"] != method:
            raise Exception(f"Method '{method}' not allowed.")
            
        handler_name = route_info["handler"]
        if handler_name not in self.globals:
            raise Exception(f"Handler '{handler_name}' not found in globals.")
            
        handler_bc = self.globals[handler_name]
        if not isinstance(handler_bc, Bytecode):
            raise Exception(f"Handler '{handler_name}' is not a valid bytecode task.")
            
        sub_vm = VirtualMachine(db_conn=self.db_conn, db_cursor=self.db_cursor)
        sub_vm.globals = dict(self.globals)
        sub_vm._register_stdlib()
        sub_vm.routes = self.routes
        
        req_map = {
            "path": path,
            "method": method,
            "_form_data": form_data or {},
            "dispatch_context": True
        }
        sub_vm.current_request = req_map
        
        param_name = handler_bc.parameters[0] if handler_bc.parameters else "req"
        
        sub_vm.run(handler_bc, initial_locals={param_name: req_map})
        return sub_vm.return_value

    def run(self, bytecode: Bytecode, initial_globals: dict = None, initial_locals: dict = None):
        if initial_globals is not None:
            self.globals = initial_globals
        elif not self.globals:
            self.globals = {}
            self._register_stdlib()
            
        self.output = []
        self.instruction_count = 0
        self.return_value = None
        
        main_frame = CallFrame(bytecode, initial_locals or {}, "main")
        self.frames = [main_frame]
        
        import time
        t_start = time.perf_counter()
        try:
            while self.frames:
                self.instruction_count += 1
                current_frame = self.frames[-1]
                
                if current_frame.ip >= len(current_frame.bytecode.instructions):
                    self.frames.pop()
                    continue
                    
                instruction = current_frame.bytecode.instructions[current_frame.ip]
                opcode = instruction.opcode
                operand = instruction.operand
                
                if opcode == Opcode.LOAD_CONST:
                    val = current_frame.bytecode.constants[operand]
                    current_frame.stack.append(val)
                    
                elif opcode == Opcode.STORE_NAME:
                    val = current_frame.stack.pop()
                    name = current_frame.bytecode.names[operand]
                    if len(self.frames) == 1:
                        self.globals[name] = val
                    else:
                        current_frame.locals[name] = val
                        
                elif opcode == Opcode.LOAD_NAME:
                    name = current_frame.bytecode.names[operand]
                    if name in current_frame.locals:
                        current_frame.stack.append(current_frame.locals[name])
                    elif name in self.globals:
                        current_frame.stack.append(self.globals[name])
                    else:
                        self._raise_runtime_error(
                            f"Variable '{name}' not found.",
                            hint=f"Did you forget to declare '{name}'?",
                            cls=UndefinedVariableError
                        )
                        
                elif opcode == Opcode.POP:
                    current_frame.stack.pop()
                        
                elif opcode == Opcode.ADD:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    current_frame.stack.append(left + right)
                    
                elif opcode == Opcode.SUB:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    current_frame.stack.append(left - right)
                    
                elif opcode == Opcode.MUL:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    current_frame.stack.append(left * right)
                    
                elif opcode == Opcode.DIV:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if right == 0 or right == 0.0:
                        self._raise_runtime_error(
                            "Division by zero.",
                            hint="Make sure the denominator is not zero.",
                            cls=DivisionByZeroError
                        )
                    current_frame.stack.append(left / right)
                    
                elif opcode == Opcode.EQUAL:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    current_frame.stack.append(left == right)
                    
                elif opcode == Opcode.GREATER:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    current_frame.stack.append(left > right)
                    
                elif opcode == Opcode.LESS:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    current_frame.stack.append(left < right)
                    
                elif opcode == Opcode.NOT:
                    val = current_frame.stack.pop()
                    current_frame.stack.append(not val)
                    
                elif opcode == Opcode.JUMP_FORWARD:
                    current_frame.ip += operand
                    continue
                    
                elif opcode == Opcode.JUMP_IF_FALSE:
                    condition = current_frame.stack.pop()
                    if not condition:
                        current_frame.ip += operand
                        continue
                        
                elif opcode == Opcode.JUMP_BACKWARD:
                    current_frame.ip -= operand
                    continue
                    
                elif opcode == Opcode.CALL_TASK:
                    n_args = operand
                    task_obj = current_frame.stack.pop()
                    
                    args = []
                    for _ in range(n_args):
                        args.append(current_frame.stack.pop())
                    args.reverse()
                    
                    if callable(task_obj):
                        try:
                            ret_val = task_obj(*args)
                            current_frame.stack.append(ret_val)
                        except sqlite3.Error as se:
                            self._raise_runtime_error(
                                f"Database query failed: {str(se)}",
                                cls=DatabaseError
                            )
                        except Exception as ce:
                            if isinstance(ce, AAYUError):
                                raise ce
                            self._raise_runtime_error(
                                str(ce),
                                cls=InvalidCallError
                            )
                    elif isinstance(task_obj, Bytecode):
                        locals_dict = {}
                        for param, val in zip(task_obj.parameters, args):
                            locals_dict[param] = val
                            
                        new_frame = CallFrame(task_obj, locals_dict, task_obj.name)
                        
                        # Advance caller frame IP so it resumes AFTER the CALL_TASK instruction
                        current_frame.ip += 1
                        
                        self.frames.append(new_frame)
                        continue
                    else:
                        self._raise_runtime_error(
                            "Object is not callable.",
                            hint="You can only run or call tasks or native library functions.",
                            cls=InvalidCallError
                        )
                    
                elif opcode == Opcode.RETURN:
                    if current_frame.stack:
                        ret_val = current_frame.stack.pop()
                    else:
                        ret_val = None
                        
                    self.frames.pop()
                    
                    if self.frames:
                        self.frames[-1].stack.append(ret_val)
                    else:
                        self.return_value = ret_val
                    continue
                    
                elif opcode == Opcode.BUILD_LIST:
                    current_frame.stack.append([])
                    
                elif opcode == Opcode.BUILD_MAP:
                    current_frame.stack.append({})
                    
                elif opcode == Opcode.ADD_TO_LIST:
                    list_obj = current_frame.stack.pop()
                    item = current_frame.stack.pop()
                    if not isinstance(list_obj, list):
                        self._raise_runtime_error(
                            "Target of 'add' must be a list.",
                            hint="Ensure the target variable is initialized as a list.",
                            cls=InvalidCallError
                        )
                    list_obj.append(item)
                    current_frame.stack.append(list_obj)
                    
                elif opcode == Opcode.MAP_SET:
                    map_obj = current_frame.stack.pop()
                    key = current_frame.stack.pop()
                    value = current_frame.stack.pop()
                    if not isinstance(map_obj, dict):
                        self._raise_runtime_error(
                            "Target of 'set' must be a map.",
                            hint="Ensure the target variable is initialized as a map.",
                            cls=InvalidCallError
                        )
                    map_obj[key] = value
                    
                elif opcode == Opcode.GET_ITEM:
                    coll = current_frame.stack.pop()
                    key = current_frame.stack.pop()
                    if isinstance(coll, list):
                        try:
                            idx = int(key)
                            current_frame.stack.append(coll[idx])
                        except (ValueError, TypeError):
                            self._raise_runtime_error(
                                f"List index must be an integer, got '{key}'.",
                                cls=IndexOutOfBoundsError
                            )
                        except IndexError:
                            self._raise_runtime_error(
                                f"List index out of range: {key}.",
                                hint=f"List size is {len(coll)}.",
                                cls=IndexOutOfBoundsError
                            )
                    elif isinstance(coll, dict):
                        if key not in coll:
                            self._raise_runtime_error(
                                f"Key '{key}' not found in map.",
                                hint=f"Available keys: {list(coll.keys())}",
                                cls=IndexOutOfBoundsError
                            )
                        current_frame.stack.append(coll[key])
                    else:
                        self._raise_runtime_error(
                            "Cannot read items from a non-collection object.",
                            hint="Ensure the object is a list or a map.",
                            cls=InvalidCallError
                        )

                elif opcode == Opcode.PRINT:
                    val = current_frame.stack.pop()
                    self.output.append(val)
                    print(val)
                    
                else:
                    raise Exception(f"VM Error: Unimplemented opcode {opcode}")
                    
                current_frame.ip += 1

        except Exception as e:
            # Reconstruct the call stack entries
            stack_trace = []
            for frame in self.frames:
                ip_to_check = frame.ip if frame is self.frames[-1] else max(0, frame.ip - 1)
                line, file = self._get_line_and_file(frame, ip_to_check)
                stack_trace.append(CallStackEntry(
                    task=frame.frame_name,
                    file=file,
                    line=line
                ))
            
            # Format diagnostic output
            if isinstance(e, AAYURuntimeError):
                msg = e.message
                hint = e.hint
                type_name = e.type_name
            else:
                msg = str(e)
                hint = "Internal Python exception: " + e.__class__.__name__
                type_name = "Runtime Error"
                
            crash_frame = stack_trace[-1] if stack_trace else CallStackEntry("main", "unknown", 1)
            
            import os
            call_stack_lines = []
            for entry in stack_trace:
                task_sig = f"{entry.task}()" if entry.task == "main" else f"{entry.task}(...)"
                file_base = os.path.basename(entry.file) if entry.file else "unknown"
                call_stack_lines.append(f"  {task_sig:<17} {file_base}:{entry.line}")
            call_stack_str = "\n".join(call_stack_lines)
            
            error_details = (
                f"\nMessage:\n"
                f"{msg}\n\n"
                f"Location:\n"
                f"File: {crash_frame.file or 'unknown'}\n"
                f"Task: {crash_frame.task}\n"
                f"Line: {crash_frame.line}\n\n"
                f"Call Stack:\n"
                f"{call_stack_str}"
            )
            
            cls = e.__class__ if isinstance(e, AAYURuntimeError) else AAYURuntimeError
            raise cls(error_details, crash_frame.line, hint)
        finally:
            self.telemetry["vm_exec_time"] += (time.perf_counter() - t_start)

