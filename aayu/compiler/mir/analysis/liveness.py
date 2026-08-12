from typing import Dict, Set
from aayu.compiler.mir.nodes import FunctionMIR, Instruction, RegisterID, Opcode
from aayu.compiler.pass_manager import AnalysisPass

class LivenessPass(AnalysisPass):
    """
    Computes Live-In and Live-Out sets for each BasicBlock.
    Required for Register Allocation (Phase 13) and Dead Code Elimination.
    """
    def __init__(self):
        self.live_in: Dict[str, Set[int]] = {}
        self.live_out: Dict[str, Set[int]] = {}
        self.use: Dict[str, Set[int]] = {}
        self.def_set: Dict[str, Set[int]] = {}

    def run(self, func: FunctionMIR) -> FunctionMIR:
        if not func.blocks:
            return func
            
        self._compute_local_liveness(func)
        self._compute_global_liveness(func)
        
        func.analysis = getattr(func, 'analysis', {})
        func.analysis['live_in'] = self.live_in
        func.analysis['live_out'] = self.live_out
        
        return func

    def _compute_local_liveness(self, func: FunctionMIR):
        self.use = {b.id: set() for b in func.blocks}
        self.def_set = {b.id: set() for b in func.blocks}
        
        for b in func.blocks:
            for instr in b.instructions:
                # Uses
                for op in instr.operands:
                    if isinstance(op, RegisterID):
                        if op.id not in self.def_set[b.id]:
                            self.use[b.id].add(op.id)
                    # PHI uses (not strictly handled locally here since PHI reads depend on predecessor edges)
                    elif isinstance(op, list) and len(op) > 0 and isinstance(op[0], tuple):
                        for block_id, val in op:
                            # Only count as 'use' for the edge, standard liveness treats PHI inputs as live-out 
                            # on the predecessor block. But for basic approximation:
                            if isinstance(val, RegisterID) and val.id not in self.def_set[b.id]:
                                self.use[b.id].add(val.id)
                                
                # Def
                if instr.dest:
                    self.def_set[b.id].add(instr.dest.id)

    def _compute_global_liveness(self, func: FunctionMIR):
        self.live_in = {b.id: set() for b in func.blocks}
        self.live_out = {b.id: set() for b in func.blocks}
        
        changed = True
        while changed:
            changed = False
            # Iterate backwards (Reverse Post Order is ideal, but Python blocks reversed is decent)
            for b in reversed(func.blocks):
                # out[b] = union(in[s] for s in successors)
                new_out = set()
                for succ in b.successors:
                    new_out.update(self.live_in[succ.id])
                
                # in[b] = use[b] U (out[b] - def[b])
                new_in = self.use[b.id].union(new_out - self.def_set[b.id])
                
                if new_in != self.live_in[b.id] or new_out != self.live_out[b.id]:
                    self.live_in[b.id] = new_in
                    self.live_out[b.id] = new_out
                    changed = True
