from aayu.compiler.ast.nodes import ASTNode, IdentifierNode
from aayu.compiler.semantic.symbols import SymbolTable
from aayu.compiler.semantic.diagnostics import DiagnosticEngine, Diagnostic, DiagnosticSeverity
from aayu.compiler.semantic.scope_pass import ScopePass

class SymbolPass:
    """
    Phase 12.0 Semantic Pipeline - Pass 2: Symbol Resolver
    Responsible for resolving all identifiers to their declared symbols.
    Reports errors for undefined variables.
    """
    def __init__(self, diag_engine: DiagnosticEngine, scope_pass: ScopePass):
        self.diag_engine = diag_engine
        self.node_scopes = scope_pass.node_scopes
        self.global_scope = scope_pass.global_scope

    def run(self, ast: ASTNode):
        self._visit(ast, self.global_scope)

    def _visit(self, node: ASTNode, current_scope: SymbolTable):
        if not node:
            return
            
        # If this node created a new scope, switch to it
        if id(node) in self.node_scopes:
            current_scope = self.node_scopes[id(node)]
            
        from aayu.compiler.ast.nodes import AssignmentNode
        if isinstance(node, IdentifierNode):
            self._visit_IdentifierNode(node, current_scope)
            return
            
        if isinstance(node, AssignmentNode):
            self._visit_AssignmentNode(node, current_scope)

        # Visit all children
        for key, value in vars(node).items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        self._visit(item, current_scope)
            elif isinstance(value, ASTNode):
                self._visit(value, current_scope)

    def _visit_IdentifierNode(self, node: IdentifierNode, current_scope: SymbolTable):
        sym = current_scope.resolve(node.name)
        if not sym:
            # Let's see if we can find a close match for suggestions
            suggestion = self._find_closest_match(node.name, current_scope)
            diag = Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="E102",
                message=f"Undefined variable '{node.name}'.",
                line=node.line, column=node.column
            )
            if suggestion:
                diag.add_suggestion(f"Did you mean '{suggestion}'?")
            self.diag_engine.report(diag)
            
    def _find_closest_match(self, name: str, scope: SymbolTable) -> str:
        # Simple Levenshtein or just prefix matching (mocked for now)
        # We would collect all symbols from scope chain and find nearest edit distance
        return None

    def _visit_AssignmentNode(self, node, current_scope: SymbolTable):
        sym = current_scope.resolve(node.target)
        if not sym:
            suggestion = self._find_closest_match(node.target, current_scope)
            diag = Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="E102",
                message=f"Undefined variable '{node.target}'.",
                line=node.line, column=node.column
            )
            if suggestion:
                diag.add_suggestion(f"Did you mean '{suggestion}'?")
            self.diag_engine.report(diag)
            
        # Still visit the value being assigned
        self._visit(node.value, current_scope)
