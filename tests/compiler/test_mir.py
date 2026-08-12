import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from aayu.compiler.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.pipeline import SemanticPipeline
from aayu.compiler.mir.builder import MIRBuilder

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

if hir:
    print("HIR generated successfully!")
    mir_builder = MIRBuilder()
    try:
        mir_module = mir_builder.build(hir)
        for func in mir_module.functions:
            print(f"CFG: {func.name}")
            for block in func.blocks:
                print(f"Block: {block.id}")
                for instr in block.instructions:
                    print(f"  {instr}")
    except Exception as e:
        print(f"MIR Generation Failed: {e}")
        import traceback
        traceback.print_exc()
else:
    print("Semantic Errors Found:")
    pipeline.diag_engine.print_all()
