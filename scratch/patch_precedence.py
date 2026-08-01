with open('compiler/lexer/tokens.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

old_ops = '    "=", "+", "-", "*", "/", "+=", "-=", "==", "!=", ">", "<", ">=", "<="'
new_ops = '    "=", "+", "-", "*", "/", "%", "+=", "-=", "==", "!=", ">", "<", ">=", "<=", "&&", "||"'
content = content.replace(old_ops, new_ops)

with open('compiler/lexer/tokens.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('compiler/parser/parser.py', 'r', encoding='utf-8') as f:
    content = f.read()

# I need to find def _parse_expression(self): and replace the parser logic.
# Currently it points to _parse_term()
old_expr = '''    def _parse_expression(self):
        return self._parse_term()'''

new_expr = '''    def _parse_expression(self):
        return self._parse_logical_or()

    def _parse_logical_or(self):
        expr = self._parse_logical_and()
        while self._match(TokenType.OPERATOR, "||"):
            operator = self._previous().value
            right = self._parse_logical_and()
            from aayu.compiler.ast.nodes import BinaryOpNode
            expr = BinaryOpNode(line=expr.line, column=expr.column, left=expr, operator=operator, right=right)
        return expr

    def _parse_logical_and(self):
        expr = self._parse_equality()
        while self._match(TokenType.OPERATOR, "&&"):
            operator = self._previous().value
            right = self._parse_equality()
            from aayu.compiler.ast.nodes import BinaryOpNode
            expr = BinaryOpNode(line=expr.line, column=expr.column, left=expr, operator=operator, right=right)
        return expr

    def _parse_equality(self):
        expr = self._parse_comparison()
        while self._match(TokenType.OPERATOR, "==") or self._match(TokenType.OPERATOR, "!="):
            operator = self._previous().value
            right = self._parse_comparison()
            from aayu.compiler.ast.nodes import BinaryOpNode
            expr = BinaryOpNode(line=expr.line, column=expr.column, left=expr, operator=operator, right=right)
        return expr

    def _parse_comparison(self):
        expr = self._parse_term()
        while self._match(TokenType.OPERATOR, ">") or self._match(TokenType.OPERATOR, ">=") or self._match(TokenType.OPERATOR, "<") or self._match(TokenType.OPERATOR, "<="):
            operator = self._previous().value
            right = self._parse_term()
            from aayu.compiler.ast.nodes import BinaryOpNode
            expr = BinaryOpNode(line=expr.line, column=expr.column, left=expr, operator=operator, right=right)
        return expr'''

content = content.replace(old_expr, new_expr)

# Fix factor to include %
old_factor = '''    def _parse_factor(self):
        expr = self._parse_primary()
        while self._match(TokenType.OPERATOR, "*") or self._match(TokenType.OPERATOR, "/"):'''

new_factor = '''    def _parse_factor(self):
        expr = self._parse_primary()
        while self._match(TokenType.OPERATOR, "*") or self._match(TokenType.OPERATOR, "/") or self._match(TokenType.OPERATOR, "%"):'''

content = content.replace(old_factor, new_factor)

with open('compiler/parser/parser.py', 'w', encoding='utf-8') as f:
    f.write(content)
