import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from aayu.compiler.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.pipeline import SemanticPipeline
from aayu.compiler.mir.builder import MIRBuilder
from aayu.compiler.mir.ssa.pass_ import SSAPass
from aayu.compiler.pass_manager import PassManager
from aayu.compiler.mir.optimizations.pass_ import FixedPointOptimizationPass
from aayu.compiler.utils.dumpers import dump_ssa, dump_mir

code = """
state global_val = 0

action OptimizeMe()
    # Constant folding + Algebraic + Copy Prop + DCE
    a = 5
    b = 0
    c = a + b
    d = c * 1
    
    # CSE
    e = a + 5
    f = a + 5
    
    # Branch Simplification + CFG Cleanup
    if true
        x = 100
    else
        x = 200 # Dead block
    end
    
    # DSE
    global_val = 1
    global_val = 2
end
"""

print("Running Compiler Pipeline up to SSA...")
lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

pipeline = SemanticPipeline()
hir = pipeline.run(ast)

if not hir:
    print("Semantic errors!")
    sys.exit(1)

mir_builder = MIRBuilder()
mir = mir_builder.build(hir)

pm = PassManager()
pm.add_pass(SSAPass())
pm.add_pass(FixedPointOptimizationPass(debug=True))

for func in mir.functions:
    try:
        pm.run(func)
    except Exception as e:
        print(f"Optimization Pipeline Failed: {e}")
        import traceback
        traceback.print_exc()

out_dir = os.path.join(os.path.dirname(__file__), "..", "conformance")
os.makedirs(out_dir, exist_ok=True)

# Dump optimized SSA
dump_ssa(mir, out_dir)

print(f"Optimization artifacts successfully dumped to {out_dir}")
