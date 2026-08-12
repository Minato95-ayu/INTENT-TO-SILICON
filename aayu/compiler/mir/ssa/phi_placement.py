from typing import Dict, Set, List
from aayu.compiler.mir.nodes import FunctionMIR, Instruction, Opcode
from aayu.compiler.pass_manager import OptimizationPass

class PhiPlacementPass(OptimizationPass):
    """
    Cytron's Algorithm for Phi Node Insertion.
    Places PHI nodes at join points in the CFG using Dominance Frontiers.
    (Operates on local variables before they are renamed to SSA RegisterIDs).
    """
    def run(self, func: FunctionMIR) -> FunctionMIR:
        if not hasattr(func, 'analysis') or 'df' not in func.analysis:
            raise Exception("Dominance Frontier not found. Run DominatorTreePass first.")
            
        df: Dict[str, Set[str]] = func.analysis['df']
        
        # 1. Gather all blocks where a local variable is defined (STORE_LOCAL)
        def_blocks: Dict[str, Set[str]] = {}
        for block in func.blocks:
            for instr in block.instructions:
                if instr.opcode == Opcode.STORE_LOCAL:
                    var_name = instr.operands[0]
                    if var_name not in def_blocks:
                        def_blocks[var_name] = set()
                    def_blocks[var_name].add(block.id)
                    
        # 2. Iteratively place PHI nodes
        phi_placed: Dict[str, Set[str]] = {} # var_name -> set of block_ids
        
        for var_name, blocks in def_blocks.items():
            phi_placed[var_name] = set()
            worklist = list(blocks)
            
            while worklist:
                b_id = worklist.pop(0)
                
                # For every block in the dominance frontier of b_id
                for d_id in df.get(b_id, []):
                    if d_id not in phi_placed[var_name]:
                        phi_placed[var_name].add(d_id)
                        # Add PHI node to block d_id
                        target_block = next(b for b in func.blocks if b.id == d_id)
                        
                        # We place a dummy PHI node. The renamer will resolve the arguments and dest.
                        # operands will hold the variable name for now so renamer knows what it's for.
                        phi_instr = Instruction(opcode=Opcode.PHI, operands=[var_name])
                        
                        # Insert PHI at the top of the block
                        target_block.instructions.insert(0, phi_instr)
                        
                        # The block with the new PHI node is also a definition, so add to worklist
                        if d_id not in blocks:
                            worklist.append(d_id)
                            blocks.add(d_id)
                            
        return func
