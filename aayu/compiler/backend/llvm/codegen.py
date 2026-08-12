from enum import Enum, auto
import os

class OutputType(Enum):
    OBJECT = auto()     # .o
    ASSEMBLY = auto()   # .s
    EXECUTABLE = auto() # .exe / elf

class LLVMCodegen:
    """
    Handles LLVM code generation (AOT) and JIT execution.
    """
    def __init__(self, target_triple: str = ""):
        self.target_triple = target_triple
        # In the future:
        # llvmlite.binding.initialize()
        # llvmlite.binding.initialize_native_target()
        # llvmlite.binding.initialize_native_asmprinter()
        
    def emit_object(self, llvm_ir: str, output_path: str):
        """Compiles LLVM IR to a native object file (.o)"""
        # For now, we simulate this by just writing the .ll file
        # In reality, this will parse the IR into an LLVM module,
        # create a TargetMachine, and emit the object bytes.
        with open(output_path + ".ll", "w") as f:
            f.write(llvm_ir)
            
    def emit_executable(self, llvm_ir: str, output_path: str):
        """Compiles LLVM IR and links it with the Native Runtime to create an executable."""
        obj_path = output_path + ".o"
        self.emit_object(llvm_ir, obj_path)
        
        # Link using Clang
        # e.g., os.system(f"clang {obj_path} runtime/native/libaayu_runtime.a -o {output_path}")
        pass

class LLVMJIT:
    """
    Handles Just-In-Time execution of AAYU LLVM IR.
    Uses ORC JIT or MCJIT.
    """
    def __init__(self):
        pass
        
    def execute(self, llvm_ir: str, entry_func: str = "main"):
        """Compiles the IR in memory and executes the entry function."""
        # For now, it's a stub.
        # It will parse the IR, create an ExecutionEngine, add the module, and run the function pointer.
        print(f"[JIT] Executing {entry_func} natively...")
        pass
