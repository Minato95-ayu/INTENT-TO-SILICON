from runtime.vm.config import VMConfig
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
    """The unified Virtual Machine orchestrator."""
    def __init__(self, config: VMConfig = None):
        self.config = config or VMConfig.development()
        self.registers = Registers()
        self.heap = Heap()
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
        self.state_scopes_map = {} # Persistent component states
        self.state_scopes = [{}] # List of dicts, stack
        self.block_stack = [] # Stack of dicts: {"type": "TRY", "handler": pc, "stack_depth": depth}
        self.constant_pool = []
        self.decoder = None
        
        # Initialize form state tracking in root scope
        self.form_state.init_form("$form")

    @property
    def state(self):
        return self.state_scopes[-1]

    def load(self, bytecode, constant_pool=None, action_addresses=None, action_params=None):
        self.constant_pool = constant_pool or []
        self.action_addresses = action_addresses or {}
        self.action_params = action_params or {}
        Validator.validate(bytecode, self.constant_pool)
        self.decoder = Decoder(bytecode, self.constant_pool)
        self.registers.reset()
        
    def call_action_by_name(self, action_name: str):
        args_to_push = []
        if hasattr(self, "closures") and action_name in self.closures:
            closure = self.closures[action_name]
            action_name = closure["action"]
            args_to_push = closure["args"]
            
        if action_name in self.action_addresses:
            target_ip = self.action_addresses[action_name]
            
            if action_name.startswith("__PAGE_START__"):
                self.interpreter.node_stack.clear()
                self.interpreter.render_tree.root = None
                
            self.call_stack.push((self.registers.ip, False))
            self.registers.ip = target_ip
            for arg in args_to_push:
                self.value_stack.push(arg)
            self.execute()
        else:
            print(f"[VM] Error: Action '{action_name}' not found.")

    def execute_subroutine(self, target_ip: int):
        """Executes a bytecode subroutine synchronously and returns the value on top of stack."""
        # Save current VM state
        old_ip = self.registers.ip
        # In a real async VM, we would use a separate context/coroutine.
        # Here we just push the current IP and run until RET (or HALT)
        self.call_stack.push((old_ip, False))
        self.registers.ip = target_ip
        
        # We need the interpreter to stop exactly when it returns from THIS call.
        # But for now, since RET restores IP from call_stack, we can just run
        # until the call_stack depth is back to what it was before this call!
        target_depth = self.call_stack.depth() - 1
        
        try:
            while True:
                if self.call_stack.depth() == target_depth:
                    break
                self.interpreter.step()
        except Exception as e:
            self.registers.ip = old_ip
            raise e
            
        # The result should be on top of the value stack

    def get_stacktrace(self) -> list:
        trace = []
        # Try to resolve current IP to action name (the nearest action address below IP)
        current_action = "<unknown>"
        closest_addr = -1
        for name, addr in self.action_addresses.items():
            if addr <= self.registers.ip and addr > closest_addr:
                closest_addr = addr
                current_action = name
        trace.append(f"at {current_action}")
        
        # Walk down call stack
        for i in range(self.call_stack.depth() - 1, -1, -1):
            ip, is_comp = self.call_stack.items[i]
            # Try to resolve IP to action name
            action_name = "<unknown>"
            for name, addr in self.action_addresses.items():
                if addr == ip:
                    action_name = name
                    break
            trace.append(f"at {action_name}")
            
        return trace

    def raise_exception(self, exception_obj):
        """Unwind stack until a TRY block is found, or crash if unhandled."""
        from runtime.vm.exceptions import AayuException
        
        if not isinstance(exception_obj, AayuException):
            exception_obj = AayuException("RuntimeError", str(exception_obj))
            
        exception_obj.stacktrace = self.get_stacktrace()
        
        # Start unwinding
        while len(self.block_stack) > 0:
            block = self.block_stack.pop()
            if block["type"] == "TRY":
                # Found a catch block!
                # 1. Restore the value stack depth
                target_depth = block["stack_depth"]
                while self.value_stack.depth() > target_depth:
                    self.value_stack.pop()
                
                # 2. Push the exception object dict to stack so catch block can capture it
                self.value_stack.push(exception_obj.to_dict())
                
                # 3. Jump to handler
                self.registers.ip = block["handler"]
                return
                
        # If we got here, it's an Uncaught Exception.
        # In Server mode, it will be caught by `api_server.py`.
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
        # Mock plugin dispatch logic for Exception Recovery testing
        return RuntimeResult.ok()
