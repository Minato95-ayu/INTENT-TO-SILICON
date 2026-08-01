import sys, os
sys.path.insert(0, os.path.abspath('.'))

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine

source = '''
action main()
    storage.set("name", "AAYU")
    name = storage.get("name")
    print name
end
'''
tokens = Lexer(source).tokenize()
ast = Parser(tokens).parse()
sem = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
prog = BytecodeEncoder().encode(pipe.to_lir(pipe.to_mir(pipe.to_hir(sem))))

vm = VirtualMachine()
vm.load(prog.bytecode, prog.constant_pool, prog.action_addresses)
vm.call_action_by_name("main")
