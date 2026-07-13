from runtime.vm.config import VMConfig
from runtime.vm.registers import Registers
from runtime.vm.stack import CallStack, ValueStack
from runtime.vm.heap import Heap
from runtime.vm.decoder import Decoder
from runtime.vm.validator import Validator
from runtime.vm.profiler import Profiler
from runtime.debugger import Debugger
from runtime.vm.interpreter import Interpreter
from runtime.vm.crash_reporter import CrashReporter
from runtime.vm.result import RuntimeResult, ResultStatus

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
