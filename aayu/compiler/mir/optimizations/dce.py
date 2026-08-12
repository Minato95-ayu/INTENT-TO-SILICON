from typing import List
from aayu.compiler.mir.nodes import FunctionMIR, RegisterID
from aayu.compiler.mir.analysis.def_use import DefUsePass
from aayu.compiler.pass_manager import OptimizationPass

class DeadCodeEliminationPass(OptimizationPass):
    """
    Generic Dead Code Elimination.
    Removes instructions whose destination register has 0 uses,
    provided the instruction has no side effects.
    """
    def __init__(self):
        self.stats_dead_inst = 0
        self.analysis_manager = None

    def run(self, func: FunctionMIR) -> bool:
        changed = False
        self.stats_dead_inst = 0
        
        # Get up-to-date Def-Use chains
        def_use = self.analysis_manager.get_analysis(DefUsePass, func)
        use_chains = def_use.uses
        
        for block in func.blocks:
            to_remove: List[int] = []
            
            for i, instr in enumerate(block.instructions):
                # We can't eliminate side-effecting instructions (CALL, STORE, JUMP, etc.)
                if instr.opcode.traits.side_effect:
                    continue
                    
                # We can't eliminate instructions with no destination (though side_effect should cover this)
                if not instr.dest:
                    continue
                    
                # Check uses
                uses = use_chains.get(instr.dest.id, [])
                if len(uses) == 0:
                    to_remove.append(i)
                    self.stats_dead_inst += 1
                    changed = True
                    
            # Remove from back to front
            for idx in sorted(to_remove, reverse=True):
                block.instructions.pop(idx)
                
        return changed
