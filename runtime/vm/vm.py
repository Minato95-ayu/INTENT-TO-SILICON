from runtime.vm.config import VMConfig
from typing import Any
from runtime.vm.registers import Registers
from runtime.vm.stack import CallStack, ValueStack
from runtime.vm.heap import Heap
from runtime.vm.decoder import Decoder
from runtime.vm.validator import Validator
from runtime.vm.profiler import Profiler
from runtime.vm.debugger import Debugger
from runtime.vm.interpreter import Interpreter
from runtime.vm.crash_reporter import CrashReporter
from runtime.vm.result import RuntimeResult, ResultStatus
from runtime.vm.database import DatabaseEngine
from runtime.vm.router import APIRouter, UIRouter

class VirtualMachine:
    'The unified Virtual Machine orchestrator.'

    def __init__(self, config: VMConfig=None):
        self.config = config or VMConfig.development()
        self.registers = Registers()
        self.heap = Heap()
        self.heap.set_vm(self)
        self.call_stack = CallStack(max_depth=self.config.max_call_depth)
        self.value_stack = ValueStack()
        self.output = []
        self.profiler = Profiler()
        self.debugger = Debugger(self)
        self.interpreter = Interpreter(self)
        from runtime.stdlib.stdlib import StdLib
        self.stdlib = StdLib(self)
        from runtime.vm.form_state import FormStateManager
        self.database = DatabaseEngine()
        self.api_router = APIRouter(self)
        self.router = UIRouter(self)
        self.form_state = FormStateManager(self)
        self.state_scopes_map = {}
        self.state_scopes = [{}]
        self.block_stack = []
        self.constant_pool = []
        self.decoder = None
        self.form_state.init_form('$form')

    @property
    def state(self):
        return self.state_scopes[-1]

    def update_state(self, name: str, value: Any):
        for scope in reversed(self.state_scopes):
            if name in scope:
                scope[name] = value
                return
        self.state_scopes[-1][name] = value

    def load(self, bytecode, constant_pool=None, action_addresses=None, action_params=None):
        self.constant_pool = constant_pool or []
        self.action_addresses = action_addresses or {}
        self.action_params = action_params or {}
        # Validator.validate(bytecode, self.constant_pool)
        self.decoder = Decoder(bytecode, self.constant_pool)
        self.registers.reset()

    def register_external(self, name: str, provider: str, func):
        """Register a host implementation for a qualified AAYU external call."""
        self.stdlib.register_external(name, provider, func)

    def bind_native_function(self, library: str, symbol: str, aayu_name: str, return_type: str, argument_types):
        """Bind one explicitly selected C-ABI function to an AAYU name."""
        from runtime.interop.native import bind_native_function
        bind_native_function(self, library, symbol, aayu_name, return_type, argument_types)

    def bind_python_function(self, module: str, symbol: str, aayu_name: str):
        """Bind one explicit Python module function to an AAYU name."""
        from runtime.interop.python import bind_python_function
        bind_python_function(self, module, symbol, aayu_name)

    def bind_rust_function(self, library: str, symbol: str, aayu_name: str, return_type: str, argument_types):
        """Bind a Rust cdylib symbol exported with ``extern "C"``."""
        from runtime.interop.native import NativeLibrary
        native_library = NativeLibrary(library)
        callback = native_library.bind(symbol, return_type, argument_types)
        self.stdlib.register_rust_external(aayu_name, callback)
        if not hasattr(self, 'native_libraries'):
            self.native_libraries = []
        self.native_libraries.append(native_library)

    def bind_javascript_function(self, module: str, symbol: str, aayu_name: str):
        """Bind a Node.js module export through an isolated JSON subprocess."""
        from runtime.interop.javascript import bind_javascript_function
        bind_javascript_function(self, module, symbol, aayu_name)

    def shutdown(self):
        """Release VM-owned servers, native handles, and database resources."""
        self.api_router.stop()
        if hasattr(self, 'database') and self.database is not None:
            self.database.close()
        if hasattr(self, 'native_libraries'):
            self.native_libraries.clear()

    def call_action_by_name(self, action_name: str):
        args_to_push = []
        if hasattr(self, 'closures') and action_name in self.closures:
            closure = self.closures[action_name]
            action_name = closure['action']
            args_to_push = closure['args']
        if action_name in self.action_addresses:
            target_ip = self.action_addresses[action_name]
            if action_name.startswith('__PAGE_START__'):
                self.interpreter.node_stack.clear()
                self.interpreter.render_tree.root = None
            self.call_stack.push((self.registers.ip, False, None, len(args_to_push), self.value_stack.depth()))
            self.registers.ip = target_ip
            for arg in args_to_push:
                self.value_stack.push(arg)
            self.execute()
        else:
            print(f"[VM] Error: Action '{action_name}' not found.")

    def execute_subroutine(self, target_ip: int, args=None):
        """Executes a bytecode subroutine synchronously and returns the value on top of stack."""
        if args is None:
            args = []
        old_ip = self.registers.ip
        base_depth = self.value_stack.depth()
        halt_ip = max(0, len(self.decoder.bytecode) - 3)
        self.call_stack.push((halt_ip, False, 1, len(args), base_depth))
        self.registers.ip = target_ip
        for arg in args:
            self.value_stack.push(arg)
        target_depth = self.call_stack.depth() - 1
        try:
            self.interpreter.run()
        except Exception as e:
            self.registers.ip = old_ip
            raise e
        return self.value_stack.pop() if self.value_stack.depth() > base_depth else None

    def get_stacktrace(self) -> list:
        trace = []
        current_action = '<unknown>'
        closest_addr = -1
        for name, addr in self.action_addresses.items():
            if addr <= self.registers.ip and addr > closest_addr:
                closest_addr = addr
                current_action = name
        trace.append(f'at {current_action}')
        for i in range(len(self.call_stack.frames) - 1, -1, -1):
            frame = self.call_stack.frames[i]
            ip = frame[0]
            is_comp = frame[1]
            action_name = '<unknown>'
            for name, addr in self.action_addresses.items():
                if addr == ip:
                    action_name = name
                    break
            trace.append(f'at {action_name}')
        return trace

    def raise_exception(self, exception_obj):
        """Unwind stack until a TRY block is found, or crash if unhandled."""
        from runtime.vm.exceptions import AayuException
        if not isinstance(exception_obj, AayuException):
            if isinstance(exception_obj, str):
                exception_obj = AayuException(exception_obj, 'AYU-1001')
            else:
                exception_obj = AayuException('RuntimeError', str(exception_obj))
        exception_obj.stacktrace = self.get_stacktrace()
        while len(self.block_stack) > 0:
            block = self.block_stack.pop()
            if block['type'] == 'TRY':
                target_depth = block['stack_depth']
                while self.value_stack.depth() > target_depth:
                    self.value_stack.pop()
                self.value_stack.push(exception_obj.to_dict())
                self.registers.ip = block['handler']
                return
        raise exception_obj
        result = None
        if self.value_stack.depth() > 0:
            result = self.value_stack.pop()
        self.registers.ip = old_ip
        return result

    def execute(self):
        try:
            self.interpreter.run()
        except Exception as e:
            report = CrashReporter.generate(e, self)
            print(report)
            raise e

    def kernel_dispatch(self) -> RuntimeResult:
        return RuntimeResult.ok()