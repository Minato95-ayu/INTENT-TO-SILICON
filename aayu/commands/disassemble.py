import sys
import os
import llvmlite.binding as llvm

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.ast_resolver import resolve_ast_imports
from aayu.compiler.semantic.pipeline import SemanticPipeline
from aayu.compiler.hir.nodes import HIRModule
from aayu.compiler.mir.builder import MIRBuilder


from aayu.compiler.backend.llvm.bridge import LLVMBridge
from aayu.compiler.backend.llvm.serializer import LLVMSerializer
from aayu.compiler.errors import CompilerError

def handle(args):
    target = None
    stage = "llvm" # Can be hir, mir, ssa, lir, llvm
    
    for i, arg in enumerate(args):
        if arg.startswith("--stage="):
            stage = arg.split("=")[1]
        elif not arg.startswith("-"):
            target = arg

    if not target:
        from aayu.package.manifest import AayuManifest
        manifest = AayuManifest()
        if manifest.exists():
            target = manifest.get_entry()
        else:
            target = "src/main.aayu"

    if not os.path.exists(target):
        print(f"Error: Target file {target} not found.")
        sys.exit(1)
        
    print(f"[AAYU] Disassembling {target} at stage '{stage}'...\n")
    try:
        with open(target, 'r', encoding='utf-8') as f:
            source = f.read()
            
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        base_directory = os.path.dirname(os.path.abspath(target))
        if not base_directory:
            base_directory = "."
        ast = resolve_ast_imports(ast, base_directory, set([os.path.abspath(target)]))
        
        semantic_pipeline = SemanticPipeline()
        hir_module = semantic_pipeline.run(ast)
        if not hir_module:
            semantic_pipeline.diag_engine.print_all()
            sys.exit(1)
            
        if stage == "hir":
            import pprint
            pprint.pprint(hir_module)
            return
            
        mir_builder = MIRBuilder()
        mir_module = mir_builder.build(hir_module)
        
        if stage == "mir":
            print(mir_module.to_string())
            return
            
        from aayu.compiler.mir.ssa.pass_ import SSAPass
        ssa_pass = SSAPass()
        for func in mir_module.functions:
            ssa_pass.run(func)
        ssa_module = mir_module
        
        if stage == "ssa":
            print(ssa_module.to_string())
            return
            
        from aayu.compiler.backend.lir_gen import LIRGenerationPass
        from aayu.compiler.machine_lir.lowering import MachineLIRLowering
        from aayu.compiler.machine_lir.nodes import MachineModule
        
        lir_pass = LIRGenerationPass()
        machine_lowering = MachineLIRLowering()
        
        machine_module = MachineModule()
        for func in ssa_module.functions:
            func_lir = lir_pass.run(func)
            machine_func = machine_lowering.lower(func_lir)
            machine_module.functions.append(machine_func)
        
        if stage == "lir":
            print(machine_module.to_string())
            return
            
        bridge = LLVMBridge()
        bridge._initialize_llvm()
        
        from aayu.compiler.backend.llvm.lowering import LLVMBackend
        backend = LLVMBackend()
        artifact = backend.lower(machine_module)
        llvm_module = artifact.llvm_module
        
        serializer = LLVMSerializer()
        ll_code = serializer.serialize(llvm_module)
        
        if stage == "llvm":
            print(ll_code)
            return
            
        print(f"Unknown stage: {stage}")
        
    except CompilerError as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nInternal Compiler Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
