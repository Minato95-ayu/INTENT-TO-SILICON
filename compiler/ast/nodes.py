from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

@dataclass
class SourceSpan:
    start_line: int
    start_col: int
    end_line: int
    end_col: int
    file: str = ""

@dataclass(frozen=True)
class ASTNode:
    """Base class for all immutable AST nodes."""
    line: int
    column: int
    span: Optional[SourceSpan] = field(default=None, kw_only=True)

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


@dataclass(frozen=True)
class ImportNode(ASTNode):
    module: str

@dataclass(frozen=True)
class ActionDeclarationNode(ASTNode):
    name: str
    statements: List[ASTNode]

@dataclass(frozen=True)
class ActionCallNode(ASTNode):
    name: str
    args: List[ASTNode]

@dataclass(frozen=True)
class AppDeclarationNode(ASTNode):
    """Declares the application name. E.g., 'app MyApp'"""
    name: str

@dataclass(frozen=True)
class RunNode(ASTNode):
    """Marks the entry point. E.g., 'run'"""
    pass

@dataclass(frozen=True)
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode
    def __post_init__(self):
        super().__init__(self.line, self.column)
