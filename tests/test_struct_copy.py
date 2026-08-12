import os
import sys
import traceback

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
    print("  TEST: Struct Copy Semantics (Pass-by-value)")
    print("=" * 60)
    
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    
    pipeline = SemanticPipeline()
    hir_module = pipeline.run(ast)
    
    if hir_module is None:
        print("Semantic pipeline failed:")
        for diag in pipeline.diag_engine.diagnostics:
            print(f"  {diag}")
        return
        
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
        state user = User { age: 21, id: 100 }
        state a = user
        a.age = 50
    end
    """
    
    try:
        run_pipeline(source)
    except Exception as e:
        traceback.print_exc()
