from typing import Optional, Any
from aayu.compiler.ast.nodes import (
    ASTNode, IdentifierNode, LiteralNode, BinaryOpNode, 
    AssignmentNode, EnumDeclarationNode, StructDeclNode, StructInitNode,
    EnumAccessNode, SubscriptNode, PrimitiveTypeNode, NullableTypeNode,
    OptionalTypeNode, UnionTypeNode, StateDeclarationNode, ActionCallNode
)
from aayu.compiler.semantic.symbols import SymbolTable
from aayu.compiler.semantic.diagnostics import Diagnostic, DiagnosticSeverity
from aayu.compiler.semantic.context import SemanticContext
from aayu.compiler.semantic.types import (
    Type, PrimitiveType, UnionType, OptionalType, EnumType, StructType,
    T_INT, T_FLOAT, T_STRING, T_BOOL, T_CHAR, T_BYTE, T_VOID, T_NEVER, T_ANY, T_NULL
)
from aayu.compiler.pass_manager import CompilerPass
from aayu.compiler.semantic.scope_pass import ScopePass
from aayu.compiler.semantic.symbol_pass import SymbolPass

class TypePass(CompilerPass):
    """
    Phase 12.0 Semantic Pipeline - Pass 3: Type Resolver
    Constitution v1.0 Compliant: Immutable AST, Immutable Outputs.
    Reads resolved symbols from SemanticContext.
    """
    requires = [ScopePass, SymbolPass]

    def __init__(self):
        self.context: Optional[SemanticContext] = None

    def run_with_context(self, node: ASTNode, context: SemanticContext) -> ASTNode:
        self.context = context
        from aayu.compiler.ast.nodes import ProjectNode, ProgramNode
        if isinstance(node, ProjectNode):
            for module_id, program_node in node.modules.items():
                mod_scope = self.context.node_scopes.get(id(program_node))
                if mod_scope:
                    self.module_id = module_id
                    self._visit(program_node, mod_scope)
        elif isinstance(node, ProgramNode):
            mod_scope = self.context.node_scopes.get(id(node))
            if mod_scope:
                self.module_id = getattr(node, 'module_id', 'local')
                self._visit(node, mod_scope)
        return node

    def run(self, node: Any) -> Any:
        raise Exception("TypePass requires a SemanticContext.")

    def _visit(self, node: ASTNode, current_scope: SymbolTable) -> Type:
        if not node:
            return T_ANY
            
        if id(node) in self.context.node_scopes:
            current_scope = self.context.node_scopes[id(node)]
            
        method_name = f'_visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self._default_visit)
        expr_type = visitor(node, current_scope)
        
        self.context.type_registry.resolved_types[node.node_id] = expr_type
        return expr_type

    def _default_visit(self, node: ASTNode, current_scope: SymbolTable) -> Type:
        for key, value in vars(node).items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        self._visit(item, current_scope)
            elif isinstance(value, ASTNode):
                self._visit(value, current_scope)
        return T_VOID

    def _visit_LiteralNode(self, node: LiteralNode, current_scope: SymbolTable) -> Type:
        if isinstance(node.value, bool): return T_BOOL
        if isinstance(node.value, int): return T_INT
        if isinstance(node.value, float): return T_FLOAT
        if isinstance(node.value, str): return T_STRING
        return T_ANY

    def _visit_PrimitiveTypeNode(self, node: PrimitiveTypeNode, current_scope: SymbolTable) -> Type:
        name = node.name
        if name in ["Int", "int"]: return T_INT
        if name in ["Float", "float"]: return T_FLOAT
        if name in ["String", "str"]: return T_STRING
        if name in ["Bool", "bool"]: return T_BOOL
        if name in ["Char", "char"]: return T_CHAR
        if name in ["Byte", "byte"]: return T_BYTE
        if name in ["Void", "void"]: return T_VOID
        if name == "Never": return T_NEVER
        if name == "Any": return T_ANY
        if name == "Null": return T_NULL
        
        # User defined type resolved by SymbolPass
        qsym = self.context.symbol_registry.resolved_symbols.get(node.node_id)
        if qsym and isinstance(qsym.symbol.data_type, (StructType, EnumType)):
            return qsym.symbol.data_type
            
        return PrimitiveType(name)

    def _visit_NullableTypeNode(self, node: NullableTypeNode, current_scope: SymbolTable) -> Type:
        inner = self._visit(node.inner, current_scope)
        from aayu.compiler.semantic.types import make_nullable
        return make_nullable(inner)

    def _visit_OptionalTypeNode(self, node: OptionalTypeNode, current_scope: SymbolTable) -> Type:
        inner = self._visit(node.inner, current_scope)
        return OptionalType(inner)

    def _visit_UnionTypeNode(self, node: UnionTypeNode, current_scope: SymbolTable) -> Type:
        types = [self._visit(t, current_scope) for t in node.types]
        return UnionType(*types)

    def _visit_IdentifierNode(self, node: IdentifierNode, current_scope: SymbolTable) -> Type:
        qsym = self.context.symbol_registry.resolved_symbols.get(node.node_id)
        if qsym and qsym.symbol.data_type:
            if isinstance(qsym.symbol.data_type, Type):
                return qsym.symbol.data_type
        return T_ANY

    def _visit_BinaryOpNode(self, node: BinaryOpNode, current_scope: SymbolTable) -> Type:
        left_type = self._visit(node.left, current_scope)
        right_type = self._visit(node.right, current_scope)
        
        if node.operator in ['+', '-', '*', '/']:
            if left_type == T_INT and right_type == T_INT:
                return T_INT
            if left_type in [T_INT, T_FLOAT] and right_type in [T_INT, T_FLOAT]:
                return T_FLOAT
            if node.operator == '+' and left_type == T_STRING and right_type == T_STRING:
                return T_STRING
                
            if left_type != T_ANY and right_type != T_ANY:
                suggestion = f"\nSuggestion:\ntoInt({node.left.name})" if node.operator == '+' and left_type == T_STRING and right_type == T_INT and hasattr(node.left, 'name') else ""
                self.context.diagnostic_registry.add(Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="E201",
                    message=f"Cannot {node.operator} '{left_type}' and '{right_type}'.{suggestion}",
                    span=node.span
                ))
            return T_ANY
            
        elif node.operator in ['==', '!=']:
            if left_type != T_ANY and right_type != T_ANY and left_type != right_type:
                self.context.diagnostic_registry.add(Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="E201",
                    message=f"Cannot compare '{left_type}' and '{right_type}' for equality.",
                    span=node.span
                ))
            return T_BOOL
            
        elif node.operator in ['<', '>', '<=', '>=']:
            return T_BOOL
            
        return T_ANY

    def _visit_AssignmentNode(self, node: AssignmentNode, current_scope: SymbolTable) -> Type:
        val_type = self._visit(node.value, current_scope)
        target_type = self._visit(node.target, current_scope)
        
        if isinstance(node.target, IdentifierNode):
            qsym = self.context.symbol_registry.resolved_symbols.get(node.target.node_id)
            if qsym:
                sym = qsym.symbol
                if not sym.data_type or sym.data_type == "Any":
                    sym.data_type = val_type
                    target_type = val_type
                    
        if isinstance(target_type, Type) and isinstance(val_type, Type):
            if not val_type.is_assignable_to(target_type) and val_type != T_ANY and target_type != T_ANY:
                self.context.diagnostic_registry.add(Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="E201",
                    message=f"Cannot assign type '{val_type}' to '{target_type}'.",
                    span=node.span
                ))
                
        return T_VOID

    def _visit_StateDeclarationNode(self, node: StateDeclarationNode, current_scope: SymbolTable) -> Type:
        val_type = self._visit(node.value, current_scope) if getattr(node, "value", None) else T_ANY
        declared_type = self._visit(node.declared_type, current_scope) if getattr(node, "declared_type", None) else T_ANY
            
        sym = current_scope.resolve(node.name)
        if sym:
            sym.data_type = declared_type if declared_type != T_ANY else val_type
        return T_VOID

    def _visit_EnumDeclarationNode(self, node: EnumDeclarationNode, current_scope: SymbolTable) -> Type:
        sym = current_scope.resolve(node.name)
        if sym and isinstance(sym.data_type, EnumType):
            self.context.type_registry.register_type(f"{self.module_id}::{node.name}", sym.data_type)
            return sym.data_type
        return T_VOID

    def _visit_StructDeclNode(self, node: StructDeclNode, current_scope: SymbolTable) -> Type:
        sym = current_scope.resolve(node.name)
        if sym and isinstance(sym.data_type, StructType):
            struct_type = sym.data_type
            for i, field_node in enumerate(node.fields):
                resolved_type = self._visit(field_node.field_type, current_scope)
                struct_type.fields[i].field_type = resolved_type
            struct_type.calculate_layout()
            self.context.type_registry.register_type(f"{self.module_id}::{node.name}", struct_type)
            return struct_type
        return T_VOID

    def _visit_StructInitNode(self, node: StructInitNode, current_scope: SymbolTable) -> Type:
        qsym = self.context.symbol_registry.resolved_symbols.get(node.node_id)
        if not qsym or not isinstance(qsym.symbol.data_type, StructType):
            print(f"DEBUG: StructInitNode name={node.struct_name} qsym={qsym} data_type={getattr(qsym.symbol, 'data_type', 'none') if qsym else 'none'}")
            self.context.diagnostic_registry.add(Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="E303",
                message=f"'{node.struct_name}' is not a known struct type.",
                span=node.span
            ))
            return T_ANY
            
        struct_type = qsym.symbol.data_type
        
        provided_fields = set(node.args.keys())
        expected_fields = set(f.name for f in struct_type.fields)
        
        for name, expr in node.args.items():
            field = struct_type.get_field(name)
            if not field:
                self.context.diagnostic_registry.add(Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="E304",
                    message=f"Struct '{node.struct_name}' has no field '{name}'.",
                    span=node.span
                ))
            else:
                arg_type = self._visit(expr, current_scope)
                if not arg_type.is_assignable_to(field.field_type) and arg_type != T_ANY:
                    self.context.diagnostic_registry.add(Diagnostic(
                        severity=DiagnosticSeverity.ERROR,
                        code="E305",
                        message=f"Type mismatch for field '{name}'. Expected '{field.field_type}', got '{arg_type}'.",
                        span=node.span
                    ))
                    
        missing = expected_fields - provided_fields
        if missing:
            self.context.diagnostic_registry.add(Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="E306",
                message=f"Missing fields for struct '{node.struct_name}': {', '.join(missing)}.",
                span=node.span
            ))
            
        return struct_type

    def _visit_EnumAccessNode(self, node: EnumAccessNode, current_scope: SymbolTable) -> Type:
        qsym = self.context.symbol_registry.resolved_symbols.get(node.node_id)
        if not qsym or not isinstance(qsym.symbol.data_type, EnumType):
            self.context.diagnostic_registry.add(Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="E301",
                message=f"'{node.enum_name}' is not a known enum type.",
                span=node.span
            ))
            return T_ANY

        enum_type = qsym.symbol.data_type
        variant = enum_type.variant_by_name(node.variant)
        if not variant:
            self.context.diagnostic_registry.add(Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="E302",
                message=f"'{node.variant}' is not a variant of enum '{node.enum_name}'. "
                        f"Available variants: {', '.join(v.name for v in enum_type.variants)}.",
                span=node.span
            ))
            return T_ANY

        return enum_type

    def _visit_SubscriptNode(self, node: SubscriptNode, current_scope: SymbolTable) -> Type:
        target_type = self._visit(node.target, current_scope)
        
        if isinstance(node.index, LiteralNode):
            attr_name = str(node.index.value)
            
            if isinstance(target_type, EnumType):
                variant = target_type.variant_by_name(attr_name)
                if variant:
                    return target_type
                else:
                    self.context.diagnostic_registry.add(Diagnostic(
                        severity=DiagnosticSeverity.ERROR,
                        code="E302",
                        message=f"'{attr_name}' is not a variant of enum '{target_type.name}'.",
                        span=node.span
                    ))
                    return T_ANY
                    
            if isinstance(target_type, StructType):
                field = target_type.get_field(attr_name)
                if field:
                    return field.field_type
                else:
                    self.context.diagnostic_registry.add(Diagnostic(
                        severity=DiagnosticSeverity.ERROR,
                        code="E307",
                        message=f"Struct '{target_type.name}' has no field '{attr_name}'.",
                        span=node.span
                    ))
                    return T_ANY
                    
            if target_type == T_ANY and isinstance(node.target, IdentifierNode):
                qsym = self.context.symbol_registry.resolved_symbols.get(node.target.node_id)
                from aayu.compiler.semantic.symbols import ModuleSymbol
                if qsym and isinstance(qsym.symbol, ModuleSymbol):
                    mod_sym = qsym.symbol
                    sym = mod_sym.exports.resolve(attr_name)
                    if sym and isinstance(sym.data_type, Type):
                        return sym.data_type

        self._visit(node.index, current_scope)
        return T_ANY
        
    def _visit_ActionCallNode(self, node: ActionCallNode, current_scope: SymbolTable) -> Type:
        qsym = self.context.symbol_registry.resolved_symbols.get(node.node_id)
        if not qsym:
            # Undefined action already handled by SymbolPass
            for arg in node.args:
                self._visit(arg, current_scope)
            return T_ANY
            
        # Optional: Check argument types against action signature here.
        # But for now just visit them
        for arg in node.args:
            self._visit(arg, current_scope)
            
        action_sym = qsym.symbol
        if action_sym.data_type and isinstance(action_sym.data_type, Type):
            return action_sym.data_type
            
        return T_ANY
