from dataclasses import dataclass, field
from typing import List, Optional, Any
from aayu.compiler.backend.llvm.types import LLVMType, void

@dataclass
class LLVMValue:
    """Represents a typed value in LLVM IR."""
    type: LLVMType
    name: str # The local/global name (e.g. '%1', '@global_var')
    
    def serialize(self) -> str:
        return f"{self.type.serialize()} {self.name}"
        
    def serialize_untyped(self) -> str:
        return self.name

@dataclass
class LLVMInstruction:
    """Base class for all LLVM instructions in the internal graph."""
    def serialize(self) -> str:
        raise NotImplementedError

@dataclass
class LLVMBasicBlock:
    name: str
    instructions: List[LLVMInstruction] = field(default_factory=list)
    
    def add_instruction(self, inst: LLVMInstruction):
        self.instructions.append(inst)
        
    def serialize(self) -> str:
        res = f"{self.name}:\n"
        for inst in self.instructions:
            res += f"  {inst.serialize()}\n"
        return res

@dataclass
class LLVMFunction:
    name: str
    return_type: LLVMType
    args: List[LLVMValue] = field(default_factory=list)
    blocks: List[LLVMBasicBlock] = field(default_factory=list)
    is_declare_only: bool = False
    
    def serialize(self) -> str:
        args_str = ", ".join(arg.serialize() for arg in self.args)
        ret_type_str = self.return_type.serialize()
        
        if self.is_declare_only:
            return f"declare {ret_type_str} @{self.name}({args_str})\n"
            
        res = f"define {ret_type_str} @{self.name}({args_str}) {{\n"
        for block in self.blocks:
            res += block.serialize()
        res += "}\n"
        return res

@dataclass
class LLVMModule:
    name: str
    functions: List[LLVMFunction] = field(default_factory=list)
    
    def serialize(self) -> str:
        res = f"; ModuleID = '{self.name}'\n"
        res += f"source_filename = \"{self.name}\"\n\n"
        for func in self.functions:
            res += func.serialize() + "\n"
        return res

# ---- Concrete Instructions ----

@dataclass
class LLVMBinaryOp(LLVMInstruction):
    op: str # "add", "sub", "mul", "sdiv", etc.
    dest: LLVMValue
    lhs: LLVMValue
    rhs: LLVMValue
    
    def serialize(self) -> str:
        return f"{self.dest.name} = {self.op} {self.dest.type.serialize()} {self.lhs.name}, {self.rhs.name}"

@dataclass
class LLVMRet(LLVMInstruction):
    val: Optional[LLVMValue] = None
    
    def serialize(self) -> str:
        if self.val is None:
            return "ret void"
        return f"ret {self.val.serialize()}"

@dataclass
class LLVMCall(LLVMInstruction):
    dest: Optional[LLVMValue]
    func_type: LLVMType
    func_name: str
    args: List[LLVMValue]
    
    def serialize(self) -> str:
        args_str = ", ".join(a.serialize() for a in self.args)
        call_str = f"call {self.func_type.serialize()} @{self.func_name}({args_str})"
        if self.dest:
            return f"{self.dest.name} = {call_str}"
        return call_str

@dataclass
class LLVMBranch(LLVMInstruction):
    target: str # label name
    
    def serialize(self) -> str:
        return f"br label %{self.target}"

@dataclass
class LLVMCondBranch(LLVMInstruction):
    cond: LLVMValue
    true_target: str
    false_target: str
    
    def serialize(self) -> str:
        return f"br {self.cond.serialize()}, label %{self.true_target}, label %{self.false_target}"

@dataclass
class LLVMAlloca(LLVMInstruction):
    dest: LLVMValue
    alloc_type: LLVMType
    
    def serialize(self) -> str:
        return f"{self.dest.name} = alloca {self.alloc_type.serialize()}"

@dataclass
class LLVMLoad(LLVMInstruction):
    dest: LLVMValue
    ptr: LLVMValue
    
    def serialize(self) -> str:
        return f"{self.dest.name} = load {self.dest.type.serialize()}, {self.ptr.serialize()}"

@dataclass
class LLVMStore(LLVMInstruction):
    val: LLVMValue
    ptr: LLVMValue
    
    def serialize(self) -> str:
        return f"store {self.val.serialize()}, {self.ptr.serialize()}"
