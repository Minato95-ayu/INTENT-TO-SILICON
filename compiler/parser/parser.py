from typing import List, Optional
from compiler.lexer.tokens import Token, TokenType
from compiler.ast.nodes import (
    ProgramNode,
    StateDeclarationNode,
    LiteralNode,
    IdentifierNode,
    AssignmentNode,
    WidgetNode,
    ImportNode,
    ActionDeclarationNode,
    ActionCallNode,
    AppDeclarationNode,
    RunNode
)

from compiler.errors import CompilerError

# Deprecated, using CompilerError directly
class ParserError(CompilerError):
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
        if self._match(TokenType.KEYWORD, "import"):
            return self._parse_import_statement()
        
        if self._match(TokenType.KEYWORD, "state"):
            return self._parse_state_declaration()
        
        if self._match(TokenType.KEYWORD, "action"):
            return self._parse_action_declaration()
        
        if self._match(TokenType.KEYWORD, "app"):
            return self._parse_app_declaration()
        
        if self._match(TokenType.KEYWORD, "run"):
            line, col = self._previous().line, self._previous().column
            return RunNode(line=line, column=col)
        
        if self._match(TokenType.KEYWORD, "page"):
            return self._parse_widget("Page")
            
        # Fallback to general widget if identifier or keyword matches lowercase widget types
        if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
            # Wait, if it's an assignment like `a = 1`
            if self.pos + 1 < self.length and self.tokens[self.pos+1].type == TokenType.OPERATOR and self.tokens[self.pos+1].value == "=":
                return self._parse_assignment()
                
            # If it's a function call like `sendMessage(text)`
            if self.pos + 1 < self.length and self.tokens[self.pos+1].type == TokenType.SYMBOL and self.tokens[self.pos+1].value == "(":
                return self._parse_action_call()
            
            # Or it's a child widget (e.g., `title "Hello"`)
            return self._parse_widget_generic()
            
        token = self._peek()
        
        hint = ""
        if token.value == "-":
            hint = "Application names and identifiers cannot contain hyphens. Use underscores (e.g., my_app)."
            
        raise CompilerError(f"Unexpected token '{token.value}'", token.line, token.column, token.source_line, hint=hint)

    def _parse_app_declaration(self):
        line, col = self._previous().line, self._previous().column
        name_token = self._consume(TokenType.IDENTIFIER, "Expect app name after 'app'.")
        return AppDeclarationNode(line=line, column=col, name=name_token.value)

    def _parse_import_statement(self):
        line, col = self._previous().line, self._previous().column
        
        module_token = self._consume(TokenType.IDENTIFIER, "Expect module name after 'import'.")
        module_path = module_token.value
        
        while self._match(TokenType.SYMBOL, "."):
            next_part = self._consume(TokenType.IDENTIFIER, "Expect identifier after '.'.")
            module_path += "." + next_part.value
            
        return ImportNode(line=line, column=col, module=module_path)

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

    def _parse_action_declaration(self):
        line, col = self._previous().line, self._previous().column
        name_token = self._consume(TokenType.IDENTIFIER, "Expect action name.")
        
        # Optional parens for now
        if self._match(TokenType.SYMBOL, "("):
            self._consume(TokenType.SYMBOL, "Expect ')' after action arguments.", value=")")
            
        statements = []
        
        while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
            statements.append(self._parse_statement())
            
        self._consume(TokenType.KEYWORD, "Expect 'end' after action block.", value="end")
        return ActionDeclarationNode(line=line, column=col, name=name_token.value, statements=statements)

    def _parse_action_call(self):
        line, col = self._peek().line, self._peek().column
        name_token = self._consume(TokenType.IDENTIFIER, "Expect function name.")
        self._consume(TokenType.SYMBOL, "Expect '(' after function name.", value="(")
        
        args = []
        if not self._check(TokenType.SYMBOL, ")"):
            args.append(self._parse_expression())
            while self._match(TokenType.SYMBOL, ","):
                args.append(self._parse_expression())
                
        self._consume(TokenType.SYMBOL, "Expect ')' after arguments.", value=")")
        return ActionCallNode(line=line, column=col, name=name_token.value, args=args)

    def _parse_expression(self):
        if self._match(TokenType.NUMBER):
            raw = self._previous().value
            value = float(raw) if '.' in raw else int(raw)
            return LiteralNode(line=self._previous().line, column=self._previous().column, value=value)
        if self._match(TokenType.STRING):
            return LiteralNode(line=self._previous().line, column=self._previous().column, value=self._previous().value)
        if self._match(TokenType.IDENTIFIER):
            return IdentifierNode(line=self._previous().line, column=self._previous().column, name=self._previous().value)
            
        token = self._peek()
        raise CompilerError(f"Expect expression, got {token.type.name}", token.line, token.column, token.source_line)

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
        
        # parse generic text prop like `heading "Chats"`
        if self._match(TokenType.STRING):
            props["text"] = self._previous().value
        # parse bare identifier as content reference like `text count`
        elif self._check(TokenType.IDENTIFIER):
            # Only if the identifier is NOT followed by '=' (which would be a key=value prop)
            if not (self.pos + 1 < self.length and self.tokens[self.pos+1].type == TokenType.OPERATOR and self.tokens[self.pos+1].value == "="):
                id_token = self._advance()
                children.append(IdentifierNode(line=id_token.line, column=id_token.column, name=id_token.value))
            
        # parse key=value props like `onClick="handleSearch"`
        while self._check(TokenType.IDENTIFIER):
            if self.pos + 1 < self.length and self.tokens[self.pos+1].type == TokenType.OPERATOR and self.tokens[self.pos+1].value == "=":
                prop_key = self._advance().value
                self._consume(TokenType.OPERATOR, "Expect '=' after prop key.", value="=")
                if self._match(TokenType.STRING):
                    props[prop_key] = self._previous().value
                elif self._match(TokenType.IDENTIFIER):
                    props[prop_key] = self._previous().value
                else:
                    peek = self._peek()
                    raise CompilerError(f"Expect prop value, got {peek.value}", peek.line, peek.column, peek.source_line)
            else:
                break
                
        # Parse children if it's a block widget
        if w_type in ["container", "card", "row", "column"]:
            while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
                children.append(self._parse_statement())
            self._consume(TokenType.KEYWORD, f"Expect 'end' after {w_type} block.", value="end")
            
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
        peek = self._peek()
        raise CompilerError(message, peek.line, peek.column, peek.source_line)
