"""
=============================================================================
FILE: lexer.py
PURPOSE: Lexical Analysis - Tokenizes AAYU source code
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles lexical analysis - tokenizes aayu source code.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import re
from typing import List, Any

class TokenType:
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    EQUALS = "EQUALS"
    COMMA = "COMMA"
    NEWLINE = "NEWLINE"
    EOF = "EOF"

class Token:
    def __init__(self, type: str, value: Any, line: int):
        self.type = type
        self.value = value
        self.line = line
        
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class ManifestLexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.tokens = []

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            char = self.source[self.pos]
            
            if char in ' \t\r':
                self.pos += 1
                continue
                
            if char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, "\n", self.line))
                self.line += 1
                self.pos += 1
                continue
                
            if char == '#':
                while self.pos < len(self.source) and self.source[self.pos] != '\n':
                    self.pos += 1
                continue
                
            if char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, "[", self.line))
                self.pos += 1
                continue
                
            if char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, "]", self.line))
                self.pos += 1
                continue
                
            if char == '=':
                self.tokens.append(Token(TokenType.EQUALS, "=", self.line))
                self.pos += 1
                continue
                
            if char == ',':
                self.tokens.append(Token(TokenType.COMMA, ",", self.line))
                self.pos += 1
                continue
                
            if char == '"':
                self.pos += 1
                start = self.pos
                while self.pos < len(self.source) and self.source[self.pos] != '"':
                    if self.source[self.pos] == '\n':
                        raise ValueError(f"Unterminated string literal at line {self.line}")
                    self.pos += 1
                val = self.source[start:self.pos]
                self.tokens.append(Token(TokenType.STRING, val, self.line))
                self.pos += 1
                continue
                
            if char.isalpha() or char == '_':
                start = self.pos
                while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] in '_-'):
                    self.pos += 1
                val = self.source[start:self.pos]
                self.tokens.append(Token(TokenType.IDENTIFIER, val, self.line))
                continue
                
            raise ValueError(f"Unexpected character '{char}' at line {self.line}")
            
        self.tokens.append(Token(TokenType.EOF, None, self.line))
        return self.tokens
