from aayu.compiler.ast.nodes import (
    ASTNode, IdentifierNode, LiteralNode, BinaryOpNode, 
    AssignmentNode, ArrayNode, DictionaryNode
)
from aayu.compiler.semantic.symbols import SymbolTable
from aayu.compiler.semantic.diagnostics import DiagnosticEngine, Diagnostic, DiagnosticSeverity
from aayu.compiler.semantic.scope_pass import ScopePass

class TypePass:
    """
    Phase 12.0 Semantic Pipeline - Pass 3: Type Resolver
    Responsible for inferring and checking types of expressions.
    Annotates AST nodes with a `.expr_type` property.
    """
    def __init__(self, diag_engine: DiagnosticEngine, scope_pass: ScopePass):
        self.diag_engine = diag_engine
        self.node_scopes = scope_pass.node_scopes
        self.global_scope = scope_pass.global_scope
        self.node_types = {}

    def run(self, ast: ASTNode):
        self._visit(ast, self.global_scope)

    def _visit(self, node: ASTNode, current_scope: SymbolTable) -> str:
        if not node:
            return "unknown"
            
        if id(node) in self.node_scopes:
            current_scope = self.node_scopes[id(node)]
            
        method_name = f'_visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self._default_visit)
        expr_type = visitor(node, current_scope)
        
        # Annotate node with inferred type in lookup table since AST is frozen
        self.node_types[id(node)] = expr_type
        return expr_type

    def _default_visit(self, node: ASTNode, current_scope: SymbolTable) -> str:
        for key, value in vars(node).items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        self._visit(item, current_scope)
            elif isinstance(value, ASTNode):
                self._visit(value, current_scope)
        return "void"

    def _visit_LiteralNode(self, node: LiteralNode, current_scope: SymbolTable) -> str:
        if isinstance(node.value, int) and not isinstance(node.value, bool):
            return "int"
        if isinstance(node.value, float):
            return "float"
        if isinstance(node.value, str):
            return "string"
        if isinstance(node.value, bool):
            return "bool"
        return "unknown"

    def _visit_IdentifierNode(self, node: IdentifierNode, current_scope: SymbolTable) -> str:
        sym = current_scope.resolve(node.name)
        if sym and sym.data_type:
            return sym.data_type
        return "any"

    def _visit_BinaryOpNode(self, node: BinaryOpNode, current_scope: SymbolTable) -> str:
        left_type = self._visit(node.left, current_scope)
        right_type = self._visit(node.right, current_scope)
        
        if node.operator in ['+', '-', '*', '/']:
            if left_type == "int" and right_type == "int":
                return "int"
            if left_type in ["int", "float"] and right_type in ["int", "float"]:
                return "float"
            if node.operator == '+' and (left_type == "string" or right_type == "string"):
                return "string"
                
            # Type error if not dynamic
            if left_type not in ["any", "unknown"] and right_type not in ["any", "unknown"]:
                self.diag_engine.report(Diagnostic(
                    severity=DiagnosticSeverity.ERROR,
                    code="E201",
                    message=f"Unsupported operand types for '{node.operator}': '{left_type}' and '{right_type}'.",
                    line=node.line, column=node.column
                ))
            return "any"
            
        elif node.operator in ['==', '!=', '<', '>', '<=', '>=']:
            return "bool"
            
        return "any"

    def _visit_AssignmentNode(self, node: AssignmentNode, current_scope: SymbolTable) -> str:
        val_type = self._visit(node.value, current_scope)
        
        sym = current_scope.resolve(node.target)
        if sym:
            # If symbol has no type yet, infer it
            if not sym.data_type or sym.data_type == "Any":
                sym.data_type = val_type
            elif sym.data_type != val_type and val_type not in ["any", "Any"]:
                pass
                
        return "void"
