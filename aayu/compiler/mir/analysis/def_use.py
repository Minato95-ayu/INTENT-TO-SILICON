from typing import Dict, List, Set, Any
from aayu.compiler.mir.nodes import FunctionMIR, Instruction, RegisterID
from aayu.compiler.pass_manager import AnalysisPass

class DefUsePass(AnalysisPass):
    """
    Builds Definition-Use (Def-Use) and Use-Definition (Use-Def) chains.
    Links RegisterIDs directly to the Instruction objects.
    """
    def __init__(self):
        self.defs: Dict[int, Instruction] = {}
        self.uses: Dict[int, List[Instruction]] = {}

    def run(self, func: FunctionMIR) -> FunctionMIR:
        self.defs.clear()
        self.uses.clear()
        
        for block in func.blocks:
            for instr in block.instructions:
                # Track definition
                if instr.dest:
                    # In true SSA, this should never be overwritten.
                    # We store it for later verification.
                    if instr.dest.id not in self.defs:
                        self.defs[instr.dest.id] = instr
                
                # Track uses
                for op in instr.operands:
                    if isinstance(op, RegisterID):
                        if op.id not in self.uses:
                            self.uses[op.id] = []
                        self.uses[op.id].append(instr)
                        
                    # Also handle PHI operands, which will be tuples: [(Block, RegisterID), ...]
                    if isinstance(op, list) and len(op) > 0 and isinstance(op[0], tuple):
                        for block_id, val in op:
                            if isinstance(val, RegisterID):
                                if val.id not in self.uses:
                                    self.uses[val.id] = []
                                self.uses[val.id].append(instr)
        
        func.analysis = getattr(func, 'analysis', {})
        func.analysis['def_use'] = self
        
        return func
        
    def get_def(self, reg: RegisterID) -> Instruction:
        return self.defs.get(reg.id)
        
    def get_uses(self, reg: RegisterID) -> List[Instruction]:
        return self.uses.get(reg.id, [])
