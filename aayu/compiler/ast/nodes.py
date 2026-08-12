from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

from aayu.compiler.errors import SourceSpan

import itertools

_global_node_counter = itertools.count(1)

def reset_node_counter():
    global _global_node_counter
    _global_node_counter = itertools.count(1)

@dataclass(frozen=True)
class ASTNode:
    """Base class for all immutable AST nodes."""
    node_id: int = field(init=False)
    line: int
    column: int
    span: Optional[SourceSpan] = field(default=None, kw_only=True)
    
    def __post_init__(self):
        # Deterministic integer ID for Semantic Context mappings
        object.__setattr__(self, 'node_id', next(_global_node_counter))


# Type System AST Nodes
class TypeNode(ASTNode):
    pass

@dataclass(frozen=True)
class PrimitiveTypeNode(TypeNode):
    name: str

@dataclass(frozen=True)
class NullableTypeNode(TypeNode):
    inner: TypeNode

@dataclass(frozen=True)
class OptionalTypeNode(TypeNode):
    inner: TypeNode

@dataclass(frozen=True)
class UnionTypeNode(TypeNode):
    types: List[TypeNode]

@dataclass(frozen=True)
class EnumDeclarationNode(ASTNode):
    name: str
    variants: List[str]

@dataclass(frozen=True)
class EnumAccessNode(ASTNode):
    enum_name: str
    variant: str

@dataclass(frozen=True)
class StructFieldNode(ASTNode):
    name: str
    field_type: TypeNode

@dataclass(frozen=True)
class StructDeclNode(ASTNode):
    name: str
    fields: List[StructFieldNode]

@dataclass(frozen=True)
class StructInitNode(ASTNode):
    struct_name: str
    args: Dict[str, ASTNode]

@dataclass(frozen=True)
class ProgramNode(ASTNode):
    statements: List[ASTNode]
    
@dataclass(frozen=True)
class ProjectNode(ASTNode):
    """
    Root node for a multi-file project.
    Maps absolute module IDs (e.g., 'core.math', 'auth') to their ProgramNodes.
    """
    modules: Dict[str, ProgramNode]

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
    declared_type: Optional[TypeNode] = None

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
    target: ASTNode
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
class ArgNode(ASTNode):
    name: str
    arg_type: Optional[TypeNode] = None

@dataclass(frozen=True)
class ActionDeclarationNode(ASTNode):
    name: str
    statements: List[ASTNode]
    args: List[ArgNode] = field(default_factory=list)
    return_type: Optional[TypeNode] = None
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
class BreakNode(ASTNode):
    pass

@dataclass(frozen=True)
class ContinueNode(ASTNode):
    pass

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
    field_type: TypeNode
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
        super().__post_init__()

@dataclass(frozen=True)
class UnaryOpNode(ASTNode):
    operator: str
    right: ASTNode
    def __post_init__(self):
        super().__post_init__()

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
