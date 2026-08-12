from aayu.compiler.machine_lir.nodes import (
    MachineModule, MachineFunction, MachineBasicBlock, MachineInstruction,
    MachineOperand, OperandType, RegisterClass
)
from aayu.compiler.errors import DiagnosticEngine, DiagnosticSeverity

class MachineLIRVerifier:
    """
    Validates MachineLIR semantics:
    - Operand types
    - Register classes
    - Basic blocks and terminators
    """
    def __init__(self, diag: DiagnosticEngine):
        self.diag = diag
        self.valid = True

    def verify(self, module: MachineModule) -> bool:
        self.valid = True
        for func in module.functions:
            self._verify_function(func)
        return self.valid
        
    def _report(self, msg: str, instr: MachineInstruction = None):
        self.valid = False
        span = instr.span if instr else None
        self.diag.report(DiagnosticSeverity.ERROR, f"MachineLIR Verification Failed: {msg}", span)

    def _verify_function(self, func: MachineFunction):
        if not func.blocks:
            self._report(f"Function {func.name} has no basic blocks.")
            return
            
        if func.entry_block is None:
            self._report(f"Function {func.name} has no entry block.")
            return
            
        for block in func.blocks:
            self._verify_block(block, func)

    def _verify_block(self, block: MachineBasicBlock, func: MachineFunction):
        if not block.instructions:
            self._report(f"Block {block.name} in {func.name} is empty.")
            return
            
        # Verify terminator
        last_instr = block.instructions[-1]
        terminators = {"JMP", "BRANCH", "RET"}
        if last_instr.opcode not in terminators:
            self._report(f"Block {block.name} in {func.name} does not end with a terminator.", last_instr)
            
        for i, instr in enumerate(block.instructions):
            if instr.opcode in terminators and i != len(block.instructions) - 1:
                self._report(f"Terminator {instr.opcode} found in the middle of block {block.name}.", instr)
            
            self._verify_instruction(instr, func)

    def _verify_instruction(self, instr: MachineInstruction, func: MachineFunction):
        # Basic sanity checks on operands
        for op in instr.operands:
            if op.type == OperandType.REGISTER:
                # Should have a valid register class
                if not isinstance(op.value.reg_class, RegisterClass):
                    self._report(f"Invalid register class {op.value.reg_class} in instruction {instr}", instr)
            elif op.type == OperandType.LABEL:
                # Target label must exist in function
                target = op.value
                found = any(b.name == target for b in func.blocks)
                if not found:
                    self._report(f"Branch target label {target} not found in function {func.name}", instr)
                    
        # Check dest
        if instr.dest:
            if instr.dest.type != OperandType.REGISTER and instr.dest.type != OperandType.STACK_SLOT:
                self._report(f"Destination must be a register or stack slot, got {instr.dest.type}", instr)
