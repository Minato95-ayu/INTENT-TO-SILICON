from aayu.compiler.mir.nodes import FunctionMIR, Opcode
from aayu.compiler.pass_manager import OptimizationPass

class BranchSimplificationPass(OptimizationPass):
    """
    Simplifies BRANCH instructions with constant conditions into unconditional JUMP instructions.
    """
    def __init__(self):
        self.stats_branches_simplified = 0

    def run(self, func: FunctionMIR) -> bool:
        changed = False
        self.stats_branches_simplified = 0
        
        for block in func.blocks:
            if not block.instructions:
                continue
                
            last_instr = block.instructions[-1]
            if last_instr.opcode == Opcode.BRANCH:
                cond = last_instr.operands[0]
                
                # If the condition is a known boolean constant
                if isinstance(cond, bool):
                    target_if_true = last_instr.operands[1]
                    target_if_false = last_instr.operands[2]
                    
                    chosen_target = target_if_true if cond else target_if_false
                    
                    last_instr.opcode = Opcode.JUMP
                    last_instr.operands = [chosen_target]
                    
                    self.stats_branches_simplified += 1
                    changed = True
                    
        return changed
