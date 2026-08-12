from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Any, Optional, Dict

class OpcodeCategory(Enum):
    LOAD = auto()
    STORE = auto()
    ARITHMETIC = auto()
    LOGICAL = auto()
    COMPARE = auto()
    BRANCH = auto()
    CALL = auto()
    MEMORY = auto()
    PHI = auto()
    DEBUG = auto()

@dataclass(frozen=True)
class OpcodeTraits:
    side_effect: bool = False
    writes_memory: bool = False
    reads_memory: bool = False
    is_terminator: bool = False

class Opcode(Enum):
    # Load
    LOAD_CONST = (auto(), OpcodeCategory.LOAD, OpcodeTraits())
    LOAD_LOCAL = (auto(), OpcodeCategory.LOAD, OpcodeTraits(reads_memory=True))
    LOAD_GLOBAL = (auto(), OpcodeCategory.LOAD, OpcodeTraits(reads_memory=True))
    LOAD_SPILL = (auto(), OpcodeCategory.LOAD, OpcodeTraits(reads_memory=True))
    LOAD_LOCAL_PTR = (auto(), OpcodeCategory.LOAD, OpcodeTraits())
    LOAD_GLOBAL_PTR = (auto(), OpcodeCategory.LOAD, OpcodeTraits())
    
    # Store / Move
    STORE_LOCAL = (auto(), OpcodeCategory.STORE, OpcodeTraits(side_effect=True, writes_memory=True))
    STORE_GLOBAL = (auto(), OpcodeCategory.STORE, OpcodeTraits(side_effect=True, writes_memory=True))
    STORE_SPILL = (auto(), OpcodeCategory.STORE, OpcodeTraits(side_effect=True, writes_memory=True))
    MOVE = (auto(), OpcodeCategory.STORE, OpcodeTraits())
    COPY = (auto(), OpcodeCategory.STORE, OpcodeTraits())
    
    # Arithmetic / Logic
    ADD = (auto(), OpcodeCategory.ARITHMETIC, OpcodeTraits())
    SUB = (auto(), OpcodeCategory.ARITHMETIC, OpcodeTraits())
    MUL = (auto(), OpcodeCategory.ARITHMETIC, OpcodeTraits())
    DIV = (auto(), OpcodeCategory.ARITHMETIC, OpcodeTraits())
    AND = (auto(), OpcodeCategory.ARITHMETIC, OpcodeTraits())
    OR = (auto(), OpcodeCategory.ARITHMETIC, OpcodeTraits())
    
    # Compare
    CMP_EQ = (auto(), OpcodeCategory.COMPARE, OpcodeTraits())
    CMP_GT = (auto(), OpcodeCategory.COMPARE, OpcodeTraits())
    CMP_LT = (auto(), OpcodeCategory.COMPARE, OpcodeTraits())
    
    # Branch
    JUMP = (auto(), OpcodeCategory.BRANCH, OpcodeTraits(side_effect=True, is_terminator=True))
    BRANCH = (auto(), OpcodeCategory.BRANCH, OpcodeTraits(side_effect=True, is_terminator=True))
    
    # Call
    CALL = (auto(), OpcodeCategory.CALL, OpcodeTraits(side_effect=True, reads_memory=True, writes_memory=True))
    RET = (auto(), OpcodeCategory.BRANCH, OpcodeTraits(side_effect=True, is_terminator=True))
    
    # Enum
    LOAD_ENUM_CONST = (auto(), OpcodeCategory.LOAD, OpcodeTraits())
    
    # Phi
    PHI = (auto(), OpcodeCategory.PHI, OpcodeTraits())
    
    # Memory / Struct (as requested: ALLOC, LOAD, STORE, GEP)
    ALLOC = (auto(), OpcodeCategory.MEMORY, OpcodeTraits(side_effect=True, writes_memory=True))
    GEP = (auto(), OpcodeCategory.MEMORY, OpcodeTraits())
    LOAD = (auto(), OpcodeCategory.LOAD, OpcodeTraits(reads_memory=True))
    STORE = (auto(), OpcodeCategory.STORE, OpcodeTraits(side_effect=True, writes_memory=True))

    @property
    def category(self) -> OpcodeCategory:
        return self.value[1]
        
    @property
    def traits(self) -> OpcodeTraits:
        return self.value[2]

@dataclass(frozen=True)
class RegisterID:
    id: int
    
    def __str__(self):
        return f"r{self.id}"

@dataclass
class Metadata:
    from aayu.compiler.errors import SourceSpan
    span: Optional[SourceSpan] = None
    symbol: str = ""
    hints: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Instruction:
    opcode: Opcode
    operands: List[Any]
    dest: Optional[RegisterID] = None
    meta: Optional[Metadata] = None
    index: int = -1

    def __str__(self):
        dest_str = f"{self.dest} = " if self.dest else ""
        ops_str = ", ".join(str(op) for op in self.operands)
        return f"{dest_str}{self.opcode.name.lower()} {ops_str}"

@dataclass
class BasicBlock:
    id: str
    instructions: List[Instruction] = field(default_factory=list)
    predecessors: List['BasicBlock'] = field(default_factory=list)
    successors: List['BasicBlock'] = field(default_factory=list)
    
    def add_instruction(self, instr: Instruction):
        self.instructions.append(instr)
        
    def __str__(self):
        lines = [f"{self.id}:"]
        for instr in self.instructions:
            lines.append(f"  {instr}")
        return "\n".join(lines)

@dataclass
class FunctionMIR:
    name: str
    blocks: List[BasicBlock] = field(default_factory=list)
    
    @property
    def entry_block(self) -> BasicBlock:
        return self.blocks[0] if self.blocks else None

    def __str__(self):
        lines = [f"Function {self.name}:"]
        for block in self.blocks:
            lines.append(str(block))
        return "\n".join(lines)

@dataclass
class MIREnumConstant:
    """
    Metadata attached to LOAD_ENUM_CONST instructions.
    Preserves enum identity through MIR/SSA optimization passes.
    Only lowered to integer at the backend boundary.
    """
    enum_name: str
    variant_name: str
    tag: int
    tag_size: int = 32  # bits

    def __str__(self):
        return f"{self.enum_name}.{self.variant_name} (tag={self.tag})"

@dataclass
class MIREnumDecl:
    """Enum declaration metadata preserved through MIR for debugger/reflection."""
    name: str
    variants: List[str] = field(default_factory=list)
    tags: List[int] = field(default_factory=list)
    tag_size: int = 32

@dataclass
class MIRStructDecl:
    name: str
    fields: List[str] = field(default_factory=list)

@dataclass
class ModuleMIR:
    functions: List[FunctionMIR] = field(default_factory=list)
    enum_decls: List[MIREnumDecl] = field(default_factory=list)
    struct_decls: List[MIRStructDecl] = field(default_factory=list)
