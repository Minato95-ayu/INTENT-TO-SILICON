import dataclasses
from aayu.compiler.ast.nodes import (
    ASTNode, LiteralNode, BinaryOpNode
)
from aayu.compiler.semantic.diagnostics import DiagnosticEngine
from aayu.compiler.semantic.scope_pass import ScopePass

class ConstantPass:
    """
    Phase 12.0 Semantic Pipeline - Pass 4: Constant Evaluator
    Responsible for folding constant expressions in the AST before HIR generation.
    Returns a new immutable AST.
    """
    def __init__(self, diag_engine: DiagnosticEngine, scope_pass: ScopePass):
        self.diag_engine = diag_engine
        self.node_scopes = scope_pass.node_scopes
        self.global_scope = scope_pass.global_scope
        self.node_types = getattr(scope_pass, 'node_types', {})

    def run(self, ast: ASTNode) -> ASTNode:
        return self._visit(ast)

    def _visit(self, node: ASTNode) -> ASTNode:
        if not node:
            return node
            
        method_name = f'_visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self._default_visit)
        return visitor(node)

    def _default_visit(self, node: ASTNode) -> ASTNode:
        # Recursively fold children and create a new node if any changed
        changes = {}
        for key, value in vars(node).items():
            if isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, ASTNode):
                        new_list.append(self._visit(item))
                    else:
                        new_list.append(item)
                changes[key] = new_list
            elif isinstance(value, ASTNode):
                changes[key] = self._visit(value)
                
        if changes:
            return dataclasses.replace(node, **changes)
        return node

    def _visit_LiteralNode(self, node: LiteralNode) -> ASTNode:
        return node

    def _visit_BinaryOpNode(self, node: BinaryOpNode) -> ASTNode:
        left = self._visit(node.left)
        right = self._visit(node.right)
        
        if isinstance(left, LiteralNode) and isinstance(right, LiteralNode):
            try:
                # Basic constant folding
                if node.operator == '+':
                    val = left.value + right.value
                elif node.operator == '-':
                    val = left.value - right.value
                elif node.operator == '*':
                    val = left.value * right.value
                elif node.operator == '/':
                    if right.value == 0:
                        return dataclasses.replace(node, left=left, right=right)
                    val = left.value / right.value
                else:
                    return dataclasses.replace(node, left=left, right=right)
                    
                type_name = "float" if isinstance(val, float) else ("int" if isinstance(val, int) else "any")
                folded = LiteralNode(line=node.line, column=node.column, value=val, type_name=type_name)
                # Keep track of type for HIR builder
                self.node_types[id(folded)] = type_name
                return folded
            except Exception:
                pass
                
        return dataclasses.replace(node, left=left, right=right)
