"""
===============================================================================
AAYU Compiler - Semantic Analyzer (Type Checker)

Purpose:
    Ye file AST ko check karti hai ki kya code statically safe hai. 
    (Kahin string me number to add nahi ho raha?)

Input:
    Abstract Syntax Tree (AST)

Output:
    Validated AST (ya Compile-time Error)

Pipeline:
    AST
        ↓
    Semantic Analysis ← (Current File)
        ↓
    Compiler

Ye file kyun important hai?
    AAYU ek strict typed language hai. Agar types galat hue to ye runtime par crash hone se bachata hai.

Difficulty:
    ⭐⭐ (Medium)

Recommended Reading Order:
    3. ast_nodes.py
    4. passes/semantic/type_checker.py (You are here)
    5. compiler.py
===============================================================================
"""
from compiler.frontend.passes.base import ASTVisitorPass
from compiler.frontend.ast_nodes import *
from compiler.frontend.type_nodes import *
from compiler.frontend.resolver.symbols import SymbolKind, Symbol
from compiler.frontend.resolver.semantic_types import GenericType, FunctionType, BuiltinTypes, PrimitiveType, AnyType, InterfaceType, GenericPlaceholderType, GenericInstance, AAYUType
from compiler.frontend.errors import AAYUTypeError
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
            
            # Lookup in symbol table for user-defined types (like interfaces or generic placeholders)
            sym = self.current_scope.lookup(type_node.name)
            if sym:
                if sym.kind == SymbolKind.INTERFACE:
                    return sym.resolved_type if sym.resolved_type else BuiltinTypes.Unknown
                elif sym.kind == SymbolKind.TYPE_PARAMETER:
                    return GenericPlaceholderType(sym.name)
                
            self.context.diagnostics.error(f"TypeError AAYU2002: Unknown type '{type_node.name}'", self.context.current_module, getattr(type_node, 'span', None))
            return BuiltinTypes.Unknown
            
        if type_node.__class__.__name__ == 'GenericTypeNode':
            base_type = self._resolve_type_node(type_node.base_type)
            args = [self._resolve_type_node(a) for a in type_node.type_args]
            return GenericInstance(base_type, args)
            
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
        self.current_scope = self.context.symbol_tables[self.context.current_module]
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
        prev_scope = getattr(self, "current_scope", None)
        if hasattr(node, "func_scope"):
            self.current_scope = node.func_scope
        elif hasattr(node, "type_scope"):
            self.current_scope = node.type_scope
            
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
        if prev_scope is not None:
            self.current_scope = prev_scope

    def visit_InterfaceDeclNode(self, node: InterfaceDeclNode):
        prev_scope = getattr(self, "current_scope", None)
        if hasattr(node, "type_scope"):
            self.current_scope = node.type_scope
            
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

        if prev_scope is not None:
            self.current_scope = prev_scope

    def visit_ExtensionDeclNode(self, node: ExtensionDeclNode):
        prev_scope = getattr(self, "current_scope", None)
        if hasattr(node, "type_scope"):
            self.current_scope = node.type_scope
            
        for method in node.methods:
            self.visit(method)
            
        if node.interface_name:
            # We must look up the interface
            interface_sym = self.context.symbol_tables[self.context.current_module].lookup(node.interface_name)
            if not interface_sym or not isinstance(interface_sym.resolved_type, InterfaceType):
                self.context.diagnostics.error(
                    f"AAYU2004: Cannot extend '{node.target_type}' with undefined interface '{node.interface_name}'.",
                    self.context.current_module,
                    node=node
                )
                return
                
            interface_type = interface_sym.resolved_type
            
            # Now verify methods match exactly
            provided_methods = {}
            for method in node.methods:
                if method.symbol:
                    param_types = []
                    for param_name, type_node in method.parameters:
                        pt = self._resolve_type_node(type_node) if type_node else BuiltinTypes.Any
                        param_types.append(pt)
                    ret_type = method.symbol.resolved_type if method.symbol.resolved_type else BuiltinTypes.Void
                    provided_methods[method.name] = FunctionType(param_types, ret_type)
                    
            for req_name, req_type in interface_type.methods.items():
                if req_name not in provided_methods:
                    self.context.diagnostics.error(
                        f"AAYU2005: Type '{node.target_type}' does not implement required method '{req_name}' from interface '{node.interface_name}'.",
                        self.context.current_module,
                        node=node
                    )
                else:
                    prov_type = provided_methods[req_name]
                    # Check signatures exactly
                    if len(prov_type.param_types) != len(req_type.param_types):
                        self.context.diagnostics.error(
                            f"AAYU2006: Method '{req_name}' in extension has incorrect parameter count.",
                            self.context.current_module,
                            node=node
                        )
                    else:
                        for p, r in zip(prov_type.param_types, req_type.param_types):
                            if p != r and p != BuiltinTypes.Any:
                                self.context.diagnostics.error(
                                    f"AAYU2006: Method '{req_name}' in extension has mismatching parameter types.",
                                    self.context.current_module,
                                    node=node
                                )
                                break
                                
                    if prov_type.return_type != req_type.return_type and prov_type.return_type != BuiltinTypes.Any:
                        self.context.diagnostics.error(
                            f"AAYU2006: Method '{req_name}' in extension has mismatching return type.",
                            self.context.current_module,
                            node=node
                        )

        if prev_scope is not None:
            self.current_scope = prev_scope

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
