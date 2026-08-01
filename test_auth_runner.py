import os
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
import sys
from aayu.runtime.vm.vm import VirtualMachine, VMConfig

filename = sys.argv[1] if len(sys.argv) > 1 else "examples/auth_test.aayu"
with open(filename, "r") as f:
    code = f.read()

print("Lexing...")
tokens = Lexer(code).tokenize()

print("Parsing...")
ast = Parser(tokens).parse()

print("Semantic Analysis...")
analyzer = SemanticAnalyzer()
semantic_ast = analyzer.analyze(ast)

print("IR Lowering...")
pipe = IRPipeline()
hir = pipe.to_hir(semantic_ast)
mir = pipe.to_mir(hir)
lir = pipe.to_lir(mir)

print("Compiling Bytecode...")
from aayu.compiler.bytecode.encoder import BytecodeEncoder
encoded = BytecodeEncoder().encode(lir)

print("Running VM...")
c = VMConfig()
c.debug_mode = True
vm = VirtualMachine(c)
vm.load(encoded.bytecode, encoded.constant_pool, encoded.action_addresses, getattr(encoded, 'action_params', {}))
try:
    vm.execute()
    vm.call_action_by_name("__PAGE_START__")
    print("State after load:", vm.state)
except Exception as e:
    import traceback
    traceback.print_exc()

print("\nInvoking 'register' action...")
try:
    import random
    email = f"test{random.randint(1000,9999)}@aayu.com"
    vm.value_stack.push(email)
    vm.value_stack.push("password123")
    vm.call_action_by_name("register")
    print("State after register:", vm.state)
except Exception as e:
    import traceback
    traceback.print_exc()

print("\nInvoking 'createSecret' action...")
try:
    vm.value_stack.push("My Super Secret")
    vm.call_action_by_name("createSecret")
except Exception as e:
    import traceback
    traceback.print_exc()

print("\nInvoking 'loadSecrets' action...")
try:
    vm.call_action_by_name("loadSecrets")
    print("State after loadSecrets:", vm.state)
except Exception as e:
    import traceback
    traceback.print_exc()

