from typing import List, Optional, Any
from .lexer import ManifestLexer, Token, TokenType
from .ast import ManifestDocument, SectionNode, KeyValueNode

class ManifestParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]
        
    def peek(self) -> Token:
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return self.tokens[-1]
        
    def advance(self) -> Token:
        tok = self.current()
        self.pos += 1
        return tok
        
    def match(self, token_type: str) -> bool:
        if self.current().type == token_type:
            self.advance()
            return True
        return False
        
    def expect(self, token_type: str) -> Token:
        if self.current().type == token_type:
            return self.advance()
        raise ValueError(f"Expected {token_type} at line {self.current().line}, got {self.current().type}")

    def parse(self) -> ManifestDocument:
        doc = ManifestDocument()
        
        while self.current().type != TokenType.EOF:
            if self.match(TokenType.NEWLINE):
                continue
                
            if self.current().type == TokenType.LBRACKET:
                section = self.parse_section()
                doc.add_section(section)
            else:
                raise ValueError(f"Expected section start '[' at line {self.current().line}, got {self.current().type}")
                
        return doc
        
    def parse_section(self) -> SectionNode:
        line = self.current().line
        self.expect(TokenType.LBRACKET)
        name_tok = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.RBRACKET)
        
        section = SectionNode(name_tok.value, line)
        
        # Skip trailing newlines on the section header line
        while self.match(TokenType.NEWLINE):
            pass
            
        while self.current().type not in (TokenType.LBRACKET, TokenType.EOF):
            if self.match(TokenType.NEWLINE):
                continue
            
            key_tok = self.expect(TokenType.IDENTIFIER)
            self.expect(TokenType.EQUALS)
            
            val = self.parse_value()
            section.add_entry(KeyValueNode(key_tok.value, val, key_tok.line))
            
            # Require newline or EOF after a value
            if self.current().type != TokenType.EOF:
                self.expect(TokenType.NEWLINE)
                
        return section
        
    def parse_value(self) -> Any:
        tok = self.current()
        if tok.type == TokenType.STRING:
            self.advance()
            return tok.value
        elif tok.type == TokenType.LBRACKET:
            # Parse array
            self.advance()
            arr = []
            while self.current().type != TokenType.RBRACKET:
                if self.match(TokenType.NEWLINE):
                    continue
                arr.append(self.parse_value())
                if self.current().type == TokenType.COMMA:
                    self.advance()
                elif self.current().type != TokenType.RBRACKET:
                    break
            self.expect(TokenType.RBRACKET)
            return arr
        else:
            raise ValueError(f"Expected value at line {tok.line}, got {tok.type}")
