from typing import Dict, Any, List
from aayu.compiler.mir.nodes import FunctionMIR, RegisterID
from aayu.compiler.pass_manager import AnalysisPass
from aayu.compiler.backend.registers import LiveInterval

class LiveIntervalConstructionPass(AnalysisPass):
    """
    Constructs LiveInterval objects for each virtual register,
    incorporating defs, uses, and block boundaries from Liveness analysis.
    """
    
    def __init__(self):
        self.intervals: Dict[int, LiveInterval] = {}

    def get_interval(self, reg_id: int) -> LiveInterval:
        if reg_id not in self.intervals:
            self.intervals[reg_id] = LiveInterval(register_id=reg_id)
        return self.intervals[reg_id]

    def run(self, func: FunctionMIR) -> FunctionMIR:
        if not func.blocks:
            return func
            
        if not hasattr(func, 'analysis') or 'live_out' not in func.analysis:
            raise Exception("Liveness analysis required for LiveInterval Construction.")
            
        rpo_blocks = func.analysis.get('rpo_blocks', func.blocks)
        live_in = func.analysis['live_in']
        live_out = func.analysis['live_out']
        
        # 1. Add uses for explicit instruction operands and defs
        for block in rpo_blocks:
            if not block.instructions:
                continue
                
            first_idx = block.instructions[0].index
            last_idx = block.instructions[-1].index
            
            # Artificial boundary uses based on Liveness Dataflow
            # This ensures intervals span across intermediate blocks where they are live
            for reg in live_in[block.id]:
                # Live entering this block
                self.get_interval(reg).add_use(first_idx)
                
            for reg in live_out[block.id]:
                # Live exiting this block
                self.get_interval(reg).add_use(last_idx)
                
            # Actual instruction uses
            for instr in block.instructions:
                # Def
                if instr.dest:
                    self.get_interval(instr.dest.id).add_use(instr.index)
                    
                # Uses
                # Note: PHI uses happen on the edge. The predecessor's LiveOut already 
                # catches it, so the interval is extended to the end of the predecessor. 
                # We still add the use here just to bump the use_count for spill_cost.
                for op in instr.operands:
                    for r in self._extract_registers(op):
                        self.get_interval(r).add_use(instr.index)
                        
        # 2. Compute spill costs
        for interval in self.intervals.values():
            interval.compute_spill_cost()
            
        # Store for future analysis
        func.analysis['intervals'] = self.intervals
        
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
