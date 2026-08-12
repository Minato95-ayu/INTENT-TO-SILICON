from aayu.compiler.backend.llvm.debug.builder import DebugGraphBuilder
from aayu.compiler.backend.llvm.debug.nodes import DINode

class DebugGraphSerializer:
    """
    Serializes the Debug Metadata Graph into raw LLVM IR metadata nodes.
    Called as a dedicated phase by the main LLVMSerializer.
    """
    def __init__(self, builder: DebugGraphBuilder):
        self.builder = builder
        self.output = []
        
    def resolve_ids(self):
        """Assigns unique IDs (!0, !1) to every node in the graph."""
        for idx, node in enumerate(self.builder.nodes):
            node.md_id = idx
            
    def emit_metadata(self) -> str:
        """Emits the named metadata and all numbered metadata nodes."""
        self.resolve_ids()
        self.output = []
        
        # 1. Named metadata
        # llvm.dbg.cu must point to the compile units
        if self.builder.compile_unit:
            self.output.append(f"!llvm.dbg.cu = !{{!{self.builder.compile_unit.md_id}}}")
            
        # llvm.module.flags for debug info version
        # Usually need !{i32 2, !"Debug Info Version", i32 3}
        # But we'll keep it simple: we define a flag node at the end.
        flag_id = len(self.builder.nodes)
        self.output.append(f"!llvm.module.flags = !{{!{flag_id}}}")
        
        # 2. Numbered metadata nodes
        for node in self.builder.nodes:
            self.output.append(f"!{node.md_id} = {node.serialize_content()}")
            
        # 3. Emit the flag node
        self.output.append(f"!{flag_id} = !{{i32 2, !\"Debug Info Version\", i32 3}}")
        
        return "\n".join(self.output)
