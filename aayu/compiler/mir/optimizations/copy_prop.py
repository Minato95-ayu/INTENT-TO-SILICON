from typing import Dict, Any
from aayu.compiler.mir.nodes import FunctionMIR, Opcode, RegisterID
from aayu.compiler.pass_manager import OptimizationPass

class CopyPropagationPass(OptimizationPass):
    """
    Identifies MOVE rX, rY instructions and replaces all uses of rX with rY.
    """
    def __init__(self):
        self.stats_copies_removed = 0

    def run(self, func: FunctionMIR) -> bool:
        changed = False
        self.stats_copies_removed = 0
        
        aliases: Dict[int, RegisterID] = {}
        
        # 1. Identify all copies
        for block in func.blocks:
            for instr in block.instructions:
                if instr.opcode == Opcode.MOVE and instr.dest:
                    src = instr.operands[0]
                    if isinstance(src, RegisterID):
                        aliases[instr.dest.id] = src
                        self.stats_copies_removed += 1
                        # We don't remove it here, DCE will remove it since it has 0 uses!
                        
        def resolve_alias(reg: RegisterID) -> RegisterID:
            curr = reg
            while curr.id in aliases:
                curr = aliases[curr.id]
            return curr

        # 2. Rewrite uses
        for block in func.blocks:
            for instr in block.instructions:
                if instr.opcode == Opcode.PHI:
                    new_edges = []
                    for edge in instr.operands:
                        pred, val = edge
                        if isinstance(val, RegisterID) and val.id in aliases:
                            new_edges.append((pred, resolve_alias(val)))
                            changed = True
                        else:
                            new_edges.append((pred, val))
                    instr.operands = new_edges
                else:
                    new_operands = []
                    for op in instr.operands:
                        if isinstance(op, RegisterID) and op.id in aliases:
                            new_operands.append(resolve_alias(op))
                            changed = True
                        else:
                            new_operands.append(op)
                    instr.operands = new_operands

        return changed
