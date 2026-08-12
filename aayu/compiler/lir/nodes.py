from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Any, Optional, Dict
from aayu.compiler.mir.nodes import RegisterID, OpcodeCategory, OpcodeTraits

class LIROpcode(Enum):
    # Load
    LIR_LOAD_CONST = (auto(), OpcodeCategory.LOAD, OpcodeTraits())
    LIR_LOAD_ENUM_CONST = (auto(), OpcodeCategory.LOAD, OpcodeTraits())
    LIR_LOAD_LOCAL = (auto(), OpcodeCategory.LOAD, OpcodeTraits(reads_memory=True))
    LIR_LOAD_GLOBAL = (auto(), OpcodeCategory.LOAD, OpcodeTraits(reads_memory=True))
    LIR_LOAD_SPILL = (auto(), OpcodeCategory.LOAD, OpcodeTraits(reads_memory=True))
    LIR_LOAD_LOCAL_PTR = (auto(), OpcodeCategory.LOAD, OpcodeTraits())
    LIR_LOAD_GLOBAL_PTR = (auto(), OpcodeCategory.LOAD, OpcodeTraits())
    
    # Store / Move
    LIR_STORE_LOCAL = (auto(), OpcodeCategory.STORE, OpcodeTraits(side_effect=True, writes_memory=True))
    LIR_STORE_GLOBAL = (auto(), OpcodeCategory.STORE, OpcodeTraits(side_effect=True, writes_memory=True))
    LIR_STORE_SPILL = (auto(), OpcodeCategory.STORE, OpcodeTraits(side_effect=True, writes_memory=True))
    LIR_MOVE = (auto(), OpcodeCategory.STORE, OpcodeTraits())
    
    # Arithmetic
    LIR_ADD = (auto(), OpcodeCategory.ARITHMETIC, OpcodeTraits())
    LIR_SUB = (auto(), OpcodeCategory.ARITHMETIC, OpcodeTraits())
    LIR_MUL = (auto(), OpcodeCategory.ARITHMETIC, OpcodeTraits())
    LIR_DIV = (auto(), OpcodeCategory.ARITHMETIC, OpcodeTraits())
    LIR_AND = (auto(), OpcodeCategory.ARITHMETIC, OpcodeTraits())
    LIR_OR = (auto(), OpcodeCategory.ARITHMETIC, OpcodeTraits())
    
    # Compare
    LIR_CMP_EQ = (auto(), OpcodeCategory.COMPARE, OpcodeTraits())
    LIR_CMP_GT = (auto(), OpcodeCategory.COMPARE, OpcodeTraits())
    LIR_CMP_LT = (auto(), OpcodeCategory.COMPARE, OpcodeTraits())
    
    # Branch
    LIR_JUMP = (auto(), OpcodeCategory.BRANCH, OpcodeTraits(side_effect=True, is_terminator=True))
    LIR_BRANCH = (auto(), OpcodeCategory.BRANCH, OpcodeTraits(side_effect=True, is_terminator=True))
    
    # Call
    LIR_CALL = (auto(), OpcodeCategory.CALL, OpcodeTraits(side_effect=True, reads_memory=True, writes_memory=True))
    LIR_RET = (auto(), OpcodeCategory.BRANCH, OpcodeTraits(side_effect=True, is_terminator=True))
    
    # Memory / Struct
    LIR_ALLOC = (auto(), OpcodeCategory.MEMORY, OpcodeTraits(side_effect=True, writes_memory=True))
    LIR_GEP = (auto(), OpcodeCategory.MEMORY, OpcodeTraits())
    LIR_LOAD = (auto(), OpcodeCategory.LOAD, OpcodeTraits(reads_memory=True))
    LIR_STORE = (auto(), OpcodeCategory.STORE, OpcodeTraits(side_effect=True, writes_memory=True))

    @property
    def category(self) -> OpcodeCategory:
        return self.value[1]
        
    @property
    def traits(self) -> OpcodeTraits:
        return self.value[2]

@dataclass
class LIRInstruction:
    opcode: LIROpcode
    operands: List[Any]
    dest: Optional[RegisterID] = None
    from aayu.compiler.errors import SourceSpan
    span: Optional[SourceSpan] = None
    
    def __str__(self):
        dest_str = f"{self.dest} = " if self.dest else ""
        ops_str = ", ".join(str(op) for op in self.operands)
        return f"{dest_str}{self.opcode.name} {ops_str}"

@dataclass
class LIRBlock:
    name: str
    instructions: List[LIRInstruction] = field(default_factory=list)
    predecessors: List['LIRBlock'] = field(default_factory=list)
    successors: List['LIRBlock'] = field(default_factory=list)
    
    def __hash__(self):
        return hash(self.name)
        
    def __str__(self):
        res = f"{self.name}:\n"
        for instr in self.instructions:
            res += f"  {instr}\n"
        return res

@dataclass
class FunctionLIR:
    name: str
    blocks: List[LIRBlock] = field(default_factory=list)
    entry_block: Optional[LIRBlock] = None
    
    # Extra metadata for backend
    locals_count: int = 0
    params_count: int = 0
    analysis: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self):
        res = f"FunctionLIR {self.name}:\n"
        for block in self.blocks:
            res += str(block)
        return res
