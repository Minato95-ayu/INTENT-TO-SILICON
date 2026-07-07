"""
=============================================================================
FILE: base.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from typing import Any
from compiler.frontend.compiler_context import CompilerContext
from compiler.frontend.ast_nodes import Node

class BasePass:
    def __init__(self, name: str):
        self.name = name

    def run(self, context: CompilerContext) -> bool:
        """
        Execute the pass.
        Returns True if successful, False if there were errors.
        Errors should be reported to context.diagnostics.
        """
        raise NotImplementedError()

class ASTVisitorPass(BasePass):
    """Base class for passes that need to visit the AST nodes"""
    
    def run(self, context: CompilerContext) -> bool:
        if not context.current_module:
            raise Exception("ASTVisitorPass requires context.current_module to be set")
            
        ast = context.asts.get(context.current_module)
        if not ast:
            context.diagnostics.error(f"No AST found for module {context.current_module}", context.current_module)
            return False
            
        self.context = context
        self.visit(ast)
        return not context.diagnostics.has_errors()

    def visit(self, node: Node):
        if node is None:
            return None
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: Node):
        for attr, value in vars(node).items():
            if isinstance(value, Node):
                self.visit(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, Node):
                        self.visit(item)

class ASTTransformerPass(BasePass):
    """Base class for passes that transform AST nodes"""
    
    def run(self, context: CompilerContext) -> bool:
        if not context.current_module:
            raise Exception("ASTTransformerPass requires context.current_module to be set")
            
        ast = context.asts.get(context.current_module)
        if not ast:
            context.diagnostics.error(f"No AST found for module {context.current_module}", context.current_module)
            return False
            
        self.context = context
        new_ast = self.visit(ast)
        context.asts[context.current_module] = new_ast
        return not context.diagnostics.has_errors()

    def visit(self, node: Node) -> Node:
        if node is None:
            return None
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: Node) -> Node:
        for attr, value in vars(node).items():
            if isinstance(value, Node):
                new_value = self.visit(value)
                setattr(node, attr, new_value)
            elif isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, Node):
                        new_item = self.visit(item)
                        if new_item is not None:
                            new_list.append(new_item)
                    else:
                        new_list.append(item)
                setattr(node, attr, new_list)
        return node
