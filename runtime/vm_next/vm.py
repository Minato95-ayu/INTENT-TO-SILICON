from runtime.vm_next.config import VMConfig
from runtime.vm_next.registers import Registers
from runtime.vm_next.stack import CallStack, ValueStack
from runtime.vm_next.heap import Heap
from runtime.vm_next.decoder import Decoder
from runtime.vm_next.validator import Validator
from runtime.vm_next.profiler import Profiler
from runtime.vm_next.debugger import Debugger
from runtime.vm_next.interpreter import Interpreter
from runtime.vm_next.crash_reporter import CrashReporter
from runtime.vm_next.result import RuntimeResult, ResultStatus

class VirtualMachine:
    """The unified Virtual Machine orchestrator."""
    def __init__(self, config: VMConfig = None):
        self.config = config or VMConfig.development()
        self.registers = Registers()
        self.heap = Heap()
        self.call_stack = CallStack(max_depth=self.config.max_call_depth)
        self.value_stack = ValueStack()
        self.profiler = Profiler()
        self.debugger = Debugger(self)
        self.interpreter = Interpreter(self)
        
        self.state = {} # Mock State Runtime
        self.constant_pool = []
        self.decoder = None

    def load(self, bytecode, constant_pool=None):
        self.constant_pool = constant_pool or []
        Validator.validate(bytecode, self.constant_pool)
        self.decoder = Decoder(bytecode, self.constant_pool)
        self.registers.reset()

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
