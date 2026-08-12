from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Any, Dict
from aayu.compiler.errors import SourceSpan

class RegisterClass(Enum):
    GENERAL = auto()  # General Purpose Register (GPR)
    FLOAT = auto()    # Floating Point Register (FPR)
    VECTOR = auto()   # SIMD Vector Register
    POINTER = auto()  # Memory Pointer (often maps to GPR, but semantically distinct)

@dataclass(frozen=True)
class MachineRegister:
    id: int
    reg_class: RegisterClass
    is_physical: bool = False
    physical_name: str = "" # E.g., 'rax' or 'x0', populated after physical allocation
    
    def __str__(self):
        if self.is_physical:
            return f"%{self.physical_name}"
        prefix = {
            RegisterClass.GENERAL: "r",
            RegisterClass.FLOAT: "f",
            RegisterClass.VECTOR: "v",
            RegisterClass.POINTER: "p"
        }[self.reg_class]
        return f"%{prefix}{self.id}"

@dataclass(frozen=True)
class MachineStackSlot:
    offset: int
    size: int
    
    def __str__(self):
        return f"[SP + {self.offset}]"

class OperandType(Enum):
    REGISTER = auto()
    IMMEDIATE = auto()
    STACK_SLOT = auto()
    LABEL = auto()
    GLOBAL = auto()

@dataclass(frozen=True)
class MachineOperand:
    type: OperandType
    value: Any # MachineRegister, int, str, MachineStackSlot, etc.
    
    def __str__(self):
        return str(self.value)

@dataclass
class MachineInstruction:
    opcode: str # e.g. "ADD", "LOAD", "STORE", "CALL"
    operands: List[MachineOperand]
    dest: Optional[MachineOperand] = None
    span: Optional[SourceSpan] = None
    
    def __str__(self):
        dest_str = f"{self.dest} = " if self.dest else ""
        ops_str = ", ".join(str(op) for op in self.operands)
        return f"{dest_str}{self.opcode} {ops_str}"

@dataclass
class MachineBasicBlock:
    name: str
    instructions: List[MachineInstruction] = field(default_factory=list)
    predecessors: List['MachineBasicBlock'] = field(default_factory=list)
    successors: List['MachineBasicBlock'] = field(default_factory=list)
    
    def __str__(self):
        res = f"{self.name}:\n"
        for instr in self.instructions:
            res += f"  {instr}\n"
        return res

@dataclass
class MachineFrame:
    """Represents the activation record (stack frame) layout for a function."""
    local_size: int = 0
    spill_size: int = 0
    outgoing_args_size: int = 0
    callee_saved_size: int = 0
    
    @property
    def total_size(self):
        return self.local_size + self.spill_size + self.outgoing_args_size + self.callee_saved_size

@dataclass
class MachineFunction:
    name: str
    blocks: List[MachineBasicBlock] = field(default_factory=list)
    entry_block: Optional[MachineBasicBlock] = None
    frame: MachineFrame = field(default_factory=MachineFrame)
    calling_convention: Any = None # To be populated by CallingConvention
    
    def __str__(self):
        res = f"MachineFunction {self.name}:\n"
        for block in self.blocks:
            res += str(block)
        return res

@dataclass
class MachineModule:
    functions: List[MachineFunction] = field(default_factory=list)
    globals: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self):
        res = "MachineModule:\n"
        for name, val in self.globals.items():
            res += f"  global {name} = {val}\n"
        for func in self.functions:
            res += str(func) + "\n"
        return res
