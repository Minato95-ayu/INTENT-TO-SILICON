import sys
import os
sys.path.insert(0, r"D:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\aayu_language")
from lexer import Lexer
from parser import Parser
from compiler import AAYUCompiler

filepath = "D:\\intent-to-silicon-research\\INTENT-TO-SILICON\\test_func_ret.aayu"
with open(filepath, 'r', encoding='utf-8') as f:
    source = f.read()

lexer = Lexer(source)
parser = Parser(lexer.tokenize(), filename=filepath)
ast = parser.parse()
compiler = AAYUCompiler()
code_obj = compiler.compile(ast)

print("Globals:", code_obj.names)
print("Constants:", code_obj.constants)

print("\nMain Bytecode:")
for i, inst in enumerate(code_obj.instructions):
    print(f"{i}: {inst.opcode} {inst.operand}")

for const in code_obj.constants:
    if hasattr(const, 'instructions'):
        print(f"\nFunction Bytecode ({const.name}):")
        for i, inst in enumerate(const.instructions):
            print(f"{i}: {inst.opcode} {inst.operand}")
