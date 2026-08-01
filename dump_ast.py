import sys
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser

source = open(sys.argv[1]).read()
tokens = Lexer(source).tokenize()
ast = Parser(tokens).parse()

for stmt in ast.statements:
    print(stmt)
