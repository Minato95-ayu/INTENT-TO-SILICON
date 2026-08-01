with open('compiler/parser/parser.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Flatten statements in parse()
old_parse = '''    def parse(self) -> ProgramNode:
        statements = []
        while not self._is_at_end():
            statements.append(self._parse_statement())
        return ProgramNode(line=1, column=1, statements=statements)'''

new_parse = '''    def parse(self) -> ProgramNode:
        statements = []
        while not self._is_at_end():
            stmt = self._parse_statement()
            if isinstance(stmt, list):
                statements.extend(stmt)
            else:
                statements.append(stmt)
        return ProgramNode(line=1, column=1, statements=statements)'''
content = content.replace(old_parse, new_parse)

old_state = '''    def _parse_state_declaration(self):
        line, col = self._previous().line, self._previous().column
        
        name_token = self._consume(TokenType.IDENTIFIER, "Expect variable name after 'state'.")
        self._consume(TokenType.OPERATOR, "Expect '=' after variable name.", value="=")
        
        value = self._parse_expression()
        
        return StateDeclarationNode(line=line, column=col, name=name_token.value, value=value)'''

new_state = '''    def _parse_state_declaration(self):
        line, col = self._previous().line, self._previous().column
        
        if self._match(TokenType.SYMBOL, "{"):
            decls = []
            while not self._check(TokenType.SYMBOL, "}") and not self._is_at_end():
                name_token = self._consume(TokenType.IDENTIFIER, "Expect variable name in state block.")
                self._consume(TokenType.OPERATOR, "Expect '=' after variable name.", value="=")
                value = self._parse_expression()
                decls.append(StateDeclarationNode(line=name_token.line, column=name_token.column, name=name_token.value, value=value))
            self._consume(TokenType.SYMBOL, "Expect '}' after state block.", value="}")
            return decls
        else:
            name_token = self._consume(TokenType.IDENTIFIER, "Expect variable name after 'state'.")
            self._consume(TokenType.OPERATOR, "Expect '=' after variable name.", value="=")
            value = self._parse_expression()
            return StateDeclarationNode(line=line, column=col, name=name_token.value, value=value)'''

content = content.replace(old_state, new_state)

with open('compiler/parser/parser.py', 'w', encoding='utf-8') as f:
    f.write(content)
