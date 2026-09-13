import sys

with open("compiler/parser/parser.py", "r", encoding="utf-8") as f:
    content = f.read()

import_ast = "from compiler.ast.nodes import ("
import_new = "from compiler.ast.nodes import (InsertNode, FindNode, RespondNode, "
content = content.replace(import_ast, import_new)

parse_statement = """    def _parse_statement(self):"""
new_statements = """    def _parse_statement(self):
        if self._match(TokenType.KEYWORD, "insert"):
            line, col = self._previous().line, self._previous().column
            model_name = self._consume(TokenType.IDENTIFIER, "Expect model name after insert.").value
            self._consume(TokenType.SYMBOL, "Expect '{'", value="{")
            fields = {}
            while not self._check(TokenType.SYMBOL) or self._peek().value != "}":
                key = self._consume(TokenType.IDENTIFIER, "Expect field name in insert.").value
                self._consume(TokenType.OPERATOR, "Expect '=' after field name.", value="=")
                value = self._parse_expression()
                fields[key] = value
            self._consume(TokenType.SYMBOL, "Expect '}' after insert fields.", value="}")
            return InsertNode(line=line, column=col, model_name=model_name, fields=fields)

        if self._match(TokenType.KEYWORD, "respond"):
            line, col = self._previous().line, self._previous().column
            value = self._parse_expression()
            return RespondNode(line=line, column=col, value=value)
"""
content = content.replace(parse_statement, new_statements)

parse_expression = """    def _parse_expression(self):"""
new_expressions = """    def _parse_expression(self):
        if self._match(TokenType.KEYWORD, "find"):
            line, col = self._previous().line, self._previous().column
            model_name = self._consume(TokenType.IDENTIFIER, "Expect model name after find.").value
            return FindNode(line=line, column=col, model_name=model_name)
"""
content = content.replace(parse_expression, new_expressions)

with open("compiler/parser/parser.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Parser Patched!")
