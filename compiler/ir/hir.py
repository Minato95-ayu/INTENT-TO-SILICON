from dataclasses import dataclass
from typing import Any

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
