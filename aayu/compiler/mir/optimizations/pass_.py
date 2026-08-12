from aayu.compiler.mir.nodes import FunctionMIR
from aayu.compiler.pass_manager import OptimizationPass
from aayu.compiler.mir.analysis.def_use import DefUsePass
from aayu.compiler.mir.ssa.verifier import SSAVerificationPass

from aayu.compiler.mir.optimizations.constant_fold import ConstantPropagationPass
from aayu.compiler.mir.optimizations.copy_prop import CopyPropagationPass
from aayu.compiler.mir.optimizations.algebraic import AlgebraicSimplificationPass
from aayu.compiler.mir.optimizations.cse import CommonSubexpressionEliminationPass
from aayu.compiler.mir.optimizations.dse import DeadStoreEliminationPass
from aayu.compiler.mir.optimizations.branch import BranchSimplificationPass
from aayu.compiler.mir.optimizations.cfg_cleanup import CFGCleanupPass
from aayu.compiler.mir.optimizations.dce import DeadCodeEliminationPass

class FixedPointOptimizationPass(OptimizationPass):
    """
    Runs the LLVM-style optimization pipeline iteratively until no more changes occur.
    """
    def __init__(self, debug=True):
        self.debug = debug
        self.analysis_manager = None
        
        self.passes = [
            ConstantPropagationPass(),
            CopyPropagationPass(),
            AlgebraicSimplificationPass(),
            CommonSubexpressionEliminationPass(),
            DeadStoreEliminationPass(),
            BranchSimplificationPass(),
            CFGCleanupPass(),
            DeadCodeEliminationPass(),
        ]
        
        self.verifier = SSAVerificationPass()

    def run(self, func: FunctionMIR) -> FunctionMIR:
        iterations = 0
        changed = True
        
        stats = {
            "constant_folded": 0,
            "copies_removed": 0,
            "algebraic_simplified": 0,
            "cse_hits": 0,
            "dead_stores_eliminated": 0,
            "branches_simplified": 0,
            "dead_blocks": 0,
            "dead_inst_removed": 0
        }
        
        while changed:
            changed = False
            iterations += 1
            
            for p in self.passes:
                # Inject analysis manager
                if hasattr(p, 'analysis_manager'):
                    p.analysis_manager = self.analysis_manager
                    
                pass_changed = p.run(func)
                
                if pass_changed:
                    changed = True
                    # Invalidate analyses! CFG or Instructions changed
                    self.analysis_manager.invalidate_all()
                    
                # Collect stats
                if isinstance(p, ConstantPropagationPass):
                    stats["constant_folded"] += p.stats_folded
                elif isinstance(p, CopyPropagationPass):
                    stats["copies_removed"] += p.stats_copies_removed
                elif isinstance(p, AlgebraicSimplificationPass):
                    stats["algebraic_simplified"] += p.stats_simplified
                elif isinstance(p, CommonSubexpressionEliminationPass):
                    stats["cse_hits"] += p.stats_cse_hits
                elif isinstance(p, DeadStoreEliminationPass):
                    stats["dead_stores_eliminated"] += p.stats_dead_stores_eliminated
                elif isinstance(p, BranchSimplificationPass):
                    stats["branches_simplified"] += p.stats_branches_simplified
                elif isinstance(p, CFGCleanupPass):
                    stats["dead_blocks"] += p.stats_dead_blocks
                elif isinstance(p, DeadCodeEliminationPass):
                    stats["dead_inst_removed"] += p.stats_dead_inst
                    
                # Verify after each pass in debug mode
                if self.debug and pass_changed:
                    self.verifier.analysis_manager = self.analysis_manager
                    self.verifier.run(func)
                    
        print(f"\nOptimization Report for {func.name}")
        print("-" * 30)
        print(f"Constant Folded       : {stats['constant_folded']}")
        print(f"Copies Removed        : {stats['copies_removed']}")
        print(f"Algebraic Simplified  : {stats['algebraic_simplified']}")
        print(f"CSE Hits              : {stats['cse_hits']}")
        print(f"Dead Stores Eliminated: {stats['dead_stores_eliminated']}")
        print(f"Branches Simplified   : {stats['branches_simplified']}")
        print(f"Dead Blocks Removed   : {stats['dead_blocks']}")
        print(f"Dead Inst Removed     : {stats['dead_inst_removed']}")
        print(f"Total Iterations      : {iterations}")
        print("-" * 30)
        
        return func
