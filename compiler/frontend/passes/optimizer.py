"""
=============================================================================
FILE: optimizer.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from .base import ASTTransformerPass
from compiler.frontend.ast_nodes import *

class StaticOptimizerPass(ASTTransformerPass):
    def __init__(self):
        super().__init__("Static Optimizer Pass")

    def visit_BinaryExpressionNode(self, node: BinaryExpressionNode) -> Node:
        # Optimize children first
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        
        # Constant Folding
        if isinstance(node.left, NumberNode) and isinstance(node.right, NumberNode):
            try:
                # We can fold simple numeric operations
                if node.operator == "+":
                    res = node.left.value + node.right.value
                    return NumberNode(res, span=node.span)
                elif node.operator == "-":
                    res = node.left.value - node.right.value
                    return NumberNode(res, span=node.span)
                elif node.operator == "*":
                    res = node.left.value * node.right.value
                    return NumberNode(res, span=node.span)
                elif node.operator == "/":
                    if node.right.value != 0:
                        res = node.left.value / node.right.value
                        return NumberNode(res, span=node.span)
            except Exception:
                pass # Fallback to not folding if it fails
        
        return node
        
    def visit_UnaryExpressionNode(self, node: UnaryExpressionNode) -> Node:
        node.right = self.visit(node.right)
        
        # Constant Folding
        if isinstance(node.right, NumberNode):
            if node.operator == "-":
                return NumberNode(-node.right.value, span=node.span)
            
        return node

    def visit_IfNode(self, node: IfNode) -> Node:
        node.condition = self.visit(node.condition)
        
        # Check if condition is a constant NumberNode (e.g., 1 or 0)
        if isinstance(node.condition, NumberNode):
            is_truthy = node.condition.value != 0
            if is_truthy:
                # Replace the entire IfNode with its body
                return BlockNode(statements=self.visit(BlockNode(statements=node.body)).statements)
            else:
                if node.else_body:
                    return BlockNode(statements=self.visit(BlockNode(statements=node.else_body)).statements)
                else:
                    return BlockNode(statements=[]) # Empty block for dead code
                    
        # Otherwise keep the IfNode and visit its branches
        node.body = self.visit(BlockNode(statements=node.body)).statements
        if node.else_body:
            node.else_body = self.visit(BlockNode(statements=node.else_body)).statements
        return node

    def visit_BlockNode(self, node: BlockNode) -> Node:
        # Dead Code Elimination within a block
        new_statements = []
        for stmt in node.statements:
            new_stmt = self.visit(stmt)
            if new_stmt is not None:
                new_statements.append(new_stmt)
            
            # If the statement is a Return, Throw, or Panic, stop appending (DCE)
            if isinstance(new_stmt, (ReturnNode, ThrowNode, PanicNode)):
                break
                
        node.statements = new_statements
        return node
        
    def visit_FunctionDeclNode(self, node: FunctionDeclNode) -> Node:
        node.body = self.visit(BlockNode(statements=node.body)).statements
        return node
