import sys
import os
import ctypes
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
    
    for arg in args:
        if not arg.startswith("-"):
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
        
    print(f"[AAYU] Compiling and running {target} via Native JIT...\n")
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
        
        # 6. Serialization
        serializer = LLVMSerializer()
        ll_code = serializer.serialize(llvm_module)
        
        t_compile = time.perf_counter()
        
        mod = llvm.parse_assembly(ll_code)
        mod.verify()
        
        # Load the runtime library
        runtime_path = os.path.abspath("aayu_runtime.dll")
        if os.path.exists(runtime_path):
            llvm.load_library_permanently(runtime_path)
            
        target_machine = bridge.target_machine
        backing_mod = llvm.parse_assembly("")
        engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
        engine.add_module(mod)
        engine.finalize_object()
        engine.run_static_constructors()
        
        # Find main function
        func_ptr = engine.get_function_address("main")
        if not func_ptr:
            print("Error: 'main' function not found in module.")
            sys.exit(1)
            
        # Execute main via ctypes
        c_main = ctypes.CFUNCTYPE(ctypes.c_int)(func_ptr)
        
        print("--- Program Output ---")
        exit_code = c_main()
        print(f"\n--- Process Exited with Code {exit_code} ---")
        
        t_exec = time.perf_counter()
        
        print(f"\nCompilation Time: {(t_compile - t_start)*1000:.2f}ms")
        print(f"Execution Time:   {(t_exec - t_compile)*1000:.2f}ms")
        
    except CompilerError as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nInternal Compiler Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
