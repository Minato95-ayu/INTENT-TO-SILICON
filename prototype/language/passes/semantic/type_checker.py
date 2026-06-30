from passes.base import ASTVisitorPass
from ast_nodes import *
from type_nodes import *
from resolver.symbols import SymbolKind, Symbol
from resolver.semantic_types import BuiltinTypes, AAYUType, FunctionType, InterfaceType
from errors import AAYUTypeError

class TypeCheckerPass(ASTVisitorPass):
    def __init__(self):
        super().__init__("TypeChecker")
        self.current_function = None

    def _resolve_type_node(self, type_node: Node) -> AAYUType:
        if type_node is None:
            return BuiltinTypes.Any

        if isinstance(type_node, (PrimitiveTypeNode, NamedTypeNode)):
            t = BuiltinTypes.get(type_node.name)
            if t is not None:
                return t
            
            # Lookup in symbol table for user-defined types (like interfaces)
            sym = self.context.symbol_tables[self.context.current_module].lookup(type_node.name)
            if sym and sym.kind == SymbolKind.INTERFACE:
                return sym.resolved_type if sym.resolved_type else BuiltinTypes.Unknown
                
            self.context.diagnostics.error(f"TypeError AAYU2002: Unknown type '{type_node.name}'", self.context.current_module, getattr(type_node, 'span', None))
            return BuiltinTypes.Unknown
            
        if isinstance(type_node, FunctionTypeNode):
            param_types = [self._resolve_type_node(p) for p in type_node.param_types]
            return_type = self._resolve_type_node(type_node.return_type) if type_node.return_type else BuiltinTypes.Void
            return FunctionType(param_types, return_type)
            
        return BuiltinTypes.Unknown

    def _report_type_error(self, code: str, msg: str, node: Node):
        line = node.span.start_line if getattr(node, 'span', None) else 1
        err = AAYUTypeError(code, msg, line)
        # We report to diagnostics directly
        self.context.diagnostics.error(f"TypeError {code}: {msg}", self.context.current_module, line=line)

    def visit_ProgramNode(self, node: ProgramNode):
        self.generic_visit(node)

    def visit_NumberNode(self, node: NumberNode):
        node.resolved_type = BuiltinTypes.Number

    def visit_TextNode(self, node: TextNode):
        node.resolved_type = BuiltinTypes.Text

    def visit_VariableNode(self, node: VariableNode):
        if node.symbol:
            if node.symbol.resolved_type is None:
                # Resolve it now if it hasn't been
                if node.symbol.declared_type:
                    node.symbol.resolved_type = self._resolve_type_node(node.symbol.declared_type)
                else:
                    node.symbol.resolved_type = BuiltinTypes.Any
            node.resolved_type = node.symbol.resolved_type
        else:
            node.resolved_type = BuiltinTypes.Any

    def visit_BinaryExpressionNode(self, node: BinaryExpressionNode):
        self.visit(node.left)
        self.visit(node.right)
        
        left_type = getattr(node.left, 'resolved_type', BuiltinTypes.Any) or BuiltinTypes.Any
        right_type = getattr(node.right, 'resolved_type', BuiltinTypes.Any) or BuiltinTypes.Any
        
        if node.operator in ('+', '-', '*', '/', '%'):
            # MVP: math ops require Number (or String for + but we keep it simple for now, allow Any)
            if left_type == BuiltinTypes.Number and right_type == BuiltinTypes.Number:
                node.resolved_type = BuiltinTypes.Number
            elif left_type == BuiltinTypes.Text and right_type == BuiltinTypes.Text and node.operator == '+':
                node.resolved_type = BuiltinTypes.Text
            elif left_type == BuiltinTypes.Any or right_type == BuiltinTypes.Any:
                node.resolved_type = BuiltinTypes.Any
            else:
                self._report_type_error("AAYU2001", f"Type mismatch: Cannot apply '{node.operator}' to {left_type} and {right_type}.", node)
                node.resolved_type = BuiltinTypes.Error
        else:
            # logic ops
            node.resolved_type = BuiltinTypes.Boolean

    def visit_DeclarationNode(self, node: DeclarationNode):
        self.visit(node.value)
        value_type = getattr(node.value, 'resolved_type', BuiltinTypes.Any) or BuiltinTypes.Any
        
        # Resolve the declared type
        if node.symbol:
            if node.symbol.declared_type:
                declared = self._resolve_type_node(node.symbol.declared_type)
            else:
                # Type Inference (Phase 5.4): Infer type from value
                declared = value_type
                
            node.symbol.resolved_type = declared
        else:
            # Local variable without a symbol
            if getattr(node, 'type_annotation', None):
                declared = self._resolve_type_node(node.type_annotation)
            else:
                declared = value_type
            
        if not declared.is_assignable_from(value_type):
            self._report_type_error("AAYU2001", f"Type mismatch: Cannot assign value of type '{value_type}' to variable '{node.name}' of type '{declared}'.", node)

    def visit_AssignmentNode(self, node: AssignmentNode):
        self.visit(node.target)
        self.visit(node.value)
        
        target_type = getattr(node.target, 'resolved_type', BuiltinTypes.Any) or BuiltinTypes.Any
        value_type = getattr(node.value, 'resolved_type', BuiltinTypes.Any) or BuiltinTypes.Any
        
        if not target_type.is_assignable_from(value_type):
            self._report_type_error("AAYU2001", f"Type mismatch: Cannot assign value of type '{value_type}' to target of type '{target_type}'.", node)

    def visit_FunctionDeclNode(self, node: FunctionDeclNode):
        # Resolve return type
        is_inferring_return = False
        if node.symbol:
            if node.symbol.declared_type:
                ret_type = self._resolve_type_node(node.symbol.declared_type)
            else:
                # Phase 5.4: Initialize as None for inference
                ret_type = None
                is_inferring_return = True
            node.symbol.resolved_type = ret_type
            
            # Resolve parameters
            if hasattr(node, 'func_scope'):
                for param_sym in node.func_scope.symbols.values():
                    if param_sym.kind == SymbolKind.PARAMETER:
                        if param_sym.declared_type:
                            param_sym.resolved_type = self._resolve_type_node(param_sym.declared_type)
                        else:
                            param_sym.resolved_type = BuiltinTypes.Any

        prev_func = self.current_function
        self.current_function = node
        
        for stmt in node.body:
            self.visit(stmt)
            
        # Post-process inference if no return was found
        if is_inferring_return and getattr(node.symbol, 'resolved_type', None) is None:
            node.symbol.resolved_type = BuiltinTypes.Void
            
        self.current_function = prev_func

    def visit_InterfaceDeclNode(self, node: InterfaceDeclNode):
        methods = {}
        for method in node.methods:
            param_types = []
            for param_name, type_node in method.parameters:
                pt = self._resolve_type_node(type_node) if type_node else BuiltinTypes.Any
                param_types.append(pt)
            ret_type = self._resolve_type_node(method.return_type) if method.return_type else BuiltinTypes.Void
            methods[method.name] = FunctionType(param_types, ret_type)
            
        interface_type = InterfaceType(node.name, methods)
        if node.symbol:
            node.symbol.resolved_type = interface_type

    def visit_ReturnNode(self, node: ReturnNode):
        self.visit(node.value)
        value_type = getattr(node.value, 'resolved_type', BuiltinTypes.Any) or BuiltinTypes.Any
        
        if self.current_function and self.current_function.symbol:
            declared_ret = self.current_function.symbol.resolved_type
            
            # Inference Mode
            if declared_ret is None:
                self.current_function.symbol.resolved_type = value_type
            else:
                if not declared_ret.is_assignable_from(value_type):
                    # In inference mode, multiple differing returns fallback to AnyType
                    if getattr(self.current_function.symbol, 'declared_type', None) is None:
                        self.current_function.symbol.resolved_type = BuiltinTypes.Any
                    else:
                        self._report_type_error("AAYU2004", f"Return type mismatch: Expected '{declared_ret}', got '{value_type}'.", node)

    def visit_MethodCallNode(self, node: MethodCallNode):
        self.generic_visit(node)
        node.resolved_type = BuiltinTypes.Any

    def visit_BuiltinFunctionNode(self, node: BuiltinFunctionNode):
        self.generic_visit(node)
        node.resolved_type = BuiltinTypes.Any
