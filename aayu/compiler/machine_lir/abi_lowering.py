from abc import ABC, abstractmethod
from aayu.compiler.machine_lir.nodes import MachineModule
from aayu.compiler.machine_lir.calling_convention import CallingConvention

class ABILoweringPass(ABC):
    """
    Transforms a generic MachineLIR module to conform strictly to a target ABI.
    This includes injecting argument moves, standardizing return layouts, and handling call frames.
    """
    def __init__(self, calling_conv: CallingConvention):
        self.calling_conv = calling_conv

    @abstractmethod
    def run(self, module: MachineModule) -> MachineModule:
        pass

class SystemVABILowering(ABILoweringPass):
    def run(self, module: MachineModule) -> MachineModule:
        # TODO: Implement physical register mapping for SystemV x64 (rdi, rsi, rdx...)
        # Inject `MOVE %rdi, %vreg0` at the start of functions
        return module

class Win64ABILowering(ABILoweringPass):
    def run(self, module: MachineModule) -> MachineModule:
        # TODO: Implement Windows x64 ABI (rcx, rdx, r8, r9 + shadow space)
        return module

class AayuBytecodeABILowering(ABILoweringPass):
    def run(self, module: MachineModule) -> MachineModule:
        # For the Bytecode VM, no physical registers exist.
        # Arguments are inherently on the evaluation stack.
        # This pass might just attach metadata or pass it straight through.
        return module
