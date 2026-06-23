from typing import List
from lexer import Token, Lexer
from ast_nodes import (
    ProgramNode, DeclarationNode, ShowNode, BinaryExpressionNode,
    VariableNode, NumberNode, TextNode, IfNode, WhileNode, TryCatchNode, RepeatNode, ForEachNode, TaskNode, RunNode, ListDeclarationNode, ListInitializationNode, ReturnNode, UseNode, RecordDeclarationNode, InstanceDeclarationNode, PropertyAccessNode, AssignmentNode, ReadExpressionNode, WriteStatementNode, AddToListNode, MapDeclarationNode, SetInMapNode, GetFromMapNode, BuiltinFunctionNode, ExportNode, ServeNode, RouteNode, RenderExpressionNode, FormGetNode, JsonSerializeNode, Node,
    EntityDeclarationNode, CreateEntityNode, FindEntityNode, UpdateEntityNode, DeleteEntityNode, CreateAccountNode, FunctionDeclNode,
    LoginNode, LogoutNode, GuardSessionNode, TestNode, ExpectNode, UIPageNode, UIComponentNode, UIElementNode, CrudNode, RelationDefNode, RoleDefNode, AllowDefNode, WorkflowDefNode, StepDefNode
)
from errors import AAYUSyntaxError

class Parser:
    def __init__(self, tokens: List[Token], filename: str = "main.aayu"):
        self.tokens = tokens
        self.current = 0
        self.in_task_depth = 0
        self.filename = filename

    def parse(self) -> ProgramNode:
        statements = []
        while not self.is_at_end():
            statements.append(self.parse_statement())
        return ProgramNode(statements=statements)

    def parse_statement(self) -> Node:
        start_token = self.peek()
        node = None
        
        if self.match("KEYWORD", "number") or self.match("KEYWORD", "text") or self.match("KEYWORD", "let"):
            node = self.parse_declaration(self.previous().value)
        elif self.match("KEYWORD", "function"):
            node = self.parse_function_declaration()
        elif self.match("KEYWORD", "print"):
            node = self.parse_print()
        elif self.match("KEYWORD", "show"):
            node = self.parse_show()
        elif self.match("KEYWORD", "if"):
            node = self.parse_if()
        elif self.match("KEYWORD", "while"):
            node = self.parse_while()
        elif self.match("KEYWORD", "try"):
            node = self.parse_try_catch()
        elif self.match("KEYWORD", "repeat"):
            node = self.parse_repeat()
        elif self.match("KEYWORD", "task"):
            node = self.parse_task()
        elif self.match("KEYWORD", "test"):
            node = self.parse_test()
        elif self.match("KEYWORD", "expect"):
            node = self.parse_expect()
        elif self.match("KEYWORD", "run"):
            node = self.parse_run()
        elif self.match("KEYWORD", "list"):
            node = self.parse_list_declaration()
        elif self.match("KEYWORD", "map"):
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
            node = self.parse_serve()
        elif self.match("KEYWORD", "route"):
            node = self.parse_route("GET")
        elif self.match("KEYWORD", "entity"):
            node = self.parse_entity_declaration()
        elif self.match("KEYWORD", "create"):
            node = self.parse_create()
        elif self.match("KEYWORD", "update"):
            node = self.parse_update()
        elif self.check("KEYWORD", "get"):
            self.advance()
            node = self.parse_route("GET")
        elif self.check("KEYWORD", "post"):
            self.advance()
            node = self.parse_route("POST")
        elif self.check("KEYWORD", "delete"):
            # Route delete is followed by a STRING token (the path, e.g. delete "/books/delete" to delete_book.)
            # Database delete is followed by an IDENTIFIER token (the entity name, e.g. delete Book where id is 1.)
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
        elif self.match("KEYWORD", "page"):
            node = self.parse_ui_block(is_page=True)
        elif self.match("KEYWORD", "component"):
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
        elif self.check("IDENTIFIER"):
            if self.current + 2 < len(self.tokens) and \
               self.tokens[self.current + 1].type == "IDENTIFIER" and \
               self.tokens[self.current + 2].value == "is":
                node = self.parse_instance_declaration()
            else:
                # Check if it's an assignment by looking ahead
                is_assignment = False
                lookahead = self.current
                while lookahead < len(self.tokens) and self.tokens[lookahead].type != "DOT":
                    if self.tokens[lookahead].value in ("is", "="):
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
            node.line = start_token.line
            node.column = start_token.column
            node.file = self.filename
        return node

    def parse_declaration(self, var_type: str) -> DeclarationNode:
        name = self.consume("IDENTIFIER", "Expect variable name.").value
        
        if self.match("KEYWORD", "is") or self.match("EQ", "="):
            pass
        else:
            token = self.peek()
            from errors import AAYUSyntaxError
            raise AAYUSyntaxError("Expect 'is' or '=' after variable name.", token.line, token.column)
        
        value = self.parse_expression()
        
        # Make dot optional for let statements
        self.match("DOT", ".")
        return DeclarationNode(var_type=var_type, name=name, value=value)

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

    def parse_try_catch(self) -> TryCatchNode:
        self.consume("DOT", "Expect '.' after 'try'.")
        
        try_body = []
        while not self.is_at_end() and not self.check("KEYWORD", "catch"):
            try_body.append(self.parse_statement())
            
        self.consume("KEYWORD", "Expect 'catch' after try block.", "catch")
        self.consume("DOT", "Expect '.' after 'catch'.")
        
        catch_body = []
        while not self.is_at_end() and not self.check("KEYWORD", "end"):
            catch_body.append(self.parse_statement())
            
        self.consume("KEYWORD", "Expect 'end' after catch block.", "end")
        self.consume("DOT", "Expect '.' after 'end'.")
        
        return TryCatchNode(try_body=try_body, catch_body=catch_body)

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

    def parse_task(self) -> TaskNode:
        name = self.consume("IDENTIFIER", "Expect task name.").value
        
        parameters = []
        if self.match("KEYWORD", "with"):
            parameters.append(self.consume("IDENTIFIER", "Expect parameter name after 'with'.").value)
            while self.match("KEYWORD", "and"):
                parameters.append(self.consume("IDENTIFIER", "Expect parameter name after 'and'.").value)
                
        self.consume("DOT", "Expect '.' after task declaration.")
        
        body = []
        self.in_task_depth += 1
        while not self.is_at_end() and not self.check("KEYWORD", "end"):
            body.append(self.parse_statement())
            
        self.consume("KEYWORD", "Expect 'end' after task block.", "end")
        self.consume("DOT", "Expect '.' after 'end'.")
        self.in_task_depth -= 1
        
        return TaskNode(name=name, parameters=parameters, body=body)

    def parse_export_statement(self) -> ExportNode:
        if self.match("KEYWORD", "task"):
            decl = self.parse_task()
            return ExportNode(declaration=decl)
        # Note: Currently scope locked to Tasks only
        raise AAYUSyntaxError(f"Can only export tasks. Found '{self.peek().value}'", self.peek().line, column=self.peek().column, hint="Use 'export task <name>'.")

    def parse_serve(self) -> ServeNode:
        handler_name = None
        if not self.match("KEYWORD", "on"):
            handler_name = self.consume("IDENTIFIER", "Expect task handler name or 'on' after 'serve'.").value
            self.consume("KEYWORD", "Expect 'on' after handler name in serve statement.", "on")
        
        port = self.parse_expression()
        self.consume("DOT", "Expect '.' after serve statement.")
        return ServeNode(handler_name=handler_name, port=port)

    def parse_route(self, method: str = "GET") -> RouteNode:
        path = self.parse_expression()
        self.consume("KEYWORD", "Expect 'to' after route path.", "to")
        handler_name = self.consume("IDENTIFIER", "Expect handler task name after 'to'.").value
        self.consume("DOT", "Expect '.' after route statement.")
        return RouteNode(path=path, handler_name=handler_name, method=method)

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
        if self.in_task_depth == 0:
            raise AAYUSyntaxError("Return can only be used inside a task.", self.peek().line, column=self.peek().column, hint="Move the 'return' statement inside a 'task' block.")
            
        value = self.parse_expression()
        self.consume("DOT", "Expect '.' after return statement.")
        
        return ReturnNode(value=value)

    def parse_use_statement(self) -> UseNode:
        module_name = self.consume("IDENTIFIER", "Expect module name after 'use'.").value
        self.consume("DOT", "Expect '.' after module name.")
        return UseNode(module=module_name)

    def parse_record_declaration(self) -> RecordDeclarationNode:
        name = self.consume("IDENTIFIER", "Expect record name.").value
        self.consume("DOT", "Expect '.' after record name.")
        
        fields = []
        while not self.is_at_end() and not self.check("KEYWORD", "end"):
            fields.append(self.consume("IDENTIFIER", "Expect field name in record.").value)
            
        self.consume("KEYWORD", "Expect 'end' after record fields.", "end")
        self.consume("DOT", "Expect '.' after 'end'.")
        
        return RecordDeclarationNode(name=name, fields=fields)

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

    def parse_assignment_statement(self) -> AssignmentNode:
        target = self.parse_primary()
        self.consume("KEYWORD", "Expect 'is' after assignment target.", "is")
        value = self.parse_expression()
        self.consume("DOT", "Expect '.' after assignment statement.")
        return AssignmentNode(target=target, value=value)

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

    def parse_for_each(self) -> ForEachNode:
        self.consume("KEYWORD", "Expect 'each' after 'for'.", "each")
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

    def parse_expression(self) -> Node:
        return self.parse_comparison()

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

    def parse_factor(self) -> Node:
        expr = self.parse_primary()

        while self.match("STAR") or self.match("SLASH"):
            operator = self.previous().value
            right = self.parse_primary()
            expr = BinaryExpressionNode(left=expr, operator=operator, right=right)

        return expr

    def parse_primary(self) -> Node:
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
            data = self.parse_expression()
            return JsonSerializeNode(data=data)

        if self.match("NUMBER"):
            return NumberNode(value=float(self.previous().value))
        if self.match("STRING"):
            # Remove surrounding quotes
            val = self.previous().value[1:-1]
            return TextNode(value=val)
        if self.match("IDENTIFIER"):
            identifier_name = self.previous().value
            
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
                object_expr = self.parse_primary()
                return PropertyAccessNode(property_name=var_node.name, object_expr=object_expr)
            return var_node
        if self.match("KEYWORD", "get"):
            key = self.parse_expression()
            self.consume("KEYWORD", "Expect 'from' after get key.", "from")
            map_name = self.consume("IDENTIFIER", "Expect map name after 'from'.").value
            return GetFromMapNode(key=key, map_name=map_name)
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
