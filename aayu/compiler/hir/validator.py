from aayu.compiler.hir.nodes import (
    HIRNode, HIRModule, HIRBlock, HIRExpr, HIRAssignment, HIRVariable, HIRCall,
    HIRBinaryOp, HIRUnaryOp, HIREnumValue, HIRStructFieldAccess, HIRStructInit,
    HIRFunctionDecl, HIRActionDecl, HIRReturn, HIRIf, HIRLoop
)
from aayu.compiler.semantic.context import SemanticContext, TypeID
from aayu.compiler.semantic.types import StructType, EnumType

from aayu.compiler.errors import InternalCompilerError

class HIRValidator:
    """
    Validates a generated HIR Module.
    Enforces Phase HIR-3 invariants explicitly: no machine checks, only semantic validation.
    """
    def __init__(self, context: SemanticContext):
        self.context = context
        self.type_registry = context.type_registry
        self.symbol_registry = getattr(context, 'symbol_registry', None)
        self.errors = []
        self._current_function_type = None

    def validate(self, module: HIRModule) -> bool:
        self.errors = []
        self._validate_node(module)
        if self.errors:
            error_details = "\n".join(self.errors)
            raise InternalCompilerError(
                phase="HIR Validation",
                invariant=f"HIR Validation Failed:\n{error_details}",
                node_id=getattr(module, 'origin_node_id', None),
                module="<unknown>"
            )
        return True

    def _validate_node(self, node: HIRNode, parent: HIRNode = None):
        if node is None:
            self.errors.append(f"Expected a valid HIR node but got None (Child of {type(parent).__name__ if parent else 'Root'})")
            return

        if not hasattr(node, "origin_node_id") or node.origin_node_id is None:
            self.errors.append(f"Invalid origin_node_id on HIR Node {getattr(node, 'hir_node_id', 'Unknown')} ({type(node).__name__})")

        if isinstance(node, HIRExpr):
            if not hasattr(node, "type_id") or node.type_id is None or node.type_id == 0:
                self.errors.append(f"Missing or Unknown type_id on Expr {node.hir_node_id} ({type(node).__name__})")
            else:
                # Ensure type exists in registry
                if not self.type_registry.get_type_by_id(node.type_id):
                    self.errors.append(f"Unregistered TypeID {node.type_id} on Expr {node.hir_node_id}")

        if isinstance(node, HIRModule):
            for global_assign in node.globals:
                self._validate_node(global_assign, node)
            for action in node.actions:
                self._validate_node(action, node)
            for func in node.functions:
                self._validate_node(func, node)
                
        elif isinstance(node, (HIRFunctionDecl, HIRActionDecl)):
            # Track current signature for return validation
            # For prototype, we might just skip strict signature checking if we don't have it
            # But we record the body
            self._current_function_type = None # TODO: fetch from symbol registry
            self._validate_node(node.body, node)
            self._current_function_type = None
            
        elif isinstance(node, HIRBlock):
            for stmt in node.statements:
                self._validate_node(stmt, node)
                
        elif isinstance(node, HIRAssignment):
            self._validate_node(node.target, node)
            self._validate_node(node.value, node)
            
        elif isinstance(node, HIRVariable):
            if not node.name:
                self.errors.append(f"Invalid symbol name on Variable {node.hir_node_id}")

        elif isinstance(node, HIRCall):
            for arg in node.args:
                self._validate_node(arg, node)
            # In a full compiler, we'd look up the target_symbol_id in self.symbol_registry
            # and verify arg types against the expected signature.
                
        elif isinstance(node, HIRStructFieldAccess):
            self._validate_node(node.target, node)
            struct_type = self.type_registry.get_type_by_id(node.struct_type_id)
            if not struct_type:
                self.errors.append(f"HIRStructFieldAccess: struct_type_id {node.struct_type_id} not found in registry")
            elif not isinstance(struct_type, StructType):
                self.errors.append(f"HIRStructFieldAccess: struct_type_id {node.struct_type_id} is not a StructType")
            else:
                # Verify field belongs to struct
                field_found = False
                for f in struct_type.fields:
                    if f.field_id == node.field_id:
                        field_found = True
                        break
                if not field_found:
                    self.errors.append(f"HIRStructFieldAccess: field_id {node.field_id} does not belong to struct")
                    
        elif isinstance(node, HIREnumValue):
            enum_type = self.type_registry.get_type_by_id(node.enum_type_id)
            if not enum_type:
                self.errors.append(f"HIREnumValue: enum_type_id {node.enum_type_id} not found in registry")
            elif not isinstance(enum_type, EnumType):
                self.errors.append(f"HIREnumValue: enum_type_id {node.enum_type_id} is not an EnumType")
            else:
                variant_found = False
                for v in enum_type.variants:
                    if v.variant_id == node.variant_id:
                        variant_found = True
                        break
                if not variant_found:
                    self.errors.append(f"HIREnumValue: variant_id {node.variant_id} does not belong to enum")
                if node.result_type_id != node.enum_type_id:
                    self.errors.append(f"HIREnumValue: result_type_id must match enum_type_id")
                    
        elif isinstance(node, HIRBinaryOp):
            self._validate_node(node.left, node)
            self._validate_node(node.right, node)
            
        elif isinstance(node, HIRUnaryOp):
            self._validate_node(node.operand, node)
            
        elif isinstance(node, HIRIf):
            self._validate_node(node.condition, node)
            self._validate_node(node.then_branch, node)
            if node.else_branch:
                self._validate_node(node.else_branch, node)
                
        elif isinstance(node, HIRLoop):
            self._validate_node(node.condition, node)
            self._validate_node(node.body, node)
            
        elif isinstance(node, HIRReturn):
            if node.value:
                self._validate_node(node.value, node)
                
        elif isinstance(node, HIRStructInit):
            struct_type = self.type_registry.get_type_by_id(node.struct_type_id)
            if not struct_type:
                self.errors.append(f"HIRStructInit: struct_type_id {node.struct_type_id} not found in registry")
            elif not isinstance(struct_type, StructType):
                self.errors.append(f"HIRStructInit: struct_type_id {node.struct_type_id} is not a StructType")
            elif len(node.args) != len(struct_type.fields):
                self.errors.append(f"HIRStructInit: expected {len(struct_type.fields)} arguments, got {len(node.args)}")
            
            for arg in node.args:
                self._validate_node(arg, node)
