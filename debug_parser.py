import os
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser

with open("examples/crud_test.aayu", "r") as f:
    code = f.read()

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

for node in ast.statements:
    if type(node).__name__ == "ModelDeclNode":
        print(f"Model: {node.name}")
        print(f"Decorators: {node.decorators}")
