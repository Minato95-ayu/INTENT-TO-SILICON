import sys
sys.path.append('aayu_language')
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

with open('test_db.aayu', 'r') as f:
    source = f.read()

lexer = Lexer(source)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

interpreter = Interpreter()
interpreter.evaluate(ast)

print("Routes:", interpreter.routes)
