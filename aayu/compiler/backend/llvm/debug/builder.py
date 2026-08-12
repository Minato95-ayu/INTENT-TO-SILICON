from typing import Dict, List, Optional
from aayu.compiler.backend.llvm.debug.nodes import (
    DINode, DICompileUnit, DIFile, DISubprogram, DILexicalBlock, DILocation
)
from aayu.compiler.backend.llvm.values import LLVMModule, LLVMFunction, LLVMInstruction

class DebugGraphBuilder:
    """
    Constructs the Pure Python LLVM Debug Metadata Graph.
    Attached to a specific LLVMModule.
    """
    def __init__(self, module: LLVMModule):
        self.module = module
        self.nodes: List[DINode] = []
        self.files: Dict[str, DIFile] = {}
        self.compile_unit: Optional[DICompileUnit] = None
        
        # Attach self to the module's metadata so the serializer can access it
        if not hasattr(module, 'metadata'):
            module.metadata = {}
        module.metadata['debug_graph'] = self
        
    def add_node(self, node: DINode) -> DINode:
        self.nodes.append(node)
        return node
        
    def create_compile_unit(self, filename: str, directory: str, producer: str = "AAYU v1.0", is_optimized: bool = False) -> DICompileUnit:
        file_node = self.get_or_create_file(filename, directory)
        # LLVM DWARF language ID for C is usually 4, C99 is 12, Rust is 28. We'll use 0x8000 for custom, or C99 (12) for now.
        cu = DICompileUnit(
            language=12,
            file=file_node,
            producer=producer,
            is_optimized=is_optimized,
            runtime_version=0,
            emission_kind=1 # Full debug
        )
        self.compile_unit = cu
        return self.add_node(cu)
        
    def get_or_create_file(self, filename: str, directory: str) -> DIFile:
        key = f"{directory}/{filename}"
        if key not in self.files:
            file_node = DIFile(filename=filename, directory=directory)
            self.files[key] = file_node
            self.add_node(file_node)
        return self.files[key]
        
    def create_function(self, func: LLVMFunction, filename: str, directory: str, line: int, scope_line: int) -> DISubprogram:
        file_node = self.get_or_create_file(filename, directory)
        subprog = DISubprogram(
            name=func.name,
            linkage_name=func.name,
            scope=file_node,
            file=file_node,
            line=line,
            is_local=False,
            is_definition=not func.is_declare_only,
            scope_line=scope_line,
            unit=self.compile_unit
        )
        self.add_node(subprog)
        
        # Attach to the LLVMFunction so we can emit !dbg !X
        func.metadata['dbg'] = subprog
        return subprog
        
    def create_lexical_block(self, scope: DINode, filename: str, directory: str, line: int, column: int) -> DILexicalBlock:
        file_node = self.get_or_create_file(filename, directory)
        block = DILexicalBlock(
            scope=scope,
            file=file_node,
            line=line,
            column=column
        )
        return self.add_node(block)
        
    def create_location(self, line: int, column: int, scope: DINode) -> DILocation:
        loc = DILocation(line=line, column=column, scope=scope)
        return self.add_node(loc)
        
    def attach_location(self, instr: LLVMInstruction, loc: DILocation):
        instr.metadata['dbg'] = loc
