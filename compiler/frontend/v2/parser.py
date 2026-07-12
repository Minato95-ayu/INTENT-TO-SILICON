"""
Aayu Parser (Sprint 22)

Converts a stream of Tokens from the Lexer into an Aayu Abstract Syntax Tree (AST).
Strictly validates syntax and ordering, but performs NO semantic analysis.
"""

from typing import List
from .lexer import Token, TokenType
from .ast_nodes import AayuAST, SystemNode, DomainNode, SharedNode, EntityNode, FeatureNode, RelationNode

class ParserError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"ParserError: {message} at Line {line}, Column {column}")


class AayuParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self, offset=0) -> Token:
        idx = self.pos + offset
        if idx >= len(self.tokens):
            return self.tokens[-1] # Return EOF token
        return self.tokens[idx]

    def _advance(self):
        if self.pos < len(self.tokens):
            self.pos += 1
        return self._peek(-1)

    def _consume(self, expected_type: TokenType, error_message: str) -> Token:
        token = self._peek()
        if token.type == expected_type:
            return self._advance()
        raise ParserError(error_message, token.line, token.column)

    def _skip_newlines(self):
        while self._peek().type == TokenType.NEWLINE:
            self._advance()

    def parse(self) -> AayuAST:
        self._skip_newlines()
        
        # 1. SYSTEM (Mandatory)
        sys_token = self._consume(TokenType.SYSTEM, "Expected 'system' declaration first")
        sys_name_token = self._consume(TokenType.IDENTIFIER, "Expected system name (identifier) after 'system'")
        
        system_node = SystemNode(line=sys_token.line, column=sys_token.column, name=sys_name_token.value)
        
        ast = AayuAST(system=system_node)
        
        # We enforce a strict section state machine:
        # 0: DOMAINS, 1: SHARED, 2: ENTITIES, 3: FEATURES, 4: RELATIONS, 5: DONE
        state = 0
        
        while self._peek().type != TokenType.EOF:
            self._skip_newlines()
            if self._peek().type == TokenType.EOF:
                break
                
            token = self._peek()
            
            if token.type == TokenType.DOMAINS:
                if state > 0:
                    raise ParserError("Out of order section: 'domains' must come after 'system' and before other sections", token.line, token.column)
                state = 1
                self._advance()
                self._consume(TokenType.COLON, "Expected ':' after 'domains'")
                self._parse_list_section(ast.domains, DomainNode)
                
            elif token.type == TokenType.SHARED:
                if state > 1:
                    raise ParserError("Out of order section: 'shared' must come before 'entities', 'features', or 'relations'", token.line, token.column)
                state = 2
                self._advance()
                self._consume(TokenType.COLON, "Expected ':' after 'shared'")
                self._parse_list_section(ast.shared, SharedNode)
                
            elif token.type == TokenType.ENTITIES:
                if state > 2:
                    raise ParserError("Out of order section: 'entities' must come before 'features' or 'relations'", token.line, token.column)
                state = 3
                self._advance()
                self._consume(TokenType.COLON, "Expected ':' after 'entities'")
                self._parse_list_section(ast.entities, EntityNode)
                
            elif token.type == TokenType.FEATURES:
                if state > 3:
                    raise ParserError("Out of order section: 'features' must come before 'relations'", token.line, token.column)
                state = 4
                self._advance()
                self._consume(TokenType.COLON, "Expected ':' after 'features'")
                self._parse_list_section(ast.features, FeatureNode)
                
            elif token.type == TokenType.RELATIONS:
                if state > 4:
                    raise ParserError("Multiple 'relations' sections not allowed", token.line, token.column)
                state = 5
                self._advance()
                self._consume(TokenType.COLON, "Expected ':' after 'relations'")
                self._parse_relations(ast.relations)
                
            else:
                raise ParserError(f"Unexpected token '{token.type.name}'. Expected a valid section block (domains, shared, entities, features, relations)", token.line, token.column)
                
        return ast

    def _parse_list_section(self, target_list: List, node_class):
        """Parses a list of identifiers under a section header."""
        self._skip_newlines()
        while self._peek().type == TokenType.IDENTIFIER:
            id_token = self._advance()
            
            # Check for optional (type)
            type_val = None
            if self._peek().type == TokenType.LPAREN:
                self._advance()
                type_token = self._consume(TokenType.IDENTIFIER, "Expected type identifier inside parentheses")
                type_val = type_token.value
                self._consume(TokenType.RPAREN, "Expected ')' after type")
                
            if node_class in (EntityNode, SharedNode):
                target_list.append(node_class(line=id_token.line, column=id_token.column, name=id_token.value, type=type_val))
            else:
                target_list.append(node_class(line=id_token.line, column=id_token.column, name=id_token.value))
                
            self._skip_newlines()

    def _parse_relations(self, target_list: List[RelationNode]):
        """Parses relation lines: IDENTIFIER -> IDENTIFIER (optional_type)"""
        self._skip_newlines()
        while self._peek().type == TokenType.IDENTIFIER:
            src_token = self._advance()
            self._consume(TokenType.ARROW, f"Expected '->' after source entity '{src_token.value}'")
            tgt_token = self._consume(TokenType.IDENTIFIER, "Expected target entity after '->'")
            
            # Check for optional (type)
            type_val = None
            if self._peek().type == TokenType.LPAREN:
                self._advance()
                type_token = self._consume(TokenType.IDENTIFIER, "Expected type identifier inside parentheses")
                type_val = type_token.value
                self._consume(TokenType.RPAREN, "Expected ')' after type")
            
            target_list.append(RelationNode(
                line=src_token.line, 
                column=src_token.column, 
                source=src_token.value, 
                target=tgt_token.value,
                type=type_val
            ))
            self._skip_newlines()
