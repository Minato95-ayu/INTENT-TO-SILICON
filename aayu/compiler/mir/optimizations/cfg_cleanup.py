from typing import Set, Dict, List
from aayu.compiler.mir.nodes import FunctionMIR, BasicBlock, Opcode
from aayu.compiler.pass_manager import OptimizationPass

class CFGCleanupPass(OptimizationPass):
    """
    Cleans up the CFG by:
    1. Identifying unreachable blocks and removing them.
    2. Rebuilding successors and predecessors edges.
    3. Updating PHI nodes to remove edges from now-dead predecessors.
    4. Simplifying single-edge PHI nodes into MOVE instructions.
    """
    def __init__(self):
        self.stats_dead_blocks = 0

    def run(self, func: FunctionMIR) -> bool:
        changed = False
        self.stats_dead_blocks = 0
        
        if not func.blocks:
            return False
            
        # 1. Discover reachable blocks (BFS)
        reachable: Set[str] = set()
        queue: List[str] = [func.blocks[0].id]
        
        block_map: Dict[str, BasicBlock] = {b.id: b for b in func.blocks}
        
        while queue:
            curr_id = queue.pop(0)
            if curr_id in reachable:
                continue
            reachable.add(curr_id)
            
            curr_block = block_map[curr_id]
            if curr_block.instructions:
                last_instr = curr_block.instructions[-1]
                if last_instr.opcode == Opcode.JUMP:
                    queue.append(last_instr.operands[0])
                elif last_instr.opcode == Opcode.BRANCH:
                    queue.append(last_instr.operands[1])
                    queue.append(last_instr.operands[2])
                    
        # Count dead blocks
        dead_count = len(func.blocks) - len(reachable)
        if dead_count > 0:
            self.stats_dead_blocks = dead_count
            changed = True
            
        # Filter dead blocks
        new_blocks = [b for b in func.blocks if b.id in reachable]
        func.blocks = new_blocks
        
        # 2. Rebuild Successors and Predecessors
        for b in func.blocks:
            b.successors.clear()
            b.predecessors.clear()
            
        for b in func.blocks:
            if not b.instructions:
                continue
            last_instr = b.instructions[-1]
            if last_instr.opcode == Opcode.JUMP:
                target_id = last_instr.operands[0]
                target_block = block_map[target_id]
                b.successors.append(target_block)
                target_block.predecessors.append(b)
            elif last_instr.opcode == Opcode.BRANCH:
                t1_id = last_instr.operands[1]
                t2_id = last_instr.operands[2]
                t1_block = block_map[t1_id]
                t2_block = block_map[t2_id]
                b.successors.append(t1_block)
                t1_block.predecessors.append(b)
                b.successors.append(t2_block)
                t2_block.predecessors.append(b)
                
        # 3. Update PHI Nodes
        for b in func.blocks:
            valid_preds = {p.id for p in b.predecessors}
            for instr in b.instructions:
                if instr.opcode == Opcode.PHI:
                    old_edges = instr.operands
                    # Keep edges only from valid current predecessors
                    new_edges = [edge for edge in old_edges if edge[0] in valid_preds]
                    
                    if len(new_edges) != len(old_edges):
                        changed = True
                        
                    if len(new_edges) == 1:
                        # Simplify PHI to MOVE!
                        instr.opcode = Opcode.MOVE
                        instr.operands = [new_edges[0][1]]
                        changed = True
                    else:
                        instr.operands = new_edges

        return changed
