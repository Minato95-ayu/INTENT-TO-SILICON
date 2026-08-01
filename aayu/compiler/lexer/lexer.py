import re
from typing import List
from .tokens import Token, TokenType, KEYWORDS, OPERATORS, SYMBOLS

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.length = len(source)

    def tokenize(self) -> List[Token]:
        tokens = []
        while self.pos < self.length:
            char = self.source[self.pos]

            if char.isspace():
                self._advance()
                continue

            if char == '#':
                self._skip_comment()
                continue

            if char.isalpha() or char == '_' or char == '$':
                tokens.append(self._read_identifier())
                continue

            if char.isdigit():
                tokens.append(self._read_number())
                continue

            if char in '"\'':
                tokens.append(self._read_string(char))
                continue

            # Check 2-char operators
            if self.pos + 1 < self.length:
                two_char = self.source[self.pos:self.pos+2]
                if two_char in OPERATORS:
                    tokens.append(Token(TokenType.OPERATOR, two_char, self.line, self.column, self._get_source_line(self.line)))
                    self._advance()
                    self._advance()
                    continue

            if char in OPERATORS:
                tokens.append(Token(TokenType.OPERATOR, char, self.line, self.column, self._get_source_line(self.line)))
                self._advance()
                continue

            if char == '@':
                if self.pos + 1 < self.length and self.source[self.pos + 1].isspace():
                    from aayu.compiler.errors import CompilerError
                    raise CompilerError("Space not allowed after '@'", self.line, self.column, self._get_source_line(self.line))
                tokens.append(Token(TokenType.SYMBOL, char, self.line, self.column, self._get_source_line(self.line)))
                self._advance()
                continue

            if char in SYMBOLS:
                tokens.append(Token(TokenType.SYMBOL, char, self.line, self.column, self._get_source_line(self.line)))
                self._advance()
                continue

            from aayu.compiler.errors import CompilerError
            raise CompilerError(f"Unexpected character '{char}'", self.line, self.column, self._get_source_line(self.line))

        tokens.append(Token(TokenType.EOF, "", self.line, self.column, self._get_source_line(self.line)))
        return tokens

    def _advance(self):
        if self.pos < self.length:
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 0
            self.pos += 1
            self.column += 1

    def _skip_comment(self):
        while self.pos < self.length and self.source[self.pos] != '\n':
            self._advance()

    def _read_identifier(self) -> Token:
        start_col = self.column
        val = ""
        while self.pos < self.length and (self.source[self.pos].isalnum() or self.source[self.pos] == '_' or self.source[self.pos] == '$'):
            val += self.source[self.pos]
            self._advance()
            
        token_type = TokenType.KEYWORD if val in KEYWORDS else TokenType.IDENTIFIER
        return Token(token_type, val, self.line, start_col)

    def _read_number(self) -> Token:
        start_col = self.column
        val = ""
        while self.pos < self.length:
            if self.source[self.pos].isdigit():
                val += self.source[self.pos]
                self._advance()
            elif self.source[self.pos] == '.':
                if self.pos + 1 < self.length and self.source[self.pos + 1].isdigit():
                    val += self.source[self.pos]
                    self._advance()
                else:
                    break
            else:
                break
            
        # Check for CSS-like units
        has_unit = False
        while self.pos < self.length and (self.source[self.pos].isalpha() or self.source[self.pos] == '%'):
            val += self.source[self.pos]
            has_unit = True
            self._advance()
            
        token_type = TokenType.STRING if has_unit else TokenType.NUMBER
        return Token(token_type, val, self.line, start_col, self._get_source_line(self.line))

    def _read_string(self, quote: str) -> Token:
        start_col = self.column
        self._advance() # skip quote
        val = ""
        while self.pos < self.length and self.source[self.pos] != quote:
            val += self.source[self.pos]
            self._advance()
            
        if self.pos < self.length:
            self._advance() # skip closing quote
            
        return Token(TokenType.STRING, val, self.line, start_col, self._get_source_line(self.line))

    def _get_source_line(self, line_no: int) -> str:
        lines = self.source.split('\n')
        if 1 <= line_no <= len(lines):
            return lines[line_no - 1]
        return ""
