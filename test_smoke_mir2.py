import sys
import os
sys.path.insert(0, os.path.abspath("."))
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline

code = """
Page Counter
    state count = 0
end
"""
tokens = Lexer(code).tokenize()
ast = Parser(tokens).parse()
ast = SemanticAnalyzer().analyze(ast)
pipeline = IRPipeline()
hir = pipeline.to_hir(ast)
mir = pipeline.to_mir(hir)
for m in mir:
    print(m.opcode, getattr(m, "operands", ""))
