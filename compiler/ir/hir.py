from dataclasses import dataclass
from typing import Any, List

@dataclass
class HIRNode:
    """High-level Intermediate Representation. Closely maps to semantic tree but flattens blocks."""
    pass

@dataclass
class HIRStateDecl(HIRNode):
    name: str
    value: Any

@dataclass
class HIRAssignment(HIRNode):
    target: str
    value: Any

@dataclass
class HIRWidget(HIRNode):
    w_type: str
    props: dict
    children: list

@dataclass
class HIRActionDecl(HIRNode):
    name: str
    body: List[HIRNode]

@dataclass
class HIRActionCall(HIRNode):
    name: str
    args: list

@dataclass
class HIRLoadVar(HIRNode):
    name: str

@dataclass
class HIRPrint(HIRNode):
    value: Any

@dataclass
class HIRImport(HIRNode):
    module: str
