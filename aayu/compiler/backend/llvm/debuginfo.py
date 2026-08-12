from dataclasses import dataclass
from aayu.compiler.errors import SourceSpan

class LLVMDebugEmitter:
    """
    Emits DWARF metadata for LLVM IR instructions.
    Currently a stub; will interface with LLVM DIBuilder.
    """
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.compile_unit = None
        self.current_scope = None
        
    def setup_compile_unit(self, filename: str, directory: str):
        # Maps to DIBuilder.createCompileUnit()
        pass
        
    def enter_function_scope(self, name: str, line: int):
        # Maps to DIBuilder.createFunction()
        pass
        
    def attach_location(self, instruction, span: SourceSpan):
        """
        Attaches !dbg metadata to an LLVM instruction based on the SourceSpan.
        Preserves File, Line, Column, and Scope.
        """
        if not span:
            return
            
        # instruction.set_metadata("dbg", ...)
        pass
