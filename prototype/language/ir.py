from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Any, Dict
from location import SourceSpan, SourceFile

class Opcode(Enum):
    LOAD_CONST = auto()
    LOAD_VAR = auto()
    STORE_VAR = auto()
    
    # Arithmetic
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    NEG = auto()
    
    # Relational
    EQ = auto()
    NE = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    
    # Logical
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Collections
    MAKE_LIST = auto()
    MAKE_MAP = auto()
    LIST_APPEND = auto()
    MAP_SET = auto()
    MAP_GET = auto()
    
    # Control Flow & Functions
    JUMP = auto()
    JUMP_IF_FALSE = auto()
    JUMP_IF_TRUE = auto()
    JUMP_BACKWARD = auto()
    CALL = auto()
    CALL_TASK = auto()
    RETURN = auto()
    POP = auto()

    # Exception Handling (Phase 4.1)
    THROW = auto()
    PANIC = auto()
    TRY_BEGIN = auto()    # operand: index into exception_table
    TRY_END = auto()
    FINALLY_BEGIN = auto()
    FINALLY_END = auto()

@dataclass
class Instruction:
    opcode: Opcode
    operand: int = None
    
    def __repr__(self):
        parts = [self.opcode.name]
        if self.operand is not None:
            parts.append(str(self.operand))
        return " ".join(parts)

@dataclass
class FunctionInfo:
    id: int
    name: str
    module: str
    entry_ip: int
    exit_ip: int

@dataclass
class InstructionRange:
    start_ip: int
    end_ip: int
    span: SourceSpan

@dataclass
class DebugInfo:
    line_table: List[InstructionRange] = field(default_factory=list)
    function_table: List[FunctionInfo] = field(default_factory=list)
    module_table: List[str] = field(default_factory=list)
    source_files: Dict[int, SourceFile] = field(default_factory=dict)
    
@dataclass
class ReflectionInfo:
    name: str = ""
    module: str = ""
    visibility: str = "private"
    is_exported: bool = False
    parameter_count: int = 0
    attributes: List[str] = field(default_factory=list)
    annotations: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Bytecode:
    instructions: List[Instruction] = field(default_factory=list)
    constants: List[Any] = field(default_factory=list)
    names: List[str] = field(default_factory=list)
    parameters: List[str] = field(default_factory=list)
    name: str = ""
    file: str = ""
    exception_table: List[dict] = field(default_factory=list)
    debug_info: DebugInfo = field(default_factory=DebugInfo)
    reflection_info: ReflectionInfo = field(default_factory=ReflectionInfo)
    
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
