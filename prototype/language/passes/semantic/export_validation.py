from ast_nodes import FunctionDeclNode, DeclarationNode
from ..base import ASTVisitorPass

class ExportValidationPass(ASTVisitorPass):
    def __init__(self):
        super().__init__("ExportValidationPass")
        
    def visit_FunctionDeclNode(self, node: FunctionDeclNode):
        # We could validate that exported functions don't reference private modules or types
        # Currently, just a stub
        self.generic_visit(node)

    def visit_DeclarationNode(self, node: DeclarationNode):
        # Validate variable exports
        self.generic_visit(node)
