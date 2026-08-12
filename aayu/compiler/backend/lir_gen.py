from typing import Dict, List, Set, Tuple
from aayu.compiler.mir.nodes import FunctionMIR, BasicBlock, Instruction, Opcode
from aayu.compiler.lir.nodes import FunctionLIR, LIRBlock, LIRInstruction, LIROpcode
from aayu.compiler.pass_manager import OptimizationPass

class LIRGenerationPass(OptimizationPass):
    """
    Translates MIR to LIR.
    Handles PHI elimination and Critical Edge splitting during translation.
    """
    
    def run(self, func: FunctionMIR) -> FunctionLIR:
        lir_func = FunctionLIR(
            name=func.name,
            locals_count=getattr(func, 'locals_count', 0),
            params_count=getattr(func, 'params_count', 0)
        )
        
        if not func.blocks:
            return lir_func
            
        # 1. Map MIR blocks to LIR blocks
        block_map: Dict[str, LIRBlock] = {}
        for block in func.blocks:
            block_map[block.id] = LIRBlock(name=block.id)
            lir_func.blocks.append(block_map[block.id])
            
        lir_func.entry_block = block_map[func.entry_block.id]
        
        # Helper to map MIR Opcodes to LIROpcodes
        def map_opcode(op: Opcode) -> LIROpcode:
            name = op.name
            if name == "PHI":
                raise ValueError("PHI nodes should not be directly mapped to LIR")
            if name == "COPY":
                return LIROpcode.LIR_MOVE
            # For others, we just prepend LIR_
            return LIROpcode["LIR_" + name]
            
        # 2. Translate instructions and wire CFG
        for mir_block in func.blocks:
            lir_block = block_map[mir_block.id]
            
            # Wire CFG
            for succ in mir_block.successors:
                lir_succ = block_map[succ.id]
                if lir_succ not in lir_block.successors:
                    lir_block.successors.append(lir_succ)
            for pred in mir_block.predecessors:
                lir_pred = block_map[pred.id]
                if lir_pred not in lir_block.predecessors:
                    lir_block.predecessors.append(lir_pred)
                    
            for instr in mir_block.instructions:
                if instr.opcode == Opcode.PHI:
                    continue # Handled later
                    
                lir_instr = LIRInstruction(
                    opcode=map_opcode(instr.opcode),
                    operands=list(instr.operands),
                    dest=instr.dest
                )
                lir_block.instructions.append(lir_instr)
                
        # 3. PHI Elimination & Critical Edge Splitting
        split_counter = 0
        
        for mir_block in func.blocks:
            phis = [i for i in mir_block.instructions if i.opcode == Opcode.PHI]
            if not phis:
                continue
                
            lir_block = block_map[mir_block.id]
            
            # We need to insert a MOVE for each PHI operand into the predecessor
            for phi in phis:
                dest = phi.dest
                
                # operands are tuples (block_name, val)
                for pred_name, val in phi.operands:
                    mir_pred = next(b for b in func.blocks if b.id == pred_name)
                    lir_pred = block_map[pred_name]
                    
                    # Check if edge (lir_pred -> lir_block) is critical
                    # Critical edge: pred has >1 successors AND block has >1 predecessors
                    is_critical = len(mir_pred.successors) > 1 and len(mir_block.predecessors) > 1
                    
                    target_block = lir_pred
                    
                    if is_critical:
                        # Split edge!
                        # We create a helper block between lir_pred and lir_block
                        split_name = f"{lir_pred.name}_split_{split_counter}"
                        split_counter += 1
                        helper_block = LIRBlock(name=split_name)
                        lir_func.blocks.append(helper_block)
                        
                        # Fix CFG
                        # lir_pred -> helper_block -> lir_block
                        lir_pred.successors.remove(lir_block)
                        lir_pred.successors.append(helper_block)
                        
                        lir_block.predecessors.remove(lir_pred)
                        lir_block.predecessors.append(helper_block)
                        
                        helper_block.predecessors.append(lir_pred)
                        helper_block.successors.append(lir_block)
                        
                        # Add Jump from helper to lir_block
                        helper_block.instructions.append(LIRInstruction(
                            opcode=LIROpcode.LIR_JUMP,
                            operands=[lir_block.name]
                        ))
                        
                        # Update the jump/branch in lir_pred to point to helper_block
                        for instr in lir_pred.instructions:
                            if instr.opcode in (LIROpcode.LIR_JUMP, LIROpcode.LIR_BRANCH):
                                for i, op in enumerate(instr.operands):
                                    if op == lir_block.name:
                                        instr.operands[i] = helper_block.name
                                        
                        target_block = helper_block
                        
                    # Insert MOVE into target_block
                    # It must be inserted BEFORE the terminator instruction (JUMP/BRANCH/RET)
                    move_instr = LIRInstruction(
                        opcode=LIROpcode.LIR_MOVE,
                        operands=[val],
                        dest=dest
                    )
                    
                    # Find insertion point
                    insert_idx = len(target_block.instructions)
                    if insert_idx > 0:
                        last_instr = target_block.instructions[-1]
                        if last_instr.opcode.traits.is_terminator:
                            insert_idx -= 1
                            
                    target_block.instructions.insert(insert_idx, move_instr)
                    
        return lir_func
