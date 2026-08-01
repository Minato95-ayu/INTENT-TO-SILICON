from typing import Optional
from aayu.compiler.ast.nodes import (
    ProgramNode, StateDeclarationNode, ActionDeclarationNode, 
    WhileNode, ForNode, ASTNode
)
from aayu.compiler.semantic.symbols import SymbolTable, Symbol
from aayu.compiler.semantic.diagnostics import DiagnosticEngine, Diagnostic, DiagnosticSeverity

class ScopePass:
    """
    Phase 12.0 Semantic Pipeline - Pass 1: Scope Builder
    Responsible for creating lexical scopes and defining symbols in their respective scopes.
    Does NOT resolve types or usage (that is done in SymbolPass and TypePass).
    """
    def __init__(self, diag_engine: DiagnosticEngine):
        self.diag_engine = diag_engine
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        
        # Map AST nodes to their creating scopes so subsequent passes can look them up
        self.node_scopes = {} 

    def run(self, ast: ProgramNode):
        self.node_scopes[id(ast)] = self.global_scope
        self._visit(ast)
        return self.global_scope

    def _visit(self, node: ASTNode):
        if not node:
            return
            
        method_name = f'_visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self._default_visit)
        visitor(node)

    def _default_visit(self, node: ASTNode):
        # By default, visit all children
        for key, value in vars(node).items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        self._visit(item)
            elif isinstance(value, ASTNode):
                self._visit(value)

    def _visit_StateDeclarationNode(self, node: StateDeclarationNode):
        # Define in current scope (global)
        sym = Symbol(node.name, "state")
        if node.name in self.current_scope.symbols:
            self.diag_engine.report(Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="E101",
                message=f"State '{node.name}' is already defined in this scope.",
                line=node.line, column=node.column,
                notes=[f"State variables must be unique."]
            ))
        else:
            self.current_scope.define(sym)
            
        self._visit(node.value)

    def _visit_ActionDeclarationNode(self, node: ActionDeclarationNode):
        sym = Symbol(node.name, "action")
        if node.name in self.current_scope.symbols:
            self.diag_engine.report(Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="E102",
                message=f"Action '{node.name}' is already defined in this scope.",
                line=node.line, column=node.column
            ))
        else:
            self.current_scope.define(sym)

        # Create new scope for action body
        prev_scope = self.current_scope
        action_scope = SymbolTable(parent=prev_scope)
        self.current_scope = action_scope
        self.node_scopes[id(node)] = action_scope

        # Define arguments in local scope
        for arg in getattr(node, 'args', []):
            arg_sym = Symbol(arg, "local")
            self.current_scope.define(arg_sym)

        for stmt in node.statements:
            self._visit(stmt)

        self.current_scope = prev_scope

    def _visit_WhileNode(self, node: WhileNode):
        self._visit(node.condition)
        
        # While loops get their own scope
        prev_scope = self.current_scope
        loop_scope = SymbolTable(parent=prev_scope)
        self.current_scope = loop_scope
        self.node_scopes[id(node)] = loop_scope
        
        for stmt in node.body:
            self._visit(stmt)
            
        self.current_scope = prev_scope

    def _visit_ForNode(self, node: ForNode):
        self._visit(node.iterable)
        
        prev_scope = self.current_scope
        loop_scope = SymbolTable(parent=prev_scope)
        self.current_scope = loop_scope
        self.node_scopes[id(node)] = loop_scope
        
        # Define iterator
        self.current_scope.define(Symbol(node.iterator, "local"))
        if getattr(node, 'index_name', None):
            self.current_scope.define(Symbol(node.index_name, "local"))
            
        for stmt in node.body:
            self._visit(stmt)
            
        self.current_scope = prev_scope
