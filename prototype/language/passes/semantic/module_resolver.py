from ast_nodes import ModuleDeclarationNode
from ..base import ASTVisitorPass

class ModuleResolverPass(ASTVisitorPass):
    def __init__(self):
        super().__init__("ModuleResolverPass")
        
    def visit_ModuleDeclarationNode(self, node: ModuleDeclarationNode):
        if node.name != self.context.current_module:
            self.context.diagnostics.error(
                f"Module name mismatch: expected '{self.context.current_module}', got '{node.name}'", 
                self.context.current_module
            )
