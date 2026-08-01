import sys
sys.path.insert(0, '../../')
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine
import traceback

with open('benchmarks/aayu_app/src/app.aayu', 'r') as f:
    src=f.read()
    
ast=Parser(Lexer(src).tokenize()).parse()
sem=SemanticAnalyzer().analyze(ast)
mir=IRPipeline().to_mir(IRPipeline().to_hir(sem))
program = BytecodeEncoder().encode(IRPipeline().to_lir(mir))
print('action addresses:', program.action_addresses)

vm = VirtualMachine()
vm.load(program.bytecode, list(program.constant_pool.values()), program.action_addresses, getattr(program, 'action_params', {}))
vm.execute()
print('vm.action_addresses after execute:', vm.action_addresses)

try:
    from aayu.runtime.server.api_server import APIRouter, AAYUAPIHandler
    print('AAYUAPIHandler crude engine tables:', AAYUAPIHandler.crud_engine.models.keys())
    # simulate what _handle_action does for login
    if 'login' in vm.action_addresses:
        print("login found! Calling it...")
        # push args
        vm.value_stack.push("test@test.com")
        vm.value_stack.push("password")
        vm.call_action_by_name("login")
        print("login returned:", vm.value_stack.pop())
    else:
        print("login NOT FOUND in vm.action_addresses!")
except Exception as e:
    traceback.print_exc()
