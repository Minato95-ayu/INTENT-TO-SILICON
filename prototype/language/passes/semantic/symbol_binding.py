from ast_nodes import FunctionDeclNode, VariableNode, BuiltinFunctionNode
from ..base import ASTVisitorPass

class SymbolBindingPass(ASTVisitorPass):
    def __init__(self):
        super().__init__("SymbolBindingPass")
        
    def run(self, context):
        self.context = context
        self.current_scope = context.symbol_tables[context.current_module]
        return super().run(context)
        
    def visit_FunctionDeclNode(self, node: FunctionDeclNode):
        if hasattr(node, 'func_scope'):
            self.current_scope = node.func_scope
            
        for stmt in node.body:
            self.visit(stmt)
            
        if hasattr(node, 'func_scope'):
            self.current_scope = self.current_scope.parent

    def visit_VariableNode(self, node: VariableNode):
        symbol = self.current_scope.lookup(node.name)
        if not symbol:
            self.context.diagnostics.error(f"Undefined identifier '{node.name}'", self.context.current_module, node=node)
        else:
            node.symbol = symbol

    def visit_BuiltinFunctionNode(self, node: BuiltinFunctionNode):
        symbol = self.current_scope.lookup(node.name)
        if not symbol:
            pass # Fallback for now, could log warning
        else:
            node.symbol = symbol
            
        for arg in node.arguments:
            self.visit(arg)
            
    def _check_visibility(self, symbol, module_symbol, node, node_type):
        if not symbol:
            self.context.diagnostics.error(f"Undefined {node_type}", self.context.current_module, node=node)
            return
            
        visibility = getattr(symbol, 'visibility', 'private')
        is_exported = getattr(symbol, 'is_exported', False)
        
        if not is_exported and visibility != 'public':
            self.context.diagnostics.error(f"Cannot access private {node_type} '{symbol.name}' from module '{module_symbol.name}'", self.context.current_module, node=node)
            
    def visit_MethodCallNode(self, node):
        self.visit(node.object_node)
        
        if hasattr(node.object_node, 'symbol') and node.object_node.symbol:
            obj_sym = node.object_node.symbol
            if hasattr(obj_sym, 'kind') and obj_sym.kind.name == 'MODULE':
                # It's a module access!
                target_table = obj_sym.module_table
                if target_table:
                    target_sym = target_table.lookup(node.method_name, current_only=True)
                    if not target_sym:
                        self.context.diagnostics.error(f"Module '{obj_sym.name}' has no function '{node.method_name}'", self.context.current_module, node=node)
                    else:
                        node.symbol = target_sym
                        self._check_visibility(target_sym, obj_sym, node, "function")
                        
        for arg in node.arguments:
            self.visit(arg)
            
    def visit_PropertyAccessNode(self, node):
        self.visit(node.object_expr)
        
        if hasattr(node.object_expr, 'symbol') and node.object_expr.symbol:
            obj_sym = node.object_expr.symbol
            if hasattr(obj_sym, 'kind') and obj_sym.kind.name == 'MODULE':
                target_table = obj_sym.module_table
                if target_table:
                    target_sym = target_table.lookup(node.property_name, current_only=True)
                    if not target_sym:
                        self.context.diagnostics.error(f"Module '{obj_sym.name}' has no property '{node.property_name}'", self.context.current_module, node=node)
                    else:
                        node.symbol = target_sym
                        self._check_visibility(target_sym, obj_sym, node, "property")
