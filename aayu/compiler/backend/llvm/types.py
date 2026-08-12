from dataclasses import dataclass, field
from typing import List, Optional

class LLVMType:
    def serialize(self) -> str:
        raise NotImplementedError

@dataclass(frozen=True)
class IntType(LLVMType):
    width: int
    
    def serialize(self) -> str:
        return f"i{self.width}"

@dataclass(frozen=True)
class FloatType(LLVMType):
    width: int
    
    def serialize(self) -> str:
        if self.width == 32:
            return "float"
        elif self.width == 64:
            return "double"
        raise ValueError(f"Unsupported float width: {self.width}")

@dataclass(frozen=True)
class PointerType(LLVMType):
    element_type: Optional[LLVMType] = None
    
    def serialize(self) -> str:
        # LLVM 15+ prefers opaque pointers (`ptr`).
        # If we need typed pointers for older LLVM, we can use `element_type`.
        return "ptr"

@dataclass(frozen=True)
class ArrayType(LLVMType):
    element_type: LLVMType
    count: int
    
    def serialize(self) -> str:
        return f"[{self.count} x {self.element_type.serialize()}]"

@dataclass(frozen=True)
class StructType(LLVMType):
    name: Optional[str]
    elements: List[LLVMType]
    is_packed: bool = False
    
    def serialize(self) -> str:
        if self.name:
            return f"%{self.name}"
        elems = ", ".join(e.serialize() for e in self.elements)
        if self.is_packed:
            return f"<{elems}>"
        return f"{{{elems}}}"

@dataclass(frozen=True)
class FunctionType(LLVMType):
    return_type: LLVMType
    args: List[LLVMType]
    is_var_arg: bool = False
    
    def serialize(self) -> str:
        args_str = ", ".join(a.serialize() for a in self.args)
        if self.is_var_arg:
            if args_str:
                args_str += ", ..."
            else:
                args_str = "..."
        return f"{self.return_type.serialize()} ({args_str})"

@dataclass(frozen=True)
class VoidType(LLVMType):
    def serialize(self) -> str:
        return "void"

# Common Type Singletons
i1 = IntType(1)
i8 = IntType(8)
i16 = IntType(16)
i32 = IntType(32)
i64 = IntType(64)
f32 = FloatType(32)
f64 = FloatType(64)
ptr = PointerType()
void = VoidType()
