import re

with open('compiler/parser/parser.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix InsertNode parsing
old_code = """            while not self._check(TokenType.SYMBOL) or self._peek().value != "}":
                key = self._consume(TokenType.IDENTIFIER, "Expect field name in insert.").value
                self._consume(TokenType.OPERATOR, "Expect '=' after field name.", value="=")
                value = self._parse_expression()
                fields[key] = value
            self._consume(TokenType.SYMBOL, "Expect '}' after insert fields.", value="}")"""

new_code = """            while not self._check(TokenType.SYMBOL) or self._peek().value != "}":
                key = self._consume(TokenType.IDENTIFIER, "Expect field name in insert.").value
                self._consume(TokenType.OPERATOR, "Expect '=' after field name.", value="=")
                value = self._parse_expression()
                fields[key] = value
                if self._match(TokenType.SYMBOL, ","):
                    pass # consume optional comma
            self._consume(TokenType.SYMBOL, "Expect '}' after insert fields.", value="}")"""

text = text.replace(old_code, new_code)

with open('compiler/parser/parser.py', 'w', encoding='utf-8') as f:
    f.write(text)
