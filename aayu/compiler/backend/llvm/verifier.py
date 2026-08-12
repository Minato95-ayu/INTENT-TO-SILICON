from aayu.compiler.backend.llvm.values import (
    LLVMModule, LLVMFunction, LLVMBasicBlock, LLVMInstruction,
    LLVMValue
)
from aayu.compiler.errors import DiagnosticEngine, DiagnosticSeverity

class LLVMIRVerifier:
    """Verifies internal LLVM IR Graph invariants."""
    def __init__(self, diag: DiagnosticEngine):
        self.diag = diag
        self.valid = True

    def _report(self, msg: str):
        self.valid = False
        self.diag.report(DiagnosticSeverity.ERROR, f"LLVM IR Verification Failed: {msg}")

    def verify(self, module: LLVMModule) -> bool:
        self.valid = True
        for func in module.functions:
            self._verify_function(func)
        return self.valid
        
    def _verify_function(self, func: LLVMFunction):
        if func.is_declare_only:
            return
            
        if not func.blocks:
            self._report(f"Function @{func.name} has no basic blocks.")
            return
            
        labels = set()
        for block in func.blocks:
            if block.name in labels:
                self._report(f"Duplicate block label '{block.name}' in @{func.name}")
            labels.add(block.name)
            self._verify_block(block, func)

    def _verify_block(self, block: LLVMBasicBlock, func: LLVMFunction):
        if not block.instructions:
            self._report(f"Block {block.name} in @{func.name} is empty.")
            return
            
        # Verify terminator
        last_instr = block.instructions[-1]
        terminators = {"br", "ret"}
        if last_instr.opcode not in terminators:
            self._report(f"Block {block.name} in @{func.name} does not end with a terminator (found {last_instr.opcode}).")
            
        for i, instr in enumerate(block.instructions):
            if instr.opcode in terminators and i != len(block.instructions) - 1:
                self._report(f"Terminator {instr.opcode} found in the middle of block {block.name}.")
            
            self._verify_instruction(instr, block, func)

    def _verify_instruction(self, instr: LLVMInstruction, block: LLVMBasicBlock, func: LLVMFunction):
        if instr.parent != block:
            self._report(f"Instruction {instr.opcode} has incorrect parent block.")
            
        # Verify uses/users links are intact
        for op in instr.operands:
            # op is a `Use`. op.value is the LLVMValue
            if op.user != instr:
                self._report(f"Use edge corrupted: {instr.opcode} uses a value but user link points elsewhere.")
                
            if op not in op.value.uses:
                self._report(f"Use edge missing: {instr.opcode} uses {op.value.name}, but not in its uses list.")
                
        # Type checking simple ops
        if instr.opcode in ("add", "sub", "mul", "sdiv"):
            lhs = instr.get_operand(0)
            rhs = instr.get_operand(1)
            if lhs.type != rhs.type:
                self._report(f"Type mismatch in {instr.opcode}: {lhs.type.serialize()} vs {rhs.type.serialize()}")
            if instr.type != lhs.type:
                self._report(f"Return type mismatch in {instr.opcode}: {instr.type.serialize()} vs {lhs.type.serialize()}")
