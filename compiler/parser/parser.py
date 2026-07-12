from typing import List, Optional
from compiler.lexer.tokens import Token, TokenType
from compiler.ast.nodes import (
    ProgramNode,
    StateDeclarationNode,
    LiteralNode,
    IdentifierNode,
    AssignmentNode,
    WidgetNode
)

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.length = len(tokens)

    def parse(self) -> ProgramNode:
        statements = []
        while not self._is_at_end():
            statements.append(self._parse_statement())
        return ProgramNode(line=1, column=1, statements=statements)

    def _parse_statement(self):
        if self._match(TokenType.KEYWORD, "state"):
            return self._parse_state_declaration()
        
        if self._match(TokenType.KEYWORD, "page"):
            return self._parse_widget("Page")
            
        # Fallback to general widget if identifier or keyword matches lowercase widget types
        if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
            # Wait, if it's an assignment like `a = 1`
            if self.pos + 1 < self.length and self.tokens[self.pos+1].type == TokenType.OPERATOR and self.tokens[self.pos+1].value == "=":
                return self._parse_assignment()
            
            # Or it's a child widget (e.g., `title "Hello"`)
            return self._parse_widget_generic()
            
        token = self._peek()
        raise ParserError(f"Unexpected token {token.value} at line {token.line}")

    def _parse_state_declaration(self):
        line, col = self._previous().line, self._previous().column
        
        name_token = self._consume(TokenType.IDENTIFIER, "Expect variable name after 'state'.")
        self._consume(TokenType.OPERATOR, "Expect '=' after variable name.", value="=")
        
        value = self._parse_expression()
        
        return StateDeclarationNode(line=line, column=col, name=name_token.value, value=value)

    def _parse_assignment(self):
        line, col = self._peek().line, self._peek().column
        name_token = self._consume(TokenType.IDENTIFIER, "Expect identifier.")
        self._consume(TokenType.OPERATOR, "Expect '='.", value="=")
        value = self._parse_expression()
        return AssignmentNode(line=line, column=col, target=name_token.value, value=value)

    def _parse_expression(self):
        if self._match(TokenType.NUMBER):
            return LiteralNode(line=self._previous().line, column=self._previous().column, value=self._previous().value)
        if self._match(TokenType.STRING):
            return LiteralNode(line=self._previous().line, column=self._previous().column, value=self._previous().value)
        if self._match(TokenType.IDENTIFIER):
            return IdentifierNode(line=self._previous().line, column=self._previous().column, name=self._previous().value)
            
        token = self._peek()
        raise ParserError(f"Expect expression, got {token.type} at line {token.line}")

    def _parse_widget(self, w_type: str):
        line, col = self._previous().line, self._previous().column
        
        name_token = self._consume(TokenType.IDENTIFIER, "Expect widget name.")
        props = {"name": name_token.value}
        children = []
        
        while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
            children.append(self._parse_statement())
            
        self._consume(TokenType.KEYWORD, "Expect 'end' after widget block.", value="end")
        
        return WidgetNode(line=line, column=col, widget_type=w_type, props=props, children=children)

    def _parse_widget_generic(self):
        token = self._advance()
        line, col = token.line, token.column
        w_type = token.value
        
        props = {}
        children = []
        
        # very simple property parsing for tests (e.g. `title "Hello"`)
        if self._match(TokenType.STRING):
            props["text"] = self._previous().value
            
        return WidgetNode(line=line, column=col, widget_type=w_type, props=props, children=children)

    # Helper methods
    def _peek(self) -> Token:
        return self.tokens[self.pos]

    def _previous(self) -> Token:
        return self.tokens[self.pos - 1]

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _check(self, t_type: TokenType, value: str = None) -> bool:
        if self._is_at_end(): return False
        if self._peek().type != t_type: return False
        if value is not None and self._peek().value != value: return False
        return True

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.pos += 1
        return self._previous()

    def _match(self, t_type: TokenType, value: str = None) -> bool:
        if self._check(t_type, value):
            self._advance()
            return True
        return False

    def _consume(self, t_type: TokenType, message: str, value: str = None) -> Token:
        if self._check(t_type, value):
            return self._advance()
        raise ParserError(f"{message} at line {self._peek().line}")
