"""
=============================================================================
FILE: linter.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from aayu.compiler.ast_nodes import *
from aayu.compiler.passes.base import BasePass
from aayu.compiler.location import SourceSpan
import re

class LintMessage:
    def __init__(self, severity: str, message: str, line: int = -1, column: int = -1, filename: str = ""):
        self.severity = severity # "ERROR", "WARNING", "INFO"
        self.message = message
        self.line = line
        self.column = column
        self.filename = filename

    def to_dict(self):
        return {
            "severity": self.severity,
            "message": self.message,
            "line": self.line,
            "column": self.column,
            "filename": self.filename
        }

    def __str__(self):
        loc = f"{self.filename}:{self.line}:{self.column}" if self.line > 0 else self.filename
        return f"[{self.severity}] {loc} - {self.message}"

class AAYULinter(BasePass):
    def __init__(self, filename=""):
        super().__init__("AAYU Linter")
        self.filename = filename
        self.messages = []
        self.in_function = False

    def add_msg(self, severity, message, node):
        line = -1
        col = -1
        if hasattr(node, 'span') and node.span:
            line = node.span.start_line
            col = node.span.start_column
        elif hasattr(node, 'line'):
            line = node.line
        self.messages.append(LintMessage(severity, message, line, col, self.filename))

    def error(self, msg, node):
        self.add_msg("ERROR", msg, node)

    def warning(self, msg, node):
        self.add_msg("WARNING", msg, node)

    def info(self, msg, node):
        self.add_msg("INFO", msg, node)

    def lint(self, node: Node):
        self.messages = []
        self.visit(node)
        return self.messages

    def visit(self, node: Node):
        if not node:
            return
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        visitor(node)

    def generic_visit(self, node):
        # Fallback to traversing children if they are AST nodes
        if hasattr(node, '__dict__'):
            for field, value in vars(node).items():
                if isinstance(value, list):
                    for item in value:
                        if hasattr(item, '__class__'):
                            self.visit(item)
                elif hasattr(value, '__class__'):
                    self.visit(value)

    # Naming Conventions
    def _check_snake_case(self, name: str, node: Node, entity_type: str):
        if name and name[0].isupper():
            self.warning(f"{entity_type} '{name}' should start with a lowercase letter.", node)

    def _check_camel_or_pascal_case(self, name: str, node: Node, entity_type: str):
        if name and name[0].islower():
            self.warning(f"{entity_type} '{name}' should start with an uppercase letter.", node)

    def visit_DeclarationNode(self, node: DeclarationNode):
        self._check_snake_case(node.name, node, "Variable")
        self.visit(node.value)

    def visit_FunctionDeclNode(self, node: FunctionDeclNode):
        self._check_snake_case(node.name, node, "Function")
        if len(node.parameters) > 5:
            self.warning(f"Function '{node.name}' has too many parameters ({len(node.parameters)} > 5).", node)
        
        if len(node.body) > 50:
            self.warning(f"Function '{node.name}' is too long ({len(node.body)} statements > 50). Consider refactoring.", node)
            
        self._check_dead_code(node.body)

        for stmt in node.body:
            self._check_useless_expression(stmt)
            self.visit(stmt)

    def visit_RecordDeclarationNode(self, node: RecordDeclarationNode):
        self._check_camel_or_pascal_case(node.name, node, "Record")

    def visit_InterfaceDeclNode(self, node: InterfaceDeclNode):
        self._check_camel_or_pascal_case(node.name, node, "Interface")

    # Empty Blocks
    def visit_IfNode(self, node: IfNode):
        self.visit(node.condition)
        if not node.body:
            self.warning("Empty 'if' block.", node)
        else:
            self._check_dead_code(node.body)
            for stmt in node.body:
                self._check_useless_expression(stmt)
                self.visit(stmt)
                
        if node.else_body is not None:
            if not node.else_body:
                self.warning("Empty 'else' block.", node)
            else:
                self._check_dead_code(node.else_body)
                for stmt in node.else_body:
                    self._check_useless_expression(stmt)
                    self.visit(stmt)

    def visit_WhileNode(self, node: WhileNode):
        self.visit(node.condition)
        if not node.body:
            self.warning("Empty 'while' block.", node)
        else:
            self._check_dead_code(node.body)
            for stmt in node.body:
                self._check_useless_expression(stmt)
                self.visit(stmt)

    def visit_ForRangeNode(self, node: ForRangeNode):
        self.visit(node.start)
        self.visit(node.end)
        if not node.body:
            self.warning("Empty 'for' block.", node)
        else:
            self._check_dead_code(node.body)
            for stmt in node.body:
                self._check_useless_expression(stmt)
                self.visit(stmt)

    def visit_ForEachNode(self, node: ForEachNode):
        self.visit(node.collection)
        if not node.body:
            self.warning("Empty 'foreach' block.", node)
        else:
            self._check_dead_code(node.body)
            for stmt in node.body:
                self._check_useless_expression(stmt)
                self.visit(stmt)

    # Dead Code
    def _check_dead_code(self, body: list):
        if not body:
            return
        terminal_index = -1
        for i, stmt in enumerate(body):
            if isinstance(stmt, (ReturnNode, ThrowNode, PanicNode)):
                terminal_index = i
                break
        
        if terminal_index != -1 and terminal_index < len(body) - 1:
            self.warning("Unreachable code after return, throw, or panic.", body[terminal_index + 1])

    # Useless Expressions
    def visit_ProgramNode(self, node: ProgramNode):
        self._check_dead_code(node.statements)
        for stmt in node.statements:
            self._check_useless_expression(stmt)
            self.visit(stmt)

    def visit_BlockNode(self, node: BlockNode):
        self._check_dead_code(node.statements)
        for stmt in node.statements:
            self._check_useless_expression(stmt)
            self.visit(stmt)

    def _check_useless_expression(self, stmt: Node):
        if isinstance(stmt, (NumberNode, TextNode, VariableNode, BinaryExpressionNode, UnaryExpressionNode, LogicalExpressionNode, ReadExpressionNode)):
            self.warning("Useless expression evaluated but not used.", stmt)

