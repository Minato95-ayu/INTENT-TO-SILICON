from typing import Dict, Any, Callable
from aayu.compiler.backend.interface import Backend, BackendArtifact
from aayu.compiler.machine_lir.nodes import MachineModule, MachineFunction, MachineInstruction, OperandType
from aayu.compiler.backend.llvm.values import (
    LLVMModule, LLVMFunction, LLVMBasicBlock, LLVMValue, LLVMConstantInt, LLVMArgument
)
from aayu.compiler.backend.llvm.builder import IRBuilder
from aayu.compiler.backend.llvm.types import i32, ptr, void

class LLVMBinaryArtifact(BackendArtifact):
    def __init__(self, llvm_module: LLVMModule):
        self.llvm_module = llvm_module
        
    def generate(self) -> bytes:
        # Serializer handles mapping the object to text
        from aayu.compiler.backend.llvm.serializer import LLVMSerializer
        serializer = LLVMSerializer()
        return serializer.serialize(self.llvm_module).encode('utf-8')

class RuntimeSymbolResolver:
    """Resolves standard library and runtime symbols to native C functions."""
    def __init__(self):
        # Maps AAYU symbol names to their native C function names and return types
        self.symbols = {
            "ping": ("aayu_ping", ptr),
            "dns_resolve": ("aayu_dns_resolve", ptr),
            "tcp_connect": ("aayu_tcp_connect", ptr),
        }
        
    def resolve(self, symbol_name: str):
        return self.symbols.get(symbol_name)

class LLVMBackend(Backend):
    def __init__(self):
        self.val_map: Dict[str, LLVMValue] = {}
        self.block_map: Dict[str, LLVMBasicBlock] = {}
        self.builder = IRBuilder()
        self.resolver = RuntimeSymbolResolver()
        self.llvm_mod = None
        self.global_map = {}
        
        self.dispatch_map: Dict[str, Callable] = {
            "ADD": self.lower_add,
            "SUB": self.lower_sub,
            "MUL": self.lower_mul,
            "DIV": self.lower_sdiv,
            "RET": self.lower_return,
            "JMP": self.lower_branch,
            "LOAD_CONST": self.lower_load_const,
            "LOAD_ENUM_CONST": self.lower_load_enum_const,
            "LOAD_GLOBAL": self.lower_load_global,
            "STORE_GLOBAL": self.lower_store_global,
            "LOAD_LOCAL": self.lower_load_local,
            "LOAD_LOCAL_PTR": self.lower_load_local_ptr,
            "LOAD_GLOBAL_PTR": self.lower_load_global_ptr,
            "STORE_LOCAL": self.lower_store_local,
            "CALL": self.lower_call,
            "ALLOC": self.lower_alloc,
            "GEP": self.lower_gep,
            "LOAD": self.lower_load,
            "STORE": self.lower_store,
            "CMP_EQ": lambda i: self.lower_cmp(i, "eq"),
            "CMP_NE": lambda i: self.lower_cmp(i, "ne"),
            "CMP_GT": lambda i: self.lower_cmp(i, "sgt"),
            "CMP_LT": lambda i: self.lower_cmp(i, "slt"),
            "AND": self.lower_and
        }
        
    def lower(self, module: MachineModule) -> BackendArtifact:
        self.llvm_mod = LLVMModule(name="aayu_module")
        
        for func in module.functions:
            llvm_func = self.lower_function(func)
            self.llvm_mod.add_function(llvm_func)
            
        return LLVMBinaryArtifact(self.llvm_mod)
        
    def lower_function(self, func: MachineFunction) -> LLVMFunction:
        self.val_map.clear()
        self.block_map.clear()
        
        # We'll default to i32 for now until full typing is established
        llvm_func = LLVMFunction(name=func.name, return_type=i32)
        
        # Pass 1: Create all blocks so they can be referenced
        for block in func.blocks:
            llvm_bb = LLVMBasicBlock(name=block.name)
            self.block_map[block.name] = llvm_bb
            llvm_func.blocks.append(llvm_bb)
            
        # Pass 2: Lower instructions
        for block in func.blocks:
            llvm_bb = self.block_map[block.name]
            self.builder.position_at_end(llvm_bb)
            
            for instr in block.instructions:
                self.lower_instruction(instr)
                
        return llvm_func
        
    def lower_instruction(self, instr: MachineInstruction):
        handler = self.dispatch_map.get(instr.opcode)
        if handler:
            handler(instr)
        else:
            raise NotImplementedError(f"Lowering for MachineLIR opcode {instr.opcode} not implemented.")

    # --- Dispatch Methods ---

    def lower_load_const(self, instr: MachineInstruction):
        # r1 = LOAD_CONST 50 or "127.0.0.1"
        dest_name = f"%v{instr.dest.value.id}"
        val_str = instr.operands[0].value
        if isinstance(val_str, str) and not val_str.isdigit() and not (val_str.replace('.', '', 1).isdigit() and val_str.count('.') == 1):
            from aayu.compiler.backend.llvm.values import LLVMConstantString, LLVMGlobal, LLVMValue
            from aayu.compiler.backend.llvm.types import ArrayType, i8, ptr
            str_len = len(val_str.encode('utf-8')) + 1
            arr_type = ArrayType(i8, str_len)
            str_const = LLVMConstantString(val_str)
            str_const.type = arr_type
            global_name = f".str.{instr.dest.value.id}"
            glob = LLVMGlobal(arr_type, global_name, initializer=str_const)
            self.llvm_mod.globals.append(glob)
            # The value used in instructions should be typed as `ptr`
            const_val = LLVMValue(ptr, f"@{global_name}")
        else:
            val = float(val_str) if '.' in str(val_str) else int(val_str)
            from aayu.compiler.backend.llvm.values import LLVMConstantInt, LLVMConstantFloat
            const_val = LLVMConstantFloat(i32, val) if isinstance(val, float) else LLVMConstantInt(i32, val)
        self.val_map[dest_name] = const_val

    def lower_load_enum_const(self, instr: MachineInstruction):
        # r1 = LOAD_ENUM_CONST MIREnumConstant(...)
        from aayu.compiler.mir.nodes import MIREnumConstant
        from aayu.compiler.backend.llvm.values import LLVMConstantInt
        from aayu.compiler.backend.llvm.types import i32, i16, i8
        
        dest_name = f"%v{instr.dest.value.id}"
        enum_meta: MIREnumConstant = instr.operands[0].value
        
        # Lower EnumType to integer size specified by the backend/target
        if enum_meta.tag_size == 8:
            llvm_type = i8
        elif enum_meta.tag_size == 16:
            llvm_type = i16
        else:
            llvm_type = i32
            
        const_val = LLVMConstantInt(llvm_type, enum_meta.tag)
        self.val_map[dest_name] = const_val
        
        # In a full debugger implementation, we would emit LLVM DIBuilder metadata here
        # mapping the tag back to enum_meta.enum_name and enum_meta.variant_name

    def lower_load_global(self, instr: MachineInstruction):
        dest_name = f"%v{instr.dest.value.id}"
        symbol_name = instr.operands[0].value
        
        global_name = f"@{symbol_name}"
        if global_name in self.global_map:
            glob_ptr = self.global_map[global_name]
            from aayu.compiler.backend.llvm.types import i32
            # Just default to i32 for now, or get from glob if supported
            load_type = getattr(glob_ptr, 'value_type', i32)
            load_instr = self.builder.load(glob_ptr, load_type, name=dest_name[1:])
            self.val_map[dest_name] = load_instr
            return
        
        resolved = self.resolver.resolve(symbol_name)
        if resolved:
            native_name, ret_type = resolved
            # Find or create external declaration
            ext_func = None
            for func in self.llvm_mod.functions:
                if func.name == native_name:
                    ext_func = func
                    break
            
            if not ext_func:
                ext_func = LLVMFunction(name=native_name, return_type=ret_type)
                ext_func.is_declare_only = True
                self.llvm_mod.add_function(ext_func)
            
            self.val_map[dest_name] = ext_func
        else:
            raise NotImplementedError(f"Unresolved global symbol: {symbol_name}")

    def lower_store_global(self, instr: MachineInstruction):
        var_name = instr.operands[0].value
        src_reg = self.get_val(instr.operands[1])
        
        global_name = f"@{var_name}"
        if global_name not in self.global_map:
            from aayu.compiler.backend.llvm.values import LLVMGlobal, LLVMConstantInt
            # assuming it's initialized to 0 if not provided
            zero_init = LLVMConstantInt(src_reg.type, 0)
            glob = LLVMGlobal(src_reg.type, var_name, initializer=zero_init)
            glob.value_type = src_reg.type
            self.llvm_mod.globals.append(glob)
            self.global_map[global_name] = glob
            
        glob_ptr = self.global_map[global_name]
        self.builder.store(src_reg, glob_ptr)

    def lower_load_local(self, instr: MachineInstruction):
        var_name = instr.operands[0].value
        dest_name = f"%v{instr.dest.value.id}"
        
        ptr_name = f"%{var_name}.ptr"
        if ptr_name not in self.val_map:
            raise RuntimeError(f"Local {var_name} loaded before store")
            
        ptr_val = self.val_map[ptr_name]
        from aayu.compiler.backend.llvm.types import i32
        load_type = getattr(ptr_val, 'value_type', i32)
        
        load_instr = self.builder.load(ptr_val, load_type, name=dest_name[1:])
        self.val_map[dest_name] = load_instr

    def lower_load_local_ptr(self, instr: MachineInstruction):
        var_name = instr.operands[0].value
        dest_name = f"%v{instr.dest.value.id}"
        
        ptr_name = f"%{var_name}.ptr"
        if ptr_name not in self.val_map:
            raise RuntimeError(f"Local {var_name} ptr loaded before store")
            
        ptr_val = self.val_map[ptr_name]
        self.val_map[dest_name] = ptr_val

    def lower_load_global_ptr(self, instr: MachineInstruction):
        var_name = instr.operands[0].value
        dest_name = f"%v{instr.dest.value.id}"
        
        global_name = f"@{var_name}"
        if global_name not in self.global_map:
            raise RuntimeError(f"Global {var_name} ptr loaded before store")
            
        glob_ptr = self.global_map[global_name]
        self.val_map[dest_name] = glob_ptr

    def lower_store_local(self, instr: MachineInstruction):
        var_name = instr.operands[0].value
        src_reg = self.get_val(instr.operands[1])
        
        ptr_name = f"%{var_name}.ptr"
        if ptr_name not in self.val_map:
            alloc = self.builder.alloca(src_reg.type, name=ptr_name[1:])
            alloc.value_type = src_reg.type
            self.val_map[ptr_name] = alloc
            
        ptr_val = self.val_map[ptr_name]
        self.builder.store(src_reg, ptr_val)

    def lower_call(self, instr: MachineInstruction):
        # r2 = CALL r1, r3
        dest_name = f"%v{instr.dest.value.id}"
        func_val = self.get_val(instr.operands[0])
        args = [self.get_val(op) for op in instr.operands[1:]]
        
        # We need a proper IRBuilder call method.
        # Assuming builder has a call method, or we synthesize an instruction
        from aayu.compiler.backend.llvm.values import LLVMInstruction
        call_instr = LLVMInstruction(func_val.type, "call", dest_name)
        call_instr.add_operand(func_val)
        for arg in args:
            call_instr.add_operand(arg)
            
        self.builder._insert(call_instr)
        self.val_map[dest_name] = call_instr

    def lower_add(self, instr: MachineInstruction):
        dest_name = f"%v{instr.dest.value.id}"
        lhs = self.get_val(instr.operands[0])
        rhs = self.get_val(instr.operands[1])
        res = self.builder.add(lhs, rhs, name=dest_name)
        self.val_map[dest_name] = res

    def lower_sub(self, instr: MachineInstruction):
        dest_name = f"%v{instr.dest.value.id}"
        lhs = self.get_val(instr.operands[0])
        rhs = self.get_val(instr.operands[1])
        res = self.builder.sub(lhs, rhs, name=dest_name)
        self.val_map[dest_name] = res

    def lower_cmp(self, instr: MachineInstruction, cond: str):
        dest_name = f"%v{instr.dest.value.id}"
        lhs = self.get_val(instr.operands[0])
        rhs = self.get_val(instr.operands[1])
        res = self.builder.icmp(cond, lhs, rhs, name=dest_name)
        self.val_map[dest_name] = res

    def lower_and(self, instr: MachineInstruction):
        dest_name = f"%v{instr.dest.value.id}"
        lhs = self.get_val(instr.operands[0])
        rhs = self.get_val(instr.operands[1])
        res = self.builder.and_(lhs, rhs, name=dest_name)
        self.val_map[dest_name] = res
        
    def lower_mul(self, instr: MachineInstruction):
        dest_name = f"%v{instr.dest.value.id}"
        lhs = self.get_val(instr.operands[0])
        rhs = self.get_val(instr.operands[1])
        res = self.builder.mul(lhs, rhs, name=dest_name)
        self.val_map[dest_name] = res
        
    def lower_sdiv(self, instr: MachineInstruction):
        dest_name = f"%v{instr.dest.value.id}"
        lhs = self.get_val(instr.operands[0])
        rhs = self.get_val(instr.operands[1])
        res = self.builder.sdiv(lhs, rhs, name=dest_name)
        self.val_map[dest_name] = res

    def lower_return(self, instr: MachineInstruction):
        if not instr.operands:
            self.builder.ret()
        else:
            val = self.get_val(instr.operands[0])
            self.builder.ret(val)

    def lower_branch(self, instr: MachineInstruction):
        target = instr.operands[0].value
        dest_block = self.block_map[target]
        self.builder.br(dest_block)

    # --- Helpers ---

    def get_val(self, operand) -> LLVMValue:
        if operand.type == OperandType.REGISTER:
            name = f"%v{operand.value.id}"
            if name in self.val_map:
                return self.val_map[name]
            raise ValueError(f"Use of uninitialized register: {name}")
        elif operand.type == OperandType.IMMEDIATE:
            return LLVMConstantInt(i32, int(operand.value))
        raise ValueError(f"Unknown operand type: {operand.type}")

    # --- Memory / Struct Lowering ---

    def lower_alloc(self, instr: MachineInstruction):
        dest_name = f"%v{instr.dest.value.id}"
        struct_name = instr.operands[0].value
        
        from aayu.compiler.backend.llvm.types import StructType
        struct_type = StructType(name=struct_name, elements=[])
        
        alloc_instr = self.builder.alloca(struct_type, name=dest_name[1:])
        self.val_map[dest_name] = alloc_instr

    def lower_gep(self, instr: MachineInstruction):
        dest_name = f"%v{instr.dest.value.id}"
        ptr_reg = self.get_val(instr.operands[0])
        idx_val = instr.operands[1].value
        
        from aayu.compiler.backend.llvm.values import LLVMConstantInt
        from aayu.compiler.backend.llvm.types import i32
        
        # GEP typically requires base idx (0) and field idx
        base_idx = LLVMConstantInt(i32, 0)
        field_idx = LLVMConstantInt(i32, int(idx_val))
        
        gep_instr = self.builder.gep(ptr_reg, [base_idx, field_idx], name=dest_name[1:])
        self.val_map[dest_name] = gep_instr

    def lower_load(self, instr: MachineInstruction):
        dest_name = f"%v{instr.dest.value.id}"
        ptr_reg = self.get_val(instr.operands[0])
        from aayu.compiler.backend.llvm.types import i32 # Assuming i32 for now
        load_instr = self.builder.load(ptr_reg, i32, name=dest_name[1:])
        self.val_map[dest_name] = load_instr

    def lower_store(self, instr: MachineInstruction):
        val_reg = self.get_val(instr.operands[0])
        ptr_reg = self.get_val(instr.operands[1])
        self.builder.store(val_reg, ptr_reg)
