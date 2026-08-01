from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine
from aayu.runtime.vm.config import VMConfig

src = open('ecommerce.aayu').read()
tokens = Lexer(src).tokenize()
ast = Parser(tokens).parse()
semantic_ast = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
hir = pipe.to_hir(semantic_ast)
mir = pipe.to_mir(hir)
lir = pipe.to_lir(mir)
print("LIR:", [n.opcode for n in lir])
prog = BytecodeEncoder().encode(lir)
print("Bytecode:", prog.bytecode)

vm_config = VMConfig()
vm_config.debug_mode = True
vm = VirtualMachine(vm_config)
vm.load(prog.bytecode, prog.constant_pool, prog.action_addresses)
vm.execute()
print("STATE_SCOPES=", vm.state_scopes)
