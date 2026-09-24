from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.ast.nodes import *

src = """
let x = arr[0]
let y = len(arr)
"""

lexer = Lexer(src)
parser = Parser(lexer.tokenize())
ast = parser.parse()

for stmt in ast.statements:
    print(stmt)
