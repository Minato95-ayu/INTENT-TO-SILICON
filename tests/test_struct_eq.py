import sys, os, traceback
sys.path.insert(0, r'd:\intent-to-silicon-research\INTENT-TO-SILICON')

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.pipeline import SemanticPipeline
from aayu.compiler.mir.builder import MIRBuilder
from aayu.compiler.backend.lir_gen import LIRGenerationPass
from aayu.compiler.machine_lir.lowering import MachineLIRLowering
from aayu.compiler.machine_lir.nodes import MachineModule
from aayu.compiler.backend.llvm.lowering import LLVMBackend

def run_pipeline(source: str):
    print("=" * 60)
    print("  TEST: Struct Equality (==)")
    print("=" * 60)
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    semantic = SemanticPipeline()
    hir_module = semantic.run(ast)
    
    mir_builder = MIRBuilder()
    mir_module = mir_builder.build(hir_module)
    
    lir_gen = LIRGenerationPass()
    lir_functions = []
    for func in mir_module.functions:
        lir_func = lir_gen.run(func)
        lir_functions.append(lir_func)
        
    machine_lowering = MachineLIRLowering()
    machine_functions = []
    for lir_func in lir_functions:
        m_func = machine_lowering.lower(lir_func)
        machine_functions.append(m_func)
        
    machine_module = MachineModule(functions=machine_functions)
    
    backend = LLVMBackend()
    artifact = backend.lower(machine_module)
    llvm_ir = artifact.generate().decode('utf-8')
    
    print("\n--- LLVM IR ---")
    print(llvm_ir)
    print("--- END ---")

if __name__ == "__main__":
    source = """
    struct User {
        age: int
        id: int
    }
    
    action main()
        state u1 = User { age: 21, id: 100 }
        state u2 = User { age: 21, id: 100 }
        state is_equal = u1 == u2
    end
    """
    run_pipeline(source)
