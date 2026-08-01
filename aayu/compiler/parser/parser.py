from typing import List, Optional
from aayu.compiler.lexer.tokens import Token, TokenType
from aayu.compiler.ast.nodes import (
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

from aayu.compiler.errors import CompilerError

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
            stmt = self._parse_statement()
            if isinstance(stmt, list):
                statements.extend(stmt)
            else:
                statements.append(stmt)
        return ProgramNode(line=1, column=1, statements=statements)

    def _parse_statement(self):
        token = self._peek()
        print(f"[PARSER DEBUG] _parse_statement at {token.line}:{token.column} token={token.value}")
        stmt = self._parse_statement_inner()
        # Consume optional statement terminator after EVERY statement
        self._match(TokenType.SYMBOL, ".")
        return stmt

    def _parse_statement_inner(self):
        if self._match(TokenType.KEYWORD, "import"):
            return self._parse_import_statement()
        
        if self._match(TokenType.KEYWORD, "state") or self._match(TokenType.KEYWORD, "const"):
            return self._parse_state_declaration()
        
        if self._match(TokenType.KEYWORD, "action"):
            return self._parse_action_declaration()
            
        if self._match(TokenType.KEYWORD, "fn"):
            return self._parse_fn_declaration()
            
        if self._match(TokenType.SYMBOL, "@"):
            decorators = []
            while True:
                # We already matched the first '@'
                dec_line, dec_col = self._previous().line, self._previous().column
                dec_name = self._consume(TokenType.IDENTIFIER, "Expect decorator name after '@'.").value
                dec_args = []
                if self._match(TokenType.SYMBOL, "("):
                    if not self._check(TokenType.SYMBOL, ")"):
                        while True:
                            dec_args.append(self._parse_expression())
                            if not self._match(TokenType.SYMBOL, ","):
                                break
                    self._consume(TokenType.SYMBOL, "Expect ')' after decorator arguments.", value=")")
                    
                from aayu.compiler.ast.nodes import DecoratorNode
                decorators.append(DecoratorNode(line=dec_line, column=dec_col, name=dec_name, args=dec_args))
                
                if not self._match(TokenType.SYMBOL, "@"):
                    break
                    
            if self._match(TokenType.KEYWORD, "action"):
                return self._parse_action_declaration(decorators)
            elif self._match(TokenType.KEYWORD, "model"):
                return self._parse_model_declaration(decorators)
            else:
                peek = self._peek()
                raise CompilerError(f"Syntax Error: Dangling decorator '@{decorators[0].name}'. Decorators must immediately precede an 'action' or 'model' declaration.", peek.line, peek.column, peek.source_line)
            
        if self._check(TokenType.IDENTIFIER) and self._peek().value in ["Page", "Component", "Form", "Scaffold", "Dialog", "Drawer", "Snackbar", "TabBar"]:
            if self.pos + 1 < self.length and self.tokens[self.pos+1].type == TokenType.IDENTIFIER:
                # Component names MUST be PascalCase.
                if self.tokens[self.pos+1].value[0].isupper():
                    return self._parse_component_declaration()
        
        if self._match(TokenType.KEYWORD, "app"):
            return self._parse_app_declaration()
        

        if self._match(TokenType.KEYWORD, "import"):
            return self._parse_import_statement()
        
        if self._match(TokenType.KEYWORD, "if"):
            return self._parse_if_statement()

        if self._match(TokenType.KEYWORD, "let"):
            return self._parse_let_declaration()

        if self._match(TokenType.KEYWORD, "state"):
            return self._parse_state_declaration()

        if self._match(TokenType.KEYWORD, "while"):
            return self._parse_while_statement()

        if self._match(TokenType.KEYWORD, "for"):
            return self._parse_for_statement()

        if self._match(TokenType.KEYWORD, "model"):
            return self._parse_model_declaration()

        if self._match(TokenType.KEYWORD, "route"):
            return self._parse_route_declaration()

        if self._match(TokenType.KEYWORD, "return"):
            return self._parse_return_statement()

        if self._match(TokenType.KEYWORD, "await"):
            from aayu.compiler.ast.nodes import AwaitNode
            stmt = self._parse_expression()
            return AwaitNode(line=self._previous().line, column=self._previous().column, expression=stmt)

        if self._match(TokenType.KEYWORD, "try"):
            return self._parse_try_statement()

        if self._match(TokenType.KEYWORD, "throw"):
            return self._parse_throw_statement()

        if self._match(TokenType.KEYWORD, "rethrow"):
            return self._parse_rethrow_statement()

        if self._match(TokenType.KEYWORD, "theme"):
            return self._parse_theme_declaration()

        if self._match(TokenType.KEYWORD, "useTheme"):
            line, col = self._previous().line, self._previous().column
            if self._check(TokenType.IDENTIFIER) or self._check(TokenType.STRING):
                name_token = self._advance()
            else:
                raise CompilerError("Expect theme name after 'useTheme'.", self._peek().line, self._peek().column, self._peek().source_line)
            from aayu.compiler.ast.nodes import UseThemeNode
            return UseThemeNode(line=line, column=col, name=name_token.value)
            
        if self._match(TokenType.KEYWORD, "bind"):
            line, col = self._previous().line, self._previous().column
            target_token = self._consume(TokenType.IDENTIFIER, "Expect target state after 'bind'.")
            from aayu.compiler.ast.nodes import BindNode
            return BindNode(line=line, column=col, target=target_token.value)
            
        if self._match(TokenType.KEYWORD, "validate"):
            return self._parse_validate()
            
        if self._match(TokenType.KEYWORD, "navigate"):
            line, col = self._previous().line, self._previous().column
            target_token = self._consume(TokenType.IDENTIFIER, "Expect target name after 'navigate'.")
            target = target_token.value
            kwargs = {}
            if self._match(TokenType.SYMBOL, "("):
                if not self._check(TokenType.SYMBOL, ")"):
                    key = self._consume(TokenType.IDENTIFIER, "Expect argument name.").value
                    self._consume(TokenType.OPERATOR, "Expect '=' after argument name.", value="=")
                    val = self._parse_expression()
                    kwargs[key] = val
                    while self._match(TokenType.SYMBOL, ","):
                        key = self._consume(TokenType.IDENTIFIER, "Expect argument name.").value
                        self._consume(TokenType.OPERATOR, "Expect '=' after argument name.", value="=")
                        val = self._parse_expression()
                        kwargs[key] = val
                self._consume(TokenType.SYMBOL, "Expect ')' after navigate arguments.", value=")")
            from aayu.compiler.ast.nodes import NavigateNode
            return NavigateNode(line=line, column=col, target=target, kwargs=kwargs)
            
        if self._match(TokenType.KEYWORD, "animate"):
            line, col = self._previous().line, self._previous().column
            properties = {}
            while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
                prop_token = self._consume(TokenType.IDENTIFIER, "Expect animate property name.")
                prop_val = self._parse_expression()
                properties[prop_token.value] = prop_val
            self._consume(TokenType.KEYWORD, "Expect 'end' after animate block.", value="end")
            from aayu.compiler.ast.nodes import AnimateNode
            return AnimateNode(line=line, column=col, properties=properties)

        lifecycle_hooks = ["onCreate", "onLoad", "onResume", "onPause", "onHide", "onShow", "onUnload", "onDestroy"]
        if self._check(TokenType.IDENTIFIER) and self._peek().value in lifecycle_hooks:
            hook_token = self._advance()
            line, col = hook_token.line, hook_token.column
            body = []
            while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
                body.append(self._parse_statement())
            self._consume(TokenType.KEYWORD, f"Expect 'end' after {hook_token.value} block.", value="end")
            from aayu.compiler.ast.nodes import LifecycleNode
            return LifecycleNode(line=line, column=col, hook=hook_token.value, body=body)

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
                
            # If it's a function call like `sendMessage(text)` or `HTTP.post(url)`
            lookahead = 1
            is_call = False
            has_dot = False
            while self.pos + lookahead < self.length:
                if self.tokens[self.pos+lookahead].type == TokenType.SYMBOL and self.tokens[self.pos+lookahead].value == "(":
                    is_call = True
                    break
                elif self.tokens[self.pos+lookahead].type == TokenType.SYMBOL and self.tokens[self.pos+lookahead].value == ".":
                    has_dot = True
                    lookahead += 2
                else:
                    break
            
            if is_call:
                return self._parse_action_call()
            
            # Or it's a child widget (e.g., `title "Hello"`)
            return self._parse_widget_generic()
            
        token = self._peek()
        
        hint = ""
        if token.value == "-":
            hint = "Application names and identifiers cannot contain hyphens. Use underscores (e.g., my_app)."
            
        raise CompilerError(f"Unexpected token '{token.value}'", token.line, token.column, token.source_line, hint=hint)


    def _parse_let_declaration(self):
        line, col = self._previous().line, self._previous().column
        name_token = self._consume(TokenType.IDENTIFIER, "Expect variable name after 'let'.")
        
        value = None
        if self._match(TokenType.OPERATOR, "="):
            value = self._parse_expression()
            
        from aayu.compiler.ast.nodes import StateDeclarationNode
        return StateDeclarationNode(line=line, column=col, name=name_token.value, value=value)

    def _parse_theme_declaration(self):
        line, col = self._previous().line, self._previous().column
        name_token = self._consume(TokenType.IDENTIFIER, "Expect theme name after 'theme'.")
        properties = {}
        while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
            prop_token = self._consume(TokenType.IDENTIFIER, "Expect property name in theme block.")
            prop_val = self._parse_expression()
            properties[prop_token.value] = prop_val
        self._consume(TokenType.KEYWORD, "Expect 'end' after theme block.", value="end")
        from aayu.compiler.ast.nodes import ThemeNode
        return ThemeNode(line=line, column=col, name=name_token.value, properties=properties)

    def _parse_validate(self):
        line, col = self._previous().line, self._previous().column
        fields = []
        while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
            field_token = self._consume(TokenType.IDENTIFIER, "Expect field name in validate block.")
            self._consume(TokenType.SYMBOL, "Expect ':' after field name.", value=":")
            rules = []
            while not self._is_at_end() and self._check(TokenType.IDENTIFIER):
                # If the next token is ':', then this identifier is actually the NEXT field name, not a rule!
                if self.pos + 1 < self.length and self.tokens[self.pos+1].type == TokenType.SYMBOL and self.tokens[self.pos+1].value == ":":
                    break
                
                rule_token = self._consume(TokenType.IDENTIFIER, "Expect validation rule name.")
                args = []
                if self._match(TokenType.SYMBOL, "("):
                    if not self._check(TokenType.SYMBOL, ")"):
                        args.append(self._parse_expression())
                        while self._match(TokenType.SYMBOL, ","):
                            args.append(self._parse_expression())
                    self._consume(TokenType.SYMBOL, "Expect ')' after rule arguments.", value=")")
                elif self._check(TokenType.NUMBER) or self._check(TokenType.STRING):
                    args.append(self._parse_expression())
                from aayu.compiler.ast.nodes import ValidationRuleNode
                rules.append(ValidationRuleNode(line=rule_token.line, column=rule_token.column, rule=rule_token.value, args=args))
            from aayu.compiler.ast.nodes import ValidateFieldNode
            fields.append(ValidateFieldNode(line=field_token.line, column=field_token.column, field_name=field_token.value, rules=rules))
        self._consume(TokenType.KEYWORD, "Expect 'end' after validate block.", value="end")
        from aayu.compiler.ast.nodes import ValidateNode
        return ValidateNode(line=line, column=col, fields=fields)
        
    def _parse_return_statement(self):
        line, col = self._previous().line, self._previous().column
        value = self._parse_expression()
        from aayu.compiler.ast.nodes import ReturnNode
        return ReturnNode(line=line, column=col, value=value)
        
    def _parse_if_statement(self):
        line, col = self._previous().line, self._previous().column
        condition = self._parse_expression()
        
        has_brace = False
        if self._match(TokenType.SYMBOL, "{"):
            has_brace = True
            
        then_branch = []
        while not self._is_at_end():
            if has_brace and self._check(TokenType.SYMBOL, "}"):
                break
            if not has_brace and (self._check(TokenType.KEYWORD, "end") or self._check(TokenType.KEYWORD, "else")):
                break
            then_branch.append(self._parse_statement())
            
        if has_brace:
            self._consume(TokenType.SYMBOL, "Expect '}' after if block.", value="}")
            
        else_branch = None
        if self._match(TokenType.KEYWORD, "else"):
            has_else_brace = False
            if self._match(TokenType.SYMBOL, "{"):
                has_else_brace = True
                
            else_branch = []
            while not self._is_at_end():
                if has_else_brace and self._check(TokenType.SYMBOL, "}"):
                    break
                if not has_else_brace and self._check(TokenType.KEYWORD, "end"):
                    break
                else_branch.append(self._parse_statement())
                
            if has_else_brace:
                self._consume(TokenType.SYMBOL, "Expect '}' after else block.", value="}")
                
        if not has_brace:
            print(f"Warning: Legacy 'end' syntax is deprecated (Line {line}). Use '{{ }}' blocks instead.")
            self._consume(TokenType.KEYWORD, "Expect 'end' after if statement.", value="end")
            
        from aayu.compiler.ast.nodes import IfNode
        return IfNode(line=line, column=col, condition=condition, then_branch=then_branch, else_branch=else_branch)
        
    def _parse_while_statement(self):
        line, col = self._previous().line, self._previous().column
        condition = self._parse_expression()
        
        has_brace = False
        if self._match(TokenType.SYMBOL, "{"):
            has_brace = True
            
        body = []
        while not self._is_at_end():
            if has_brace and self._check(TokenType.SYMBOL, "}"):
                break
            if not has_brace and self._check(TokenType.KEYWORD, "end"):
                break
            body.append(self._parse_statement())
            
        if has_brace:
            self._consume(TokenType.SYMBOL, "Expect '}' after while block.", value="}")
        else:
            print(f"Warning: Legacy 'end' syntax is deprecated (Line {line}). Use '{{ }}' blocks instead.")
            self._consume(TokenType.KEYWORD, "Expect 'end' after while statement.", value="end")
            
        from aayu.compiler.ast.nodes import WhileNode
        return WhileNode(line=line, column=col, condition=condition, body=body)

    def _parse_for_statement(self):
        line, col = self._previous().line, self._previous().column
        first_ident = self._consume(TokenType.IDENTIFIER, "Expect iterator name after 'for'.").value
        index_name = None
        iterator = first_ident
        if self._match(TokenType.SYMBOL, ","):
            index_name = first_ident
            iterator = self._consume(TokenType.IDENTIFIER, "Expect iterator value name after comma.").value
            
        self._consume(TokenType.KEYWORD, "Expect 'in' after iterator name.", value="in")
        iterable = self._parse_expression()
        
        has_brace = False
        if self._match(TokenType.SYMBOL, "{"):
            has_brace = True
            
        body = []
        while not self._is_at_end():
            if has_brace and self._check(TokenType.SYMBOL, "}"):
                break
            if not has_brace and self._check(TokenType.KEYWORD, "end"):
                break
            body.append(self._parse_statement())
            
        if has_brace:
            self._consume(TokenType.SYMBOL, "Expect '}' after for block.", value="}")
        else:
            print(f"Warning: Legacy 'end' syntax is deprecated (Line {line}). Use '{{ }}' blocks instead.")
            self._consume(TokenType.KEYWORD, "Expect 'end' after for loop.", value="end")
            
        from aayu.compiler.ast.nodes import ForNode
        return ForNode(line=line, column=col, iterator=iterator, iterable=iterable, body=body, index_name=index_name)

    def _parse_try_statement(self):
        line, col = self._previous().line, self._previous().column
        self._match(TokenType.SYMBOL, "{")
        try_block = []
        while not self._is_at_end() and not self._check(TokenType.KEYWORD, "catch") and not self._check(TokenType.KEYWORD, "finally") and not self._check(TokenType.KEYWORD, "end") and not self._check(TokenType.SYMBOL, "}"):
            try_block.append(self._parse_statement())
        self._match(TokenType.SYMBOL, "}")
            
        catch_var = None
        catch_block = []
        if self._match(TokenType.KEYWORD, "catch"):
            if self._match(TokenType.SYMBOL, "("):
                catch_var = self._consume(TokenType.IDENTIFIER, "Expect variable name in catch.").value
                self._consume(TokenType.SYMBOL, "Expect ')' after catch variable.", value=")")
            elif self._check(TokenType.IDENTIFIER):
                catch_var = self._consume(TokenType.IDENTIFIER, "Expect variable name in catch.").value
            self._match(TokenType.SYMBOL, "{")
            while not self._is_at_end() and not self._check(TokenType.KEYWORD, "finally") and not self._check(TokenType.KEYWORD, "end") and not self._check(TokenType.SYMBOL, "}"):
                catch_block.append(self._parse_statement())
            self._match(TokenType.SYMBOL, "}")
                
        finally_block = []
        if self._match(TokenType.KEYWORD, "finally"):
            self._match(TokenType.SYMBOL, "{")
            while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end") and not self._check(TokenType.SYMBOL, "}"):
                finally_block.append(self._parse_statement())
            self._match(TokenType.SYMBOL, "}")
                
        self._match(TokenType.KEYWORD, "end")
        from aayu.compiler.ast.nodes import TryNode
        return TryNode(line=line, column=col, try_block=try_block, catch_var=catch_var, catch_block=catch_block, finally_block=finally_block)

    def _parse_throw_statement(self):
        line, col = self._previous().line, self._previous().column
        value = self._parse_expression()
        from aayu.compiler.ast.nodes import ThrowNode
        return ThrowNode(line=line, column=col, value=value)

    def _parse_rethrow_statement(self):
        line, col = self._previous().line, self._previous().column
        from aayu.compiler.ast.nodes import RethrowNode
        return RethrowNode(line=line, column=col)

    def _parse_model_declaration(self, decorators=None):
        line, col = self._previous().line, self._previous().column
        name = self._consume(TokenType.IDENTIFIER, "Expect model name.").value
        self._consume(TokenType.SYMBOL, "Expect '{' before model body.", value="{")
        
        fields = []
        while not self._is_at_end() and not self._check(TokenType.SYMBOL, "}"):
            field_line, field_col = self._peek().line, self._peek().column
            field_name = self._consume(TokenType.IDENTIFIER, "Expect field name.").value
            self._consume(TokenType.SYMBOL, "Expect ':' after field name.", value=":")
            field_type = self._consume(TokenType.IDENTIFIER, "Expect field type.").value
            
            # Typing check
            if field_type not in ["String", "Int", "Boolean", "Float", "List", "Dict"]:
                # Custom types are allowed in full-stack AAYU, but we can emit a warning or check it here
                # As per user request: if it's not a known type, maybe it's a relation, but for now we accept it and semantic analyzer validates it.
                pass

            attributes = []
            while self._match(TokenType.SYMBOL, "@"):
                attr_line, attr_col = self._previous().line, self._previous().column
                attr_name = self._consume(TokenType.IDENTIFIER, "Expect attribute name after '@'.").value
                attr_args = []
                if self._match(TokenType.SYMBOL, "("):
                    if not self._check(TokenType.SYMBOL, ")"):
                        while True:
                            # Arguments can be identifiers like User.id or strings
                            arg = self._advance().value
                            # If it's a nested identifier like User.id
                            while self._match(TokenType.SYMBOL, "."):
                                arg += "." + self._advance().value
                            attr_args.append(arg)
                            if not self._match(TokenType.SYMBOL, ","):
                                break
                    self._consume(TokenType.SYMBOL, "Expect ')' after attribute arguments.", value=")")
                
                from aayu.compiler.ast.nodes import ModelAttributeNode
                attributes.append(ModelAttributeNode(line=attr_line, column=attr_col, name=attr_name, args=attr_args))
                
            VALIDATION_MODIFIERS = ["required", "unique", "min", "max", "regex", "enum", "default", "nullable"]
            while self._check(TokenType.IDENTIFIER) and self._peek().value in VALIDATION_MODIFIERS:
                attr_line, attr_col = self._peek().line, self._peek().column
                attr_name = self._advance().value
                attr_args = []
                if self._match(TokenType.SYMBOL, "("):
                    if not self._check(TokenType.SYMBOL, ")"):
                        while True:
                            # Parsing inline arguments
                            arg = self._advance().value
                            if isinstance(arg, str) and arg.startswith('"') and arg.endswith('"'):
                                arg = arg[1:-1]
                            attr_args.append(arg)
                            if not self._match(TokenType.SYMBOL, ","):
                                break
                    self._consume(TokenType.SYMBOL, "Expect ')' after modifier arguments.", value=")")
                from aayu.compiler.ast.nodes import ModelAttributeNode
                attributes.append(ModelAttributeNode(line=attr_line, column=attr_col, name=attr_name, args=attr_args))
                
            from aayu.compiler.ast.nodes import ModelFieldNode
            fields.append(ModelFieldNode(line=field_line, column=field_col, name=field_name, field_type=field_type, attributes=attributes))
            
        self._consume(TokenType.SYMBOL, f"Expected '}}' to close model '{name}' at line {line}", value="}")
            
        from aayu.compiler.ast.nodes import ModelDeclNode
        
        dec_payloads = [{"name": d.name, "args": d.args} for d in (decorators or [])]
        dec_names = [d["name"] for d in dec_payloads]
        if "public" not in dec_names and "private" not in dec_names and "auth" not in dec_names:
            dec_payloads.append({"name": "auth", "args": []})
            
        return ModelDeclNode(line=line, column=col, name=name, fields=fields, decorators=dec_payloads)
        
    def _parse_route_declaration(self):
        line, col = self._previous().line, self._previous().column
        path = self._consume(TokenType.STRING, "Expect route path.").value
        methods = []
        while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
            method_name = self._consume(TokenType.KEYWORD, "Expect HTTP method.").value
            body = []
            while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
                body.append(self._parse_statement())
            self._consume(TokenType.KEYWORD, "Expect 'end' after method.", value="end")
            from aayu.compiler.ast.nodes import MethodNode
            methods.append(MethodNode(line=self._previous().line, column=self._previous().column, method=method_name, body=body))
        self._consume(TokenType.KEYWORD, "Expect 'end' after route.", value="end")
        from aayu.compiler.ast.nodes import RouteNode
        return RouteNode(line=line, column=col, path=path, methods=methods)

    def _parse_app_declaration(self):

        line, col = self._previous().line, self._previous().column
        name_token = self._consume(TokenType.IDENTIFIER, "Expect app name after 'app'.")
        return AppDeclarationNode(line=line, column=col, name=name_token.value)

    def _parse_import_statement(self):
        line, col = self._previous().line, self._previous().column
        
        if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
            module_token = self._advance()
        else:
            raise CompilerError("Expect module name after 'import'.", self._peek().line, self._peek().column)
            
        module_path = module_token.value
        
        while self._match(TokenType.SYMBOL, "."):
            if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
                next_part = self._advance()
                module_path += "." + next_part.value
            else:
                raise CompilerError("Expect identifier after '.'.", self._peek().line, self._peek().column)
                
        return ImportNode(line=line, column=col, module=module_path)

    def _parse_state_declaration(self):
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
            return StateDeclarationNode(line=line, column=col, name=name_token.value, value=value)

    def _parse_assignment(self):
        line, col = self._peek().line, self._peek().column
        name_token = self._consume(TokenType.IDENTIFIER, "Expect identifier.")
        self._consume(TokenType.OPERATOR, "Expect '='.", value="=")
        value = self._parse_expression()
        return AssignmentNode(line=line, column=col, target=name_token.value, value=value)

    def _parse_component_declaration(self):
        component_type = self._advance().value # e.g. Form, Page
        line, col = self._previous().line, self._previous().column
        name = self._consume(TokenType.IDENTIFIER, f"Expect {component_type} name.").value
        
        statements = []
        while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
            statements.append(self._parse_statement())
            
        self._consume(TokenType.KEYWORD, f"Expect 'end' after {component_type} block.", value="end")
        from aayu.compiler.ast.nodes import ActionDeclarationNode, WidgetNode, ImportNode
        
        ui_statements = []
        other_statements = []
        for stmt in statements:
            if isinstance(stmt, (WidgetNode, ImportNode)):
                ui_statements.append(stmt)
            else:
                other_statements.append(stmt)
                
        component_widget = WidgetNode(line=line, column=col, widget_type=component_type, props={"name": name}, children=ui_statements)
        other_statements.append(component_widget)
        
        # Treat component as an action declaration to simplify the IR pipeline
        return ActionDeclarationNode(line=line, column=col, name=name, statements=other_statements)

    def _parse_action_declaration(self, decorators=None):
        line, col = self._previous().line, self._previous().column
        name_token = self._consume(TokenType.IDENTIFIER, "Expect action name.")
        
        args = []
        if self._match(TokenType.SYMBOL, "("):
            if not self._check(TokenType.SYMBOL, ")"):
                while True:
                    arg_name = self._consume(TokenType.IDENTIFIER, "Expect argument name.").value
                    args.append(arg_name)
                    if not self._match(TokenType.SYMBOL, ","):
                        break
            self._consume(TokenType.SYMBOL, "Expect ')' after action arguments.", value=")")
            
        statements = []
        
        while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
            statements.append(self._parse_statement())
            
        self._consume(TokenType.KEYWORD, "Expect 'end' after action block.", value="end")
        from aayu.compiler.ast.nodes import ActionDeclarationNode
        return ActionDeclarationNode(line=line, column=col, name=name_token.value, statements=statements, args=args, decorators=decorators or [])

    def _parse_fn_declaration(self):
        line, col = self._previous().line, self._previous().column
        name_token = self._consume(TokenType.IDENTIFIER, "Expect function name after 'fn'.")
        
        args = []
        if self._match(TokenType.SYMBOL, "("):
            if not self._check(TokenType.SYMBOL, ")"):
                while True:
                    arg_name = self._consume(TokenType.IDENTIFIER, "Expect argument name.").value
                    args.append(arg_name)
                    if not self._match(TokenType.SYMBOL, ","):
                        break
            self._consume(TokenType.SYMBOL, "Expect ')' after function arguments.", value=")")
            
        self._consume(TokenType.SYMBOL, "Expect '{' before function body.", value="{")
        statements = []
        
        while not self._is_at_end() and not self._check(TokenType.SYMBOL, "}"):
            statements.append(self._parse_statement())
            
        self._consume(TokenType.SYMBOL, "Expect '}' after function body.", value="}")
        from aayu.compiler.ast.nodes import ActionDeclarationNode
        return ActionDeclarationNode(line=line, column=col, name=name_token.value, statements=statements, args=args, decorators=[])

    def _parse_action_call(self):
        line, col = self._peek().line, self._peek().column
        if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
            name = self._advance().value
        else:
            raise CompilerError("Expect function name.", line, col, self._peek().source_line)
            
        while self._check(TokenType.SYMBOL, ".") and self.pos + 1 < self.length and self.tokens[self.pos].line == self.tokens[self.pos+1].line:
            if not (self.tokens[self.pos+1].type == TokenType.IDENTIFIER or self.tokens[self.pos+1].type == TokenType.KEYWORD):
                break
            self._advance() # consume .
            prop = self._advance().value
            name = f"{name}.{prop}"
            
        self._consume(TokenType.SYMBOL, "Expect '(' after function name.", value="(")
        
        args = []
        if not self._check(TokenType.SYMBOL, ")"):
            args.append(self._parse_expression())
            while self._match(TokenType.SYMBOL, ","):
                args.append(self._parse_expression())
                
        self._consume(TokenType.SYMBOL, "Expect ')' after arguments.", value=")")
        return ActionCallNode(line=line, column=col, name=name, args=args)

    def _parse_expression(self):
        return self._parse_logical_or()

    def _parse_logical_or(self):
        expr = self._parse_logical_and()
        while self._match(TokenType.OPERATOR, "||"):
            operator = self._previous().value
            right = self._parse_logical_and()
            from aayu.compiler.ast.nodes import BinaryOpNode
            expr = BinaryOpNode(line=expr.line, column=expr.column, left=expr, operator=operator, right=right)
        return expr

    def _parse_logical_and(self):
        expr = self._parse_equality()
        while self._match(TokenType.OPERATOR, "&&"):
            operator = self._previous().value
            right = self._parse_equality()
            from aayu.compiler.ast.nodes import BinaryOpNode
            expr = BinaryOpNode(line=expr.line, column=expr.column, left=expr, operator=operator, right=right)
        return expr

    def _parse_equality(self):
        expr = self._parse_comparison()
        while self._match(TokenType.OPERATOR, "==") or self._match(TokenType.OPERATOR, "!="):
            operator = self._previous().value
            right = self._parse_comparison()
            from aayu.compiler.ast.nodes import BinaryOpNode
            expr = BinaryOpNode(line=expr.line, column=expr.column, left=expr, operator=operator, right=right)
        return expr

    def _parse_comparison(self):
        expr = self._parse_term()
        while self._match(TokenType.OPERATOR, ">") or self._match(TokenType.OPERATOR, ">=") or self._match(TokenType.OPERATOR, "<") or self._match(TokenType.OPERATOR, "<="):
            operator = self._previous().value
            right = self._parse_term()
            from aayu.compiler.ast.nodes import BinaryOpNode
            expr = BinaryOpNode(line=expr.line, column=expr.column, left=expr, operator=operator, right=right)
        return expr

    def _parse_term(self):
        expr = self._parse_factor()
        while self._match(TokenType.OPERATOR, "+") or self._match(TokenType.OPERATOR, "-"):
            operator = self._previous().value
            right = self._parse_factor()
            from aayu.compiler.ast.nodes import BinaryOpNode
            expr = BinaryOpNode(line=expr.line, column=expr.column, left=expr, operator=operator, right=right)
        return expr

    def _parse_factor(self):
        expr = self._parse_unary()
        while self._match(TokenType.OPERATOR, "*") or self._match(TokenType.OPERATOR, "/") or self._match(TokenType.OPERATOR, "%"):
            operator = self._previous().value
            right = self._parse_unary()
            from aayu.compiler.ast.nodes import BinaryOpNode
            expr = BinaryOpNode(line=expr.line, column=expr.column, left=expr, operator=operator, right=right)
        return expr

    def _parse_unary(self):
        if self._match(TokenType.OPERATOR, "-") or self._match(TokenType.OPERATOR, "!"):
            operator = self._previous().value
            right = self._parse_unary()
            from aayu.compiler.ast.nodes import UnaryOpNode
            return UnaryOpNode(line=self._previous().line, column=self._previous().column, operator=operator, right=right)
        return self._parse_primary()

    def _parse_primary(self):
        expr = None
        if self._match(TokenType.NUMBER):
            raw = self._previous().value
            value = float(raw) if '.' in raw else int(raw)
            expr = LiteralNode(line=self._previous().line, column=self._previous().column, value=value)
        elif self._match(TokenType.STRING):
            expr = LiteralNode(line=self._previous().line, column=self._previous().column, value=self._previous().value)
        elif self._match(TokenType.KEYWORD, "true"):
            expr = LiteralNode(line=self._previous().line, column=self._previous().column, value=True)
        elif self._match(TokenType.KEYWORD, "false"):
            expr = LiteralNode(line=self._previous().line, column=self._previous().column, value=False)
        elif self._match(TokenType.KEYWORD, "null"):
            expr = LiteralNode(line=self._previous().line, column=self._previous().column, value=None)
        elif self._check(TokenType.IDENTIFIER):
            # Check if it's an action call
            lookahead = 1
            is_call = False
            while self.pos + lookahead < self.length:
                if self.tokens[self.pos+lookahead].type == TokenType.SYMBOL and self.tokens[self.pos+lookahead].value == "(":
                    is_call = True
                    break
                elif self.tokens[self.pos+lookahead].type == TokenType.SYMBOL and self.tokens[self.pos+lookahead].value == ".":
                    if self.pos + lookahead + 1 < self.length and self.tokens[self.pos+lookahead].line == self.tokens[self.pos+lookahead+1].line:
                        lookahead += 2
                    else:
                        break
                else:
                    break
            
            if is_call:
                expr = self._parse_action_call()
            else:
                id_token = self._advance()
                name = id_token.value
                expr = IdentifierNode(line=id_token.line, column=id_token.column, name=name)
        elif self._match(TokenType.SYMBOL, "["):
            line, col = self._previous().line, self._previous().column
            elements = []
            if not self._check(TokenType.SYMBOL, "]"):
                elements.append(self._parse_expression())
                while self._match(TokenType.SYMBOL, ","):
                    elements.append(self._parse_expression())
            self._consume(TokenType.SYMBOL, "Expect ']' after array elements.", value="]")
            from aayu.compiler.ast.nodes import ArrayNode
            expr = ArrayNode(line=line, column=col, elements=elements)
        elif self._match(TokenType.SYMBOL, "{"):
            line, col = self._previous().line, self._previous().column
            pairs = {}
            if not self._check(TokenType.SYMBOL, "}"):
                if not self._check(TokenType.STRING):
                    raise CompilerError("Expect string key in dictionary.", self._peek().line, self._peek().column, self._peek().source_line)
                key = self._advance().value
                self._consume(TokenType.SYMBOL, "Expect ':' after dictionary key.", value=":")
                val = self._parse_expression()
                pairs[key] = val
                while self._match(TokenType.SYMBOL, ","):
                    if not self._check(TokenType.STRING):
                        raise CompilerError("Expect string key in dictionary.", self._peek().line, self._peek().column, self._peek().source_line)
                    key = self._advance().value
                    self._consume(TokenType.SYMBOL, "Expect ':' after dictionary key.", value=":")
                    val = self._parse_expression()
                    pairs[key] = val
            self._consume(TokenType.SYMBOL, "Expect '}' after dictionary elements.", value="}")
            from aayu.compiler.ast.nodes import DictionaryNode
            expr = DictionaryNode(line=line, column=col, pairs=pairs)
        elif self._match(TokenType.SYMBOL, "("):
            expr = self._parse_expression()
            self._consume(TokenType.SYMBOL, "Expect ')' after expression.", value=")")
        else:
            token = self._peek()
            raise CompilerError(f"Expect expression, got {token.type.name}", token.line, token.column, token.source_line)
            
        # Postfix operators
        while True:
            if self._match(TokenType.SYMBOL, "["):
                index_expr = self._parse_expression()
                self._consume(TokenType.SYMBOL, "Expect ']' after array index.", value="]")
                from aayu.compiler.ast.nodes import SubscriptNode
                expr = SubscriptNode(line=expr.line, column=expr.column, target=expr, index=index_expr)
            elif self._check(TokenType.SYMBOL, ".") and self.pos + 1 < self.length and self.tokens[self.pos+1].type == TokenType.IDENTIFIER:
                if self.tokens[self.pos].line != self.tokens[self.pos+1].line:
                    break
                self._advance() # consume '.'
                prop = self._advance()
                from aayu.compiler.ast.nodes import SubscriptNode
                expr = SubscriptNode(line=expr.line, column=expr.column, target=expr, index=LiteralNode(line=prop.line, column=prop.column, value=prop.value))
            else:
                break
                
        return expr

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
        takes_positional = w_type.lower() in ["text", "heading", "button", "icon", "avatar", "chatbubble"] or (w_type[0].islower() if w_type else False)
        positional_consumed = False
        
        if takes_positional:
            if self._match(TokenType.STRING):
                props["text"] = self._previous().value
                positional_consumed = True
            # parse bare identifier as content reference like `text count`
            elif self._check(TokenType.IDENTIFIER):
                # If it's an event handler (starts with 'on'), parse full expression
                if w_type.startswith("on"):
                    props["value_node"] = self._parse_expression()
                    positional_consumed = True
                # Only if the identifier is NOT followed by '=' (which would be a key=value prop)
                elif not (self.pos + 1 < self.length and self.tokens[self.pos+1].type == TokenType.OPERATOR and self.tokens[self.pos+1].value == "="):
                    id_token = self._peek()
                    is_prop_block = id_token.value.startswith("on") or id_token.value in [
                        "padding", "margin", "color", "backgroundColor", "width", "height", "size",
                        "border", "borderRadius", "shadow", "opacity", "visible", "align", "justify"
                    ]
                    if not is_prop_block:
                        props["value_node"] = self._parse_expression()
                        positional_consumed = True
            
        # parse key=value props like `onClick="handleSearch"`
        while self._check(TokenType.IDENTIFIER):
            if self.pos + 1 < self.length and self.tokens[self.pos+1].type == TokenType.OPERATOR and self.tokens[self.pos+1].value == "=":
                prop_key = self._advance().value
                self._consume(TokenType.OPERATOR, "Expect '=' after prop key.", value="=")
                props[prop_key] = self._parse_expression()
            else:
                break
                
        is_property = not w_type.istitle() and not w_type.isupper()
        if is_property and positional_consumed:
            return WidgetNode(line=line, column=col, widget_type=w_type, props=props, children=[])
                
        # Parse children if it's a block widget
        became_block = False
        if w_type.lower() in ["container", "card", "row", "column", "page", "list", "grid", "stack", "center", "expanded", "padding", "scrollview", "appbar", "navigationbar", "drawer", "dialog", "snackbar", "form"]:
            while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
                children.append(self._parse_statement())
            self._consume(TokenType.KEYWORD, f"Expect 'end' after {w_type} block.", value="end")
        else:
            while not self._is_at_end():
                token = self._peek()
                if (token.type == TokenType.KEYWORD and token.value in ["animate", "bind", "validate"]) or \
                   (token.type == TokenType.IDENTIFIER and not token.value.istitle() and not token.value.isupper()):
                    became_block = True
                    children.append(self._parse_statement())
                else:
                    break
            if became_block:
                self._consume(TokenType.KEYWORD, f"Expect 'end' after {w_type} block with directives.", value="end")
            
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
