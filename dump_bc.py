import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), "prototype", "language"))
from lexer import Lexer
from parser import Parser
from compiler import AAYUCompiler

with open(r"prototype\tests\runtime\test_functions.aayu", "r") as f:
    code = f.read()

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
compiler = AAYUCompiler(filename="test_functions.aayu")
bc = compiler.compile(ast)

for i, inst in enumerate(bc.instructions):
    print(f"IP={i} OP={inst.opcode.name} OPERAND={inst.operand}")
