from typing import Any
from compiler_context import CompilerContext
from ast_nodes import Node

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
