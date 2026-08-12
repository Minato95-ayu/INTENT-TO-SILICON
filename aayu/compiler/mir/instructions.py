from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, List, Optional, Union

class Opcode(Enum):
    # Data Flow
    MOVE = auto()
    LOAD_CONST = auto()
    LOAD_GLOBAL = auto()
    STORE_GLOBAL = auto()
    PHI = auto()

    # Arithmetic
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()

    # Logic / Relational
    COMPARE = auto()  # EQ, NEQ, LT, GT, LTE, GTE
    AND = auto()
    OR = auto()
    NOT = auto()

    # Control Flow
    JUMP = auto()
    BRANCH = auto()
    CALL = auto()
    RETURN = auto()

@dataclass
class Register:
    """Virtual Register representation for MIR"""
    id: int
    name: str
    
    def __str__(self):
        return f"%{self.name}_{self.id}"
    
    def __hash__(self):
        return hash(self.id)

@dataclass
class Instruction:
    """Base Three-Address Code Instruction"""
    opcode: Opcode
    dest: Optional[Register]
    args: List[Any]  # Can be Registers, literals, string names, or block ids
    metadata: Any = None

    def __str__(self):
        arg_str = ", ".join(str(a) for a in self.args)
        if self.dest:
            return f"{self.dest} = {self.opcode.name} {arg_str}"
        return f"{self.opcode.name} {arg_str}"
