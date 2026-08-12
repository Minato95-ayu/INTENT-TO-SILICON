import itertools
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from aayu.compiler.semantic.context import TypeID
from aayu.compiler.semantic.types import FieldID, VariantID

# Global deterministic counter for HIR node IDs
_global_hir_counter = itertools.count(1)

@dataclass(frozen=True, kw_only=True)
class HIRNode:
    """
    Base class for all High-Level Intermediate Representation nodes.
    Strictly follows HIR-3 Architecture Phase specifications.
    """
    hir_node_id: int = field(default_factory=lambda: next(_global_hir_counter))
    origin_node_id: int  # Must link back to the exact AST node ID
    module_id: str = "local"
    flags: int = 0

@dataclass(frozen=True, kw_only=True)
class HIRExpr(HIRNode):
    """Base for expressions that yield a value."""
    type_id: TypeID

@dataclass(frozen=True, kw_only=True)
class HIRLiteral(HIRExpr):
    value: Any

@dataclass(frozen=True, kw_only=True)
class HIRNullLiteral(HIRExpr):
    pass

@dataclass(frozen=True, kw_only=True)
class HIRVariable(HIRExpr):
    """Represents a local or global variable access."""
    name: str
    symbol_id: int = 0  # To be populated by symbol registry
    is_global: bool = False

@dataclass(frozen=True, kw_only=True)
class HIRBinaryOp(HIRExpr):
    operator: str
    left: HIRExpr
    right: HIRExpr

@dataclass(frozen=True, kw_only=True)
class HIRUnaryOp(HIRExpr):
    operator: str
    operand: HIRExpr

@dataclass(frozen=True, kw_only=True)
class HIRCall(HIRExpr):
    target_symbol_id: int
    args: List[HIRExpr]

@dataclass(frozen=True, kw_only=True)
class HIRAssignment(HIRNode):
    target: HIRExpr
    value: HIRExpr

@dataclass(frozen=True, kw_only=True)
class HIRBlock(HIRNode):
    """
    Represents a scope, a collection of statements, and a control flow boundary.
    """
    statements: List[HIRNode]

@dataclass(frozen=True, kw_only=True)
class HIRIf(HIRNode):
    condition: HIRExpr
    then_branch: HIRBlock
    else_branch: Optional[HIRBlock] = None

@dataclass(frozen=True, kw_only=True)
class HIRLoop(HIRNode):
    condition: HIRExpr
    body: HIRBlock

@dataclass(frozen=True, kw_only=True)
class HIRBreak(HIRNode):
    pass

@dataclass(frozen=True, kw_only=True)
class HIRContinue(HIRNode):
    pass

@dataclass(frozen=True, kw_only=True)
class HIRFunctionDecl(HIRNode):
    name: str
    symbol_id: int
    body: HIRBlock
    effect: str = "Pure"

@dataclass(frozen=True, kw_only=True)
class HIRActionDecl(HIRNode):
    name: str
    symbol_id: int
    body: HIRBlock
    effect: str = "StateMutation"

@dataclass(frozen=True, kw_only=True)
class HIRReturn(HIRNode):
    value: Optional[HIRExpr] = None

# --- Enum IR Nodes ---

@dataclass(frozen=True, kw_only=True)
class HIREnumValue(HIRExpr):
    """
    Represents accessing a specific enum variant (e.g., Color.Red).
    """
    enum_type_id: TypeID
    variant_id: VariantID
    result_type_id: TypeID

@dataclass(frozen=True, kw_only=True)
class HIREnumFieldAccess(HIRExpr):
    """Future payload support for Enums."""
    target: HIRExpr
    enum_type_id: TypeID
    variant_id: VariantID
    result_type_id: TypeID

# --- Struct IR Nodes ---

@dataclass(frozen=True, kw_only=True)
class HIRStructInit(HIRExpr):
    struct_type_id: TypeID
    args: List[HIRExpr] # Ordered by Canonical Field Identity

@dataclass(frozen=True, kw_only=True)
class HIRStructFieldAccess(HIRExpr):
    target: HIRExpr
    struct_type_id: TypeID
    field_id: FieldID
    result_type_id: TypeID

@dataclass(frozen=True, kw_only=True)
class HIRModule(HIRNode):
    globals: List[HIRAssignment]
    actions: List[HIRActionDecl]
    functions: List[HIRFunctionDecl] = field(default_factory=list)
