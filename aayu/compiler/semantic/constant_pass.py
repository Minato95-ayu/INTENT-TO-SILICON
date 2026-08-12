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
        changes = {}
        for key, value in vars(node).items():
            if isinstance(value, list):
                new_list = []
                changed = False
                for item in value:
                    if isinstance(item, ASTNode):
                        new_item = self._visit(item)
                        if id(new_item) != id(item):
                            changed = True
                        new_list.append(new_item)
                    else:
                        new_list.append(item)
                if changed:
                    changes[key] = new_list
            elif isinstance(value, dict):
                new_dict = {}
                changed = False
                for k, v in value.items():
                    if isinstance(v, ASTNode):
                        new_v = self._visit(v)
                        if id(new_v) != id(v):
                            changed = True
                        new_dict[k] = new_v
                    else:
                        new_dict[k] = v
                if changed:
                    changes[key] = new_dict
            elif isinstance(value, ASTNode):
                new_val = self._visit(value)
                if id(new_val) != id(value):
                    changes[key] = new_val
                
        if changes:
            new_node = dataclasses.replace(node, **changes)
            # Migrate metadata to the new node ID
            if id(node) in self.node_scopes:
                self.node_scopes[id(new_node)] = self.node_scopes[id(node)]
            if node.node_id in self.node_types:
                self.node_types[new_node.node_id] = self.node_types[node.node_id]
            return new_node
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
                folded = LiteralNode(line=node.line, column=node.column, value=val)
                # Keep track of type for HIR builder
                self.node_types[id(folded)] = type_name
                return folded
            except Exception:
                pass
                
        return dataclasses.replace(node, left=left, right=right)
