import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from aayu.compiler.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.pipeline import SemanticPipeline
from aayu.compiler.mir.builder import MIRBuilder
from aayu.compiler.mir.ssa.pass_ import SSAPass
from aayu.compiler.utils.dumpers import dump_ast, dump_hir, dump_mir, dump_cfg_dot, dump_dominator, dump_ssa

code = """
action Test()
    count = 10
    if count > 5
        count = count + 5
    else
        count = count - 5
    end
end
"""

print("Running Phase 12.0 Semantic Pipeline + Phase 12.2 MIR...")
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

print("Running Phase 12.4 SSA Construction...")
ssa_pass = SSAPass()
for func in mir.functions:
    try:
        ssa_pass.run(func)
    except Exception as e:
        print(f"SSA Generation Failed: {e}")
        import traceback
        traceback.print_exc()

out_dir = os.path.join(os.path.dirname(__file__), "..", "conformance")
os.makedirs(out_dir, exist_ok=True)

dump_ast(ast, out_dir)
dump_hir(hir, out_dir)
dump_mir(mir, out_dir)
dump_cfg_dot(mir, out_dir)
dump_dominator(mir, out_dir)
dump_ssa(mir, out_dir)

print(f"All SSA artifacts successfully dumped to {out_dir}")
