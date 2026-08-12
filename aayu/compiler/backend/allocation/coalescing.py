from typing import Dict, List, Set
from aayu.compiler.mir.nodes import FunctionMIR, Instruction, RegisterID
from aayu.compiler.pass_manager import OptimizationPass
from aayu.compiler.backend.registers import LiveInterval

class RegisterCoalescingPass(OptimizationPass):
    """
    Eliminates redundant MOVE instructions by coalescing non-overlapping LiveIntervals.
    """
    
    def run(self, func: FunctionMIR) -> FunctionMIR:
        if not func.blocks:
            return func
            
        if not hasattr(func, 'analysis') or 'intervals' not in func.analysis:
            raise Exception("Live Intervals required for Register Coalescing.")
            
        intervals: Dict[int, LiveInterval] = func.analysis['intervals']
        
        # 1. Build Move Graph and find coalescing candidates
        moves_to_remove = set()
        merged_map: Dict[int, int] = {} # target -> source
        
        # A simple aggressive coalescer:
        # If we see `rA = copy rB`, and `interval(rA)` does not overlap with `interval(rB)`
        # Then we can merge them into a single interval and eliminate the copy.
        # Since we're SSA, we have 'copy' instructions usually coming from optimizations
        # or lowering. Wait, does MIR have a `copy`? Currently we have `phi`, which implicitly
        # are moves at the edges. Also, if there are explicit `copy` opcodes.
        
        # Let's search for explicit 'copy' or 'move' instructions.
        for block in func.blocks:
            for instr in block.instructions:
                if instr.opcode.name in ("COPY", "MOVE"):
                    src = instr.operands[0]
                    dest = instr.dest
                    if dest and hasattr(src, 'id'):
                        r_src = src.id
                        r_dest = dest.id
                        
                        # Resolve true root via merged_map
                        while r_src in merged_map: r_src = merged_map[r_src]
                        while r_dest in merged_map: r_dest = merged_map[r_dest]
                        
                        if r_src == r_dest:
                            moves_to_remove.add(id(instr))
                            continue
                            
                        # Check overlap
                        int_src = intervals.get(r_src)
                        int_dest = intervals.get(r_dest)
                        
                        if int_src and int_dest:
                            # They overlap if max(start1, start2) < min(end1, end2)
                            overlap = max(int_src.start, int_dest.start) < min(int_src.end, int_dest.end)
                            
                            if not overlap:
                                # Union!
                                # Extend interval
                                int_src.start = min(int_src.start, int_dest.start)
                                int_src.end = max(int_src.end, int_dest.end)
                                int_src.uses.extend(int_dest.uses)
                                int_src.uses = list(set(int_src.uses))
                                
                                # Mark as merged
                                merged_map[r_dest] = r_src
                                moves_to_remove.add(id(instr))
                                
        # 2. Rewrite remaining uses in instructions to point to the coalesced registers
        moves_removed_count = 0
        
        for block in func.blocks:
            new_instrs = []
            for instr in block.instructions:
                if id(instr) in moves_to_remove:
                    moves_removed_count += 1
                    continue
                    
                # Rewrite operands
                new_operands = []
                for op in instr.operands:
                    if hasattr(op, 'id') and isinstance(op, RegisterID):
                        r_op = op.id
                        while r_op in merged_map: r_op = merged_map[r_op]
                        new_operands.append(RegisterID(id=r_op))
                    else:
                        new_operands.append(op)
                instr.operands = new_operands
                
                # Rewrite dest
                if instr.dest and isinstance(instr.dest, RegisterID):
                    r_dest = instr.dest.id
                    while r_dest in merged_map: r_dest = merged_map[r_dest]
                    instr.dest = RegisterID(id=r_dest)
                    
                new_instrs.append(instr)
                
            block.instructions = new_instrs
            
        # Store metrics
        func.analysis['moves_removed'] = moves_removed_count
        
        return func
