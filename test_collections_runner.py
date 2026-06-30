import sys
sys.path.insert(0, r"D:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language")
sys.path.insert(0, r"D:\intent-to-silicon-research\INTENT-TO-SILICON\prototype")

from lexer import Lexer
from parser import Parser
from passes.lowering import LoweringPass
from compiler import AAYUCompiler
from runtime.vm.vm import VirtualMachine

filepath = r"D:\intent-to-silicon-research\INTENT-TO-SILICON\test_collections.aayu"
with open(filepath, 'r', encoding='utf-8') as f:
    source = f.read()

print("Lexing...")
lexer = Lexer(source)
tokens = lexer.tokenize()

print("Parsing...")
parser = Parser(tokens, filename=filepath)
ast = parser.parse()

print("Lowering...")
lowering = LoweringPass()
lowered_ast = lowering.lower(ast)

print("Compiling...")
compiler = AAYUCompiler()
bytecode = compiler.compile(lowered_ast)

print("Executing...")
vm = VirtualMachine()
print("Globals keys:", vm.globals.keys())
vm.run(bytecode)

for out in vm.output:
    print(out)
