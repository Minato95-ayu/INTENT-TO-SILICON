from typing import Dict, Tuple, Any
from aayu.compiler.mir.nodes import FunctionMIR, Opcode, RegisterID
from aayu.compiler.pass_manager import OptimizationPass

class CommonSubexpressionEliminationPass(OptimizationPass):
    """
    Eliminates redundant computations.
    If 'r1 = a + b' and later 'r2 = a + b' are encountered, the latter
    is replaced with 'r2 = MOVE r1'.
    """
    def __init__(self):
        self.stats_cse_hits = 0

    def run(self, func: FunctionMIR) -> bool:
        changed = False
        self.stats_cse_hits = 0
        
        # Maps expression hash to the RegisterID that computes it
        expr_cache: Dict[Tuple[Opcode, Tuple[Any, ...], str], RegisterID] = {}
        
        for block in func.blocks:
            for instr in block.instructions:
                # We only perform CSE on side-effect free instructions
                if not instr.opcode.traits.side_effect and not instr.opcode.traits.reads_memory and not instr.opcode.traits.writes_memory and instr.dest:
                    
                    # Compute a safe hash key including metadata to prevent false positives
                    metadata_str = str(instr.metadata) if hasattr(instr, 'metadata') else ""
                    
                    # Operands can be RegisterIDs or constants. Convert to tuple.
                    ops = []
                    for op in instr.operands:
                        if isinstance(op, RegisterID):
                            ops.append(f"reg_{op.id}")
                        elif isinstance(op, list):
                            # Not hashable easily, skip CSE for complex structures like PHI
                            ops = None
                            break
                        else:
                            ops.append(op)
                            
                    if ops is None:
                        continue
                        
                    expr_key = (instr.opcode, tuple(ops), metadata_str)
                    
                    if expr_key in expr_cache:
                        # CSE Hit!
                        cached_reg = expr_cache[expr_key]
                        instr.opcode = Opcode.MOVE
                        instr.operands = [cached_reg]
                        self.stats_cse_hits += 1
                        changed = True
                    else:
                        # Cache it for future instructions
                        expr_cache[expr_key] = instr.dest
                        
        return changed
