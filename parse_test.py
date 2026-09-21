import sys
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
with open('test_token.aayu', 'r') as f:
    src = f.read()
lexer = Lexer(src)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
analyzer = SemanticAnalyzer()
ast = analyzer.analyze(ast)
print(ast)
