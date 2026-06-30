from ..values.null import NullValue
from ..values.number import NumberValue
from ..values.string import StringValue
from ..values.boolean import BooleanValue
from ..values.function import FunctionValue, NativeFunctionValue
from ..values.list import ListValue
from ..values.map import MapValue
from ..values.exception import ExceptionValue, PanicValue, LanguageException, AssertionException
import sqlite3
from enum import Enum
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

from dataclasses import dataclass, field
from typing import List, Optional
from runtime.memory import MemoryManager
from runtime.values import RuntimeValue, NumberValue, StringValue, BooleanValue, NullValue, FunctionValue, ListValue, MapValue, NativeFunctionValue
from runtime.diagnostics import RuntimeDiagnostic, DiagnosticSeverity, AAYUUnhandledException
from runtime.debugger.debugger import DebuggerRuntime
class ExecutionState(Enum):
    NORMAL = "NORMAL"
    THROWING = "THROWING"
    PANICKING = "PANICKING"

from location import SourceSpan

@dataclass
class StackFrame:
    """Stack trace entry generated during unwinding."""
    module: str
    function: str
    span: SourceSpan
    instruction_pointer: int
    locals: dict | None = None

@dataclass
class ExceptionFrame:
    """Tracks a try block boundary for the VM unwinder."""
    instruction_pointer: int          # IP where TRY_BEGIN was issued
    catch_target: int                 # IP to jump to for catch (-1 if none)
    finally_target: int               # IP to jump to for finally (-1 if none)
    stack_depth: int                  # Stack depth at TRY_BEGIN
    call_frame_depth: int             # Number of call frames at TRY_BEGIN
    is_active: bool = True
    try_depth: int = 0                # Nesting depth for nested try blocks

@dataclass
class ExceptionContext:
    """Groups all runtime exception information. The VM owns exactly one."""
    state: ExecutionState = ExecutionState.NORMAL
    exception: Optional[RuntimeValue] = None   # ExceptionValue or PanicValue
    stack_trace: List[StackFrame] = field(default_factory=list)

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
    def __init__(self, db_conn=None, db_cursor=None, db_lock=None, trace_execution: bool = False, debugger: Optional[DebuggerRuntime] = None):
        self.frames = []
        self.memory = MemoryManager()
        self.globals = self.memory.globals
        self.output = []
        self.instruction_count = 0
        self.return_value = None
        self.trace_execution = trace_execution
        self.debugger = debugger
        if self.debugger:
            self.debugger.attach(self)
        self.telemetry = {
            "db_wait_time": 0.0,
            "db_exec_time": 0.0,
            "template_render_time": 0.0,
            "vm_exec_time": 0.0
        }
        # Phase 4.1 - Exception System
        self.exception_frames: List[ExceptionFrame] = []
        self.exception_context = ExceptionContext()
        self._try_depth_counter = 0
        
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
        def _print_fn(args):
            val = args[0].stringify() if args else ""
            print(val)
            self.output.append(val)
            return None
            
        self.globals["print"] = NativeFunctionValue("print", _print_fn)
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
        
        # Populate new registered methods and collections
        if hasattr(self.stdlib, 'populate_globals'):
            self.stdlib.populate_globals(self.globals)
        
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

    def _get_location(self, frame, ip) -> SourceSpan:
        line_table = frame.bytecode.debug_info.line_table
        if not line_table:
            # Fallback for empty tables
            return SourceSpan(0, 1, 1, 1, 1)
            
        # Binary search for highest start_ip <= ip
        low, high = 0, len(line_table) - 1
        best_match = line_table[0].span
        
        while low <= high:
            mid = (low + high) // 2
            entry = line_table[mid]
            
            if entry.start_ip <= ip:
                best_match = entry.span
                low = mid + 1
            else:
                high = mid - 1
                
        return best_match

    def _raise_runtime_error(self, message, hint="", cls=AAYURuntimeError):
        if self.frames:
            current_frame = self.frames[-1]
            span = self._get_location(current_frame, current_frame.ip)
            line = span.start_line
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

    # Phase 4.1 - Exception Handling Infrastructure
    def _build_frame_info(self, frame, ip=None):
        """Build a StackFrame for stack trace from a CallFrame."""
        ip_to_check = ip if ip is not None else frame.ip
        span = self._get_location(frame, ip_to_check)
        
        # Module might come from DebugInfo
        module_name = frame.bytecode.debug_info.module_table[0] if frame.bytecode.debug_info.module_table else 'main'
        if not module_name and hasattr(frame.bytecode, 'name'):
            module_name = frame.bytecode.name or 'main'
            
        locals_dict = {k: v.stringify() if isinstance(v, RuntimeValue) else str(v) 
                       for k, v in self.memory.get_locals().items()}

        return StackFrame(
            module=module_name,
            function=frame.frame_name,
            span=span,
            instruction_pointer=ip_to_check,
            locals=locals_dict
        )

    def _build_stack_trace(self):
        """Build stack trace from all current call frames during unwinding."""
        trace = []
        for frame in self.frames:
            ip = frame.ip if frame is self.frames[-1] else max(0, frame.ip - 1)
            trace.append(self._build_frame_info(frame, ip))
        return trace

    def _handle_throw(self, exception_value, current_frame):
        """Handle THROW opcode - begin recoverable unwinding."""
        # Wrap raw strings as LanguageException
        if isinstance(exception_value, StringValue):
            exception_value = LanguageException(exception_value.to_python())
        elif not isinstance(exception_value, ExceptionValue):
            exception_value = LanguageException(str(exception_value.stringify() if hasattr(exception_value, 'stringify') else exception_value))

        self.exception_context.state = ExecutionState.THROWING
        self.exception_context.exception = exception_value
        self.exception_context.stack_trace = self._build_stack_trace()
        exception_value.stack_trace = self.exception_context.stack_trace
        exception_value.debug_info = current_frame.bytecode.debug_info

        self._unwind(current_frame)

    def _handle_panic(self, panic_value, current_frame):
        """Handle PANIC opcode - begin fatal unwinding."""
        if isinstance(panic_value, StringValue):
            panic_value = PanicValue(panic_value.to_python())
        elif not isinstance(panic_value, PanicValue):
            panic_value = PanicValue(str(panic_value.stringify() if hasattr(panic_value, 'stringify') else panic_value))

        self.exception_context.state = ExecutionState.PANICKING
        self.exception_context.exception = panic_value
        self.exception_context.stack_trace = self._build_stack_trace()
        panic_value.stack_trace = self.exception_context.stack_trace
        panic_value.debug_info = current_frame.bytecode.debug_info

        self._unwind(current_frame)

    def _unwind(self, current_frame):
        """Core stack unwinder. Searches for exception handlers."""
        state = self.exception_context.state

        # Search exception frames from innermost to outermost
        while self.exception_frames:
            exc_frame = self.exception_frames[-1]

            if not exc_frame.is_active:
                self.exception_frames.pop()
                continue

            # For THROWING: try catch first, then finally
            if state == ExecutionState.THROWING and exc_frame.catch_target >= 0:
                # Jump to catch block
                exc_frame.is_active = False
                target_frame = self.frames[-1]
                # Restore stack to depth at TRY_BEGIN
                target_frame.stack = target_frame.stack[:exc_frame.stack_depth]
                # Push exception onto stack so STORE_VAR can bind it
                target_frame.stack.append(self.exception_context.exception)
                target_frame.ip = exc_frame.catch_target
                self.exception_context.state = ExecutionState.NORMAL
                self.exception_context.exception = None
                return

            # For THROWING or PANICKING: run finally if present
            if exc_frame.finally_target >= 0:
                exc_frame.is_active = False
                target_frame = self.frames[-1]
                target_frame.stack = target_frame.stack[:exc_frame.stack_depth]
                target_frame.ip = exc_frame.finally_target
                # Don't clear exception state yet — FINALLY_END will resume unwinding
                return

            # No handler in this frame, pop and continue
            self.exception_frames.pop()

        # No handler found — pop call frames up until we find one or reach root
        if len(self.frames) > 1:
            self.memory.pop_frame()
            self.memory.restore_constants()
            self.frames.pop()
            if self.frames:
                # Continue unwinding in the caller
                self._unwind(self.frames[-1])
                return

        # Unhandled - format and raise Python exception
        exc = self.exception_context.exception
        trace = self.exception_context.stack_trace
        state = self.exception_context.state

        severity = DiagnosticSeverity.PANIC if state == ExecutionState.PANICKING else DiagnosticSeverity.ERROR
        error_code = getattr(exc, 'error_code', 'AAYU1000')
        category = getattr(exc, 'category', 'Runtime')
        msg = getattr(exc, 'message', str(exc))

        import time
        diagnostic = RuntimeDiagnostic(
            exception=exc,
            stack_trace=trace,
            message=msg,
            severity=severity,
            timestamp=time.time(),
            error_code=error_code,
            category=category,
            exit_code=1
        )

        self.exception_context.state = ExecutionState.NORMAL
        self.exception_context.exception = None
        self.exception_context.stack_trace = []
        raise AAYUUnhandledException(diagnostic)

    def run(self, bytecode: Bytecode, initial_globals: dict = None, initial_locals: dict = None):
        if initial_globals is not None:
            # Not fully supported with MemoryManager MVP but we'll try
            pass
        elif not self.globals:
            self._register_stdlib()
            if hasattr(self, 'stdlib') and hasattr(self.stdlib, 'populate_globals'):
                self.stdlib.populate_globals(self.globals)
            self.memory.globals = self.globals
            
        self.output = []
        self.instruction_count = 0
        self.return_value = NullValue()
        self.exception_frames = []
        self.exception_context = ExceptionContext()
        self._try_depth_counter = 0
        
        main_frame = CallFrame(bytecode, "main")
        self.frames = [main_frame]
        
        # Initialize memory for this run
        self.memory.set_constants(bytecode.constants)
        
        # Convert initial_locals to RuntimeValues
        init_locs = {}
        if initial_locals:
            for k, v in initial_locals.items():
                if isinstance(v, dict):
                    # Simple conversion for request map
                    map_val = MapValue()
                    for dk, dv in v.items():
                        map_val.set(dk, StringValue(str(dv)))
                    init_locs[k] = map_val
                elif isinstance(v, RuntimeValue):
                    init_locs[k] = v
                else:
                    init_locs[k] = StringValue(str(v))
                    
        self._pushed_initial_frame = False
        if initial_locals is not None:
            self.memory.push_frame(init_locs)
            self._pushed_initial_frame = True
        
        import time
        t_start = time.perf_counter()
        try:
            while self.frames:
                self.instruction_count += 1
                if self.instruction_count > 1000000:
                    self._raise_runtime_error("Maximum instruction limit exceeded")
                    
                current_frame = self.frames[-1]
                
                if current_frame.ip >= len(current_frame.bytecode.instructions):
                    self.frames.pop()
                    if getattr(self, '_pushed_initial_frame', False) and not self.frames:
                        self.memory.pop_frame()
                    elif self.frames:
                        self.memory.pop_frame()
                        self.memory.restore_constants()
                    continue
                    
                instruction = current_frame.bytecode.instructions[current_frame.ip]
                opcode = instruction.opcode
                operand = instruction.operand
                
                # Phase 4.4 Debugger Hook
                if self.debugger:
                    self.debugger.before_instruction(self, current_frame, opcode, operand)
                
                from .handlers import dispatch

                # Phase 4.1 - Exception opcodes handled directly in VM loop
                if opcode == Opcode.TRY_BEGIN:
                    entry = current_frame.bytecode.exception_table[operand]
                    self._try_depth_counter += 1
                    exc_frame = ExceptionFrame(
                        instruction_pointer=current_frame.ip,
                        catch_target=entry.get('catch_target', -1),
                        finally_target=entry.get('finally_target', -1),
                        stack_depth=len(current_frame.stack),
                        call_frame_depth=len(self.frames),
                        try_depth=self._try_depth_counter
                    )
                    self.exception_frames.append(exc_frame)
                    current_frame.ip += 1
                    continue

                elif opcode == Opcode.TRY_END:
                    # Normal exit from try block — pop exception frame
                    if self.exception_frames:
                        self.exception_frames[-1].is_active = False
                    current_frame.ip += 1
                    continue

                elif opcode == Opcode.THROW:
                    exception_value = current_frame.stack.pop() if current_frame.stack else StringValue("Unknown error")
                    self._handle_throw(exception_value, current_frame)
                    continue

                elif opcode == Opcode.PANIC:
                    panic_value = current_frame.stack.pop() if current_frame.stack else StringValue("Unknown panic")
                    self._handle_panic(panic_value, current_frame)
                    continue

                elif opcode == Opcode.FINALLY_BEGIN:
                    current_frame.ip += 1
                    continue

                elif opcode == Opcode.FINALLY_END:
                    # If we were unwinding, resume
                    if self.exception_context.state != ExecutionState.NORMAL:
                        self._unwind(current_frame)
                    else:
                        current_frame.ip += 1
                    continue
                                
                elif opcode == Opcode.RETURN:
                    if len(self.frames) == 1:
                        self.return_value = current_frame.stack.pop() if current_frame.stack else NullValue()
                        break
                    else:
                        ret_val = current_frame.stack.pop() if current_frame.stack else NullValue()
                        self.memory.pop_frame()
                        self.memory.restore_constants()
                        self.frames.pop()
                        if self.frames:
                            current_frame = self.frames[-1]
                            current_frame.stack.append(ret_val)
                        continue
                        
                handled_jump = dispatch(opcode, operand, current_frame, self)
                if not handled_jump:
                    current_frame.ip += 1
        except AAYUUnhandledException:
            raise
        except Exception as e:
            # Reconstruct the call stack entries
            stack_trace = []
            for frame in self.frames:
                ip_to_check = frame.ip if frame is self.frames[-1] else max(0, frame.ip - 1)
                span = self._get_location(frame, ip_to_check)
                line = span.start_line
                file_path = "unknown"
                if frame.bytecode and hasattr(frame.bytecode, 'debug_info') and frame.bytecode.debug_info:
                    if span.file_id in frame.bytecode.debug_info.source_files:
                        file_path = frame.bytecode.debug_info.source_files[span.file_id].path
                
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

