from parser import Parser
from lexer import Lexer
from compiler import AAYUCompiler
source = '''map m.
set "a" to 1 in m.
show get "b" from m.'''
parser = Parser(Lexer(source).tokenize())
ast = parser.parse()
compiler = AAYUCompiler()
compiler.compile(ast)
for instr in compiler.bytecode.instructions:
    print(instr)
