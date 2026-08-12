from dataclasses import dataclass
import time

@dataclass
class CompilerMetrics:
    # Timings
    compile_time_ms: float = 0.0
    optimization_time_ms: float = 0.0
    allocation_time_ms: float = 0.0
    
    # Counts
    ast_nodes: int = 0
    hir_nodes: int = 0
    mir_instructions: int = 0
    ssa_registers: int = 0
    phi_count: int = 0
    blocks: int = 0
    cfg_edges: int = 0
    dominators: int = 0
    
    # Execution constraints
    peak_stack: int = 0
    peak_locals: int = 0
    
    # Binary info
    bytecode_size: int = 0
    constant_pool_size: int = 0
    
    # Timer state
    _start_time: float = 0.0
    
    def start_timer(self):
        self._start_time = time.time()
        
    def stop_timer(self) -> float:
        elapsed = (time.time() - self._start_time) * 1000
        self._start_time = 0.0
        return elapsed

    def report(self) -> str:
        out = []
        out.append("=== Compiler Metrics ===")
        out.append(f"AST Nodes:          {self.ast_nodes}")
        out.append(f"HIR Nodes:          {self.hir_nodes}")
        out.append(f"MIR Instructions:   {self.mir_instructions}")
        out.append(f"SSA Registers:      {self.ssa_registers}")
        out.append(f"PHI Count:          {self.phi_count}")
        out.append(f"Blocks:             {self.blocks}")
        out.append(f"CFG Edges:          {self.cfg_edges}")
        out.append(f"Dominators:         {self.dominators}")
        out.append(f"Peak Stack:         {self.peak_stack}")
        out.append(f"Peak Locals:        {self.peak_locals}")
        out.append(f"Bytecode Size:      {self.bytecode_size} bytes")
        out.append(f"Constant Pool Size: {self.constant_pool_size}")
        out.append(f"Optimization Time:  {self.optimization_time_ms:.2f} ms")
        out.append(f"Allocation Time:    {self.allocation_time_ms:.2f} ms")
        out.append(f"Total Compile Time: {self.compile_time_ms:.2f} ms")
        out.append("========================")
        return "\n".join(out)
