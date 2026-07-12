"""
=============================================================================
FILE: scope_builder.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from compiler.frontend.ast_nodes import DeclarationNode, FunctionDeclNode, TaskNode, ExportNode, ExportListNode, InterfaceDeclNode, ExtensionDeclNode, RecordDeclarationNode
from compiler.frontend.resolver.symbols import VariableSymbol, FunctionSymbol, ParameterSymbol, InterfaceSymbol, SymbolTable, ScopeType
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
            elif isinstance(stmt, ExtensionDeclNode):
                for method in stmt.methods:
                    # Create symbols for extension methods without adding them to the global scope
                    symbol = FunctionSymbol(method.name, self.current_scope, False, 'public')
                    if hasattr(method, 'return_type') and method.return_type:
                        symbol.declared_type = method.return_type
                    method.symbol = symbol
                
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
            
            # Helper to create type scopes
            def setup_type_scope(node, parent_scope):
                if hasattr(node, 'type_parameters') and node.type_parameters:
                    from compiler.frontend.resolver.symbols import TypeParameterSymbol
                    name = getattr(node, "name", getattr(node, "target_type", "unknown"))
                    type_scope = SymbolTable(name + '_types', ScopeType.TYPE_PARAMETER, parent_scope)
                    node.type_scope = type_scope
                    for tp in node.type_parameters:
                        sym = TypeParameterSymbol(tp, type_scope)
                        type_scope.define(sym)
                    return type_scope
                return parent_scope

            def setup_func_scope(func_node, parent_scope):
                type_parent = setup_type_scope(func_node, parent_scope)
                func_scope = SymbolTable(func_node.name, ScopeType.FUNCTION, type_parent)
                func_node.func_scope = func_scope
                for param in func_node.parameters:
                    if isinstance(param, tuple):
                        param_name, param_type = param
                    else:
                        param_name = param
                        param_type = None
                    param_symbol = ParameterSymbol(param_name, func_scope)
                    if param_type:
                        param_symbol.declared_type = param_type
                    func_scope.define(param_symbol)

            if isinstance(actual_stmt, (FunctionDeclNode, TaskNode)):
                setup_func_scope(actual_stmt, self.current_scope)
            elif isinstance(actual_stmt, (InterfaceDeclNode, RecordDeclarationNode)):
                setup_type_scope(actual_stmt, self.current_scope)
            elif isinstance(actual_stmt, ExtensionDeclNode):
                ext_scope = setup_type_scope(actual_stmt, self.current_scope)
                for method in actual_stmt.methods:
                    setup_func_scope(method, ext_scope)
