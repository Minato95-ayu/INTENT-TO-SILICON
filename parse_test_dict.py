from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.ast.nodes import *

src = """
let node = {"type": "Literal", "value": 10}
let t = node["type"]
"""

lexer = Lexer(src)
parser = Parser(lexer.tokenize())
ast = parser.parse()

for stmt in ast.statements:
    print(stmt)
