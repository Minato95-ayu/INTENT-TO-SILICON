from typing import List, Optional, Any
from dataclasses import dataclass, field
from aayu.compiler.backend.llvm.types import LLVMType, void

class LLVMValue:
    """Base class for all values computed by a program that may be used as operands."""
    def __init__(self, value_type: LLVMType, name: str = ""):
        self.type = value_type
        self.name = name
        self.uses: List['Use'] = []
        
    def add_use(self, use: 'Use'):
        self.uses.append(use)
        
    def remove_use(self, use: 'Use'):
        if use in self.uses:
            self.uses.remove(use)
            
    def replace_all_uses_with(self, new_value: 'LLVMValue'):
        """Replaces all uses of this value with the new value."""
        for use in list(self.uses):
            use.set(new_value)

class Use:
    """Represents the edge between a Value definition and its User."""
    def __init__(self, value: LLVMValue, user: 'LLVMUser'):
        self.value = value
        self.user = user
        if value:
            value.add_use(self)
            
    def set(self, new_value: LLVMValue):
        if self.value:
            self.value.remove_use(self)
        self.value = new_value
        if new_value:
            new_value.add_use(self)

class LLVMUser(LLVMValue):
    """Base class for values that use other values (e.g. Instructions)."""
    def __init__(self, value_type: LLVMType, name: str = ""):
        super().__init__(value_type, name)
        self.operands: List[Use] = []
        
    def add_operand(self, val: LLVMValue):
        use = Use(val, self)
        self.operands.append(use)
        
    def set_operand(self, index: int, val: LLVMValue):
        if index < len(self.operands):
            self.operands[index].set(val)
        else:
            raise IndexError("Operand index out of bounds")
            
    def get_operand(self, index: int) -> LLVMValue:
        return self.operands[index].value

class LLVMConstant(LLVMUser):
    """Base class for constants."""
    pass

class LLVMConstantInt(LLVMConstant):
    def __init__(self, value_type: LLVMType, value: int):
        super().__init__(value_type, str(value))
        self.value = value

class LLVMConstantFloat(LLVMConstant):
    def __init__(self, value_type: LLVMType, value: float):
        super().__init__(value_type, str(value))
        self.value = value

class LLVMConstantString(LLVMConstant):
    def __init__(self, value: str):
        from aayu.compiler.backend.llvm.types import ptr
        super().__init__(ptr, f'c"{value}\\00"')
        self.value = value

class LLVMArgument(LLVMValue):
    """Represents an incoming argument to a function."""
    def __init__(self, value_type: LLVMType, name: str, parent: 'LLVMFunction'):
        super().__init__(value_type, name)
        self.parent = parent

class LLVMGlobal(LLVMUser):
    """Represents a global variable."""
    def __init__(self, value_type: LLVMType, name: str, initializer: Optional[LLVMConstant] = None):
        super().__init__(value_type, name) # The type of a global is actually a pointer to its value type. But we keep it simple.
        self.initializer = initializer

class LLVMInstruction(LLVMUser):
    """Base class for all instructions."""
    def __init__(self, value_type: LLVMType, opcode: str, name: str = ""):
        super().__init__(value_type, name)
        self.opcode = opcode
        self.parent: Optional['LLVMBasicBlock'] = None
        self.metadata: dict[str, str] = {}

class LLVMBasicBlock(LLVMValue):
    """A basic block is a value because it can be branched to (used by branch instructions)."""
    def __init__(self, name: str, parent: Optional['LLVMFunction'] = None):
        super().__init__(void, name) # Label type is effectively void/label
        self.parent = parent
        self.instructions: List[LLVMInstruction] = []
        
    def insert_instruction(self, instr: LLVMInstruction):
        instr.parent = self
        self.instructions.append(instr)

class LLVMFunction(LLVMGlobal):
    """A function is a global value."""
    def __init__(self, name: str, return_type: LLVMType):
        super().__init__(return_type, name)
        self.return_type = return_type
        self.args: List[LLVMArgument] = []
        self.blocks: List[LLVMBasicBlock] = []
        self.is_declare_only = False
        self.parent: Optional['LLVMModule'] = None
        self.metadata: dict[str, Any] = {}

class LLVMModule:
    """The root of the IR graph."""
    def __init__(self, name: str):
        self.name = name
        self.functions: List[LLVMFunction] = []
        self.globals: List[LLVMGlobal] = []
        self.struct_types: List['StructType'] = []
        
    def add_function(self, func: LLVMFunction):
        func.parent = self
        self.functions.append(func)
