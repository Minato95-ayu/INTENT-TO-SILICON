from typing import Dict, List
from aayu.compiler.mir.nodes import FunctionMIR, Opcode, Instruction
from aayu.compiler.pass_manager import OptimizationPass

class DeadStoreEliminationPass(OptimizationPass):
    """
    Eliminates redundant STORE_GLOBAL instructions if they are overwritten
    before being read. Obeys memory alias barriers (CALL, LOAD_GLOBAL).
    """
    def __init__(self):
        self.stats_dead_stores_eliminated = 0

    def run(self, func: FunctionMIR) -> bool:
        changed = False
        self.stats_dead_stores_eliminated = 0
        
        # DSE is best run backwards within a basic block, or forwards tracking pending stores
        for block in func.blocks:
            # maps variable name -> index of the pending store instruction
            pending_stores: Dict[str, int] = {}
            to_remove: List[int] = []
            
            for i, instr in enumerate(block.instructions):
                if instr.opcode == Opcode.STORE_GLOBAL:
                    var_name = instr.operands[0]
                    if var_name in pending_stores:
                        # Found a store that overwrites a previous pending store!
                        # We can eliminate the previous one.
                        to_remove.append(pending_stores[var_name])
                        self.stats_dead_stores_eliminated += 1
                        changed = True
                    # Register this new store as pending
                    pending_stores[var_name] = i
                    
                elif instr.opcode == Opcode.LOAD_GLOBAL:
                    var_name = instr.operands[0]
                    # The variable is read, so the pending store is no longer dead
                    if var_name in pending_stores:
                        del pending_stores[var_name]
                        
                elif instr.opcode.traits.reads_memory or instr.opcode.traits.writes_memory or instr.opcode == Opcode.CALL:
                    # Full memory barrier (CALL might read or write anything)
                    # Also unknown memory writes/reads
                    pending_stores.clear()
                    
            # Remove the instructions (in reverse order to preserve indices)
            for idx in sorted(to_remove, reverse=True):
                block.instructions.pop(idx)
                
        return changed
