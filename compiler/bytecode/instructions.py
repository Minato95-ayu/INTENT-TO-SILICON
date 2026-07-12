from dataclasses import dataclass
from typing import Any, List

@dataclass
class Instruction:
    opcode: str
    arg1: Any = None
    arg2: Any = None
    
    def serialize(self):
        return (self.opcode, self.arg1, self.arg2)

@dataclass
class BytecodeObject:
    instructions: List[Instruction]
    constants: List[Any]
