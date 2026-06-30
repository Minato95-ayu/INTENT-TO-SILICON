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
from runtime.memory import MemoryManager
from runtime.values import RuntimeValue, NumberValue, StringValue, BooleanValue, NullValue, FunctionValue, ListValue, MapValue, NativeFunctionValue

@dataclass
class CallStackEntry:
    task: str
    file: str
    line: int

class CallFrame:
    def __init__(self, bytecode: Bytecode, frame_name: str = "main"):
        self.bytecode = bytecode
        self.ip = 0
        self.stack = []
        self.frame_name = frame_name
        self.source_file = getattr(bytecode, 'file', '')

class VirtualMachine:
    def __init__(self, db_conn=None, db_cursor=None, db_lock=None, db_path="aayu_db.sqlite"):
        self.frames = []
        self.memory = MemoryManager()
        self.globals = {} # Kept for legacy compatibility if needed
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
            self.db_conn = sqlite3.connect(db_path, check_same_thread=False, timeout=30.0)
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
                self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS Role (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE
                )''')
                self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS Permission (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role_id INTEGER,
                    action TEXT,
                    resource_name TEXT
                )''')
                self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS AccountRole (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER,
                    role_id INTEGER
                )''')
                self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS Workflow (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    entity_name TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )''')
                self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS WorkflowStep (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workflow_id INTEGER,
                    name TEXT,
                    order_index INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )''')
                self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS WorkflowState (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workflow_id INTEGER,
                    entity_id INTEGER,
                    current_step_id INTEGER,
                    status TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
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
        self.globals["db_register_relation"] = self.stdlib.db_register_relation
        self.globals["db_register_role"] = self.stdlib.db_register_role
        self.globals["db_register_permission"] = self.stdlib.db_register_permission
        self.globals["db_register_workflow"] = self.stdlib.db_register_workflow
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
        self.globals["http_request"] = self.stdlib.http_request
        self.globals["dataframe_read_csv"] = self.stdlib.dataframe_read_csv
        self.globals["rag_add_document"] = self.stdlib.rag_add_document
        self.globals["rag_search"] = self.stdlib.rag_search
        
        # Populate new registry-based stdlib functions
        self.stdlib.populate_globals(self.globals)
        
        # Add print dummy for VM's CALL handler
        from runtime.values.function import FunctionValue
        self.globals["print"] = FunctionValue("print", None)
        
        # Load ML Module
        try:
            from runtime.ml_lib import ML_MODULE
            for k, v in ML_MODULE.items():
                self.globals[f"ml_{k}"] = v
        except ImportError:
            pass
            
        # Load Vision Module
        try:
            from runtime.vision_lib import VISION_MODULE
            for k, v in VISION_MODULE.items():
                self.globals[f"vision_{k}"] = v
        except ImportError:
            pass

    def _get_line_and_file(self, frame: CallFrame, ip: int = None):
        if ip is None:
            ip = frame.ip
            
        file_name = frame.source_file
        line = None
        
        # Binary search in debug_info.line_table
        debug_info = frame.bytecode.debug_info
        if debug_info and debug_info.line_table:
            # Simple linear search for now since it's a prototype
            for range_info in debug_info.line_table:
                if range_info.start_ip <= ip <= range_info.end_ip:
                    line = range_info.span.start_line
                    
                    # If the debug info contains file info, override
                    if debug_info.source_files:
                        for file_id, file_obj in debug_info.source_files.items():
                            file_name = file_obj.path
                            break # In real implementation we'd map instruction to file_id
                    break
        
        if line is None:
            return 1, file_name
        return line, file_name

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
        from runtime.values.function import FunctionValue
        if isinstance(handler_bc, FunctionValue):
            handler_bc = handler_bc.bytecode
        
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
            # Not fully supported with MemoryManager MVP but we'll try
            pass
        elif not self.globals:
            self._register_stdlib()
            
        self.output = []
        self.instruction_count = 0
        self.return_value = NullValue()
        
        # Load globals into memory builtins
        for k, v in self.globals.items():
            self.memory.builtins[k] = v
        
        main_frame = CallFrame(bytecode, "main")
        self.frames = [main_frame]
        
        # Initialize memory for this run
        self.memory.set_constants(bytecode.constants)
        
        # Convert initial_locals to RuntimeValues
        def _to_runtime_val(py_val):
            if isinstance(py_val, dict):
                map_val = MapValue(self.memory.heap.allocate('map', {}).id, self.memory.heap)
                for dk, dv in py_val.items():
                    str_key = StringValue(self.memory.heap.allocate('string', str(dk)).id, self.memory.heap)
                    val = _to_runtime_val(dv)
                    map_val.set(str_key, val)
                return map_val
            elif isinstance(py_val, list):
                list_val = ListValue(self.memory.heap.allocate('list', []).id, self.memory.heap)
                for item in py_val:
                    list_val.append(_to_runtime_val(item))
                return list_val
            elif isinstance(py_val, RuntimeValue):
                return py_val
            elif isinstance(py_val, (int, float)):
                return NumberValue(py_val)
            elif isinstance(py_val, bool):
                return BooleanValue(py_val)
            else:
                return StringValue(self.memory.heap.allocate('string', str(py_val)).id, self.memory.heap)

        init_locs = {}
        if initial_locals:
            for k, v in initial_locals.items():
                init_locs[k] = _to_runtime_val(v)
                    
        self.memory.push_frame(init_locs)
        
        import time
        t_start = time.perf_counter()
        try:
            while self.frames:
                self.instruction_count += 1
                current_frame = self.frames[-1]
                
                if current_frame.ip >= len(current_frame.bytecode.instructions):
                    self.frames.pop()
                    self.memory.pop_frame()
                    continue
                    
                instruction = current_frame.bytecode.instructions[current_frame.ip]
                opcode = instruction.opcode
                operand = instruction.operand
                
                if opcode == Opcode.LOAD_CONST:
                    val = self.memory.constants[operand]
                    current_frame.stack.append(val)
                    
                elif opcode == Opcode.STORE_VAR:
                    val = current_frame.stack.pop()
                    name = current_frame.bytecode.names[operand]
                    self.memory.store(name, val)
                        
                elif opcode == Opcode.LOAD_VAR:
                    name = current_frame.bytecode.names[operand]
                    val = self.memory.load(name)
                    if isinstance(val, NullValue):
                        from errors import UndefinedVariableError
                        self._raise_runtime_error(f"Variable '{name}' not found.", cls=UndefinedVariableError)
                    current_frame.stack.append(val)
                    
                elif opcode == Opcode.MAKE_LIST:
                    list_id = self.memory.heap.allocate('list', [])
                    current_frame.stack.append(ListValue(list_id.id, self.memory.heap))

                elif opcode == Opcode.MAKE_MAP:
                    map_id = self.memory.heap.allocate('map', {})
                    current_frame.stack.append(MapValue(map_id.id, self.memory.heap))

                elif opcode == Opcode.LIST_APPEND:
                    coll = current_frame.stack.pop()
                    val = current_frame.stack.pop()
                    if not isinstance(coll, ListValue):
                        self._raise_runtime_error("Cannot append to non-list")
                    coll.append(val)
                    current_frame.stack.append(val) # POP follows list_append in compiler

                elif opcode == Opcode.MAP_SET:
                    coll = current_frame.stack.pop()
                    key = current_frame.stack.pop()
                    val = current_frame.stack.pop()
                    if not isinstance(coll, MapValue):
                        self._raise_runtime_error("Cannot set on non-map")
                    try:
                        coll.set(key, val)
                    except Exception as e:
                        self._raise_runtime_error(str(e))

                elif opcode == Opcode.MAP_GET:
                    coll = current_frame.stack.pop()
                    key = current_frame.stack.pop()
                    if isinstance(coll, (MapValue, ListValue)):
                        try:
                            val = coll.get(key)
                            current_frame.stack.append(val)
                        except Exception as e:
                            import errors
                            if isinstance(e, errors.AAYURuntimeError):
                                raise e
                            self._raise_runtime_error(str(e))
                    else:
                        self._raise_runtime_error("Cannot get from non-collection")

                elif opcode == Opcode.ADD:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(NumberValue(left.value + right.value))
                    elif isinstance(left, StringValue) or isinstance(right, StringValue):
                        res_str = left.stringify() + right.stringify()
                        current_frame.stack.append(StringValue(self.memory.heap.allocate('string', res_str).id, self.memory.heap))
                    else:
                        self._raise_runtime_error(f"Cannot add {left.type_name()} and {right.type_name()}")
                        
                elif opcode == Opcode.SUB:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(NumberValue(left.value - right.value))
                    else:
                        self._raise_runtime_error("Subtraction requires numbers")
                        
                elif opcode == Opcode.MUL:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(NumberValue(left.value * right.value))
                    else:
                        self._raise_runtime_error("Multiplication requires numbers")
                        
                elif opcode == Opcode.DIV:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        if right.value == 0:
                            raise DivisionByZeroError("Division by zero.", 0)
                        current_frame.stack.append(NumberValue(left.value / right.value))
                    else:
                        self._raise_runtime_error("Division requires numbers")
                        
                elif opcode == Opcode.MOD:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        if right.value == 0:
                            raise DivisionByZeroError("Modulo by zero", 0)
                        current_frame.stack.append(NumberValue(left.value % right.value))
                    else:
                        self._raise_runtime_error("Modulo requires numbers")
                        
                elif opcode == Opcode.NEG:
                    val = current_frame.stack.pop()
                    if isinstance(val, NumberValue):
                        current_frame.stack.append(NumberValue(-val.value))
                    else:
                        self._raise_runtime_error("Negation requires number")
                    
                elif opcode == Opcode.EQ:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    current_frame.stack.append(BooleanValue(left.equals(right)))
                    
                elif opcode == Opcode.LT:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(BooleanValue(left.value < right.value))
                    else:
                        self._raise_runtime_error("Less-than requires numbers")
                        
                elif opcode == Opcode.GT:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(BooleanValue(left.value > right.value))
                    else:
                        self._raise_runtime_error("Greater-than requires numbers")
                    
                elif opcode == Opcode.JUMP:
                    current_frame.ip += operand
                    continue
                    
                elif opcode == Opcode.JUMP_IF_FALSE:
                    condition = current_frame.stack.pop()
                    if not condition.truthy():
                        current_frame.ip += operand
                        continue
                        
                elif opcode == Opcode.JUMP_BACKWARD:
                    current_frame.ip -= operand
                    continue
                        
                elif opcode == Opcode.CALL or opcode == Opcode.CALL_TASK:
                    n_args = operand
                    args = []
                    for _ in range(n_args):
                        args.append(current_frame.stack.pop())
                    args.reverse()
                    
                    fn_obj = current_frame.stack.pop()
                    
                    # Native functions / stdlib
                    if isinstance(fn_obj, NativeFunctionValue):
                        import inspect
                        try:
                            sig = inspect.signature(fn_obj.call_fn)
                            if 'vm' in sig.parameters:
                                ret = fn_obj.call_fn(args, self)
                            else:
                                ret = fn_obj.call_fn(args)
                        except (ValueError, TypeError):
                            # Fallback for builtins
                            ret = fn_obj.call_fn(args)
                        current_frame.stack.append(ret if ret is not None else NullValue())
                    elif getattr(fn_obj, 'name', None) == "print":
                        val = args[0].stringify() if args else ""
                        print(val)
                        self.output.append(val)
                        current_frame.stack.append(NullValue())
                    elif isinstance(fn_obj, FunctionValue):
                        # Create new frame for function
                        func_bc = fn_obj.bytecode
                        func_frame = CallFrame(func_bc, func_bc.name)
                        
                        # Bind parameters
                        locals_dict = {}
                        for i, param in enumerate(func_bc.parameters):
                            locals_dict[param] = args[i] if i < len(args) else NullValue()
                            
                        self.frames.append(func_frame)
                        self.memory.push_frame(locals_dict)
                        # Switch constants pool
                        # Wait, we need to save the old constants pool or bind constants to bytecode.
                        # For MVP, assuming constants are flattened or we can fetch from bytecode directly:
                        self.memory.set_constants(func_bc.constants)
                        continue # Start executing the new frame
                    else:
                        # Legacy support for python functions in globals
                        if callable(fn_obj):
                            # Convert args to python
                            py_args = [a.to_python() if hasattr(a, 'to_python') else (a.value if hasattr(a, 'value') else a) for a in args]
                            ret = fn_obj(*py_args)
                            if isinstance(ret, RuntimeValue):
                                current_frame.stack.append(ret)
                            else:
                                def _to_rt(v):
                                    if isinstance(v, list):
                                        allocated = self.memory.heap.allocate('list', [])
                                        lst = ListValue(allocated.id, self.memory.heap)
                                        lst._get_payload().extend([_to_rt(x) for x in v])
                                        return lst
                                    elif isinstance(v, dict):
                                        allocated = self.memory.heap.allocate('map', {})
                                        mp = MapValue(allocated.id, self.memory.heap)
                                        for k, val in v.items():
                                            mp._get_payload()[k] = _to_rt(val)
                                        return mp
                                    elif isinstance(v, bool):
                                        return BooleanValue(v)
                                    elif isinstance(v, (int, float)):
                                        return NumberValue(v)
                                    elif isinstance(v, str):
                                        return StringValue(self.memory.heap.allocate('string', v).id, self.memory.heap)
                                    elif v is None:
                                        return NullValue()
                                    else:
                                        return StringValue(self.memory.heap.allocate('string', str(v)).id, self.memory.heap)
                                        
                                class_name = ret.__class__.__name__
                                if class_name in ("AayuJSONResponse", "AayuHTMLResponse", "AayuTextResponse"):
                                    current_frame.stack.append(ret)
                                else:
                                    current_frame.stack.append(_to_rt(ret))
                        else:
                            import errors
                            self._raise_runtime_error(f"Object is not callable: {repr(fn_obj)} (type: {type(fn_obj)})", cls=errors.InvalidCallError)
                        
                elif opcode == Opcode.RETURN:
                    if current_frame.stack:
                        ret_val = current_frame.stack.pop()
                    else:
                        ret_val = NullValue()
                        
                    self.frames.pop()
                    
                    popped_locals = {}
                    if self.memory.locals_stack:
                        popped_locals = self.memory.locals_stack.pop()
    
                    if self.frames:
                        # Restore previous frame's constants
                        self.memory.set_constants(self.frames[-1].bytecode.constants)
                        self.frames[-1].stack.append(ret_val)
                    else:
                        # Top-level return: persist main frame locals to globals
                        for k, v in popped_locals.items():
                            self.globals[k] = v
                        self.return_value = ret_val
                    continue
                    
                elif opcode == Opcode.POP:
                    if current_frame.stack:
                        current_frame.stack.pop()
                        
                else:
                    self._raise_runtime_error(f"VM Error: Unimplemented opcode {opcode}")
                    
                current_frame.ip += 1

        except Exception as e:
            import traceback
            py_err = traceback.format_exc()
            # Reconstruct the call stack entries
            stack_trace = []
            for frame in self.frames:
                ip_to_check = frame.ip if frame is self.frames[-1] else max(0, frame.ip - 1)
                line, file_path = self._get_line_and_file(frame, ip_to_check)
                stack_trace.append(CallStackEntry(
                    task=frame.frame_name,
                    file=file_path,
                    line=line
                ))

            # Format diagnostic output
            if isinstance(e, AAYURuntimeError):
                msg = e.message
                hint = e.hint
                type_name = e.type_name
            else:
                msg = str(e)
                import sqlite3
                if isinstance(e, sqlite3.Error):
                    msg = f"Database query failed: {msg}"
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
                f"\nPython Traceback:\n{py_err}\n"
                f"\nMessage:\n"
                f"{msg}\n\n"
                f"Location:\n"
                f"File: {crash_frame.file or 'unknown'}\n"
                f"Task: {crash_frame.task}\n"
                f"Line: {crash_frame.line}\n"
                f"IP: {self.frames[-1].ip if self.frames else 'unknown'}\n\n"
                f"Call Stack:\n"
                f"{call_stack_str}"
            )
            
            import sqlite3
            import errors
            if isinstance(e, errors.AAYURuntimeError):
                cls = e.__class__
            elif isinstance(e, sqlite3.Error):
                cls = errors.DatabaseError
            else:
                cls = errors.AAYURuntimeError
            raise cls(error_details, crash_frame.line, hint)
        finally:
            self.telemetry["vm_exec_time"] += (time.perf_counter() - t_start)

