import sys
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.ir.cfg_builder import CFGBuilder
with open('test_token.aayu', 'r') as f:
    src = f.read()
lexer = Lexer(src)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
analyzer = SemanticAnalyzer()
ast = analyzer.analyze(ast)
pipeline = IRPipeline()
hir = [pipeline._semantic_to_hir(stmt) for stmt in ast.statements]
print(hir)
cfg_builder = CFGBuilder()
cfg = cfg_builder.build(hir)
print(cfg)
