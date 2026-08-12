import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aayu.compiler.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.pipeline import SemanticPipeline
from aayu.compiler.mir.builder import MIRBuilder
from aayu.compiler.utils.dumpers import dump_ast, dump_hir, dump_mir, dump_cfg_dot

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

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

pipeline = SemanticPipeline()
hir = pipeline.run(ast)

mir_builder = MIRBuilder()
mir = mir_builder.build(hir)

out_dir = os.path.join(os.path.dirname(__file__), "..", "tests", "conformance")

dump_ast(ast, out_dir)
dump_hir(hir, out_dir)
dump_mir(mir, out_dir)
dump_cfg_dot(mir, out_dir)

print(f"Artifacts successfully dumped to {out_dir}")
