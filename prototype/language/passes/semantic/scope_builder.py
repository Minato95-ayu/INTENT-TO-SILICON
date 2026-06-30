from ast_nodes import DeclarationNode, FunctionDeclNode, TaskNode, ExportNode, ExportListNode, InterfaceDeclNode
from resolver.symbols import VariableSymbol, FunctionSymbol, ParameterSymbol, InterfaceSymbol, SymbolTable, ScopeType
from ..base import ASTVisitorPass

class ScopeBuilderPass(ASTVisitorPass):
    def __init__(self):
        super().__init__("ScopeBuilderPass")
        
    def run(self, context):
        self.context = context
        mod_name = context.current_module
        if mod_name not in context.symbol_tables:
            context.diagnostics.error(f"No symbol table initialized for module {mod_name}", mod_name)
            return False
            
        self.current_scope = context.symbol_tables[mod_name]
        return super().run(context)
        
    def visit_ProgramNode(self, node):
        # Extract exported items from ExportNode wrappers
        for stmt in node.statements:
            if isinstance(stmt, ExportNode):
                if isinstance(stmt.declaration, TaskNode):
                    stmt.declaration.is_exported = True
                    stmt.declaration.visibility = "public"

        for stmt in node.statements:
            if isinstance(stmt, DeclarationNode):
                symbol = VariableSymbol(stmt.name, self.current_scope, stmt.is_exported, getattr(stmt, 'visibility', 'private'))
                if hasattr(stmt, 'type_annotation') and stmt.type_annotation:
                    symbol.declared_type = stmt.type_annotation
                self.current_scope.define(symbol)
                stmt.symbol = symbol
            elif isinstance(stmt, FunctionDeclNode):
                symbol = FunctionSymbol(stmt.name, self.current_scope, stmt.is_exported, getattr(stmt, 'visibility', 'private'))
                if hasattr(stmt, 'return_type') and stmt.return_type:
                    symbol.declared_type = stmt.return_type
                self.current_scope.define(symbol)
                stmt.symbol = symbol
            elif isinstance(stmt, InterfaceDeclNode):
                symbol = InterfaceSymbol(stmt.name, self.current_scope, stmt.is_exported, getattr(stmt, 'visibility', 'private'))
                self.current_scope.define(symbol)
                stmt.symbol = symbol
            elif isinstance(stmt, TaskNode):
                is_exported = getattr(stmt, 'is_exported', False)
                symbol = FunctionSymbol(stmt.name, self.current_scope, is_exported, getattr(stmt, 'visibility', 'private'))
                self.current_scope.define(symbol)
                stmt.symbol = symbol
                
        # Handle block exports like export { add, subtract }
        for stmt in node.statements:
            if isinstance(stmt, ExportListNode):
                for sym_name in stmt.symbols:
                    sym = self.current_scope.lookup(sym_name, current_only=True)
                    if sym:
                        sym.is_exported = True
                        sym.visibility = "public"
                    else:
                        self.context.diagnostics.error(f"Cannot export undefined symbol '{sym_name}'", self.context.current_module, node=stmt)
                
        # We don't visit the bodies here; bodies are handled during SymbolBindingPass
        for stmt in node.statements:
            actual_stmt = stmt.declaration if isinstance(stmt, ExportNode) else stmt
            if isinstance(actual_stmt, (FunctionDeclNode, TaskNode)):
                func_scope = SymbolTable(actual_stmt.name, ScopeType.FUNCTION, self.current_scope)
                actual_stmt.func_scope = func_scope
                
                for param in actual_stmt.parameters:
                    if isinstance(param, tuple):
                        param_name, param_type = param
                    else:
                        param_name = param
                        param_type = None
                        
                    param_symbol = ParameterSymbol(param_name, func_scope)
                    if param_type:
                        param_symbol.declared_type = param_type
                    func_scope.define(param_symbol)
