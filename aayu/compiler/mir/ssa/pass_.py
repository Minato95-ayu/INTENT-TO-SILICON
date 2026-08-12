from aayu.compiler.mir.nodes import FunctionMIR
from aayu.compiler.pass_manager import OptimizationPass
from aayu.compiler.mir.analysis.dominator_tree import DominatorTreePass
from aayu.compiler.mir.ssa.phi_placement import PhiPlacementPass
from aayu.compiler.mir.ssa.renamer import SSARenamerPass
from aayu.compiler.mir.ssa.verifier import SSAVerificationPass
from aayu.compiler.mir.analysis.def_use import DefUsePass
from aayu.compiler.mir.analysis.liveness import LivenessPass

class SSAPass(OptimizationPass):
    """
    Orchestrates the conversion of a CFG-aware FunctionMIR into strict SSA form.
    Executes Analysis -> SSA Construction -> Validation.
    """
    def __init__(self):
        self.dom_pass = DominatorTreePass()
        self.phi_pass = PhiPlacementPass()
        self.rename_pass = SSARenamerPass()
        self.verify_pass = SSAVerificationPass()
        self.def_use_pass = DefUsePass()
        self.liveness_pass = LivenessPass()

    def run(self, func: FunctionMIR) -> FunctionMIR:
        # 1. Pre-SSA Analysis
        func = self.dom_pass.run(func)
        
        # 2. SSA Construction
        func = self.phi_pass.run(func)
        func = self.rename_pass.run(func)
        
        # 3. Post-SSA Verification
        func = self.verify_pass.run(func)
        
        # 4. Post-SSA Analysis
        func = self.def_use_pass.run(func)
        func = self.liveness_pass.run(func)
        
        return func
