from typing import List, Set
from aayu.compiler.mir.nodes import FunctionMIR, BasicBlock
from aayu.compiler.pass_manager import AnalysisPass

class InstructionNumberingPass(AnalysisPass):
    """
    Assigns sequential indices to all instructions in the CFG using 
    Reverse Post Order (RPO). Indices are incremented by 2 to leave gaps
    for later pseudo-instruction insertions (like spills).
    """
    
    def __init__(self):
        self.rpo_blocks: List[BasicBlock] = []

    def run(self, func: FunctionMIR) -> FunctionMIR:
        if not func.blocks:
            return func
            
        # 1. Compute RPO of basic blocks
        self.rpo_blocks = self._compute_rpo(func)
        
        # 2. Assign indices to instructions
        current_index = 0
        for block in self.rpo_blocks:
            for instr in block.instructions:
                instr.index = current_index
                current_index += 2
                
        # Store for future analysis
        func.analysis = getattr(func, 'analysis', {})
        func.analysis['rpo_blocks'] = self.rpo_blocks
        
        return func
        
    def _compute_rpo(self, func: FunctionMIR) -> List[BasicBlock]:
        visited: Set[str] = set()
        post_order: List[BasicBlock] = []
        
        def dfs(block: BasicBlock):
            visited.add(block.id)
            for succ in block.successors:
                if succ.id not in visited:
                    dfs(succ)
            post_order.append(block)
            
        dfs(func.entry_block)
        
        return list(reversed(post_order))
