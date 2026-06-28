from dataclasses import dataclass
from typing import List, Union

@dataclass
class Node:
    pass

@dataclass
class FunctionDeclNode(Node):
    name: str
    parameters: List[str]
    body: List[Node]

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

@dataclass
class RelationDefNode(Node):
    def __init__(self, entity1: str, rel_type: str, entity2: str):
        self.entity1 = entity1
        self.rel_type = rel_type
        self.entity2 = entity2

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
