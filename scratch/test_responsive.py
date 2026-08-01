import sys, os
sys.path.insert(0, os.path.abspath('.'))
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine

source = """
Page Home
    Container width_mobile="100%" width_tablet="50%" width="200"
    end
end
run Home
"""

ast = Parser(Lexer(source).tokenize()).parse()
sem = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
encoder = BytecodeEncoder()
prog = encoder.encode(pipe.to_lir(pipe.to_mir(pipe.to_hir(sem))))

vm = VirtualMachine()
vm.load(prog.bytecode, prog.constant_pool, prog.action_addresses)
vm.call_action_by_name('__PAGE_START_Home')
vm.execute()

if vm.interpreter.render_tree.root:
    def print_node(node, indent=''):
        print(indent + node.type, getattr(node, 'props', {}))
        for child in node.children:
            print_node(child, indent + '  ')
    print_node(vm.interpreter.render_tree.root)
