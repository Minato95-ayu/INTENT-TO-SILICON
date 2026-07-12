from dataclasses import dataclass
from typing import Any, List

@dataclass
class LIRNode:
    """Low-level Intermediate Representation. Maps almost 1:1 with Bytecode instructions."""
    opcode: str
    operands: List[Any]
