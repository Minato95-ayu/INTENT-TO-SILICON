from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Any

class Opcode(Enum):
    LOAD_CONST = auto()
    LOAD_VAR = auto()
    STORE_VAR = auto()
    
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    
    EQ = auto()
    LT = auto()
    GT = auto()
    
    JUMP = auto()
    JUMP_IF_FALSE = auto()
    CALL = auto()
    RETURN = auto()

@dataclass
class Instruction:
    opcode: Opcode
    operand: int = None
    line: int = None
    file: str = ""
    
    def __repr__(self):
        parts = [self.opcode.name]
        if self.operand is not None:
            parts.append(str(self.operand))
        if self.line is not None:
            parts.append(f"(line {self.line})")
        return " ".join(parts)

@dataclass
class Bytecode:
    instructions: List[Instruction] = field(default_factory=list)
    constants: List[Any] = field(default_factory=list)
    names: List[str] = field(default_factory=list)
    parameters: List[str] = field(default_factory=list)
    name: str = ""
    file: str = ""
    
    def format(self) -> str:
        res = []
        res.append("Constants:")
        for idx, const in enumerate(self.constants):
            # Print strings with quotes to be clear
            if isinstance(const, str):
                res.append(f"{idx} -> \"{const}\"")
            elif isinstance(const, Bytecode):
                res.append(f"{idx} -> <FunctionBytecode {const.name}>")
                child_res = const.format().split("\n")
                for line in child_res:
                    res.append("    " + line)
            else:
                res.append(f"{idx} -> {const}")
                
        res.append("\nNames:")
        for idx, name in enumerate(self.names):
            res.append(f"{idx} -> {name}")
            
        res.append("\nInstructions:")
        for i, inst in enumerate(self.instructions):
            res.append(f"{i:04d}  {inst}")
            
        return "\n".join(res)
