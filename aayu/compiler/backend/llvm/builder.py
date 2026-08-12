from typing import List, Optional
from aayu.compiler.backend.llvm.values import (
    LLVMBasicBlock, LLVMInstruction, LLVMValue, LLVMConstantInt, LLVMConstantFloat
)
from aayu.compiler.backend.llvm.types import LLVMType, void

class IRBuilder:
    """Fluent API for constructing LLVM IR graph instructions within a BasicBlock."""
    def __init__(self):
        self.block: Optional[LLVMBasicBlock] = None
        self._name_counter = 0
        
    def position_at_end(self, block: LLVMBasicBlock):
        self.block = block
        
    def _next_name(self) -> str:
        name = f"%v{self._name_counter}"
        self._name_counter += 1
        return name
        
    def _insert(self, instr: LLVMInstruction) -> LLVMInstruction:
        if not self.block:
            raise RuntimeError("IRBuilder has no block to insert into.")
        self.block.insert_instruction(instr)
        return instr

    # --- Arithmetic ---
    
    def add(self, lhs: LLVMValue, rhs: LLVMValue, name: str = "") -> LLVMInstruction:
        if not name: name = self._next_name()
        instr = LLVMInstruction(lhs.type, "add", name)
        instr.add_operand(lhs)
        instr.add_operand(rhs)
        return self._insert(instr)
        
    def sub(self, lhs: LLVMValue, rhs: LLVMValue, name: str = "") -> LLVMInstruction:
        if not name: name = self._next_name()
        instr = LLVMInstruction(lhs.type, "sub", name)
        instr.add_operand(lhs)
        instr.add_operand(rhs)
        return self._insert(instr)
        
    def mul(self, lhs: LLVMValue, rhs: LLVMValue, name: str = "") -> LLVMInstruction:
        if not name: name = self._next_name()
        instr = LLVMInstruction(lhs.type, "mul", name)
        instr.add_operand(lhs)
        instr.add_operand(rhs)
        return self._insert(instr)
        
    def sdiv(self, lhs: LLVMValue, rhs: LLVMValue, name: str = "") -> LLVMInstruction:
        if not name: name = self._next_name()
        instr = LLVMInstruction(lhs.type, "sdiv", name)
        instr.add_operand(lhs)
        instr.add_operand(rhs)
        return self._insert(instr)

    def icmp(self, cond: str, lhs: LLVMValue, rhs: LLVMValue, name: str = "") -> LLVMInstruction:
        if not name: name = self._next_name()
        from aayu.compiler.backend.llvm.types import i1
        instr = LLVMInstruction(i1, "icmp", name)
        instr.metadata["cond"] = cond
        instr.add_operand(lhs)
        instr.add_operand(rhs)
        return self._insert(instr)
        
    def and_(self, lhs: LLVMValue, rhs: LLVMValue, name: str = "") -> LLVMInstruction:
        if not name: name = self._next_name()
        instr = LLVMInstruction(lhs.type, "and", name)
        instr.add_operand(lhs)
        instr.add_operand(rhs)
        return self._insert(instr)

    # --- Memory ---
    
    def alloca(self, alloc_type: LLVMType, name: str = "") -> LLVMInstruction:
        if not name: name = self._next_name()
        from aayu.compiler.backend.llvm.types import ptr
        instr = LLVMInstruction(ptr, "alloca", name)
        # Store alloc_type somewhere, maybe as metadata for now
        instr.metadata["alloc_type"] = alloc_type
        return self._insert(instr)
        
    def load(self, ptr_val: LLVMValue, load_type: LLVMType, name: str = "") -> LLVMInstruction:
        if not name: name = self._next_name()
        instr = LLVMInstruction(load_type, "load", name)
        instr.add_operand(ptr_val)
        return self._insert(instr)
        
    def store(self, val: LLVMValue, ptr_val: LLVMValue) -> LLVMInstruction:
        instr = LLVMInstruction(void, "store")
        instr.add_operand(val)
        instr.add_operand(ptr_val)
        return self._insert(instr)
        
    def gep(self, ptr_val: LLVMValue, indices: List[LLVMValue], result_type: LLVMType = None, name: str = "") -> LLVMInstruction:
        if not name: name = self._next_name()
        from aayu.compiler.backend.llvm.types import ptr
        # result_type should actually be computed based on base type and indices,
        # but for LLVM opaque pointers, the pointer itself is enough for representation.
        # we still pass result_type if we want to add metadata.
        instr = LLVMInstruction(ptr, "getelementptr", name)
        instr.add_operand(ptr_val)
        for idx in indices:
            instr.add_operand(idx)
        return self._insert(instr)
        
    # --- Control Flow ---
    
    def ret(self, val: Optional[LLVMValue] = None) -> LLVMInstruction:
        instr = LLVMInstruction(void, "ret")
        if val:
            instr.add_operand(val)
        return self._insert(instr)
        
    def br(self, dest: LLVMBasicBlock) -> LLVMInstruction:
        instr = LLVMInstruction(void, "br")
        instr.add_operand(dest)
        return self._insert(instr)
        
    def cond_br(self, cond: LLVMValue, true_dest: LLVMBasicBlock, false_dest: LLVMBasicBlock) -> LLVMInstruction:
        instr = LLVMInstruction(void, "br")
        instr.add_operand(cond)
        instr.add_operand(true_dest)
        instr.add_operand(false_dest)
        return self._insert(instr)
        
    def call(self, func: LLVMValue, args: List[LLVMValue], name: str = "") -> LLVMInstruction:
        # Assuming func is LLVMFunction, return type is func.return_type
        ret_type = func.type if hasattr(func, 'type') else void
        if not name and ret_type != void: 
            name = self._next_name()
            
        instr = LLVMInstruction(ret_type, "call", name)
        instr.add_operand(func)
        for arg in args:
            instr.add_operand(arg)
        return self._insert(instr)
