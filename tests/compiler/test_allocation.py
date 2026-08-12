import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from aayu.compiler.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.pipeline import SemanticPipeline
from aayu.compiler.mir.builder import MIRBuilder
from aayu.compiler.mir.ssa.pass_ import SSAPass
from aayu.compiler.pass_manager import PassManager
from aayu.compiler.backend.analysis.numbering import InstructionNumberingPass
from tests.compiler.test_optimizations import dump_ssa

def test_numbering():
    # A simple program with branching to test RPO numbering
    source = """
    state global_val = 1
    action AllocateMe()
        a = 10
        b = 20
        if a > b
            c = a + b
        else
            c = a - b
        end
        global_val = c
    end
    """
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    pipeline = SemanticPipeline()
    hir_module = pipeline.run(ast)
    
    mir_builder = MIRBuilder()
    mir_module = mir_builder.build(hir_module)
    
    func = mir_module.functions[0]
    
    # 1. SSA
    ssa_pass = SSAPass()
    ssa_pass.run(func)
    
    # 2. Numbering and Liveness
    from aayu.compiler.backend.analysis.liveness import LivenessPass
    from aayu.compiler.backend.analysis.pressure import RegisterPressurePass
    from aayu.compiler.backend.analysis.intervals import LiveIntervalConstructionPass
    
    pm = PassManager()
    num_pass = InstructionNumberingPass()
    live_pass = LivenessPass()
    pressure_pass = RegisterPressurePass()
    interval_pass = LiveIntervalConstructionPass()
    
    pm.add_pass(num_pass)
    pm.add_pass(live_pass)
    pm.add_pass(pressure_pass)
    pm.add_pass(interval_pass)
    pm.run(func)
    
    # 3. Dump
    out_dir = os.path.join(os.path.dirname(__file__), "..", "conformance")
    os.makedirs(out_dir, exist_ok=True)
    
    dump_path = os.path.join(out_dir, "numbering.dump")
    with open(dump_path, "w") as f:
        f.write(f"Function {func.name} RPO Numbering:\n")
        for b in func.analysis['rpo_blocks']:
            f.write(f"  {b.id}:\n")
            for instr in b.instructions:
                f.write(f"    [{instr.index:03d}] {instr}\n")
                
    dump_path_liveness = os.path.join(out_dir, "liveness.dump")
    with open(dump_path_liveness, "w") as f:
        f.write(f"Function {func.name} Liveness:\n")
        for b in func.analysis['rpo_blocks']:
            f.write(f"  {b.id}:\n")
            f.write(f"    LiveIn : {sorted(list(func.analysis['live_in'][b.id]))}\n")
            f.write(f"    LiveOut: {sorted(list(func.analysis['live_out'][b.id]))}\n")
            
    dump_path_pressure = os.path.join(out_dir, "pressure.dump")
    with open(dump_path_pressure, "w") as f:
        f.write(f"Function {func.name} Peak Register Pressure:\n")
        f.write(f"Peak Pressure    : {func.analysis.get('pressure_peak', 0)}\n")
        f.write(f"Average Pressure : {func.analysis.get('pressure_avg', 0):.2f}\n\n")
        f.write("Pressure Histogram\n")
        hist = func.analysis.get('pressure_histogram', {})
        for p in sorted(hist.keys()):
            f.write(f"  {p} : {hist[p]} instructions\n")
        f.write("\n")
        
        for b in func.analysis['rpo_blocks']:
            f.write(f"  {b.id}:\n")
            for instr in b.instructions:
                press = func.analysis['pressure'].get(instr.index, 0)
                f.write(f"    [{instr.index:03d}] Pressure={press:02d} | {instr}\n")
            
    dump_path_intervals = os.path.join(out_dir, "intervals.dump")
    with open(dump_path_intervals, "w") as f:
        f.write(f"Function {func.name} Live Intervals:\n")
        intervals = func.analysis['intervals']
        for reg_id in sorted(intervals.keys()):
            f.write(f"  {intervals[reg_id]}\n")
            
    # 4. Linear Scan for multiple K values
    from aayu.compiler.backend.allocation.linear_scan import LinearScanAllocationPass
    from aayu.compiler.backend.allocation.spill_rewrite import SpillRewritePass
    from aayu.compiler.backend.allocation.coalescing import RegisterCoalescingPass
    import copy
    
    dump_path_alloc = os.path.join(out_dir, "allocation.dump")
    dump_path_spill = os.path.join(out_dir, "spill.dump")
    dump_path_coalescing = os.path.join(out_dir, "coalescing.dump")
    
    with open(dump_path_alloc, "w") as f_alloc, open(dump_path_spill, "w") as f_spill, open(dump_path_coalescing, "w") as f_coal:
        f_alloc.write(f"Function {func.name} Allocation Results:\n\n")
        f_spill.write(f"Function {func.name} Spill Statistics:\n\n")
        f_coal.write(f"Function {func.name} Coalescing Statistics:\n\n")
        
        for k in [2, 4, 8, 16]:
            # Reset assignments
            for interval in func.analysis['intervals'].values():
                interval.assigned_register = None
                interval.spill_slot = None
                
            # Create a fresh deepcopy of func for each K because SpillRewrite mutates instructions
            k_func = copy.deepcopy(func)
                
            alloc_pass = LinearScanAllocationPass(num_registers=k)
            alloc_pass.run(k_func)
            
            spill_rewrite_pass = SpillRewritePass()
            spill_rewrite_pass.run(k_func)
            
            coal_pass = RegisterCoalescingPass()
            coal_pass.run(k_func)
            
            # Write Allocation Dump
            f_alloc.write(f"--- Allocation with K = {k} ---\n")
            f_alloc.write(f"Spill Count: {k_func.analysis.get('spills', 0)}\n")
            intervals = k_func.analysis['intervals']
            for reg_id in sorted(intervals.keys()):
                f_alloc.write(f"  {intervals[reg_id]}\n")
            f_alloc.write("\n")
            
            # Write Spill Dump
            f_spill.write(f"--- Spills with K = {k} ---\n")
            f_spill.write(f"Spills: {k_func.analysis.get('spills', 0)}\n")
            f_spill.write(f"Reloads: {k_func.analysis.get('reloads', 0)}\n")
            f_spill.write(f"Stack Slots: {k_func.analysis.get('stack_slots', 0)}\n\n")
            
            # Write Coalescing Dump
            f_coal.write(f"--- Coalescing with K = {k} ---\n")
            f_coal.write(f"Moves Removed: {k_func.analysis.get('moves_removed', 0)}\n\n")
            
    print(f"Numbering, Liveness, Pressure, Intervals, Allocation, Spill, and Coalescing artifacts successfully dumped to {out_dir}")

if __name__ == "__main__":
    test_numbering()
