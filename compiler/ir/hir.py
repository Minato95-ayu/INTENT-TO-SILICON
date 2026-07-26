from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict

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
    args: List[str] = field(default_factory=list)
    decorators: List[Dict[str, Any]] = field(default_factory=list)

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

@dataclass
class HIRLoadConst(HIRNode):
    value: Any

@dataclass
class HIRBinaryOp(HIRNode):
    left: HIRNode
    op: str
    right: HIRNode

@dataclass
class HIRIf(HIRNode):
    condition: HIRNode
    then_branch: List[HIRNode]
    else_branch: List[HIRNode]

@dataclass
class HIRFor(HIRNode):
    iterator: str
    iterable: HIRNode
    body: List[HIRNode]
    index_name: Optional[str] = None

@dataclass
class HIRModelAttribute:
    name: str
    args: List[str]

@dataclass
class HIRModelField:
    name: str
    field_type: str
    attributes: List[HIRModelAttribute]

@dataclass
class HIRModel(HIRNode):
    name: str
    fields: List[HIRModelField]
    decorators: List[dict] = field(default_factory=list)

@dataclass
class HIRMethod:
    method: str
    body: List[HIRNode]

@dataclass
class HIRRoute(HIRNode):
    path: str
    methods: List[HIRMethod]

@dataclass
class HIRReturn(HIRNode):
    value: HIRNode

@dataclass
class HIRTry(HIRNode):
    try_block: list
    catch_var: str
    catch_block: list
    finally_block: list

@dataclass
class HIRThrow(HIRNode):
    value: HIRNode

@dataclass
class HIRRethrow(HIRNode):
    pass

@dataclass
class HIRTheme(HIRNode):
    name: str
    properties: dict

@dataclass
class HIRUseTheme(HIRNode):
    name: str

@dataclass
class HIRNavigate(HIRNode):
    target: str
    kwargs: dict

@dataclass
class HIRDictionary(HIRNode):
    pairs: dict

@dataclass
class HIRSubscript(HIRNode):
    target: HIRNode
    index: HIRNode

@dataclass
class HIRAwait(HIRNode):
    expression: HIRNode

@dataclass
class HIRBind(HIRNode):
    target: str

@dataclass
class HIRValidate(HIRNode):
    fields: list

@dataclass
class HIRAnimate(HIRNode):
    properties: dict

@dataclass
class HIRLifecycle(HIRNode):
    hook: str
    body: List[HIRNode]

@dataclass
class HIRClosure(HIRNode):
    action_name: str
    args: List[HIRNode]

@dataclass
class HIRArrayNode(HIRNode):
    elements: List[HIRNode]

@dataclass
class HIRForNode(HIRNode):
    iterator: str
    iterable: HIRNode
    body: List[HIRNode]
