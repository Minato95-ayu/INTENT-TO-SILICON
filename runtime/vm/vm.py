from compiler.bytecode.instructions import BytecodeObject
from runtime.kernel.core import RuntimeKernel

class VirtualMachine:
    def __init__(self, kernel: RuntimeKernel):
        self.kernel = kernel
        self.ip = 0
        self.stack = []

    def execute(self, bytecode: BytecodeObject):
        instructions = bytecode.instructions
        self.ip = 0
        
        while self.ip < len(instructions):
            inst = instructions[self.ip]
            self._dispatch_instruction(inst)
            self.ip += 1

    def _dispatch_instruction(self, inst):
        opcode = inst.opcode
        
        if opcode == "STATE_INIT":
            # Dispatch to State Runtime
            self.kernel.dispatch("state", "set", {
                "key": inst.arg1,
                "value": inst.arg2
            })
        elif opcode.startswith("BUILD_"):
            # Dispatch to UI Runtime
            w_type = opcode[6:]
            self.kernel.dispatch("ui", "build", {
                "type": w_type,
                "name": inst.arg1
            })
        elif opcode == "LOAD_CONST":
            self.stack.append(inst.arg1)
        elif opcode == "POP":
            if self.stack:
                self.stack.pop()
        else:
            raise NotImplementedError(f"Opcode {opcode} not implemented in VM")
