from typing import Dict, Set, List, Any
from aayu.compiler.mir.nodes import FunctionMIR, BasicBlock, RegisterID
from aayu.compiler.pass_manager import AnalysisPass

class LivenessPass(AnalysisPass):
    """
    Computes LiveIn and LiveOut sets for each BasicBlock in a FunctionMIR.
    """
    
    def __init__(self):
        self.live_in: Dict[str, Set[int]] = {}
        self.live_out: Dict[str, Set[int]] = {}
        self.use: Dict[str, Set[int]] = {}
        self.def_: Dict[str, Set[int]] = {}

    def run(self, func: FunctionMIR) -> FunctionMIR:
        if not func.blocks:
            return func
            
        self._compute_use_def(func)
        self._compute_liveness(func)
        
        # Store for future analysis
        func.analysis = getattr(func, 'analysis', {})
        func.analysis['live_in'] = self.live_in
        func.analysis['live_out'] = self.live_out
        
        return func
        
    def _extract_registers(self, operand: Any) -> List[int]:
        if isinstance(operand, RegisterID):
            return [operand.id]
        elif isinstance(operand, list):
            regs = []
            for item in operand:
                regs.extend(self._extract_registers(item))
            return regs
        elif isinstance(operand, tuple):
            regs = []
            for item in operand:
                regs.extend(self._extract_registers(item))
            return regs
        return []

    def _compute_use_def(self, func: FunctionMIR):
        # We need a way to track phi uses per predecessor
        self.phi_uses: Dict[str, Set[int]] = {b.id: set() for b in func.blocks}
        
        for block in func.blocks:
            b_use = set()
            b_def = set()
            
            for instr in block.instructions:
                if instr.opcode.name == "PHI":
                    # For PHI nodes, uses happen on the edges, NOT in the block itself
                    for edge in instr.operands:
                        pred_id, val = edge
                        if isinstance(val, RegisterID):
                            self.phi_uses[pred_id].add(val.id)
                    # Def is still in the block
                    if instr.dest:
                        b_def.add(instr.dest.id)
                else:
                    # Normal instruction Uses
                    for op in instr.operands:
                        regs = self._extract_registers(op)
                        for r in regs:
                            if r not in b_def:
                                b_use.add(r)
                    
                    # Def
                    if instr.dest:
                        b_def.add(instr.dest.id)
                    
            self.use[block.id] = b_use
            self.def_[block.id] = b_def

    def _compute_liveness(self, func: FunctionMIR):
        # Initialize
        for block in func.blocks:
            self.live_in[block.id] = set()
            self.live_out[block.id] = set()
            
        # Iterate until no changes
        changed = True
        while changed:
            changed = False
            # Iterate backwards (or just any order, RPO backwards is fastest)
            for block in reversed(func.analysis.get('rpo_blocks', func.blocks)):
                # LiveOut = union of LiveIn of all successors + PHI edge uses
                new_out = set(self.phi_uses[block.id])
                for succ in block.successors:
                    new_out.update(self.live_in[succ.id])
                    
                # LiveIn = Use U (LiveOut - Def)
                new_in = set(self.use[block.id])
                new_in.update(new_out - self.def_[block.id])
                
                if new_out != self.live_out[block.id]:
                    self.live_out[block.id] = new_out
                    changed = True
                    
                if new_in != self.live_in[block.id]:
                    self.live_in[block.id] = new_in
                    changed = True
