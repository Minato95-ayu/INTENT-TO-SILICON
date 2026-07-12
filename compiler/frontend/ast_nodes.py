"""
===============================================================================
AAYU Compiler - Abstract Syntax Tree (AST) Nodes

Purpose:
    Ye file mein wo classes hain jo code ke structure ko Memory me save karti hain (Nodes).

Input:
    None (Ye sirf Data Structures hain)

Output:
    AST Objects used by Parser

Pipeline:
    Parser
        ↓
    AST      ← (Current File)
        ↓
    Semantic Analysis
        ↓
    Compiler

Ye file kyun important hai?
    Poore Compiler aur BrainOS ko yahi nodes padh kar samajh aata hai ki code me kya likha hai. Jaise ek VariableNode ka naam aur value kya hai.

Difficulty:
    ⭐ (Easy)

Recommended Reading Order:
    2. parser.py
    3. ast_nodes.py (You are here)
    4. passes/semantic/type_checker.py
===============================================================================
"""
from dataclasses import dataclass, field
from typing import List, Union, Any, Optional, Dict

from compiler.frontend.location import SourceSpan

@dataclass
class Node:
    span: SourceSpan = field(default=None, kw_only=True)
    resolved_type: Any = field(default=None, kw_only=True)  # Phase 5.3 - Evaluated semantic type

@dataclass
class FunctionDeclNode(Node):
    name: str
    parameters: List[Any]  # Can be just `str` or `(str, TypeNode)` for typed params
    body: List[Node]
    is_exported: bool = False
    visibility: str = "private"
    symbol: Any = None
    return_type: Any = None  # TypeNode
    type_parameters: List[str] = field(default_factory=list)


@dataclass
class BlockNode(Node):
    statements: List[Node]

@dataclass
class ProgramNode(Node):
    statements: List[Node]

@dataclass
class NumberNode(Node):
    value: float

@dataclass
class TextNode(Node):
    value: str

@dataclass
class VariableNode(Node):
    name: str
    symbol: Any = None



@dataclass
class LogicalExpressionNode(Node):
    left: Node
    operator: str
    right: Node

@dataclass
class UnaryExpressionNode(Node):
    operator: str
    right: Node

@dataclass
class BinaryExpressionNode(Node):
    left: Node
    operator: str
    right: Node

@dataclass
class DeclarationNode(Node):
    var_type: str
    name: str
    value: Node
    is_exported: bool = False
    visibility: str = "private"
    symbol: Any = None
    type_annotation: Any = None  # TypeNode

@dataclass
class ShowNode(Node):
    expression: Node

@dataclass
class IfNode(Node):
    condition: Node
    body: List[Node]
    else_body: List[Node] = None

@dataclass
class WhileNode(Node):
    condition: Node
    body: List[Node]

@dataclass
class TryCatchNode(Node):
    try_body: List[Node]
    catch_body: List[Node]

@dataclass
class RepeatNode(Node):
    count: Node
    body: List[Node]

@dataclass
class ForEachNode(Node):
    iterator: str
    collection: Node
    body: List[Node]

@dataclass
class ForRangeNode(Node):
    iterator: str
    start: Node
    end: Node
    body: List[Node]


@dataclass
class TaskNode(Node):
    name: str
    parameters: List[str]  # Future proofing for Sprint A-5
    body: List[Node]
    visibility: str = "private"
    symbol: Any = None

@dataclass
class RunNode(Node):
    name: str
    arguments: List[Node]
    module_name: str = None

@dataclass
class ExportNode(Node):
    declaration: Node

@dataclass
class ListDeclarationNode(Node):
    name: str
    elements: List[Node]

@dataclass
class ListInitializationNode(Node):
    name: str
    value: Node

@dataclass
class ReturnNode(Node):
    value: Node

@dataclass
class UseNode(Node):
    module: str

@dataclass
class RecordDeclarationNode(Node):
    name: str
    fields: List[str]
    type_parameters: List[str] = field(default_factory=list)

@dataclass
class InstanceDeclarationNode(Node):
    type_name: str
    name: str
    properties: dict

@dataclass
class PropertyAccessNode(Node):
    property_name: str
    object_expr: Node

@dataclass
class ProjectDefNode(Node):
    name: str

@dataclass
class PageDefNode(Node):
    name: str
    children: list = None

@dataclass
class TitleDefNode(Node):
    text: str

@dataclass
class ButtonDefNode(Node):
    text: str

@dataclass
class UIServeNode(Node):
    pass

@dataclass
class ThemeNode(Node):
    name: str
    properties: list = None

@dataclass
class StateDefNode(Node):
    name: str
    initial_value: Node

@dataclass
class RouteDefNode(Node):
    path: str
    target_page: str

@dataclass
class EventNode(Node):
    event_type: str
    action_block: Node

@dataclass
class LayoutNode(Node):
    layout_type: str
    properties: list = None
    children: list = None

@dataclass
class ComponentNode(Node):
    component_type: str
    properties: list = None
    children: list = None

@dataclass
class InterfaceMethodNode(Node):
    name: str
    parameters: List[tuple] # (name: str, type: TypeNode)
    return_type: Node = None # TypeNode

@dataclass
class InterfaceDeclNode(Node):
    name: str
    methods: List[InterfaceMethodNode]
    is_exported: bool = False
    visibility: str = "private"
    symbol: Any = None
    type_parameters: List[str] = field(default_factory=list)

@dataclass
class ExtensionDeclNode(Node):
    target_type: str
    interface_name: Any # Optional[str] but keeping Any for simplicity or str with None
    methods: List[TaskNode] # We use TaskNode for methods
    symbol: Any = None
    type_parameters: List[str] = field(default_factory=list)

@dataclass
class AssignmentNode(Node):
    target: Node
    value: Node

@dataclass
class ReadExpressionNode(Node):
    file_path: Node

@dataclass
class WriteStatementNode(Node):
    data: Node
    destination: Node


@dataclass
class AddToListNode(Node):
    item: Node
    list_name: str

@dataclass
class MapDeclarationNode(Node):
    name: str

@dataclass
class SetInMapNode(Node):
    key: Node
    value: Node
    map_name: str

@dataclass
class GetFromMapNode(Node):
    key: Node
    map_name: str

@dataclass
class BuiltinFunctionNode(Node):
    name: str
    arguments: List[Node]


@dataclass
class ServeNode(Node):
    port: Node
    handler_name: str = None

@dataclass
class RouteNode(Node):
    path: Node
    handler_name: str
    method: str = "GET"

@dataclass
class RenderExpressionNode(Node):
    template_path: Node
    context_map_name: str = None

@dataclass
class FormGetNode(Node):
    key: Node
    req_name: str

@dataclass
class JsonSerializeNode(Node):
    data: Node

@dataclass
class EntityDeclarationNode(Node):
    name: str
    fields: List[str]

@dataclass
class CreateEntityNode(Node):
    entity_name: str
    data_map: str

@dataclass
class FindEntityNode(Node):
    entity_name: str
    condition_field: str = None
    condition_value: Node = None

class MethodCallNode(Node):
    def __init__(self, object_node: Node, method_name: str, arguments: List[Node]):
        self.object_node = object_node
        self.method_name = method_name
        self.arguments = arguments

@dataclass
class RelationDefNode(Node):
    def __init__(self, entity1: str, rel_type: str, entity2: str):
        self.entity1 = entity1
        self.rel_type = rel_type
        self.entity2 = entity2

class ListLiteralNode(Node):
    def __init__(self, elements: List[Node]):
        self.elements = elements

class MapLiteralNode(Node):
    def __init__(self, elements: list):
        self.elements = elements



@dataclass
class ModuleDeclarationNode(Node):
    name: str

@dataclass
class ImportNode(Node):
    module_name: str
    alias: Optional[str] = None
    selective_imports: Optional[Dict[str, Optional[str]]] = None

@dataclass
class ExportListNode(Node):
    symbols: List[str]

# Phase 4.1 - Exception System Nodes
@dataclass
class ThrowNode(Node):
    expression: Node

@dataclass
class PanicNode(Node):
    message: Node

@dataclass
class CatchNode(Node):
    binding: str
    block: List[Node]
    symbol: Optional['Symbol'] = None # Local symbol for the binding

@dataclass
class FinallyNode(Node):
    block: List[Node]

@dataclass
class TryNode(Node):
    try_block: List[Node]
    catch_node: Optional[CatchNode]
    finally_node: Optional[FinallyNode]

@dataclass
class AssertNode(Node):
    condition: Node

@dataclass
class CreateRelationNode(Node):
    def __init__(self, entity1: str, rel_type: str, entity2: str):
        self.entity1 = entity1
        self.rel_type = rel_type
        self.entity2 = entity2

@dataclass
class RoleDefNode(Node):
    name: str

@dataclass
class AllowDefNode(Node):
    role: str
    action: str
    target_entity: str

@dataclass
class StepDefNode(Node):
    name: str
    requires_role: str = None
    after_step: str = None

@dataclass
class WorkflowDefNode(Node):
    name: str
    entity_name: str
    steps: list[StepDefNode]

@dataclass
class UpdateEntityNode(Node):
    entity_name: str
    condition_field: str
    condition_value: Node
    data_map: str

@dataclass
class DeleteEntityNode(Node):
    entity_name: str
    condition_field: str
    condition_value: Node

@dataclass
class TestNode(Node):
    name: str
    body: List[Node]

@dataclass
class ExpectNode(Node):
    actual: Node
    expected: Node
    operator: str

@dataclass
class CreateAccountNode(Node):
    data_map_name: str

@dataclass
class LoginNode(Node):
    user_map_name: str

@dataclass
class LogoutNode(Node):
    req_name: str

@dataclass
class GuardSessionNode(Node):
    pass

@dataclass
class UIPageNode(Node):
    name: str
    elements: List[Node]

@dataclass
class UIComponentNode(Node):
    name: str
    elements: List[Node]

@dataclass
class UIElementNode(Node):
    element_type: str
    value: Node = None
    children: List[Node] = None

@dataclass
class CrudNode(Node):
    entity_name: str

# --- Phase 2: Full-Stack Framework Nodes ---

@dataclass
class StorageNode(Node):
    name: str

@dataclass
class ModelFieldNode(Node):
    name: str
    field_type: str

@dataclass
class ModelNode(Node):
    name: str
    fields: List[ModelFieldNode]

@dataclass
class EndpointNode(Node):
    method: str
    path: str
    returns: str = None
    action_block: Node = None

@dataclass
class ServiceNode(Node):
    name: str
    endpoints: List[EndpointNode]

@dataclass
class SecurityNode(Node):
    features: List[str]

# --- Database/Storage AST Nodes (Phase C) ---

@dataclass
class InsertNode(Node):
    model_name: str
    fields: Dict[str, Node]

@dataclass
class FindNode(Node):
    model_name: str

@dataclass
class UpdateNode(Node):
    model_name: str
    fields: Dict[str, Node]

@dataclass
class DeleteNode(Node):
    model_name: str

@dataclass
class WhereNode(Node):
    condition: Node

@dataclass
class OrderNode(Node):
    field_name: str
    direction: str = 'ASC'

@dataclass
class LimitNode(Node):
    count: int

@dataclass
class OffsetNode(Node):
    count: int
