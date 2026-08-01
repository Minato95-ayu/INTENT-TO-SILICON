import sys, os
sys.path.insert(0, os.path.abspath('.'))
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine
import logging

# Enable DEBUG logging for VM
logging.basicConfig(level=logging.DEBUG)

source = """
action testStorage()
    storage.set("mykey", "Hello Storage!")
end
"""
tokens = Lexer(source).tokenize()
ast = Parser(tokens).parse()
sem = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
encoder = BytecodeEncoder()
prog = encoder.encode(pipe.to_lir(pipe.to_mir(pipe.to_hir(sem))))

print('Action addresses:', prog.action_addresses)
for i, inst in enumerate(prog.bytecode):
    print(f"[{i:04d}] {inst}")

vm = VirtualMachine()
vm.load(prog.bytecode, prog.constant_pool, prog.action_addresses)
vm.call_action_by_name('testStorage')
