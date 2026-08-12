import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from aayu.compiler.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.ast.nodes import ASTNode
from aayu.compiler.semantic.pipeline import SemanticPipeline
from aayu.compiler.mir.builder import MIRBuilder
from aayu.compiler.mir.ssa.pass_ import SSAPass
from aayu.compiler.pass_manager import PassManager
from aayu.compiler.backend.lir_gen import LIRGenerationPass
from aayu.compiler.backend.lir_verifier import LIRVerifierPass

def create_mir() -> 'FunctionMIR':
    # A simple AAYU program with branches to force PHI creation
    source = """
    state global_val = 10
    action TestLIR()
        a = 1
        b = 2
        if a > b
            a = 100
        else
            a = 200
        end
        b = a
    end
    """
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    pipeline = SemanticPipeline()
    hir = pipeline.run(ast)
    
    mir_builder = MIRBuilder()
    module_mir = mir_builder.build(hir)
    
    func = module_mir.functions[0]
    
    ssa_pass = SSAPass()
    ssa_pass.run(func)
    
    return func

def test_lir_generation():
    func_mir = create_mir()
    
    out_dir = os.path.join(os.path.dirname(__file__), "..", "conformance")
    os.makedirs(out_dir, exist_ok=True)
    
    dump_path = os.path.join(out_dir, "lir.dump")
    
    lir_gen = LIRGenerationPass()
    func_lir = lir_gen.run(func_mir)
    
    verifier = LIRVerifierPass()
    verifier.run(func_lir)
    
    with open(dump_path, "w") as f:
        f.write(str(func_lir))
        
    print(f"LIR artifacts successfully dumped to {out_dir}")

if __name__ == "__main__":
    test_lir_generation()
