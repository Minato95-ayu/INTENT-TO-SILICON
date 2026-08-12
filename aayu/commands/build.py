import sys
import os
import time
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
    output_name = None
    
    for i, arg in enumerate(args):
        if arg == "-o" and i + 1 < len(args):
            output_name = args[i + 1]
        elif not arg.startswith("-") and args[i-1] != "-o":
            target = arg

    if not target:
        from aayu.package.manifest import AayuManifest
        manifest = AayuManifest()
        if manifest.exists():
            target = manifest.get_entry()
        else:
            target = "src/main.aayu"
            
    if not output_name:
        base_name = os.path.splitext(os.path.basename(target))[0]
        if sys.platform == "win32":
            output_name = f"{base_name}.obj"
        else:
            output_name = f"{base_name}.o"

    if not os.path.exists(target):
        print(f"Error: Target file {target} not found.")
        sys.exit(1)
        
    print(f"[AAYU] Compiling {target} to {output_name} (AOT)...\n")
    try:
        t_start = time.perf_counter()
        
        with open(target, 'r', encoding='utf-8') as f:
            source = f.read()
            
        # 1. Frontend: Lex & Parse
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        # 2. Resolve Imports
        base_directory = os.path.dirname(os.path.abspath(target))
        if not base_directory:
            base_directory = "."
        ast = resolve_ast_imports(ast, base_directory, set([os.path.abspath(target)]))
        
        # 3. Semantic Pipeline -> HIR
        semantic_pipeline = SemanticPipeline()
        hir_module = semantic_pipeline.run(ast)
        if not hir_module:
            semantic_pipeline.diag_engine.print_all()
            sys.exit(1)
            
        # 4. Lowering: HIR -> MIR -> SSA -> MachineLIR
        mir_builder = MIRBuilder()
        mir_module = mir_builder.build(hir_module)
        
        from aayu.compiler.mir.ssa.pass_ import SSAPass
        ssa_pass = SSAPass()
        for func in mir_module.functions:
            ssa_pass.run(func)
        ssa_module = mir_module
        
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
        
        # 5. LLVM Backend
        bridge = LLVMBridge()
        bridge._initialize_llvm()
        
        from aayu.compiler.backend.llvm.lowering import LLVMBackend
        backend = LLVMBackend()
        artifact = backend.lower(machine_module)
        llvm_module = artifact.llvm_module
        
        # 6. Serialization (LLVM IR)
        serializer = LLVMSerializer()
        ll_code = serializer.serialize(llvm_module)
        
        # Save .ll for debugging
        ll_out = output_name + ".ll"
        with open(ll_out, 'w', encoding='utf-8') as f:
            f.write(ll_code)
        print(f"[AAYU] Saved LLVM IR to {ll_out}")
        
        # 7. Object File Emission
        mod = llvm.parse_assembly(ll_code)
        mod.verify()
        
        target_machine = bridge.target_machine
        obj_code = target_machine.emit_object(mod)
        
        with open(output_name, 'wb') as f:
            f.write(obj_code)
            
        t_end = time.perf_counter()
        
        print(f"[AAYU] Successfully compiled to {output_name} in {(t_end - t_start)*1000:.2f}ms.")
        print("[AAYU] (Link it with aayu_runtime.dll to create the final executable!)")
        
    except CompilerError as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nInternal Compiler Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
