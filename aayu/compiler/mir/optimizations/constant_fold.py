from typing import Dict, Any
from aayu.compiler.mir.nodes import FunctionMIR, Opcode, OpcodeCategory, RegisterID
from aayu.compiler.pass_manager import OptimizationPass

class ConstantPropagationPass(OptimizationPass):
    """
    Performs Constant Propagation and Constant Folding.
    Tracks known constant values and folds arithmetic/logical operations.
    Returns whether the CFG was modified.
    """
    def __init__(self):
        self.stats_folded = 0
        self.stats_propagated = 0

    def run(self, func: FunctionMIR) -> bool:
        changed = False
        self.stats_folded = 0
        self.stats_propagated = 0
        
        constants: Dict[int, Any] = {}
        
        for block in func.blocks:
            for instr in block.instructions:
                
                # 1. Propagate constants into operands
                new_operands = []
                for op in instr.operands:
                    if isinstance(op, RegisterID) and op.id in constants:
                        new_operands.append(constants[op.id])
                        self.stats_propagated += 1
                        changed = True
                    else:
                        new_operands.append(op)
                instr.operands = new_operands
                
                # 2. Fold constants if possible
                if instr.opcode == Opcode.LOAD_CONST and instr.dest:
                    constants[instr.dest.id] = instr.operands[0]
                    
                elif instr.opcode.category in (OpcodeCategory.ARITHMETIC, OpcodeCategory.COMPARE):
                    if all(not isinstance(op, RegisterID) for op in instr.operands):
                        # All operands are constants, we can fold!
                        result = self._evaluate(instr.opcode, instr.operands)
                        if result is not None:
                            instr.opcode = Opcode.LOAD_CONST
                            instr.operands = [result]
                            if instr.dest:
                                constants[instr.dest.id] = result
                            self.stats_folded += 1
                            changed = True

        return changed

    def _evaluate(self, opcode: Opcode, operands: list) -> Any:
        try:
            if opcode == Opcode.ADD:
                return operands[0] + operands[1]
            elif opcode == Opcode.SUB:
                return operands[0] - operands[1]
            elif opcode == Opcode.MUL:
                return operands[0] * operands[1]
            elif opcode == Opcode.DIV:
                return operands[0] / operands[1]
            elif opcode == Opcode.CMP_EQ:
                return operands[0] == operands[1]
            elif opcode == Opcode.CMP_GT:
                return operands[0] > operands[1]
            elif opcode == Opcode.CMP_LT:
                return operands[0] < operands[1]
        except Exception:
            pass
        return None
