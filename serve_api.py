import sys
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine
from aayu.runtime.vm.config import VMConfig
from aayu.runtime.server.api_server import APIServer

def main():
    source_file = sys.argv[1] if len(sys.argv) > 1 else "examples/auth_test.aayu"
    source = open(source_file).read()
    
    # 1. Compilation
    print("Compiling Bytecode...")
    l = Lexer(source)
    ast = Parser(l.tokenize()).parse()
    ast = SemanticAnalyzer().analyze(ast)
    pipe = IRPipeline()
    hir = pipe.to_hir(ast)
    mir = pipe.to_mir(hir)
    lir = pipe.to_lir(mir)
    encoded = BytecodeEncoder().encode(lir)

    # 2. Runtime Initialization
    print("Initializing VM...")
    vm = VirtualMachine(VMConfig())
    vm.load(encoded.bytecode, encoded.constant_pool, encoded.action_addresses, getattr(encoded, 'action_params', {}))
    vm.execute()
    
    # 3. Start API Server
    server = APIServer(vm, port=8000)
    server.start()

if __name__ == "__main__":
    main()
