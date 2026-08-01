import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from aayu.compiler.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.pipeline import SemanticPipeline

code = """
state app_title = "My App"
state count = 10 + 5

action Increment(amount)
    count = count + amount
end

action BadAction()
    count = "string" + 5
end
"""

print("Running Phase 12.0 Semantic Pipeline...")
lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

pipeline = SemanticPipeline()
hir = pipeline.run(ast)

if hir:
    print("HIR generated successfully!")
else:
    print("Semantic Errors Found:")
    pipeline.diag_engine.print_all()
