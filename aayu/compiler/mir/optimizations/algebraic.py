from aayu.compiler.mir.nodes import FunctionMIR, Opcode, RegisterID
from aayu.compiler.pass_manager import OptimizationPass

class AlgebraicSimplificationPass(OptimizationPass):
    """
    Simplifies algebraic identities:
    x + 0 -> x
    x * 1 -> x
    x * 0 -> 0
    Replaces with a MOVE or LOAD_CONST which will be handled by subsequent passes.
    """
    def __init__(self):
        self.stats_simplified = 0

    def run(self, func: FunctionMIR) -> bool:
        changed = False
        self.stats_simplified = 0
        
        for block in func.blocks:
            for instr in block.instructions:
                if instr.opcode == Opcode.ADD:
                    if len(instr.operands) == 2:
                        left, right = instr.operands
                        if right == 0:
                            instr.opcode = Opcode.MOVE
                            instr.operands = [left]
                            self.stats_simplified += 1
                            changed = True
                        elif left == 0:
                            instr.opcode = Opcode.MOVE
                            instr.operands = [right]
                            self.stats_simplified += 1
                            changed = True
                            
                elif instr.opcode == Opcode.SUB:
                    if len(instr.operands) == 2:
                        left, right = instr.operands
                        if right == 0:
                            instr.opcode = Opcode.MOVE
                            instr.operands = [left]
                            self.stats_simplified += 1
                            changed = True
                            
                elif instr.opcode == Opcode.MUL:
                    if len(instr.operands) == 2:
                        left, right = instr.operands
                        if right == 1:
                            instr.opcode = Opcode.MOVE
                            instr.operands = [left]
                            self.stats_simplified += 1
                            changed = True
                        elif left == 1:
                            instr.opcode = Opcode.MOVE
                            instr.operands = [right]
                            self.stats_simplified += 1
                            changed = True
                        elif right == 0 or left == 0:
                            instr.opcode = Opcode.LOAD_CONST
                            instr.operands = [0]
                            self.stats_simplified += 1
                            changed = True
                            
                elif instr.opcode == Opcode.DIV:
                    if len(instr.operands) == 2:
                        left, right = instr.operands
                        if right == 1:
                            instr.opcode = Opcode.MOVE
                            instr.operands = [left]
                            self.stats_simplified += 1
                            changed = True
                            
        return changed
