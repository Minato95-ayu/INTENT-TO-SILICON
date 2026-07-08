"""
===============================================================================
AAYU Compiler - Parser

Purpose:
    Ye file Lexer se aaye tokens ko padhti hai aur ek Abstract Syntax Tree (AST) banati hai.

Input:
    Token stream (List of Tokens)

Output:
    Abstract Syntax Tree (AST)

Pipeline:
    Lexer
        ↓
    Parser   ← (Current File)
        ↓
    AST
        ↓
    Semantic Analysis

Ye file kyun important hai?
    Agar parser galat hoga, to compiler code ke structure ko galat samjhega aur aage ka process fail ho jayega. Ye ek hand-written recursive descent parser hai.

Difficulty:
    ⭐⭐⭐ (Hard)

Recommended Reading Order:
    1. lexer.py
    2. parser.py (You are here)
    3. ast_nodes.py
===============================================================================
"""
from typing import List
from compiler.frontend.lexer import Token, Lexer
from compiler.frontend.ast_nodes import *
from compiler.frontend.errors import AAYUSyntaxError

class Parser:
    def __init__(self, tokens: List[Token], filename: str = "main.aayu", file_id: int = 0):
        self.tokens = tokens
        self.current = 0
        self.execution_scope_depth = 0
        self.filename = filename
        self.file_id = file_id

    def parse(self) -> ProgramNode:
        statements = []
        while not self.is_at_end():
            statements.append(self.parse_statement())
        return ProgramNode(statements=statements)

    def parse_statement(self) -> Node:
        """
        Purpose:
            Single statement parse karta hai (Jaise Variable declare karna, Print karna).
        """
        start_token = self.peek()
        node = None
        
        is_exported = False
        visibility = "private"
        
        # Check for export block or export task: export { ... } or export task ...
        if self.check("KEYWORD", "export") and (self.peek_next().type == "LBRACE" or getattr(self.peek_next(), 'value', None) == "task"):
            self.advance() # consume 'export'
            node = self.parse_export_statement()
            # Do not fall through, we parsed the whole statement
        else:
            if self.match("KEYWORD", "export"):
                is_exported = True
                
            if self.match("KEYWORD", "public"):
                visibility = "public"
            elif self.match("KEYWORD", "private"):
                visibility = "private"

        if node is None:
            if self.match("KEYWORD", "number") or self.match("KEYWORD", "text") or self.match("KEYWORD", "let"):
                node = self.parse_declaration(self.previous().value, is_exported, visibility)
            elif self.match("KEYWORD", "module"):
                node = self.parse_module_declaration()
            elif self.match("KEYWORD", "import"):
                node = self.parse_import_statement()
            elif self.match("KEYWORD", "function"):
                node = self.parse_function_declaration(is_exported, visibility)
            elif self.match("KEYWORD", "print"):
                node = self.parse_print()
            elif self.match("KEYWORD", "show"):
                node = self.parse_show()
            elif self.match("KEYWORD", "if"):
                node = self.parse_if()
            elif self.match("KEYWORD", "while"):
                node = self.parse_while()
            elif self.match("KEYWORD", "try"):
                node = self.parse_try_block()
            elif self.match("KEYWORD", "repeat"):
                node = self.parse_repeat()
            elif self.match("KEYWORD", "task"):
                node = self.parse_task(visibility)
            elif self.match("KEYWORD", "test"):
                node = self.parse_test()
            elif self.match("KEYWORD", "expect"):
                node = self.parse_expect()
            elif self.match("KEYWORD", "run"):
                node = self.parse_run()
            elif self.match("KEYWORD", "list"):
                if self.check("DOUBLE_COLON"):
                    self.current -= 1
                    node = self.parse_expression()
                    self.consume("DOT", "Expect '.' after expression statement.")
                else:
                    node = self.parse_list_declaration()
            elif self.match("KEYWORD", "map"):
                if self.check("DOUBLE_COLON"):
                    self.current -= 1
                    node = self.parse_expression()
                    self.consume("DOT", "Expect '.' after expression statement.")
                else:
                    node = self.parse_map_declaration()
            elif self.match("KEYWORD", "for"):
                node = self.parse_for_each()
            elif self.match("KEYWORD", "return"):
                node = self.parse_return_statement()
            elif self.match("KEYWORD", "use"):
                node = self.parse_use_statement()
            elif self.match("KEYWORD", "export"):
                node = self.parse_export_statement()
            elif self.match("KEYWORD", "record"):
                node = self.parse_record_declaration()
            elif self.match("KEYWORD", "write"):
                node = self.parse_write_statement()
            elif self.match("KEYWORD", "add"):
                node = self.parse_add_statement()
            elif self.match("KEYWORD", "set"):
                node = self.parse_set_statement()
            elif self.match("KEYWORD", "serve"):
                if self.check("DOT"):
                    self.advance()
                    node = UIServeNode()
                else:
                    node = self.parse_serve()
            elif self.match("KEYWORD", "route"):
                node = self.parse_route("GET")
            # Agar entity keyword mila, to Entity parse karo.
            elif self.match("KEYWORD", "entity"):
                node = self.parse_entity_declaration()
            elif self.match("KEYWORD", "create"):
                node = self.parse_create()
            elif self.match("KEYWORD", "insert"):
                node = self.parse_insert()
            elif self.match("KEYWORD", "update"):
                node = self.parse_update()
            elif self.check("KEYWORD", "get"):
                self.advance()
                node = self.parse_route("GET")
            elif self.check("KEYWORD", "post"):
                self.advance()
                node = self.parse_route("POST")
            elif self.check("KEYWORD", "delete"):
                if self.peek_next().type == "STRING":
                    self.advance()
                    node = self.parse_route("DELETE")
                else:
                    self.advance()
                    node = self.parse_delete()
            elif self.match("KEYWORD", "login"):
                node = self.parse_login()
            elif self.match("KEYWORD", "logout"):
                node = self.parse_logout()
            elif self.match("KEYWORD", "guard"):
                node = self.parse_guard()
            elif self.match("KEYWORD", "storage"):
                node = self.parse_storage()
            elif self.match("KEYWORD", "model"):
                node = self.parse_model()
            elif self.match("KEYWORD", "service"):
                node = self.parse_service()
            elif self.match("KEYWORD", "security"):
                node = self.parse_security()
            elif self.match("KEYWORD", "project"):
                node = self.parse_project_def()
            elif self.match("KEYWORD", "theme"):
                node = self.parse_theme_def()
            elif self.check("KEYWORD", "state"):
                node = self.parse_state_def()
            elif self.check("KEYWORD", "page"):
                # Differentiate between flat page and block page
                # In flat, it's just 'page Home.'
                # In block, it has 'end.' later. Let's just consume the flat one for now.
                # Since the old parse_ui_block is breaking, we can check if it's the new style by looking for 'end'.
                self.advance()
                if self.is_flat_ui_syntax():
                    node = self.parse_page_def()
                else:
                    node = self.parse_ui_block(is_page=True)
            elif self.match("KEYWORD", "title"):
                node = self.parse_title_def()
            elif self.match("KEYWORD", "button"):
                node = self.parse_button_def()
            elif self.check("KEYWORD", "component"):
                self.advance()
                node = self.parse_ui_block(is_page=False)
            elif self.match("KEYWORD", "crud"):
                node = self.parse_crud()
            elif self.match("KEYWORD", "relation"):
                node = self.parse_relation()
            elif self.match("KEYWORD", "role"):
                node = self.parse_role()
            elif self.match("KEYWORD", "allow"):
                node = self.parse_allow()
            elif self.match("KEYWORD", "workflow"):
                node = self.parse_workflow()
            elif self.match("KEYWORD", "interface"):
                node = self.parse_interface_declaration()
            elif self.match("KEYWORD", "extend"):
                node = self.parse_extension_declaration()
            elif self.match("KEYWORD", "throw"):
                node = self.parse_throw_statement()
            elif self.match("KEYWORD", "panic"):
                node = self.parse_panic_statement()
            elif self.match("KEYWORD", "assert"):
                node = self.parse_assert_statement()
            elif self.check("IDENTIFIER"):
                if self.current + 2 < len(self.tokens) and \
                   self.tokens[self.current + 1].type == "IDENTIFIER" and \
                   self.tokens[self.current + 2].value == "is":
                    node = self.parse_instance_declaration()
                else:
                    is_assignment = False
                    lookahead = self.current
                    while lookahead < len(self.tokens) and self.tokens[lookahead].type != "DOT":
                        if self.tokens[lookahead].value in ("is", "=", "+=", "-="):
                            is_assignment = True
                            break
                        lookahead += 1
                    
                    if is_assignment:
                        node = self.parse_assignment_statement()
                    else:
                        node = self.parse_expression()
                        self.consume("DOT", "Expect '.' after expression statement.")
            else:
                raise AAYUSyntaxError(f"Unexpected token '{self.peek().value}'", self.peek().line, column=self.peek().column, hint="Check for typos or missing keywords.")
            
        if node:
            end_token = self.tokens[self.current - 1] if self.current > 0 else start_token
            from compiler.frontend.location import SourceSpan
            node.span = SourceSpan(
                file_id=self.file_id,
                start_line=start_token.line,
                start_column=start_token.column,
                end_line=end_token.line,
                end_column=end_token.column
            )
            node.line = start_token.line
            node.column = start_token.column
            node.file = self.filename
        return node

    def parse_type_annotation(self) -> Any:
        from compiler.frontend.type_nodes import NamedTypeNode, GenericTypeNode
        name = self.consume("IDENTIFIER", "Expect type name.").value
        if self.match("LESS", "<"):
            type_args = []
            if not self.check("GREATER", ">"):
                while True:
                    type_args.append(self.parse_type_annotation())
                    if not self.match("COMMA", ","):
                        break
            self.consume("GREATER", "Expect '>' after type arguments.", ">")
            return GenericTypeNode(NamedTypeNode(name), type_args)
        return NamedTypeNode(name)

    def parse_optional_type_parameters(self) -> list[str]:
        type_params = []
        if self.match("LESS", "<"):
            if not self.check("GREATER", ">"):
                while True:
                    param = self.consume("IDENTIFIER", "Expect type parameter name.").value
                    if param in type_params:
                        from compiler.frontend.errors import AAYUSyntaxError
                        raise AAYUSyntaxError(f"Duplicate type parameter '{param}'.", self.previous().line, column=self.previous().column)
                    type_params.append(param)
                    if not self.match("COMMA", ","):
                        break
            self.consume("GREATER", "Expect '>' after type parameters.", ">")
        return type_params

    def parse_declaration(self, var_type: str, is_exported: bool = False, visibility: str = "private") -> DeclarationNode:
        name = self.consume("IDENTIFIER", "Expect variable name.").value
        
        type_annotation = None
        if self.match("COLON", ":"):
            type_annotation = self.parse_type_annotation()
        
        if self.match("KEYWORD", "is") or self.match("EQ", "="):
            pass
        else:
            token = self.peek()
            from compiler.frontend.errors import AAYUSyntaxError
            raise AAYUSyntaxError("Expect 'is' or '=' after variable name.", token.line, token.column)
        
        value = self.parse_expression()
        
        self.match("DOT", ".")
        node = DeclarationNode(var_type=var_type, name=name, value=value, is_exported=is_exported, visibility=visibility)
        node.type_annotation = type_annotation
        return node

    def parse_module_declaration(self) -> ModuleDeclarationNode:
        name = self.consume("IDENTIFIER", "Expect module name.").value
        self.consume("DOT", "Expect '.' after module name.")
        return ModuleDeclarationNode(name=name)

    def parse_import_statement(self) -> ImportNode:
        name_parts = []
        name_parts.append(self.consume("IDENTIFIER", "Expect module name to import.").value)
        
        dot_consumed = False
        while self.match("DOT"):
            if self.check("IDENTIFIER"):
                name_parts.append(self.advance().value)
            else:
                dot_consumed = True
                break
                
        module_name = ".".join(name_parts)
        alias = None
        selective_imports = None

        if not dot_consumed:
            if self.match("KEYWORD", "as"):
                alias = self.consume("IDENTIFIER", "Expect alias after 'as'.").value
                self.consume("DOT", "Expect '.' after import alias.")
            elif self.match("DOUBLE_COLON"):
                self.consume("LBRACE", "Expect '{' for selective imports.")
                selective_imports = {}
                if not self.check("RBRACE"):
                    while True:
                        sym = self.consume("IDENTIFIER", "Expect symbol name.").value
                        sym_alias = None
                        if self.match("KEYWORD", "as"):
                            sym_alias = self.consume("IDENTIFIER", "Expect alias after 'as'.").value
                        selective_imports[sym] = sym_alias
                        if not self.match("COMMA"):
                            break
                self.consume("RBRACE", "Expect '}' after selective imports.")
                self.consume("DOT", "Expect '.' after import statement.")
            else:
                self.consume("DOT", "Expect '.' after import statement.")
                
        return ImportNode(module_name=module_name, alias=alias, selective_imports=selective_imports)

    def parse_print(self) -> BuiltinFunctionNode:
        self.consume("LPAREN", "Expect '(' after print.")
        arguments = []
        if not self.check("RPAREN", ")"):
            arguments.append(self.parse_expression())
        self.consume("RPAREN", "Expect ')' after print arguments.")
        self.match("DOT", ".")
        return BuiltinFunctionNode(name="print", arguments=arguments)

    def parse_show(self) -> ShowNode:
        expression = self.parse_expression()
        self.consume("DOT", "Expect '.' after show statement.")
        return ShowNode(expression=expression)

    def parse_if(self) -> IfNode:
        condition = self.parse_expression()
        self.match("DOT", ".")
        
        body = []
        else_body = None
        
        while not self.is_at_end() and not self.check("KEYWORD", "end") and not self.check("KEYWORD", "else"):
            body.append(self.parse_statement())
            
        if self.match("KEYWORD", "else"):
            self.match("DOT", ".")
            else_body = []
            while not self.is_at_end() and not self.check("KEYWORD", "end"):
                else_body.append(self.parse_statement())
            
        self.consume("KEYWORD", "Expect 'end' after if statement.", "end")
        self.match("DOT", ".")
        
        return IfNode(condition=condition, body=body, else_body=else_body)

    def parse_while(self) -> WhileNode:
        condition = self.parse_expression()
        self.consume("DOT", "Expect '.' after while condition.")
        
        body = []
        while not self.is_at_end() and not self.check("KEYWORD", "end"):
            body.append(self.parse_statement())
            
        self.consume("KEYWORD", "Expect 'end' after while block.", "end")
        self.consume("DOT", "Expect '.' after 'end'.")
        
        return WhileNode(condition=condition, body=body)

    def parse_try_block(self) -> TryNode:
        self.consume("DOT", "Expect '.' after 'try'.")
        
        try_body = []
        while not self.is_at_end() and not self.check("KEYWORD", "catch") and not self.check("KEYWORD", "finally") and not self.check("KEYWORD", "end"):
            try_body.append(self.parse_statement())
        
        catch_node = None
        if self.match("KEYWORD", "catch"):
            # Parse catch binding: catch (e).
            self.consume("LPAREN", "Expect '(' after 'catch'.")
            binding = self.consume("IDENTIFIER", "Expect exception binding name.").value
            self.consume("RPAREN", "Expect ')' after catch binding.")
            self.consume("DOT", "Expect '.' after catch declaration.")
            
            catch_body = []
            while not self.is_at_end() and not self.check("KEYWORD", "finally") and not self.check("KEYWORD", "end"):
                catch_body.append(self.parse_statement())
            catch_node = CatchNode(binding=binding, block=catch_body)
        
        finally_node = None
        if self.match("KEYWORD", "finally"):
            self.consume("DOT", "Expect '.' after 'finally'.")
            finally_body = []
            while not self.is_at_end() and not self.check("KEYWORD", "end"):
                finally_body.append(self.parse_statement())
            finally_node = FinallyNode(block=finally_body)
        
        self.consume("KEYWORD", "Expect 'end' after try block.", "end")
        self.consume("DOT", "Expect '.' after 'end'.")
        
        return TryNode(try_block=try_body, catch_node=catch_node, finally_node=finally_node)

    def parse_throw_statement(self) -> ThrowNode:
        expression = self.parse_expression()
        self.match("DOT", ".")
        return ThrowNode(expression=expression)

    def parse_panic_statement(self) -> PanicNode:
        message = self.parse_expression()
        self.match("DOT", ".")
        return PanicNode(message=message)

    def parse_assert_statement(self) -> AssertNode:
        condition = self.parse_expression()
        self.match("DOT", ".")
        return AssertNode(condition=condition)

    def parse_repeat(self) -> RepeatNode:
        count = self.parse_expression()
        self.consume("KEYWORD", "Expect 'times' after repeat count.", "times")
        self.consume("DOT", "Expect '.' after 'times'.")
        
        body = []
        while not self.is_at_end() and not self.check("KEYWORD", "end"):
            body.append(self.parse_statement())
            
        self.consume("KEYWORD", "Expect 'end' after repeat block.", "end")
        self.consume("DOT", "Expect '.' after 'end'.")
        
        return RepeatNode(count=count, body=body)

    def parse_task(self, visibility: str = "private") -> TaskNode:
        if self.match("IDENTIFIER"):
            name = self.previous().value
        elif self.match("KEYWORD"):
            name = self.previous().value
        else:
            name = self.consume("IDENTIFIER", "Expect task name.").value
        
        parameters = []
        if self.match("KEYWORD", "with"):
            parameters.append(self.consume("IDENTIFIER", "Expect parameter name after 'with'.").value)
            while self.match("KEYWORD", "and"):
                parameters.append(self.consume("IDENTIFIER", "Expect parameter name after 'and'.").value)
                
        self.consume("DOT", "Expect '.' after task declaration.")
        
        body = []
        self.execution_scope_depth += 1
        while not self.is_at_end() and not self.check("KEYWORD", "end"):
            body.append(self.parse_statement())
            
        self.consume("KEYWORD", "Expect 'end' after task block.", "end")
        self.consume("DOT", "Expect '.' after 'end'.")
        self.execution_scope_depth -= 1
        
        return TaskNode(name=name, parameters=parameters, body=body, visibility=visibility)

    def parse_export_statement(self) -> ExportNode:
        if self.match("KEYWORD", "task"):
            decl = self.parse_task("public")
            return ExportNode(declaration=decl)
        
        if self.match("LBRACE"):
            symbols = []
            if not self.check("RBRACE"):
                while True:
                    symbols.append(self.consume("IDENTIFIER", "Expect exported symbol.").value)
                    if not self.match("COMMA"):
                        break
            self.consume("RBRACE", "Expect '}' after export list.")
            self.consume("DOT", "Expect '.' after export list.")
            return ExportListNode(symbols=symbols)
            
        # Note: Currently scope locked to Tasks or Blocks only
        raise AAYUSyntaxError(f"Can only export tasks or a block of symbols. Found '{self.peek().value}'", self.peek().line, column=self.peek().column, hint="Use 'export task <name>' or 'export { symbol }'.")

    def parse_serve(self) -> ServeNode:
        handler_name = None
        if not self.match("KEYWORD", "on"):
            handler_name = self.consume("IDENTIFIER", "Expect task handler name or 'on' after 'serve'.").value
            self.consume("KEYWORD", "Expect 'on' after handler name in serve statement.", "on")
        
        port = self.parse_expression()
        self.consume("DOT", "Expect '.' after serve statement.")
        return ServeNode(handler_name=handler_name, port=port)

    def parse_route(self, method: str = "GET") -> Node:
        path = self.parse_expression()
        if self.match("KEYWORD", "to"):
            if self.check("IDENTIFIER") or self.check("KEYWORD"):
                handler_name = self.advance().value
            else:
                raise AAYUSyntaxError("Expect handler task name after 'to'.", self.peek().line, column=self.peek().column)
            self.consume("DOT", "Expect '.' after route declaration.")
            return RouteNode(path=path, handler_name=handler_name, method=method)
        else:
            # Frontend route: route "/" Home.
            target_page = self.consume("IDENTIFIER", "Expect page name for frontend route.").value
            self.consume("DOT", "Expect '.' after route declaration.")
            # path is an AST expression, we expect it to be a TextNode
            path_str = path.value if hasattr(path, 'value') else ""
            return RouteDefNode(path=path_str, target_page=target_page)

    def _parse_run_core(self) -> RunNode:
        # Check for qualified access: IDENTIFIER.IDENTIFIER
        module_name = None
        task_name = self.consume("IDENTIFIER", "Expect task name after 'run'.").value
        
        # Only consume DOT if the token AFTER it is an IDENTIFIER
        if self.peek().type == "DOT" and self.peek_next().type == "IDENTIFIER":
            self.consume("DOT", "Expect '.'")
            module_name = task_name
            task_name = self.consume("IDENTIFIER", "Expect task name after module dot.").value
            
        args = []
        if self.match("KEYWORD", "with"):
            args.append(self.parse_expression())
            while self.match("KEYWORD", "and"):
                args.append(self.parse_expression())
                
        return RunNode(name=task_name, arguments=args, module_name=module_name)

    def parse_test(self):
        start_token = self.tokens[self.current - 1]
        name_token = self.consume("STRING", "Expect test name as a string.")
        name = name_token.value.strip('"')
        self.consume("DOT", "Expect '.' after test name.")
        
        body = []
        while not self.is_at_end() and not (self.peek().type == "KEYWORD" and self.peek().value == "end"):
            body.append(self.parse_statement())
            
        self.consume("KEYWORD", "Expect 'end' at the end of test declaration.")
        self.consume("DOT", "Expect '.' after 'end'.")
        
        node = TestNode(name, body)
        node.line = start_token.line
        return node

    def parse_expect(self):
        start_token = self.tokens[self.current - 1]
        actual = self.parse_expression()
        self.consume("KEYWORD", "Expect 'equals' in expect statement.")
        expected = self.parse_expression()
        self.consume("DOT", "Expect '.' after expect statement.")
        
        node = ExpectNode(actual, expected, "equals")
        node.line = start_token.line
        return node

    def parse_run(self) -> RunNode:
        node = self._parse_run_core()
        self.consume("DOT", "Expect '.' after run statement.")
        return node

    def parse_return_statement(self) -> ReturnNode:
        if self.execution_scope_depth == 0:
            raise AAYUSyntaxError("Return can only be used inside an execution scope (task, function, etc.).", self.peek().line, column=self.peek().column, hint="Move the 'return' statement inside a 'task' or 'function' block.")
            
        value = self.parse_expression()
        self.consume("DOT", "Expect '.' after return statement.")
        
        return ReturnNode(value=value)

    def parse_function_declaration(self, is_exported: bool = False, visibility: str = "private") -> FunctionDeclNode:
        start_token = self.previous()
        name = self.consume("IDENTIFIER", "Expect function name.").value
        type_parameters = self.parse_optional_type_parameters()
        self.consume("LPAREN", "Expect '(' after function name.")
        parameters = []
        if not self.check("RPAREN"):
            param_name = self.consume("IDENTIFIER", "Expect parameter name.").value
            param_type = None
            if self.match("COLON", ":"):
                param_type = self.parse_type_annotation()
            parameters.append((param_name, param_type))
            while self.match("COMMA"):
                param_name = self.consume("IDENTIFIER", "Expect parameter name.").value
                param_type = None
                if self.match("COLON", ":"):
                    param_type = self.parse_type_annotation()
                parameters.append((param_name, param_type))
        self.consume("RPAREN", "Expect ')' after parameters.")
        
        return_type = None
        if self.match("COLON", ":"):
            return_type = self.parse_type_annotation()
        
        body = []
        self.execution_scope_depth += 1
        while not self.check("KEYWORD", "end") and not self.is_at_end():
            body.append(self.parse_statement())
            
        self.execution_scope_depth -= 1
            
        self.consume("KEYWORD", "Expected 'end' to close function block", "end")
        self.consume("DOT", "Expected '.' after 'end'")
        
        node = FunctionDeclNode(name=name, parameters=parameters, body=body, is_exported=is_exported, visibility=visibility, type_parameters=type_parameters)
        node.return_type = return_type
        node.line = start_token.line
        node.column = start_token.column
        return node

    def parse_interface_declaration(self, is_exported: bool = False, visibility: str = "private") -> InterfaceDeclNode:
        name = self.consume("IDENTIFIER", "Expect interface name.").value
        type_parameters = self.parse_optional_type_parameters()
        methods = []
        while not self.check("KEYWORD", "end") and not self.is_at_end():
            self.consume("KEYWORD", "Expect 'function' in interface.", "function")
            
            token = self.advance()
            if token.type not in ("IDENTIFIER", "KEYWORD"):
                from compiler.frontend.errors import AAYUSyntaxError
                raise AAYUSyntaxError(f"Expect method name. Found '{token.value}'", token.line, column=token.column)
            method_name = token.value
            
            self.consume("LPAREN", "Expect '(' after method name.")
            parameters = []
            if not self.check("RPAREN"):
                param_name = self.consume("IDENTIFIER", "Expect parameter name.").value
                param_type = None
                if self.match("COLON", ":"):
                    param_type = self.parse_type_annotation()
                parameters.append((param_name, param_type))
                while self.match("COMMA"):
                    param_name = self.consume("IDENTIFIER", "Expect parameter name.").value
                    param_type = None
                    if self.match("COLON", ":"):
                        param_type = self.parse_type_annotation()
                    parameters.append((param_name, param_type))
            self.consume("RPAREN", "Expect ')' after parameters.")
            
            return_type = None
            if self.match("COLON", ":"):
                return_type = self.parse_type_annotation()
                
            self.consume("DOT", "Expect '.' after interface method signature.")
            methods.append(InterfaceMethodNode(name=method_name, parameters=parameters, return_type=return_type))
            
        self.consume("KEYWORD", "Expect 'end' after interface body.", "end")
        self.consume("DOT", "Expect '.' after 'end'.")
        
        return InterfaceDeclNode(
            name=name, 
            methods=methods, 
            is_exported=is_exported, 
            visibility=visibility,
            type_parameters=type_parameters
        )

    def parse_extension_declaration(self) -> ExtensionDeclNode:
        target_type = self.consume("IDENTIFIER", "Expect target type name for extension.").value
        type_parameters = self.parse_optional_type_parameters()
        interface_name = None
        if self.match("KEYWORD", "with"):
            interface_name = self.consume("IDENTIFIER", "Expect interface name after 'with'.").value
            self.parse_optional_type_parameters()
            
        self.consume("DOT", "Expect '.' after extension declaration.")
        
        methods = []
        while not self.check("KEYWORD", "end") and not self.is_at_end():
            if self.match("KEYWORD", "function"):
                methods.append(self.parse_function_declaration())
            elif self.match("KEYWORD", "task"):
                methods.append(self.parse_task())
            else:
                from compiler.frontend.errors import AAYUSyntaxError
                token = self.peek()
                raise AAYUSyntaxError(f"Expect 'function' or 'task' in extension block. Found '{token.value}'", token.line, column=token.column)
                
        self.consume("KEYWORD", "Expect 'end' after extension block.", "end")
        self.consume("DOT", "Expect '.' after 'end'.")
        
        return ExtensionDeclNode(
            target_type=target_type, 
            interface_name=interface_name, 
            methods=methods, 
            type_parameters=type_parameters
        )

    def parse_use_statement(self) -> UseNode:
        module_name = self.consume("IDENTIFIER", "Expect module name after 'use'.").value
        self.consume("DOT", "Expect '.' after module name.")
        return UseNode(module=module_name)

    def parse_record_declaration(self) -> RecordDeclarationNode:
        name = self.consume("IDENTIFIER", "Expect record name.").value
        type_parameters = self.parse_optional_type_parameters()
        self.consume("DOT", "Expect '.' after record declaration.")
        
        fields = []
        while not self.is_at_end() and not self.check("KEYWORD", "end"):
            fields.append(self.consume("IDENTIFIER", "Expect field name in record.").value)
            if self.match("COLON", ":"):
                self.parse_type_annotation()
            
        self.consume("KEYWORD", "Expect 'end' after record body.", "end")
        self.consume("DOT", "Expect '.' after record end.")
        
        return RecordDeclarationNode(
            name=name, 
            fields=fields, 
            type_parameters=type_parameters
        )

    def parse_instance_declaration(self) -> InstanceDeclarationNode:
        type_name = self.consume("IDENTIFIER", "Expect record type name.").value
        name = self.consume("IDENTIFIER", "Expect instance name.").value
        self.consume("KEYWORD", "Expect 'is' after instance name.", "is")
        self.consume("DOT", "Expect '.' after 'is'.")
        
        properties = {}
        while not self.is_at_end() and not self.check("KEYWORD", "end"):
            field = self.consume("IDENTIFIER", "Expect field name.").value
            expr = self.parse_expression()
            properties[field] = expr
            
        self.consume("KEYWORD", "Expect 'end' after instance properties.", "end")
        self.consume("DOT", "Expect '.' after 'end'.")
        
        return InstanceDeclarationNode(type_name=type_name, name=name, properties=properties)

    def parse_assignment_statement(self) -> Node:
        target = self.parse_primary()
        if self.match("KEYWORD", "is") or self.match("EQ"):
            value = self.parse_expression()
            self.consume("DOT", "Expect '.' after assignment statement.")
            return AssignmentNode(target=target, value=value)
        elif self.match("PLUS_EQ") or self.match("MINUS_EQ"):
            operator = self.previous().value
            value = self.parse_expression()
            self.consume("DOT", "Expect '.' after assignment statement.")
            return BinaryExpressionNode(left=target, operator=operator, right=value)
        else:
            raise AAYUSyntaxError("Expect 'is', '=', '+=', or '-=' after assignment target.", self.peek().line, column=self.peek().column)

    def parse_write_statement(self) -> WriteStatementNode:
        data = self.parse_expression()
        self.consume("KEYWORD", "Expect 'to' after write data.", "to")
        destination = self.parse_expression()
        self.consume("DOT", "Expect '.' after write statement.")
        return WriteStatementNode(data=data, destination=destination)

    def parse_list_declaration(self) -> Node:
        name = self.consume("IDENTIFIER", "Expect list name.").value
        
        if self.match("KEYWORD", "is"):
            if self.match("KEYWORD", "find"):
                expr = self.parse_find()
                self.consume("DOT", "Expect '.' after find declaration.")
                return ListInitializationNode(name=name, value=expr)
            else:
                value = self.parse_expression()
                self.consume("DOT", "Expect '.' after list declaration.")
                return DeclarationNode(var_type="list", name=name, value=value)
        else:
            self.consume("DOT", "Expect '.' after list declaration.")
            return ListDeclarationNode(name=name, elements=[])

    def parse_add_statement(self) -> AddToListNode:
        item = self.parse_expression()
        self.consume("KEYWORD", "Expect 'to' after item to add.", "to")
        list_name = self.consume("IDENTIFIER", "Expect list name after 'to'.").value
        self.consume("DOT", "Expect '.' after add statement.")
        return AddToListNode(item=item, list_name=list_name)

    def parse_entity_declaration(self):
            name = self.consume("IDENTIFIER", "Expect entity name.").value
            self.consume("DOT", "Expect '.' after entity name.")
        
            fields = []
            while not self.check("KEYWORD") or self.peek().value not in ["end"]:
                if self.is_at_end():
                    raise AAYUSyntaxError(f"Unterminated entity '{name}', expect 'end.'", self.peek().line, hint="You may have forgotten 'end.' to close the entity block.", column=self.peek().column)
                ftype = self.consume("KEYWORD", "Expect field type.").value
                fname = self.consume("IDENTIFIER", "Expect field name.").value
                self.consume("DOT", "Expect '.' after field declaration.")
                fields.append({"type": ftype, "name": fname})
            
            self.consume("KEYWORD", "Expect 'end' after entity fields.", "end")
            self.consume("DOT", "Expect '.' after end.")
            return EntityDeclarationNode(name=name, fields=fields)

    def parse_crud(self) -> CrudNode:
        entity_name = self.consume("IDENTIFIER", "Expect entity name after 'crud'.").value
        self.consume("DOT", "Expect '.' after crud statement.")
        return CrudNode(entity_name=entity_name)

    def parse_relation(self) -> RelationDefNode:
        entity1 = self.consume("IDENTIFIER", "Expect first entity name after 'relation'.").value
        
        # Check for relationship type
        if self.match("KEYWORD", "one_to_one"):
            rel_type = "one_to_one"
        elif self.match("KEYWORD", "one_to_many"):
            rel_type = "one_to_many"
        elif self.match("KEYWORD", "many_to_one"):
            rel_type = "many_to_one"
        elif self.match("KEYWORD", "many_to_many"):
            rel_type = "many_to_many"
        else:
            raise AAYUSyntaxError("Expect relationship type (one_to_one, one_to_many, many_to_one, many_to_many)", self.peek().line, self.peek().column)
            
        entity2 = self.consume("IDENTIFIER", f"Expect second entity name after '{rel_type}'.").value
        self.consume("DOT", "Expect '.' after relation statement.")
        
        return RelationDefNode(entity1=entity1, rel_type=rel_type, entity2=entity2)

    def parse_role(self) -> RoleDefNode:
        role_name = self.consume("IDENTIFIER", "Expect role name after 'role'.").value
        self.consume("DOT", "Expect '.' after role statement.")
        return RoleDefNode(name=role_name)

    def parse_allow(self) -> AllowDefNode:
        role_name = self.consume("IDENTIFIER", "Expect role name after 'allow'.").value
        
        # Action could be an identifier like 'create', 'read', 'update', 'delete', 'view', 'manage'
        action_token = self.peek()
        if action_token.type in ["IDENTIFIER", "KEYWORD"]:
            action = action_token.value
            self.advance()
        else:
            raise AAYUSyntaxError("Expect action (e.g. create, read, update, delete, view, manage) after role name in allow statement.", action_token.line, action_token.column)
            
        target_entity = self.consume("IDENTIFIER", "Expect target entity name after action in allow statement.").value
        self.consume("DOT", "Expect '.' after allow statement.")
        return AllowDefNode(role=role_name, action=action, target_entity=target_entity)

    def parse_workflow(self) -> WorkflowDefNode:
        name = self.consume("IDENTIFIER", "Expect workflow name.").value
        
        # Check for optional 'for <Entity>'
        entity_name = name
        if self.match("KEYWORD", "for"):
            entity_name = self.consume("IDENTIFIER", "Expect entity name after 'for' in workflow.").value
            
        self.consume("DOT", "Expect '.' after workflow declaration.")
        
        steps = []
        while not self.check("KEYWORD") or self.peek().value != "end":
            if self.is_at_end():
                raise AAYUSyntaxError("Unterminated workflow block, expect 'end.'", self.peek().line, self.peek().column)
                
            if self.match("KEYWORD", "step"):
                step_name = self.consume("IDENTIFIER", "Expect step name.").value
                
                # Check for optional 'requires <Role>' and 'after <Step>'
                requires_role = None
                after_step = None
                
                # Simple parsing for MVP, expecting DOT
                # Loop until DOT
                while not self.check("DOT") and not self.is_at_end():
                    # For future extensions like 'requires Role' or 'after Step'
                    self.advance() # Skip tokens for now if any
                    
                self.consume("DOT", "Expect '.' after step declaration.")
                steps.append(StepDefNode(name=step_name, requires_role=requires_role, after_step=after_step))
            else:
                # Ignore other statements in workflow block for now or raise error
                raise AAYUSyntaxError("Expect 'step' statement inside workflow block.", self.peek().line, self.peek().column)
                
        self.consume("KEYWORD", "Expect 'end'.")
        self.consume("DOT", "Expect '.' after end.")
        
        return WorkflowDefNode(name=name, entity_name=entity_name, steps=steps)

    def parse_create(self):
        token = self.peek()
        if token.type == "KEYWORD" and token.value == "account":
            name = self.consume("KEYWORD", "Expect 'account'.", "account").value
        else:
            name = self.consume("IDENTIFIER", "Expect entity or account.").value
            
        self.consume("KEYWORD", "Expect 'with'.", "with")
        data_map = self.consume("IDENTIFIER", "Expect map name after with.").value
        self.consume("DOT", "Expect '.' after create.")
        
        if name == "account":
            return CreateAccountNode(data_map_name=data_map)
        return CreateEntityNode(entity_name=name, data_map=data_map)

    def parse_find(self):
        name = self.consume("IDENTIFIER", "Expect entity name.").value
        if self.match("KEYWORD", "where"):
            field = self.consume("STRING", "Expect field string.").value
            self.consume("KEYWORD", "Expect 'equal'.", "equal")
            self.consume("KEYWORD", "Expect 'to'.", "to")
            val = self.parse_expression()
            return FindEntityNode(entity_name=name, condition_field=field, condition_value=val)
        return FindEntityNode(entity_name=name, condition_field=None, condition_value=None)

    def parse_update(self):
        name = self.consume("IDENTIFIER", "Expect entity name.").value
        self.consume("KEYWORD", "Expect 'where'.", "where")
        field = self.consume("STRING", "Expect field string.").value
        self.consume("KEYWORD", "Expect 'equal'.", "equal")
        self.consume("KEYWORD", "Expect 'to'.", "to")
        cond_val = self.parse_expression()
        self.consume("KEYWORD", "Expect 'with'.", "with")
        data_map = self.consume("IDENTIFIER", "Expect map name after with.").value
        self.consume("DOT", "Expect '.' after update.")
        return UpdateEntityNode(entity_name=name, condition_field=field, condition_value=cond_val, data_map=data_map)

    def parse_delete(self):
        name = self.consume("IDENTIFIER", "Expect entity name.").value
        self.consume("KEYWORD", "Expect 'where'.", "where")
        field = self.consume("STRING", "Expect field string.").value
        self.consume("KEYWORD", "Expect 'equal'.", "equal")
        self.consume("KEYWORD", "Expect 'to'.", "to")
        cond_val = self.parse_expression()
        self.consume("DOT", "Expect '.' after delete.")
        return DeleteEntityNode(entity_name=name, condition_field=field, condition_value=cond_val)

    def parse_login(self):
        creds = self.consume("IDENTIFIER", "Expect credentials map name.").value
        self.consume("DOT", "Expect '.' after login.")
        return LoginNode(user_map_name=creds)

    def parse_logout(self):
        req = self.consume("IDENTIFIER", "Expect request map name.").value
        self.consume("DOT", "Expect '.' after logout.")
        return LogoutNode(req_name=req)

    def parse_guard(self):
        self.consume("KEYWORD", "Expect 'session'.", "session")
        self.consume("DOT", "Expect '.' after guard session.")
        return GuardSessionNode()
    def parse_map_declaration(self) -> Node:
        name = self.consume("IDENTIFIER", "Expect map name.").value
        if self.match("KEYWORD", "is"):
            value = self.parse_expression()
            self.consume("DOT", "Expect '.' after map declaration.")
            return DeclarationNode(var_type="map", name=name, value=value)
        else:
            self.consume("DOT", "Expect '.' after map declaration.")
            return MapDeclarationNode(name=name)

    def parse_set_statement(self) -> SetInMapNode:
        key = self.parse_expression()
        self.consume("KEYWORD", "Expect 'to' after set key.", "to")
        value = self.parse_expression()
        self.consume("KEYWORD", "Expect 'in' after set value.", "in")
        map_name = self.consume("IDENTIFIER", "Expect map name after 'in'.").value
        self.consume("DOT", "Expect '.' after set statement.")
        return SetInMapNode(key=key, value=value, map_name=map_name)

    def parse_for_each(self) -> Node:
        # Actually parses both 'for each' and 'for i in 1..10'
        if self.match("KEYWORD", "each"):
            iterator = self.consume("IDENTIFIER", "Expect iterator name.").value
            self.consume("KEYWORD", "Expect 'in' after iterator name.", "in")
            
            collection = self.parse_expression()
            self.consume("DOT", "Expect '.' after for-each declaration.")
            
            body = []
            while not self.is_at_end() and not self.check("KEYWORD", "end"):
                body.append(self.parse_statement())
                
            self.consume("KEYWORD", "Expect 'end' after for-each block.", "end")
            self.consume("DOT", "Expect '.' after 'end'.")
            
            return ForEachNode(iterator=iterator, collection=collection, body=body)
        else:
            iterator = self.consume("IDENTIFIER", "Expect iterator name.").value
            self.consume("KEYWORD", "Expect 'in' after iterator name.", "in")
            
            start = self.parse_expression()
            self.consume("DOT_DOT", "Expect '..' after start range.")
            end = self.parse_expression()
            
            # optional dot if people write 'for i in 1..10.' but it shouldn't be strictly necessary for just the range? Wait, AAYU uses DOT for statement termination. Let's consume DOT.
            # Actually AAYU statements typically end with DOT.
            if self.check("DOT"):
                self.consume("DOT", "Expect '.' after for-range declaration.")
                
            body = []
            while not self.is_at_end() and not self.check("KEYWORD", "end"):
                body.append(self.parse_statement())
                
            self.consume("KEYWORD", "Expect 'end' after for-range block.", "end")
            self.consume("DOT", "Expect '.' after 'end'.")
            
            return ForRangeNode(iterator=iterator, start=start, end=end, body=body)

    def parse_expression(self) -> Node:
        return self.parse_logical_or()


    def parse_logical_or(self) -> Node:
        expr = self.parse_logical_and()
        while self.match("KEYWORD", "or"):
            operator = "or"
            right = self.parse_logical_and()
            expr = LogicalExpressionNode(left=expr, operator=operator, right=right)
        return expr

    def parse_logical_and(self) -> Node:
        expr = self.parse_comparison()
        while self.match("KEYWORD", "and"):
            operator = "and"
            right = self.parse_comparison()
            expr = LogicalExpressionNode(left=expr, operator=operator, right=right)
        return expr

    def parse_comparison(self) -> Node:
        expr = self.parse_term()
        
        has_is = self.match("KEYWORD", "is")
        
        operator = None
        if has_is:
            if self.match("KEYWORD", "greater"):
                self.consume("KEYWORD", "Expect 'than' after 'greater'.", "than")
                operator = ">"
            elif self.match("KEYWORD", "less"):
                self.consume("KEYWORD", "Expect 'than' after 'less'.", "than")
                operator = "<"
            elif self.match("KEYWORD", "equal"):
                self.consume("KEYWORD", "Expect 'to' after 'equal'.", "to")
                operator = "=="
            else:
                raise AAYUSyntaxError("Expect comparator after 'is'", self.peek().line, column=self.peek().column, hint="Example: 'is greater than', 'is less than', 'is equal to'.")
        elif self.match("EQ_EQ"):
            operator = "=="
        elif self.match("NOT_EQ"):
            operator = "!="
        elif self.match("GTE"):
            operator = ">="
        elif self.match("LTE"):
            operator = "<="
        elif self.match("GREATER"):
            operator = ">"
        elif self.match("LESS"):
            operator = "<"
            
        if operator:
            right = self.parse_term()
            expr = BinaryExpressionNode(left=expr, operator=operator, right=right)
            
        return expr

    def parse_term(self) -> Node:
        expr = self.parse_factor()

        while self.match("PLUS") or self.match("MINUS"):
            operator = self.previous().value
            right = self.parse_factor()
            expr = BinaryExpressionNode(left=expr, operator=operator, right=right)

        return expr

    
    def parse_unary(self) -> Node:
        if self.match("KEYWORD", "not"):
            operator = "not"
            right = self.parse_unary()
            return UnaryExpressionNode(operator=operator, right=right)
        if self.match("MINUS"):
            operator = self.previous().value
            right = self.parse_unary()
            return UnaryExpressionNode(operator=operator, right=right)
        return self.parse_postfix()

    def parse_postfix(self) -> Node:
        expr = self.parse_primary()
        
        while True:
            # Differentiate between method call dot and statement terminator dot.
            if (self.peek().type == "DOT" and 
                self.peek_next().type in ("IDENTIFIER", "KEYWORD") and 
                self.peek_next_next().type == "LPAREN" and
                self.peek().line == self.peek_next().line):
                self.consume("DOT", "Expect '.'")
                method_token = self.advance() # Consume IDENTIFIER or KEYWORD
                method_name = method_token.value
                self.consume("LPAREN", "Expect '(' after method name.")
                args = []
                if not self.check("RPAREN"):
                    args.append(self.parse_expression())
                    while self.match("COMMA"):
                        args.append(self.parse_expression())
                self.consume("RPAREN", "Expect ')' after arguments.")
                expr = MethodCallNode(object_node=expr, method_name=method_name, arguments=args)
            else:
                break
                
        return expr

    def parse_factor(self) -> Node:
        expr = self.parse_unary()

        while self.match("STAR") or self.match("SLASH") or self.match("PERCENT"):
            operator = self.previous().value
            right = self.parse_unary()
            expr = BinaryExpressionNode(left=expr, operator=operator, right=right)

        return expr

    def parse_primary(self) -> Node:
        if self.match("LPAREN"):
            expr = self.parse_expression()
            self.consume("RPAREN", "Expect ')' after expression.")
            return expr
            
        if self.match("KEYWORD", "read"):
            file_path = self.parse_expression()
            return ReadExpressionNode(file_path=file_path)
            
        if self.match("KEYWORD", "render"):
            template_path = self.parse_expression()
            context_map_name = None
            if self.match("KEYWORD", "with"):
                context_map_name = self.consume("IDENTIFIER", "Expect context map name after 'with'.").value
            return RenderExpressionNode(template_path=template_path, context_map_name=context_map_name)
            
        if self.match("KEYWORD", "form"):
            key = self.parse_expression()
            self.consume("KEYWORD", "Expect 'from' after form key.", "from")
            req_name = self.consume("IDENTIFIER", "Expect request map name after 'from'.").value
            return FormGetNode(key=key, req_name=req_name)
            
        if self.match("KEYWORD", "json"):
            if self.check("DOUBLE_COLON"):
                self.current -= 1 # unconsume json so it can be handled as namespace
            else:
                data = self.parse_expression()
                return JsonSerializeNode(data=data)

        if self.match("LBRACKET"):
            elements = []
            if not self.check("RBRACKET"):
                elements.append(self.parse_expression())
                while self.match("COMMA"):
                    elements.append(self.parse_expression())
            self.consume("RBRACKET", "Expect ']' after list elements.")
            return ListLiteralNode(elements=elements)

        if self.match("LBRACE"):
            elements = []
            if not self.check("RBRACE"):
                key = self.parse_expression()
                self.consume("COLON", "Expect ':' after map key.")
                value = self.parse_expression()
                elements.append((key, value))
                while self.match("COMMA"):
                    key = self.parse_expression()
                    self.consume("COLON", "Expect ':' after map key.")
                    value = self.parse_expression()
                    elements.append((key, value))
            self.consume("RBRACE", "Expect '}' after map elements.")
            return MapLiteralNode(elements=elements)

        if self.match("NUMBER"):
            return NumberNode(value=float(self.previous().value))
        if self.match("STRING"):
            # Remove surrounding quotes
            val = self.previous().value[1:-1]
            return TextNode(value=val)
        is_ident = False
        if self.match("IDENTIFIER"):
            is_ident = True
        elif self.check("KEYWORD") and not self.is_at_end() and getattr(self.peek_next(), 'type', None) == "DOUBLE_COLON":
            self.advance()
            is_ident = True
            
        if is_ident:
            identifier_name = self.previous().value
            
            # Support for namespace resolution like `math::sqrt`
            if self.match("DOUBLE_COLON"):
                if self.match("IDENTIFIER") or self.match("KEYWORD"):
                    member_name = self.previous().value
                else:
                    raise AAYUSyntaxError("Expect member name after '::'.", self.peek().line, column=self.peek().column)
                identifier_name = f"{identifier_name}::{member_name}"
            
            if self.match("LPAREN"):
                args = []
                if not self.check("RPAREN"):
                    args.append(self.parse_expression())
                    while self.match("COMMA"):
                        args.append(self.parse_expression())
                self.consume("RPAREN", "Expect ')' after arguments.")
                return BuiltinFunctionNode(name=identifier_name, arguments=args)
                
            var_node = VariableNode(name=identifier_name)
            if self.match("KEYWORD", "of"):
                object_expr = self.parse_unary()
                return PropertyAccessNode(property_name=var_node.name, object_expr=object_expr)
            return var_node
        if self.match("KEYWORD", "get"):
            key = self.parse_expression()
            self.consume("KEYWORD", "Expect 'from' after get key.", "from")
            map_name = self.consume("IDENTIFIER", "Expect map name after 'from'.").value
            return GetFromMapNode(key=key, map_name=map_name)

        if self.match("KEYWORD", "find"):
            from compiler.frontend.ast_nodes import FindNode
            model_name = self.consume("IDENTIFIER", "Expect model name after 'find'.").value
            return FindNode(model_name=model_name)
        if self.match("KEYWORD", "run"):
            return self._parse_run_core()

        raise AAYUSyntaxError(f"Expect expression. Found '{self.peek().value}'.", self.peek().line, column=self.peek().column, hint="Provide a valid value or variable.")

    def parse_ui_block(self, is_page: bool) -> Node:
        start_token = self.tokens[self.current - 1]
        name = self.consume("IDENTIFIER", "Expect name for UI block.").value
        self.consume("DOT", "Expect '.' after UI block name.")
        
        elements = []
        while not self.is_at_end() and not (self.peek().type == "KEYWORD" and self.peek().value == "end"):
            elements.append(self.parse_ui_element())
            
        self.consume("KEYWORD", "Expect 'end' at the end of UI block.", "end")
        self.consume("DOT", "Expect '.' after 'end'.")
        
        if is_page:
            node = UIPageNode(name, elements)
        else:
            node = UIComponentNode(name, elements)
        node.line = start_token.line
        return node

    def is_flat_ui_syntax(self) -> bool:
        # Check if 'end' exists before EOF or another 'page' or 'project' or 'serve'
        for i in range(self.current, len(self.tokens)):
            if self.tokens[i].type == "KEYWORD" and self.tokens[i].value == "end":
                return False
            if self.tokens[i].type == "KEYWORD" and self.tokens[i].value in ["page", "project", "serve"]:
                return True
        return True

    def parse_project_def(self) -> Node:
        token = self.tokens[self.current - 1]
        name = self.consume("IDENTIFIER", "Expect project name.").value
        self.consume("DOT", "Expect '.' after project name.")
        node = ProjectDefNode(name=name)
        node.line = token.line
        return node

    def parse_page_def(self) -> Node:
        token = self.tokens[self.current - 1]
        name = self.consume("IDENTIFIER", "Expect page name.").value
        children = []
        if self.match("LBRACE"):
            while not self.is_at_end() and not self.check("RBRACE"):
                children.append(self.parse_app_ui_block())
            self.consume("RBRACE", "Expect '}' after page body.")
        else:
            self.consume("DOT", "Expect '.' or '{' after page name.")
        
        node = PageDefNode(name=name, children=children)
        node.line = token.line
        return node

    def parse_title_def(self) -> Node:
        token = self.tokens[self.current - 1]
        text = self.consume("STRING", "Expect string after title.").value[1:-1]
        self.consume("DOT", "Expect '.' after title text.")
        node = TitleDefNode(text=text)
        node.line = token.line
        return node

    def parse_button_def(self) -> Node:
        token = self.tokens[self.current - 1]
        text = self.consume("STRING", "Expect string after button.").value[1:-1]
        self.consume("DOT", "Expect '.' after button text.")
        node = ButtonDefNode(text=text)
        node.line = token.line
        return node

    def parse_ui_element(self) -> Node:
        token = self.peek()
        # A custom component reference starts with an IDENTIFIER
        if token.type == "IDENTIFIER":
            self.advance()
            self.consume("DOT", "Expect '.' after custom component reference.")
            return UIElementNode(element_type="component_ref", value=TextNode(token.value), children=None)
            
        if token.type != "KEYWORD":
            raise AAYUSyntaxError("Expect UI element keyword or component name.", token.line, column=token.column)
            
        element_type = self.advance().value
        ui_keywords = [
            "heading", "text", "button", "card", "row", "column", "input", "navbar", "image", "form",
            "table", "modal", "sidebar", "dashboard", "chart", "tabs", "badge", "alert"
        ]
        
        if element_type not in ui_keywords:
            raise AAYUSyntaxError(f"'{element_type}' is not a valid UI element.", token.line, column=token.column)
            
        value_node = None
        # if next token is string, it's the inner text/value
        if self.check("STRING"):
            val_str = self.advance().value[1:-1]
            value_node = TextNode(val_str)
            if self.match("KEYWORD", "to"):
                var_name = self.consume("IDENTIFIER", "Expect variable name after 'to'.").value
                value_node.name = var_name
        elif self.check("IDENTIFIER"):
            val_name = self.advance().value
            value_node = VariableNode(name=val_name)
            
        self.consume("DOT", "Expect '.' after UI element.")
        
        is_block = element_type in ["row", "column", "card", "form", "table", "modal", "sidebar", "dashboard", "tabs"]
        children = None
        if is_block:
            children = []
            while not self.is_at_end() and not (self.peek().type == "KEYWORD" and self.peek().value == "end"):
                children.append(self.parse_ui_element())
            self.consume("KEYWORD", f"Expect 'end' for {element_type} block.", "end")
            self.consume("DOT", "Expect '.' after 'end'.")
            
        return UIElementNode(element_type=element_type, value=value_node, children=children)

    # --- Helper Methods ---

    def match(self, token_type: str, token_value: str = None) -> bool:
        if self.check(token_type, token_value):
            self.advance()
            return True
        return False

    def check(self, token_type: str, token_value: str = None) -> bool:
        if self.is_at_end():
            return False
        if self.peek().type != token_type:
            return False
        if token_value and self.peek().value != token_value:
            return False
        return True

    def parse_app_ui_block(self) -> Node:
        token = self.peek()
        if token.type == "KEYWORD" and token.value == "state":
            return self.parse_state_def()
        
        # Check for properties like padding 20. or center.
        properties_list = ["padding", "margin", "width", "height", "radius", "background", "color", "font", "shadow", "center", "alignStart", "alignEnd", "spaceBetween", "spaceAround", "spaceEvenly"]
        layout_list = ["stack", "container", "grid", "flex", "wrap", "scroll", "spacer", "divider", "row", "column"]
        component_list = ["heading", "text", "button", "password", "textarea", "checkbox", "radio", "switch", "slider", "progress", "avatar", "footer", "hero", "dialog", "accordion", "video", "audio", "canvas", "icon", "card", "input", "navbar", "image", "table", "modal", "sidebar", "dashboard", "chart", "tabs", "badge", "alert", "list", "form"]

        if token.type == "KEYWORD":
            element_type = self.advance().value
            
            if element_type in properties_list:
                # e.g. padding 20. or center.
                val_node = None
                if not self.check("DOT"):
                    val_node = self.parse_expression()
                self.consume("DOT", f"Expect '.' after property {element_type}.")
                return ComponentNode(component_type="property", properties=[{"name": element_type, "value": val_node}])

            elif element_type in layout_list or element_type in component_list:
                node = ComponentNode(component_type=element_type, properties=[], children=[])
                if element_type in layout_list:
                    node = LayoutNode(layout_type=element_type, properties=[], children=[])
                
                # Check for string value, e.g. heading "Ayush Kaushik".
                if self.check("STRING"):
                    val_str = self.advance().value[1:-1]
                    node.properties.append({"name": "text", "value": TextNode(val_str)})
                elif self.check("IDENTIFIER"):
                    val_name = self.advance().value
                    node.properties.append({"name": "bind", "value": VariableNode(name=val_name)})

                # Check for nested block vs DOT
                if self.match("LBRACE"):
                    while not self.is_at_end() and not self.check("RBRACE"):
                        child = self.parse_app_ui_block()
                        if getattr(child, "component_type", None) == "property":
                            node.properties.extend(child.properties)
                        elif getattr(child, "event_type", None) is not None:
                            # Attach event
                            node.properties.append({"name": "event", "value": child})
                        else:
                            node.children.append(child)
                    self.consume("RBRACE", f"Expect '}}' after {element_type} body.")
                elif self.check("KEYWORD", "click"):
                    # Event attachment, skip DOT
                    pass
                else:
                    self.consume("DOT", f"Expect '.' or '{{' after {element_type}.")
                
                # Check if next token is 'click' attached to this component (flat syntax event attachment)
                if self.check("KEYWORD", "click"):
                    self.advance()
                    self.consume("LBRACE", "Expect '{' after 'click'.")
                    action_stmts = []
                    while not self.is_at_end() and not self.check("RBRACE"):
                        action_stmts.append(self.parse_statement())
                    self.consume("RBRACE", "Expect '}' after click block.")
                    action_block = ProgramNode(statements=action_stmts)
                    node.properties.append({"name": "event", "value": EventNode(event_type="click", action_block=action_block)})
                    
                return node

    # --- Phase 2: Full-Stack Parsers ---

    def parse_storage(self) -> Node:
        name = self.consume("IDENTIFIER", "Expect storage name.").value
        self.consume("DOT", "Expect '.' after storage declaration.")
        return StorageNode(name=name)

    def parse_model(self) -> Node:
        name = self.consume("IDENTIFIER", "Expect model name.").value
        self.consume("LBRACE", "Expect '{' after model name.")
        fields = []
        while not self.is_at_end() and not self.check("RBRACE"):
            field_name = self.consume("IDENTIFIER", "Expect field name.").value
            # Field type could be Int, String, Boolean or another Model
            if self.match("IDENTIFIER") or self.match("KEYWORD"):
                field_type = self.previous().value
            else:
                raise AAYUSyntaxError("Expect field type.", self.peek().line, column=self.peek().column)
            
            # Allow arrays like User[]
            if self.match("LBRACKET"):
                self.consume("RBRACKET", "Expect ']' after '[' for array type.")
                field_type += "[]"
                
            self.consume("DOT", "Expect '.' after field declaration.")
            fields.append(ModelFieldNode(name=field_name, field_type=field_type))
            
        self.consume("RBRACE", "Expect '}' after model body.")
        return ModelNode(name=name, fields=fields)

    def parse_service(self) -> Node:
        name = self.consume("IDENTIFIER", "Expect service name.").value
        self.consume("LBRACE", "Expect '{' after service name.")
        endpoints = []
        while not self.is_at_end() and not self.check("RBRACE"):
            if self.match("KEYWORD", "get") or self.match("KEYWORD", "post") or \
               self.match("KEYWORD", "put") or self.match("KEYWORD", "delete"):
                method = self.previous().value.upper()
                path = self.consume("STRING", "Expect endpoint path as string.").value
                
                # Check if it has 'returns'
                returns_type = None
                if self.match("DOT"):
                    pass # Just a flat definition: get "/users".
                elif self.match("LBRACE"):
                    # Block definition
                    action_stmts = []
                    while not self.is_at_end() and not self.check("RBRACE"):
                        action_stmts.append(self.parse_statement())
                    self.consume("RBRACE", "Expect '}' after endpoint block.")
                elif self.match("IDENTIFIER"):
                    # Maybe it's not a dot, but more keywords
                    pass
                else:
                    self.consume("DOT", "Expect '.' after endpoint definition.")
                    
                endpoints.append(EndpointNode(method=method, path=path.strip('"')))
            else:
                self.advance() # Skip unknown tokens in service block for now
                
        self.consume("RBRACE", "Expect '}' after service body.")
        return ServiceNode(name=name, endpoints=endpoints)

    def parse_security(self) -> Node:
        self.consume("LBRACE", "Expect '{' after security keyword.")
        features = []
        while not self.is_at_end() and not self.check("RBRACE"):
            if self.match("KEYWORD") or self.match("IDENTIFIER"):
                features.append(self.previous().value)
                self.consume("DOT", "Expect '.' after security feature.")
            else:
                self.advance()
        self.consume("RBRACE", "Expect '}' after security body.")
        return SecurityNode(features=features)


                
        raise AAYUSyntaxError(f"Unexpected token '{token.value}' in UI block.", token.line, column=token.column)

    def parse_state_def(self) -> Node:
        token = self.consume("KEYWORD", "Expect 'state'.", "state")
        name = self.consume("IDENTIFIER", "Expect state variable name.").value
        self.consume("EQ", "Expect '=' after state name.")
        initial_value = self.parse_expression()
        self.consume("DOT", "Expect '.' after state declaration.")
        node = StateDefNode(name=name, initial_value=initial_value)
        node.line = token.line
        return node

    def parse_theme_def(self) -> Node:
        token = self.tokens[self.current - 1]
        name = self.consume("IDENTIFIER", "Expect theme name.").value
        properties = []
        if self.match("LBRACE"):
            while not self.is_at_end() and not self.check("RBRACE"):
                if self.check("IDENTIFIER") or self.check("KEYWORD"):
                    prop_name = self.advance().value
                else:
                    raise AAYUSyntaxError("Expect property name in theme.", self.peek().line, column=self.peek().column)
                prop_val = self.parse_expression()
                self.consume("DOT", "Expect '.' after theme property.")
                properties.append({"name": prop_name, "value": prop_val})
            self.consume("RBRACE", "Expect '}' after theme body.")
        else:
            self.consume("DOT", "Expect '.' or '{' after theme name.")
        
        node = ThemeNode(name=name, properties=properties)
        node.line = token.line
        return node

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == "EOF"

    def peek(self) -> Token:
        return self.tokens[self.current]

    def peek_next(self) -> Token:
        if self.current + 1 < len(self.tokens):
            return self.tokens[self.current + 1]
        return Token("EOF", "", self.peek().line, column=self.peek().column)

    def peek_next_next(self) -> Token:
        if self.current + 2 < len(self.tokens):
            return self.tokens[self.current + 2]
        return Token("EOF", "", self.peek().line, column=self.peek().column)

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def consume(self, token_type: str, message: str, token_value: str = None) -> Token:
        if self.check(token_type, token_value):
            return self.advance()
            
        hint = ""
        if token_value == "end":
            hint = f"You may have forgotten 'end.' to close the current block."
        elif token_type == "DOT":
            hint = "You may have forgotten a period '.' at the end of the statement."
        elif token_type == "IDENTIFIER" and not token_value:
            hint = "Expected a name or identifier here (e.g. a variable or entity name)."
        else:
            hint = "Check for typos or missing keywords."
            
        raise AAYUSyntaxError(f"{message} Found '{self.peek().value}'", self.peek().line, hint=hint, column=self.peek().column)

    def parse_insert(self):
        from compiler.frontend.ast_nodes import InsertNode
        model_name = self.consume("IDENTIFIER", "Expect model name after 'insert'.").value
        self.consume("LBRACE", "Expect '{' after model name in insert.")
        fields = {}
        while not self.is_at_end() and not self.check("RBRACE"):
            field_name = self.consume("IDENTIFIER", "Expect field name in insert block.").value
            self.consume("EQ", "Expect '=' after field name.")
            value = self.parse_expression()
            self.consume("DOT", "Expect '.' after field value.")
            fields[field_name] = value
        self.consume("RBRACE", "Expect '}' after insert block.")
        return InsertNode(model_name=model_name, fields=fields)

    def parse_update(self):
        from compiler.frontend.ast_nodes import UpdateNode
        model_name = self.consume("IDENTIFIER", "Expect model name after 'update'.").value
        self.consume("LBRACE", "Expect '{' after model name in update.")
        fields = {}
        while not self.is_at_end() and not self.check("RBRACE"):
            field_name = self.consume("IDENTIFIER", "Expect field name in update block.").value
            self.consume("EQ", "Expect '=' after field name.")
            value = self.parse_expression()
            self.consume("DOT", "Expect '.' after field value.")
            fields[field_name] = value
        self.consume("RBRACE", "Expect '}' after update block.")
        return UpdateNode(model_name=model_name, fields=fields)

    def parse_delete(self):
        from compiler.frontend.ast_nodes import DeleteNode
        model_name = self.consume("IDENTIFIER", "Expect model name after 'delete'.").value
        self.consume("DOT", "Expect '.' after delete statement.")
        return DeleteNode(model_name=model_name)

if __name__ == "__main__":
    def parse_entity_declaration(self):
        name = self.consume("IDENTIFIER", "Expect entity name.").value
        self.consume("DOT", "Expect '.' after entity name.")
        
        fields = []
        while not self.check("KEYWORD") or self.peek().value not in ["end"]:
            if self.is_at_end():
                raise AAYUSyntaxError(f"Unterminated entity '{name}', expect 'end.'", self.peek().line, hint="You may have forgotten 'end.' to close the entity block.", column=self.peek().column)
                
            ftype = self.consume("KEYWORD", "Expect field type.").value
            fname = self.consume("IDENTIFIER", "Expect field name.").value
            self.consume("DOT", "Expect '.' after field declaration.")
            fields.append({"type": ftype, "name": fname})
            
        self.consume("KEYWORD", "Expect 'end' after entity fields.", "end")
        self.consume("DOT", "Expect '.' after end.")
        return EntityDeclarationNode(name=name, fields=fields)

    def parse_create(self):
        name = self.consume("IDENTIFIER", "Expect entity or account.").value
        self.consume("KEYWORD", "Expect 'with'.", "with")
        data_map = self.parse_expression()
        self.consume("DOT", "Expect '.' after create.")
    
        if name == "account":
            return CreateAccountNode(data_map=data_map)
        return CreateEntityNode(entity_name=name, data_map=data_map)

    def parse_find(self):
        name = self.consume("IDENTIFIER", "Expect entity name.").value
        if self.match("KEYWORD", "where"):
            field = self.consume("STRING", "Expect field string.").value
            self.consume("KEYWORD", "Expect 'equal'.", "equal")
            self.consume("KEYWORD", "Expect 'to'.", "to")
            val = self.parse_expression()
            return FindEntityNode(entity_name=name, condition_field=field, condition_value=val)
        return FindEntityNode(entity_name=name, condition_field=None, condition_value=None)

    def parse_update(self):
        name = self.consume("IDENTIFIER", "Expect entity name.").value
        self.consume("KEYWORD", "Expect 'where'.", "where")
        field = self.consume("STRING", "Expect field string.").value
        self.consume("KEYWORD", "Expect 'equal'.", "equal")
        self.consume("KEYWORD", "Expect 'to'.", "to")
        cond_val = self.parse_expression()
        self.consume("KEYWORD", "Expect 'with'.", "with")
        data_map = self.parse_expression()
        self.consume("DOT", "Expect '.' after update.")
        return UpdateEntityNode(entity_name=name, condition_field=field, condition_value=cond_val, data_map=data_map)

    def parse_delete(self):
        name = self.consume("IDENTIFIER", "Expect entity name.").value
        self.consume("KEYWORD", "Expect 'where'.", "where")
        field = self.consume("STRING", "Expect field string.").value
        self.consume("KEYWORD", "Expect 'equal'.", "equal")
        self.consume("KEYWORD", "Expect 'to'.", "to")
        cond_val = self.parse_expression()
        self.consume("DOT", "Expect '.' after delete.")
        return DeleteEntityNode(entity_name=name, condition_field=field, condition_value=cond_val)

    def parse_login(self):
        creds = self.parse_expression()
        self.consume("DOT", "Expect '.' after login.")
        return LoginNode(credentials=creds)

    def parse_logout(self):
        req = self.parse_expression()
        self.consume("DOT", "Expect '.' after logout.")
        return LogoutNode(request=req)

    def parse_guard(self):
        self.consume("IDENTIFIER", "Expect 'session'.")
        self.consume("DOT", "Expect '.' after guard session.")
        return GuardSessionNode()

