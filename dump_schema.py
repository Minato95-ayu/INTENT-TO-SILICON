import sys
import json
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine
from aayu.runtime.vm.config import VMConfig

source = open("examples/validation_test.aayu").read()
l = Lexer(source)
ast = Parser(l.tokenize()).parse()
ast = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
hir = pipe.to_hir(ast)
mir = pipe.to_mir(hir)
lir = pipe.to_lir(mir)
encoded = BytecodeEncoder().encode(lir)

vm = VirtualMachine(VMConfig())
vm.load(encoded.bytecode, encoded.constant_pool, encoded.action_addresses, getattr(encoded, 'action_params', {}))
vm.execute()

print(json.dumps(vm.database.models["User"]["fields"], indent=2))
