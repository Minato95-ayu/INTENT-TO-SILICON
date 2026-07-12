from dataclasses import dataclass
from typing import List, Optional, Any, Dict

@dataclass(frozen=True)
class ASTNode:
    """Base class for all immutable AST nodes."""
    line: int
    column: int

@dataclass(frozen=True)
class ProgramNode(ASTNode):
    statements: List[ASTNode]

@dataclass(frozen=True)
class StateDeclarationNode(ASTNode):
    name: str
    value: ASTNode

@dataclass(frozen=True)
class LiteralNode(ASTNode):
    value: Any

@dataclass(frozen=True)
class IdentifierNode(ASTNode):
    name: str

@dataclass(frozen=True)
class AssignmentNode(ASTNode):
    target: str
    value: ASTNode

@dataclass(frozen=True)
class WidgetNode(ASTNode):
    widget_type: str
    props: Dict[str, Any]
    children: List['WidgetNode']
