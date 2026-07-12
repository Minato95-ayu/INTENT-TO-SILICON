from dataclasses import dataclass
from typing import List, Optional, Any, Dict
from compiler.semantic.symbols import SymbolTable

@dataclass(frozen=True)
class SemanticNode:
    line: int
    column: int
    scope: SymbolTable

@dataclass(frozen=True)
class SemanticProgramNode(SemanticNode):
    statements: List[SemanticNode]

@dataclass(frozen=True)
class SemanticStateDeclNode(SemanticNode):
    name: str
    value: SemanticNode

@dataclass(frozen=True)
class SemanticLiteralNode(SemanticNode):
    value: Any
    type_name: str

@dataclass(frozen=True)
class SemanticAssignmentNode(SemanticNode):
    target: str
    value: SemanticNode

@dataclass(frozen=True)
class SemanticWidgetNode(SemanticNode):
    widget_type: str
    props: Dict[str, Any]
    children: List['SemanticWidgetNode']
