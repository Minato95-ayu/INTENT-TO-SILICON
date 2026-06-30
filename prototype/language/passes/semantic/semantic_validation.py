from ast_nodes import FunctionDeclNode
from ..base import ASTVisitorPass

class SemanticValidationPass(ASTVisitorPass):
    def __init__(self):
        super().__init__("SemanticValidationPass")
        
    def visit_FunctionDeclNode(self, node: FunctionDeclNode):
        # E.g. Check return paths
        self.generic_visit(node)
