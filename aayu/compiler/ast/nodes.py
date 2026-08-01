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
class PropDeclarationNode(ASTNode):
    name: str

@dataclass(frozen=True)
class RouteDeclarationNode(ASTNode):
    name: str
    value: ASTNode

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
class ListAccessNode(ASTNode):
    target: ASTNode
    index: ASTNode

@dataclass(frozen=True)
class ArrayNode(ASTNode):
    elements: List[ASTNode]



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
class DecoratorNode(ASTNode):
    name: str
    args: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class ActionDeclarationNode(ASTNode):
    name: str
    statements: List[ASTNode]
    args: List[str] = field(default_factory=list)
    decorators: List[DecoratorNode] = field(default_factory=list)

@dataclass(frozen=True)
class ActionCallNode(ASTNode):
    name: str
    args: List[ASTNode]

@dataclass(frozen=True)
class IfNode(ASTNode):
    condition: ASTNode
    then_branch: List[ASTNode]
    else_branch: Optional[List[ASTNode]] = None

@dataclass(frozen=True)
class WhileNode(ASTNode):
    line: int
    column: int
    condition: ASTNode
    body: List[ASTNode]

@dataclass(frozen=True)
class ForNode(ASTNode):
    iterator: str
    iterable: ASTNode
    body: List[ASTNode]
    index_name: Optional[str] = None

@dataclass(frozen=True)
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass(frozen=True)
class AppDeclarationNode(ASTNode):
    """Declares the application name. E.g., 'app MyApp'"""
    name: str

@dataclass(frozen=True)
class RunNode(ASTNode):
    """Marks the entry point. E.g., 'run'"""
    pass

@dataclass(frozen=True)
class ModelAttributeNode(ASTNode):
    name: str
    args: List[str]

@dataclass(frozen=True)
class ModelFieldNode(ASTNode):
    name: str
    field_type: str
    attributes: List[ModelAttributeNode]

@dataclass(frozen=True)
class ModelDeclNode(ASTNode):
    name: str
    fields: List[ModelFieldNode]
    decorators: List[dict] = field(default_factory=list)

@dataclass(frozen=True)
class MethodNode(ASTNode):
    method: str
    body: List[ASTNode]

@dataclass(frozen=True)
class RouteNode(ASTNode):
    path: str
    methods: List[MethodNode]

@dataclass(frozen=True)
class ReturnNode(ASTNode):
    value: ASTNode

@dataclass(frozen=True)
class TryNode(ASTNode):
    try_block: List[ASTNode]
    catch_var: str
    catch_block: List[ASTNode]
    finally_block: List[ASTNode]

@dataclass(frozen=True)
class ThrowNode(ASTNode):
    value: ASTNode

@dataclass(frozen=True)
class RethrowNode(ASTNode):
    pass

@dataclass(frozen=True)
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode
    def __post_init__(self):
        super().__init__(self.line, self.column)

@dataclass(frozen=True)
class UnaryOpNode(ASTNode):
    operator: str
    right: ASTNode
    def __post_init__(self):
        super().__init__(self.line, self.column)

@dataclass(frozen=True)
class ThemeNode(ASTNode):
    """Declares a theme and its properties. E.g., 'theme Dark ... end'"""
    name: str
    properties: dict = field(default_factory=dict)
    
@dataclass(frozen=True)
class UseThemeNode(ASTNode):
    """Declares the default theme to use. E.g., 'useTheme Dark'"""
    name: str

@dataclass(frozen=True)
class NavigateNode(ASTNode):
    """Navigation command. E.g., 'navigate Profile(id=15)'"""
    target: str
    kwargs: dict = field(default_factory=dict)

@dataclass(frozen=True)
class DictionaryNode(ASTNode):
    pairs: Dict[str, ASTNode]

@dataclass(frozen=True)
class SubscriptNode(ASTNode):
    target: ASTNode
    index: ASTNode

@dataclass(frozen=True)
class AwaitNode(ASTNode):
    expression: ASTNode

@dataclass(frozen=True)
class BindNode(ASTNode):
    target: str

@dataclass(frozen=True)
class ValidationRuleNode(ASTNode):
    rule: str
    args: List[ASTNode] = field(default_factory=list)

@dataclass(frozen=True)
class ValidateFieldNode(ASTNode):
    field_name: str
    rules: List[ValidationRuleNode]

@dataclass(frozen=True)
class ValidateNode(ASTNode):
    fields: List[ValidateFieldNode]

@dataclass(frozen=True)
class AnimateNode(ASTNode):
    properties: Dict[str, Any]

@dataclass(frozen=True)
class LifecycleNode(ASTNode):
    hook: str
    body: List[ASTNode]
