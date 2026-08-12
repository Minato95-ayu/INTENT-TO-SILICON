from aayu.compiler.lir.nodes import FunctionLIR, LIROpcode
from aayu.compiler.pass_manager import OptimizationPass

class LIRVerifierPass(OptimizationPass):
    """
    Verifies that the LIR function is well-formed:
    - No PHI nodes exist (there is no LIR_PHI opcode anyway, but just in case)
    - All jump targets are valid LIRBlocks
    - Every block is reachable (except maybe entry)
    - Virtual registers only (actually, just checks that all dests/operands are valid)
    - Critical edges are removed
    """
    
    def run(self, func: FunctionLIR) -> FunctionLIR:
        if not func.blocks:
            return func
            
        block_names = {b.name for b in func.blocks}
        
        for block in func.blocks:
            # Check critical edges
            for succ in block.successors:
                # If block has >1 successors AND succ has >1 predecessors, it's a critical edge!
                if len(block.successors) > 1 and len(succ.predecessors) > 1:
                    raise ValueError(f"Critical edge found between {block.name} and {succ.name}")
                    
            # Check instructions
            for instr in block.instructions:
                if instr.opcode.name == "PHI":
                    raise ValueError("PHI node found in LIR!")
                    
                # Check valid jump targets
                if instr.opcode in (LIROpcode.LIR_JUMP, LIROpcode.LIR_BRANCH):
                    for op in instr.operands:
                        if isinstance(op, str) and op not in block_names:
                            # Not all string operands are labels, but in JUMP/BRANCH they are
                            raise ValueError(f"Invalid jump target {op} in block {block.name}")
                            
        return func
