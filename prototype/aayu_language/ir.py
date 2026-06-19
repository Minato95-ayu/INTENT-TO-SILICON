from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Any

class Opcode(Enum):
    # Stack and Memory
    LOAD_CONST = auto()
    LOAD_NAME = auto()
    STORE_NAME = auto()
    POP = auto()
    
    # Arithmetic and Logic
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    EQUAL = auto()
    GREATER = auto()
    LESS = auto()
    NOT = auto()
    
    # Control Flow
    JUMP_FORWARD = auto()
    JUMP_IF_FALSE = auto()
    JUMP_BACKWARD = auto()
    
    # Special Features
    PRINT = auto()
    BUILD_LIST = auto()
    CALL_TASK = auto()
    RETURN = auto()

@dataclass
class Instruction:
    opcode: Opcode
    operand: int = None
    
    def __repr__(self):
        if self.operand is not None:
            return f"{self.opcode.name} {self.operand}"
        return self.opcode.name

@dataclass
class Bytecode:
    instructions: List[Instruction] = field(default_factory=list)
    constants: List[Any] = field(default_factory=list)
    names: List[str] = field(default_factory=list)
    
    def format(self) -> str:
        res = []
        res.append("Constants:")
        for idx, const in enumerate(self.constants):
            # Print strings with quotes to be clear
            if isinstance(const, str):
                res.append(f"{idx} -> \"{const}\"")
            else:
                res.append(f"{idx} -> {const}")
                
        res.append("\nNames:")
        for idx, name in enumerate(self.names):
            res.append(f"{idx} -> {name}")
            
        res.append("\nInstructions:")
        for i, inst in enumerate(self.instructions):
            res.append(f"{i:04d}  {inst}")
            
        return "\n".join(res)
