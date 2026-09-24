from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.ast.nodes import *

src = """
action add(a, b)
    return a + b
end

let result = add(10, 20)
"""

lexer = Lexer(src)
parser = Parser(lexer.tokenize())
ast = parser.parse()

for stmt in ast.statements:
    print(stmt)
