from enum import Enum, auto

class OptimizationLevel(Enum):
    O0 = auto() # No optimization, fast compile
    O1 = auto() # Basic optimizations
    O2 = auto() # Most optimizations, recommended
    O3 = auto() # Aggressive optimizations (inlining, loop unrolling)
    Os = auto() # Optimize for size
    Oz = auto() # Aggressively optimize for size

class LLVMOptimizer:
    """
    Configures and runs LLVM optimization passes on the generated IR.
    """
    def __init__(self, level: OptimizationLevel = OptimizationLevel.O2):
        self.level = level
        # In the future, this will configure `llvmlite.binding.ModulePassManagerBuilder`
        self.passes = []
        self._configure_pipeline()
        
    def _configure_pipeline(self):
        if self.level == OptimizationLevel.O0:
            return
            
        # Basic Cleanup
        self.passes.append("mem2reg")      # Promote memory to registers (redundant due to SSA, but good hygiene)
        self.passes.append("simplifycfg")  # Simplify Control Flow Graph
        
        if self.level in (OptimizationLevel.O1, OptimizationLevel.O2, OptimizationLevel.O3, OptimizationLevel.Os, OptimizationLevel.Oz):
            self.passes.append("instcombine")  # Combine instructions
            self.passes.append("gvn")          # Global Value Numbering (CSE)
            self.passes.append("sroa")         # Scalar Replacement of Aggregates
            self.passes.append("adce")         # Aggressive Dead Code Elimination
            
        if self.level in (OptimizationLevel.O2, OptimizationLevel.O3):
            self.passes.append("licm")         # Loop Invariant Code Motion
            
        if self.level == OptimizationLevel.O3:
            self.passes.append("inline")       # Function Inlining
            self.passes.append("loop-unroll")  # Loop Unrolling

    def run(self, llvm_ir_str: str) -> str:
        # Currently a no-op until `llvmlite` bindings are hooked up.
        # This will parse the IR, run the configured passes, and return optimized IR.
        return llvm_ir_str
