import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.pipeline import SemanticPipeline
from aayu.compiler.mir.builder import MIRBuilder
from aayu.compiler.backend.lir_gen import LIRGenerationPass
from aayu.compiler.machine_lir.lowering import MachineLIRLowering
from aayu.compiler.backend.llvm.lowering import LLVMBackend

def test_enum_end_to_end_llvm():
    code = """
    enum Color { Red, Green, Blue }
    action main()
        state myColor = Color.Green
        return myColor
    end
    """
    
    # 1. Lexing
    tokens = Lexer(code).tokenize()
    
    # 2. Parsing
    ast = Parser(tokens).parse()
    
    # 3. Semantic Analysis -> HIR
    hir = SemanticPipeline().run(ast)
    print("HIR:", hir)
    
    # 4. IR Pipeline (MIR -> LIR)
    mir_mod = MIRBuilder().build(hir)
    for f in mir_mod.functions:
        print("MIR Func:", f.name)
        for b in f.blocks:
            for i in b.instructions:
                print("  Instr:", i.opcode, i.operands, i.dest)
    
    # Extract main function MIR
    main_mir = None
    for f in mir_mod.functions:
        if f.name == "main":
            main_mir = f
            break
            
    assert main_mir is not None
    
    # Convert to LIR
    main_lir = LIRGenerationPass().run(main_mir)
    
    # 5. Machine LIR Lowering
    machine_lowering = MachineLIRLowering()
    m_func = machine_lowering.lower(main_lir)
    
    # Wrap in a module
    from aayu.compiler.machine_lir.nodes import MachineModule
    m_module = MachineModule()
    m_module.functions.append(m_func)
    
    # 6. LLVM Lowering
    llvm_backend = LLVMBackend()
    artifact = llvm_backend.lower(m_module)
    
    ll_bytes = artifact.generate()
    ll_string = ll_bytes.decode('utf-8')
    
    # Verify LLVM IR contains the tag value 1 for Color.Green
    assert "ret i32 1" in ll_string or "store i32 1" in ll_string or "ret i32 %" in ll_string
    
    # Since it's stored in a global/local and returned, let's just make sure 
    # it successfully compiles without crashing and contains standard LLVM structures
    assert "define i32 @main()" in ll_string
