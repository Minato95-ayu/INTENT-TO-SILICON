from typing import Optional, Any
import ctypes

try:
    import llvmlite.binding as llvm
    LLVMLITE_AVAILABLE = True
except ImportError:
    LLVMLITE_AVAILABLE = False

from aayu.compiler.backend.llvm.values import LLVMModule
from aayu.compiler.backend.llvm.serializer import LLVMSerializer

class LLVMBridge:
    """
    Acts as the bridge between AAYU's Pure Python LLVM IR Graph and the C++ LLVM backend.
    Responsible for Verification, Optimization, and Code Generation via llvmlite.
    """
    def __init__(self):
        self._initialized = False
        self.target_machine = None
        self.engine = None
        
    def _initialize_llvm(self):
        if not LLVMLITE_AVAILABLE:
            raise RuntimeError("llvmlite is not installed. Cannot use the LLVM bridge.")
        if self._initialized:
            return
            
        # Initialize LLVM targets (core initialization is automatic in new llvmlite)
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        self._initialized = True
        
        target = llvm.Target.from_default_triple()
        self.target_machine = target.create_target_machine()
        
        # Load Native Runtime via Loader
        from aayu.compiler.backend.llvm.runtime_loader import RuntimeLoader
        RuntimeLoader.initialize()

    def parse_module(self, module: LLVMModule) -> Any:
        """Serializes the pure Python graph and parses it into an llvmlite module."""
        self._initialize_llvm()
        
        serializer = LLVMSerializer()
        ll_str = serializer.serialize(module)
        
        return llvm.parse_assembly(ll_str)

    def verify(self, llvm_mod: Any) -> bool:
        """Runs the official LLVM C++ Verifier on the parsed module."""
        try:
            llvm_mod.verify()
            return True
        except Exception as e:
            raise RuntimeError(f"LLVM Verification Failed:\n{e}")

    def optimize(self, llvm_mod: Any, profile: str = "ReleaseFast"):
        """
        Runs the LLVM ModulePassManager.
        Profiles: Debug (O0), Release (O2), ReleaseFast (O3), Size (Oz)
        """
        self._initialize_llvm()
        
        pm = llvm.ModulePassManager()
        
        if profile != "Debug":
            # Basic optimization pipeline for Release/ReleaseFast/Size
            pm.add_instruction_combine_pass()
            pm.add_dead_code_elimination_pass()
            pm.add_sroa_pass()
            pm.add_simplify_cfg_pass()
            
            if profile == "ReleaseFast":
                pm.add_loop_unroll_pass()
                
            if profile == "Size":
                pm.add_global_dead_code_eliminate_pass()
                pm.add_dead_arg_elimination_pass()
            
        pto = llvm.PipelineTuningOptions()
        pb = llvm.create_pass_builder(self.target_machine, pto)
        pm.run(llvm_mod, pb)

    def emit_assembly(self, llvm_mod: Any) -> str:
        """Generates target-specific assembly (.s) string."""
        self._initialize_llvm()
        return self.target_machine.emit_assembly(llvm_mod)

    def emit_object(self, llvm_mod: Any) -> bytes:
        """Generates target-specific object file (.o/.obj) bytes."""
        self._initialize_llvm()
        return self.target_machine.emit_object(llvm_mod)
        
    def create_jit(self, llvm_mod: Any):
        """Creates an ExecutionEngine (MCJIT) for the given module."""
        self._initialize_llvm()
        
        # MCJIT requires a backing module
        backing_mod = llvm.parse_assembly("")
        self.engine = llvm.create_mcjit_compiler(backing_mod, self.target_machine)
        self.engine.add_module(llvm_mod)
        self.engine.finalize_object()
        
    def run_function(self, func_name: str, args=None) -> Any:
        """Executes a function in the JIT and returns the result."""
        if not self.engine:
            raise RuntimeError("JIT not initialized. Call create_jit() first.")
            
        func_ptr = self.engine.get_function_address(func_name)
        if func_ptr == 0:
            raise ValueError(f"Function {func_name} not found in JIT.")
            
        # Example for simple void()->int casting.
        # A full JIT wrapper requires ctypes definition of the signature.
        cfunc = ctypes.CFUNCTYPE(ctypes.c_int)(func_ptr)
        return cfunc()
