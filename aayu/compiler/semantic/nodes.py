from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from aayu.compiler.semantic.symbols import SymbolTable

@dataclass
class SemanticNode:
    line: int
    column: int
    scope: SymbolTable

@dataclass
class SemanticProgramNode(SemanticNode):
    statements: List[SemanticNode]

@dataclass
class SemanticPropDeclNode(SemanticNode):
    name: str

@dataclass
class SemanticStateDeclNode(SemanticNode):
    name: str
    value: SemanticNode

@dataclass
class SemanticLiteralNode(SemanticNode):
    value: Any
    type_name: str

@dataclass
class SemanticListAccessNode(SemanticNode):
    target: SemanticNode
    index: SemanticNode

@dataclass
class SemanticArrayNode(SemanticNode):
    elements: List[SemanticNode]

@dataclass
class SemanticForNode(SemanticNode):
    iterator: str
    iterable: SemanticNode
    body: List[SemanticNode]
    index_name: Optional[str] = None

@dataclass
class SemanticAssignmentNode(SemanticNode):
    target: str
    value: SemanticNode

@dataclass
class SemanticWidgetNode(SemanticNode):
    widget_type: str
    props: Dict[str, Any]
    children: List['SemanticWidgetNode']


@dataclass
class SemanticImportNode(SemanticNode):
    module: str

@dataclass
class SemanticIdentifierNode(SemanticNode):
    name: str

@dataclass
class SemanticDecoratorNode:
    name: str
    args: List[str]

@dataclass
class SemanticActionDeclNode(SemanticNode):
    name: str
    statements: List[SemanticNode]
    args: List[str] = field(default_factory=list)
    decorators: List[SemanticDecoratorNode] = field(default_factory=list)

@dataclass
class SemanticActionCallNode(SemanticNode):
    name: str
    args: List[SemanticNode]

@dataclass
class SemanticBinaryOpNode(SemanticNode):
    left: SemanticNode
    op: str
    right: SemanticNode

@dataclass
class SemanticIfNode(SemanticNode):
    condition: SemanticNode
    then_branch: List[SemanticNode]
    else_branch: Optional[List[SemanticNode]]

@dataclass
class SemanticWhileNode(SemanticNode):
    condition: SemanticNode
    body: List[SemanticNode]

@dataclass
class SemanticForNode(SemanticNode):
    iterator: str
    iterable: SemanticNode
    body: List[SemanticNode]
    index_name: Optional[str] = None

@dataclass
class SemanticModelAttributeNode:
    name: str
    args: List[str]

@dataclass
class SemanticModelFieldNode:
    name: str
    field_type: str
    attributes: List[SemanticModelAttributeNode]

@dataclass
class SemanticModelDeclNode(SemanticNode):
    name: str
    fields: List[SemanticModelFieldNode]
    decorators: List[dict] = field(default_factory=list)

@dataclass
class SemanticMethodNode(SemanticNode):
    method: str
    body: List[SemanticNode]

@dataclass
class SemanticRouteNode(SemanticNode):
    path: str
    methods: List[SemanticMethodNode]

@dataclass
class SemanticReturnNode(SemanticNode):
    value: SemanticNode

@dataclass
class SemanticTryNode(SemanticNode):
    try_block: List[SemanticNode]
    catch_var: str
    catch_block: List[SemanticNode]
    finally_block: List[SemanticNode]

@dataclass
class SemanticThrowNode(SemanticNode):
    value: SemanticNode

@dataclass
class SemanticRethrowNode(SemanticNode):
    pass

@dataclass
class SemanticThemeNode(SemanticNode):
    name: str
    properties: Dict[str, any]
    
@dataclass
class SemanticUseThemeNode(SemanticNode):
    name: str

@dataclass
class SemanticNavigateNode(SemanticNode):
    target: str
    kwargs: Dict[str, SemanticNode]


@dataclass
class SemanticDictionaryNode(SemanticNode):
    pairs: Dict[str, SemanticNode]

@dataclass
class SemanticSubscriptNode(SemanticNode):
    target: SemanticNode
    index: SemanticNode

@dataclass
class SemanticAwaitNode(SemanticNode):
    expression: SemanticNode

@dataclass
class SemanticBindNode(SemanticNode):
    target: str

@dataclass
class SemanticValidationRuleNode:
    rule: str
    args: List[SemanticNode]

@dataclass
class SemanticValidateFieldNode:
    field_name: str
    rules: List[SemanticValidationRuleNode]

@dataclass
class SemanticValidateNode(SemanticNode):
    fields: List[SemanticValidateFieldNode]

@dataclass
class SemanticAnimateNode(SemanticNode):
    properties: Dict[str, SemanticNode]

@dataclass
class SemanticLifecycleNode(SemanticNode):
    hook: str
    body: List[SemanticNode]

@dataclass
class SemanticClosureNode(SemanticNode):
    action_name: str
    args: List[SemanticNode]
