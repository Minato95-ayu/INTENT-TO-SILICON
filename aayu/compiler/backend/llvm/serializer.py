from aayu.compiler.backend.llvm.values import (
    LLVMModule, LLVMFunction, LLVMBasicBlock, LLVMInstruction,
    LLVMConstant, LLVMArgument, LLVMGlobal, LLVMConstantInt, LLVMConstantFloat,
    LLVMValue
)
from aayu.compiler.backend.llvm.types import LLVMType, void

class LLVMSerializer:
    """Serializes the pure Python LLVM IR Graph into a stable, deterministic .ll string."""
    def __init__(self):
        self.output = []

    def serialize(self, module: LLVMModule) -> str:
        self.output = []
        self.output.append(f"; ModuleID = '{module.name}'")
        self.output.append(f"source_filename = \"{module.name}\"\n")
        
        dbg_serializer = None
        if hasattr(module, 'metadata') and 'debug_graph' in module.metadata:
            from aayu.compiler.backend.llvm.debug.serializer import DebugGraphSerializer
            dbg_serializer = DebugGraphSerializer(module.metadata['debug_graph'])
            dbg_serializer.resolve_ids()
            
        if hasattr(module, 'struct_types'):
            for struct_ty in module.struct_types:
                # Assuming struct_ty is of StructType and has a name and elements
                elems = ", ".join(e.serialize() for e in struct_ty.elements)
                self.output.append(f"%{struct_ty.name} = type {{{elems}}}\n")
            
        for glob in module.globals:
            self._serialize_global(glob)
            
        for func in module.functions:
            self._serialize_function(func)
            
        if dbg_serializer:
            self.output.append("\n; --- Debug Metadata ---")
            self.output.append(dbg_serializer.emit_metadata())
            
        return "\n".join(self.output)

    def _serialize_global(self, glob: LLVMGlobal):
        init = self._serialize_value_inline(glob.initializer) if glob.initializer else "zeroinitializer"
        if type(glob.initializer).__name__ == "LLVMConstantString":
            self.output.append(f"@{glob.name} = private unnamed_addr constant {glob.type.serialize()} {init}, align 1")
        else:
            self.output.append(f"@{glob.name} = global {glob.type.serialize()} {init}")

    def _serialize_function(self, func: LLVMFunction):
        args_str = ", ".join(f"{arg.type.serialize()} %{arg.name}" for arg in func.args)
        ret_type_str = func.return_type.serialize()
        
        if func.is_declare_only:
            attrs = func.metadata.get("attributes", [])
            attrs_str = (" " + " ".join(attrs)) if attrs else ""
            if not args_str:
                args_str = "..."
            self.output.append(f"declare {ret_type_str} @{func.name}({args_str}){attrs_str}\n")
            return
            
        dbg_node = func.metadata.get('dbg')
        dbg_str = f" !dbg !{dbg_node.md_id}" if dbg_node and dbg_node.md_id is not None else ""
        
        self.output.append(f"define {ret_type_str} @{func.name}({args_str}){dbg_str} {{")
        for block in func.blocks:
            self._serialize_block(block)
        self.output.append("}\n")

    def _serialize_block(self, block: LLVMBasicBlock):
        self.output.append(f"{block.name}:")
        for instr in block.instructions:
            self._serialize_instruction(instr)

    def _serialize_value_inline(self, val: LLVMValue) -> str:
        if isinstance(val, LLVMConstantInt) or isinstance(val, LLVMConstantFloat):
            return str(val.value)
        elif type(val).__name__ == "LLVMConstantString":
            return val.name  # val.name contains the c"string\00" format
        elif isinstance(val, LLVMArgument):
            return f"%{val.name}"
        elif isinstance(val, LLVMBasicBlock):
            return f"%{val.name}"
        elif isinstance(val, LLVMFunction) or isinstance(val, LLVMGlobal):
            return f"@{val.name}"
        else:
            name_str = val.name if val.name else ""
            if name_str and not name_str.startswith("%") and not name_str.startswith("@"):
                return f"%{name_str}"
            return name_str

    def _serialize_operand_type(self, val: LLVMValue) -> str:
        if isinstance(val, LLVMGlobal) or isinstance(val, LLVMFunction):
            return "ptr"
        if type(val).__name__ == "LLVMConstantString":
            return "ptr"
        return val.type.serialize()

    def _serialize_instruction(self, instr: LLVMInstruction):
        line = "  "
        if instr.name and instr.type != void:
            if instr.name.startswith("%"):
                line += f"{instr.name} = "
            else:
                line += f"%{instr.name} = "
            
        line += instr.opcode
        
        if instr.opcode in ("add", "sub", "mul", "sdiv", "and"):
            lhs = instr.get_operand(0)
            rhs = instr.get_operand(1)
            line += f" {self._serialize_operand_type(lhs)} {self._serialize_value_inline(lhs)}, {self._serialize_value_inline(rhs)}"
            
        elif instr.opcode == "icmp":
            cond = instr.metadata.get("cond", "eq")
            lhs = instr.get_operand(0)
            rhs = instr.get_operand(1)
            line += f" {cond} {self._serialize_operand_type(lhs)} {self._serialize_value_inline(lhs)}, {self._serialize_value_inline(rhs)}"
            
        elif instr.opcode == "alloca":
            alloc_type = instr.metadata.get("alloc_type", void)
            line += f" {alloc_type.serialize()}"
            
        elif instr.opcode == "load":
            ptr = instr.get_operand(0)
            line += f" {instr.type.serialize()}, {self._serialize_operand_type(ptr)} {self._serialize_value_inline(ptr)}"
            
        elif instr.opcode == "store":
            val = instr.get_operand(0)
            ptr = instr.get_operand(1)
            line += f" {self._serialize_operand_type(val)} {self._serialize_value_inline(val)}, {self._serialize_operand_type(ptr)} {self._serialize_value_inline(ptr)}"
            
        elif instr.opcode == "getelementptr":
            # Format: getelementptr <base_type>, ptr <base_ptr>, i32 <idx0>, i32 <idx1>, ...
            base_ptr = instr.get_operand(0)
            # Try to get the base type from the pointer's alloca metadata, or use i8 as fallback
            base_type_str = "i8"
            alloc_type = instr.metadata.get("gep_base_type")
            if alloc_type:
                base_type_str = alloc_type.serialize()
            elif hasattr(base_ptr, 'metadata') and 'alloc_type' in base_ptr.metadata:
                base_type_str = base_ptr.metadata['alloc_type'].serialize()
            
            indices_parts = []
            for i in range(1, len(instr.operands)):
                idx = instr.get_operand(i)
                indices_parts.append(f"{self._serialize_operand_type(idx)} {self._serialize_value_inline(idx)}")
            
            line += f" {base_type_str}, {self._serialize_operand_type(base_ptr)} {self._serialize_value_inline(base_ptr)}, {', '.join(indices_parts)}"
            
        elif instr.opcode == "br":
            if len(instr.operands) == 1:
                dest = instr.get_operand(0)
                line += f" label {self._serialize_value_inline(dest)}"
            else:
                cond = instr.get_operand(0)
                true_dest = instr.get_operand(1)
                false_dest = instr.get_operand(2)
                line += f" i1 {self._serialize_value_inline(cond)}, label {self._serialize_value_inline(true_dest)}, label {self._serialize_value_inline(false_dest)}"
                
        elif instr.opcode == "ret":
            if len(instr.operands) > 0:
                val = instr.get_operand(0)
                line += f" {self._serialize_operand_type(val)} {self._serialize_value_inline(val)}"
            else:
                line += " void"
                
        elif instr.opcode == "call":
            func = instr.get_operand(0)
            args = []
            for i in range(1, len(instr.operands)):
                arg = instr.get_operand(i)
                args.append(f"{self._serialize_operand_type(arg)} {self._serialize_value_inline(arg)}")
            line += f" {func.type.serialize()} {self._serialize_value_inline(func)}({', '.join(args)})"
            
        dbg_node = instr.metadata.get('dbg')
        if dbg_node and getattr(dbg_node, 'md_id', None) is not None:
            line += f", !dbg !{dbg_node.md_id}"
            
        self.output.append(line)
