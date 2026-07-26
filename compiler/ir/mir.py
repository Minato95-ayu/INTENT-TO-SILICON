from dataclasses import dataclass
from typing import Any, List

@dataclass
class MIRNode:
    """Middle-level Intermediate Representation. Control flow is flattened into basic blocks."""
    pass

@dataclass
class MIRInstruction(MIRNode):
    opcode: str
    operands: List[Any]

@dataclass
class MIRCreateArray(MIRNode):
    elements: List[MIRNode]

@dataclass
class MIRLoop(MIRNode):
    iterator: str
    iterable: MIRNode
    body: List[MIRNode]
