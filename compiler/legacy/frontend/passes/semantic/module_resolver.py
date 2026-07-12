"""
=============================================================================
FILE: module_resolver.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from compiler.frontend.ast_nodes import ModuleDeclarationNode
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
