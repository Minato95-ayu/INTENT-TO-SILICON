import sys, os
sys.path.insert(0, os.path.abspath('.'))
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine

source = """
action testStorage()
    storage.set("mykey", "Hello Storage!")
    val = storage.get("mykey")
    print(val)
    
    storage.remove("mykey")
    val2 = storage.get("mykey")
    print("After remove:", val2)
end
"""

ast = Parser(Lexer(source).tokenize()).parse()
sem = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
encoder = BytecodeEncoder()
prog = encoder.encode(pipe.to_lir(pipe.to_mir(pipe.to_hir(sem))))

vm = VirtualMachine()
vm.load(prog.bytecode, prog.constant_pool, prog.action_addresses)
vm.call_action_by_name('testStorage')
vm.execute()

print('TEST_STORAGE_DONE')
