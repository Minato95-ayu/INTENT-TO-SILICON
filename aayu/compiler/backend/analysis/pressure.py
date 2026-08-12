from typing import Dict, Set, List, Any
from aayu.compiler.mir.nodes import FunctionMIR, RegisterID
from aayu.compiler.pass_manager import AnalysisPass

class RegisterPressurePass(AnalysisPass):
    """
    Computes the peak register pressure at each instruction.
    Requires InstructionNumberingPass and LivenessPass to have run.
    """
    
    def __init__(self):
        # instr.index -> peak pressure (int)
        self.pressure: Dict[int, int] = {}

    def run(self, func: FunctionMIR) -> FunctionMIR:
        if not func.blocks:
            return func
            
        if not hasattr(func, 'analysis') or 'live_out' not in func.analysis:
            raise Exception("Liveness analysis required for RegisterPressurePass.")
            
        rpo_blocks = func.analysis.get('rpo_blocks', func.blocks)
        live_out = func.analysis['live_out']
        
        for block in rpo_blocks:
            # Start with the LiveOut set of the block
            current_live = set(live_out[block.id])
            
            # Iterate backwards through instructions
            for instr in reversed(block.instructions):
                uses = set()
                defs = set()
                
                # Extract uses
                if instr.opcode.name != "PHI":
                    for op in instr.operands:
                        for r in self._extract_registers(op):
                            uses.add(r)
                            
                # Extract defs
                if instr.dest:
                    defs.add(instr.dest.id)
                
                # The registers that must be held in physical registers AT this instruction
                # includes everything live after it, plus its inputs, plus its outputs.
                active_at_instr = current_live.union(uses).union(defs)
                self.pressure[instr.index] = len(active_at_instr)
                
                # Update current_live for the next instruction backwards:
                # Remove what is defined here, add what is used here.
                current_live.difference_update(defs)
                current_live.update(uses)
                
        # Compute metrics
        pressures = list(self.pressure.values())
        peak_pressure = max(pressures) if pressures else 0
        avg_pressure = sum(pressures) / len(pressures) if pressures else 0.0
        
        histogram: Dict[int, int] = {}
        for p in pressures:
            histogram[p] = histogram.get(p, 0) + 1
            
        # Store for future analysis
        func.analysis['pressure'] = self.pressure
        func.analysis['pressure_peak'] = peak_pressure
        func.analysis['pressure_avg'] = avg_pressure
        func.analysis['pressure_histogram'] = histogram
        
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
