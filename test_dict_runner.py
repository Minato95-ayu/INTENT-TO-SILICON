import os
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
import sys
from aayu.runtime.vm.vm import VirtualMachine, VMConfig

filename = sys.argv[1] if len(sys.argv) > 1 else "examples/test_dict.aayu"
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
encoder = BytecodeEncoder()
prog = encoder.encode(lir)

print("Running VM...")
vm = VirtualMachine(VMConfig())
vm.load(prog.bytecode, prog.constant_pool, prog.action_addresses)
try:
    vm.execute()
    vm.call_action_by_name("__PAGE_START__")
    # verify state
    print("Messages after run:", vm.state.get("messages", []))
except Exception as e:
    print("VM Exception:", e)

# Test Action execution via router
print("\nInvoking 'testDict' action...")
try:
    # Set VM router component_context so action can run (it runs globally since no classes)
    vm.router.execute_action("testDict", [])
    print("Messages after testDict:", vm.state.get("messages", []))
except Exception as e:
    print("Action execution failed:", e)

