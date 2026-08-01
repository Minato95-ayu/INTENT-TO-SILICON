from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine
from aayu.runtime.vm.config import VMConfig

import sys
source_file = sys.argv[1] if len(sys.argv) > 1 else "whatsapp_clone/test_for.aayu"
source = open(source_file).read()
l = Lexer(source)
ast = Parser(l.tokenize()).parse()
ast = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
hir = pipe.to_hir(ast)
mir = pipe.to_mir(hir)
lir = pipe.to_lir(mir)
encoder = BytecodeEncoder()
prog = encoder.encode(lir)

vm = VirtualMachine(VMConfig())
vm.load(prog.bytecode, prog.constant_pool.values(), prog.action_addresses)
vm.execute()
def print_tree(node, depth=0):
    print("  " * depth + str(node) + " " + str(node.props))
    for child in node.children:
        print_tree(child, depth + 1)

if vm.interpreter.render_tree and vm.interpreter.render_tree.root:
    print_tree(vm.interpreter.render_tree.root)
    # Start UI if present
    start_hot_reload_server(vm)
else:
    print("[VM] Starting in Headless Mode (API Server)")
    try:
        from aayu.runtime.server.api_server import APIRouter
        router = APIRouter(vm)
        # In a real app we'd read port from config, but here default to 8000
        router.start(port=8000)
    except Exception as e:
        print(f"Failed to start API Server: {e}")
    print("Action addresses:", vm.action_addresses)
    if "__PAGE_START__" in vm.action_addresses:
        print("Calling __PAGE_START__")
        vm.call_action_by_name("__PAGE_START__")
        
        if hasattr(vm, "closures"):
            print(f"Closures: {vm.closures}")
            if vm.closures:
                closure_id = list(vm.closures.keys())[0]
                print(f"Dispatching closure: {closure_id}")
                vm.call_action_by_name(closure_id)
                vm.execute()
                print(f"Notes after dispatch: {vm.state.get('notes')}")
