from typing import Dict, Set
from aayu.compiler.mir.nodes import FunctionMIR, Instruction, Opcode, RegisterID
from aayu.compiler.pass_manager import VerificationPass

class SSAVerificationPass(VerificationPass):
    """
    Verifies that a FunctionMIR is in strict SSA form.
    Checks:
    - One definition per register
    - Def dominates all uses (except PHI edges)
    - PHI node validity
    """
    def run(self, func: FunctionMIR) -> FunctionMIR:
        if not self.verify(func):
            raise Exception("SSA Verification Failed!")
        return func
        
    def verify(self, func: FunctionMIR) -> bool:
        if getattr(self, 'analysis_manager', None):
            from aayu.compiler.mir.analysis.dominator_tree import DominatorTreePass
            self.analysis_manager.get_analysis(DominatorTreePass, func)
            
        if not hasattr(func, 'analysis') or 'dom' not in func.analysis:
            raise Exception("Dominator analysis required for SSA verification.")
            
        dom: Dict[str, Set[str]] = func.analysis['dom']
        
        defs: Dict[int, str] = {} # reg_id -> block_id
        
        # Pass 1: Find all definitions
        for b in func.blocks:
            for instr in b.instructions:
                if instr.dest:
                    if instr.dest.id in defs:
                        print(f"SSA Verification Error: Register {instr.dest.id} defined more than once.")
                        return False
                    defs[instr.dest.id] = b.id

        # Pass 2: Verify uses and PHI nodes
        for b in func.blocks:
            for instr in b.instructions:
                if instr.opcode == Opcode.PHI:
                    preds = {p.id for p in b.predecessors}
                    phi_preds = set()
                    
                    for edge in instr.operands:
                        if not isinstance(edge, tuple) or len(edge) != 2:
                            print(f"SSA Verification Error: Invalid PHI edge format {edge} in block {b.id}.")
                            return False
                            
                        pred_id, val = edge
                        if pred_id not in preds:
                            print(f"SSA Verification Error: PHI edge from {pred_id} which is not a predecessor of {b.id}.")
                            return False
                            
                        if pred_id in phi_preds:
                            print(f"SSA Verification Error: Duplicate PHI edge from predecessor {pred_id} in block {b.id}.")
                            return False
                            
                        phi_preds.add(pred_id)
                        
                        if isinstance(val, RegisterID):
                            if val.id not in defs:
                                print(f"SSA Verification Error: Undefined register {val.id} used in PHI node in block {b.id}.")
                                return False
                            
                            # Dominance check for PHI: def must dominate the PREDECESSOR block
                            def_block = defs[val.id]
                            if def_block not in dom[pred_id]:
                                print(f"SSA Verification Error: Definition of {val.id} in {def_block} does not dominate PHI predecessor {pred_id}.")
                                return False

                    if len(phi_preds) != len(preds):
                        print(f"SSA Verification Error: PHI node in block {b.id} has {len(phi_preds)} edges but block has {len(preds)} predecessors.")
                        return False

                else:
                    # Normal instruction
                    for op in instr.operands:
                        if isinstance(op, RegisterID):
                            if op.id not in defs:
                                print(f"SSA Verification Error: Undefined register {op.id} used in block {b.id}.")
                                return False
                            
                            def_block = defs[op.id]
                            if def_block not in dom[b.id]:
                                print(f"SSA Verification Error: Definition of {op.id} in {def_block} does not dominate use in {b.id}.")
                                return False

        return True
