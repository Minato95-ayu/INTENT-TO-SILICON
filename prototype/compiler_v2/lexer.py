"""
Aayu Lexer (Sprint 21)

Converts raw Aayu ADL (.aayu) source code into a linear stream of tokens.
Intentionally "boring" and unambiguous. Skips empty lines and comments.
"""

from enum import Enum, auto
from dataclasses import dataclass
import re
from typing import List


class TokenType(Enum):
    # Keywords
    SYSTEM = auto()
    DOMAINS = auto()
    SHARED = auto()
    ENTITIES = auto()
    FEATURES = auto()
    RELATIONS = auto()
    
    # Symbols
    COLON = auto()
    ARROW = auto()
    LPAREN = auto()
    RPAREN = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Structural
    NEWLINE = auto()
    EOF = auto()
    UNKNOWN = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    
    def __repr__(self):
        if self.type in (TokenType.SYSTEM, TokenType.DOMAINS, TokenType.SHARED, 
                         TokenType.ENTITIES, TokenType.FEATURES, TokenType.RELATIONS,
                         TokenType.COLON, TokenType.ARROW, TokenType.NEWLINE, TokenType.EOF):
            # For exact matches, just print the type name
            if self.type == TokenType.NEWLINE:
                return "NEWLINE"
            if self.type == TokenType.EOF:
                return "EOF"
            if self.type == TokenType.COLON:
                return "COLON"
            if self.type == TokenType.ARROW:
                return "ARROW"
            if self.type == TokenType.LPAREN:
                return "LPAREN"
            if self.type == TokenType.RPAREN:
                return "RPAREN"
            return self.type.name
        else:
            return f"{self.type.name}({self.value})"


class Lexer:
    KEYWORDS = {
        "system": TokenType.SYSTEM,
        "domains": TokenType.DOMAINS,
        "shared": TokenType.SHARED,
        "entities": TokenType.ENTITIES,
        "features": TokenType.FEATURES,
        "relations": TokenType.RELATIONS
    }

    def __init__(self, source_code: str):
        self.source_code = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def _advance(self, steps=1):
        for _ in range(steps):
            if self.pos < len(self.source_code):
                if self.source_code[self.pos] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1

    def _peek(self, offset=0):
        idx = self.pos + offset
        if idx >= len(self.source_code):
            return '\0'
        return self.source_code[idx]

    def tokenize(self) -> List[Token]:
        emitted_tokens_on_current_line = False

        while self.pos < len(self.source_code):
            c = self._peek()

            # Handle Whitespace (ignore spaces and tabs)
            if c in (' ', '\t'):
                self._advance()
                continue

            # Handle Comments
            if c == '#':
                while self._peek() != '\n' and self._peek() != '\0':
                    self._advance()
                continue

            # Handle Newlines
            if c == '\n':
                if emitted_tokens_on_current_line:
                    self.tokens.append(Token(TokenType.NEWLINE, "\\n", self.line, self.column))
                    emitted_tokens_on_current_line = False
                self._advance()
                continue

            # Handle Symbols
            if c == ':':
                self.tokens.append(Token(TokenType.COLON, ":", self.line, self.column))
                self._advance()
                emitted_tokens_on_current_line = True
                continue
                
            if c == '-' and self._peek(1) == '>':
                self.tokens.append(Token(TokenType.ARROW, "->", self.line, self.column))
                self._advance(2)
                emitted_tokens_on_current_line = True
                continue

            if c == '(':
                self.tokens.append(Token(TokenType.LPAREN, "(", self.line, self.column))
                self._advance()
                emitted_tokens_on_current_line = True
                continue
                
            if c == ')':
                self.tokens.append(Token(TokenType.RPAREN, ")", self.line, self.column))
                self._advance()
                emitted_tokens_on_current_line = True
                continue

            # Handle Identifiers and Keywords
            if c.isalpha() or c == '_':
                start_col = self.column
                start_pos = self.pos
                while self._peek().isalnum() or self._peek() == '_':
                    self._advance()
                
                value = self.source_code[start_pos:self.pos]
                
                # Check if it's a keyword
                token_type = self.KEYWORDS.get(value, TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, value, self.line, start_col))
                emitted_tokens_on_current_line = True
                continue

            # Handle Unknown characters
            self.tokens.append(Token(TokenType.UNKNOWN, c, self.line, self.column))
            self._advance()
            emitted_tokens_on_current_line = True

        # Ensure we always end with an EOF token, and maybe a NEWLINE before it
        if emitted_tokens_on_current_line:
            self.tokens.append(Token(TokenType.NEWLINE, "\\n", self.line, self.column))
            
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        
        return self.tokens
