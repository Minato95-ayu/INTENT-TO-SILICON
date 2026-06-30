from ast_nodes import *
from ir import Opcode, Instruction, Bytecode

class AAYUCompiler:
    def __init__(self, filename: str = ""):
        self.bytecode = Bytecode()
        self.loop_counter = 0
        self.filename = filename
        self.current_line = None
        self.ui_generator = None
        self.entity_registry = {}
        
    def _add_constant(self, value) -> int:
        if value in self.bytecode.constants:
            return self.bytecode.constants.index(value)
        self.bytecode.constants.append(value)
        return len(self.bytecode.constants) - 1
        
    def _add_name(self, name: str) -> int:
        if name in self.bytecode.names:
            return self.bytecode.names.index(name)
        self.bytecode.names.append(name)
        return len(self.bytecode.names) - 1
        
    def _emit(self, opcode: Opcode, operand: int = None):
        self.bytecode.instructions.append(
            Instruction(opcode, operand)
        )
        
    def compile(self, node: Node) -> Bytecode:
        self.bytecode.file = self.filename
        self.visit(node)
        return self.bytecode
        
    def visit(self, node: Node):
        old_line = self.current_line
        if hasattr(node, 'line') and node.line is not None:
            self.current_line = node.line
            
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        try:
            return visitor(node)
        finally:
            self.current_line = old_line
        

    def visit_ShowNode(self, node):
        fn_idx = self._add_name('print')
        self._emit(Opcode.LOAD_VAR, fn_idx)
        self.visit(node.expression)
        self._emit(Opcode.CALL, 1)
        self._emit(Opcode.POP)
    def generic_visit(self, node: Node):
        raise NotImplementedError(f"No visit_{type(node).__name__} method defined in compiler")
        
    def visit_ProgramNode(self, node: ProgramNode):
        for stmt in node.statements:
            self.visit(stmt)
        self._emit(Opcode.RETURN)

    def visit_UseNode(self, node: UseNode):
        import os
        from errors import AAYUError
        from lexer import Lexer
        from parser import Parser
        
        module_name = node.module
        
        # Check standard package directory
        package_dir = os.path.join(".aayu", "packages", module_name)
        module_file = os.path.join(package_dir, "main.aayu")
        
        if not os.path.exists(module_file):
            # Fallback to single file import if user wants to import a local file
            if os.path.exists(f"{module_name}.aayu"):
                module_file = f"{module_name}.aayu"
            else:
                line = node.line if hasattr(node, 'line') else 1
                raise AAYUError("Import Error", f"Module '{module_name}' not found.", line, f"Did you forget to run 'aayu install {module_name}'?")
                
        with open(module_file, "r", encoding="utf-8") as f:
            source = f.read()
            
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename=module_file)
        ast = parser.parse()
        
        # Compile the included AST inline
        self.visit(ast)
            
    def visit_NumberNode(self, node: NumberNode):
        idx = self._add_constant(node.value)
        self._emit(Opcode.LOAD_CONST, idx)
        
    def visit_TextNode(self, node: TextNode):
        idx = self._add_constant(node.value)
        self._emit(Opcode.LOAD_CONST, idx)
        
    def visit_VariableNode(self, node: VariableNode):
        idx = self._add_name(node.name)
        self._emit(Opcode.LOAD_VAR, idx)
        
    def visit_DeclarationNode(self, node: DeclarationNode):
        self.visit(node.value)
        idx = self._add_name(node.name)
        self._emit(Opcode.STORE_VAR, idx)

    def visit_FunctionDeclNode(self, node: FunctionDeclNode):
        child_compiler = AAYUCompiler(filename=self.filename)
        child_compiler.bytecode.name = node.name
        child_compiler.bytecode.parameters = node.parameters
        
        # Compile function body
        for stmt in node.body:
            child_compiler.visit(stmt)
            
        # Ensure function always returns
        child_compiler._emit(Opcode.LOAD_CONST, child_compiler._add_constant(None))
        child_compiler._emit(Opcode.RETURN)
        
        func_bytecode = child_compiler.bytecode
        
        const_idx = self._add_constant(func_bytecode)
        self._emit(Opcode.LOAD_CONST, const_idx)
        
        name_idx = self._add_name(node.name)
        self._emit(Opcode.STORE_VAR, name_idx)
        
    def visit_BuiltinFunctionNode(self, node: BuiltinFunctionNode):
        if node.name in ["print"]:
            # Push function name
            fn_idx = self._add_constant(node.name)
            self._emit(Opcode.LOAD_CONST, fn_idx)
        else:
            # User defined function: load the function object from variable
            name_idx = self._add_name(node.name)
            self._emit(Opcode.LOAD_VAR, name_idx)
            
        # Load arguments
        for arg in node.arguments:
            self.visit(arg)
            
        # Emit CALL
        self._emit(Opcode.CALL, len(node.arguments))
        
    def visit_BinaryExpressionNode(self, node: BinaryExpressionNode):
        self.visit(node.left)
        self.visit(node.right)
        
        if node.operator in ('is', 'equals', 'equal to', '==', 'EQUAL'):
            self._emit(Opcode.EQ)
        elif node.operator in ('less', 'less than', '<', 'LESS'):
            self._emit(Opcode.LT)
        elif node.operator in ('greater', 'greater than', '>', 'GREATER'):
            self._emit(Opcode.GT)
        elif node.operator in ('plus', '+', 'PLUS'):
            self._emit(Opcode.ADD)
        elif node.operator in ('minus', '-', 'MINUS'):
            self._emit(Opcode.SUB)
        elif node.operator in ('times', '*', 'TIMES'):
            self._emit(Opcode.MUL)
        elif node.operator in ('divided by', '/', 'DIVIDE'):
            self._emit(Opcode.DIV)
            
    def visit_IfNode(self, node: IfNode):
        self.visit(node.condition)
        
        # Emit JUMP_IF_FALSE with placeholder
        jump_if_false_idx = len(self.bytecode.instructions)
        self._emit(Opcode.JUMP_IF_FALSE, 0)
        
        for stmt in node.body:
            self.visit(stmt)
            
        if node.else_body:
            jump_forward_idx = len(self.bytecode.instructions)
            self._emit(Opcode.JUMP, 0)
            
            # Patch JUMP_IF_FALSE to jump here
            self.bytecode.instructions[jump_if_false_idx].operand = len(self.bytecode.instructions) - jump_if_false_idx
            
            for stmt in node.else_body:
                self.visit(stmt)
                
            # Patch JUMP to jump here
            self.bytecode.instructions[jump_forward_idx].operand = len(self.bytecode.instructions) - jump_forward_idx
        else:
            # Patch JUMP_IF_FALSE to jump here
            self.bytecode.instructions[jump_if_false_idx].operand = len(self.bytecode.instructions) - jump_if_false_idx

    def visit_WhileNode(self, node: WhileNode):
        start_idx = len(self.bytecode.instructions)
        self.visit(node.condition)
        
        jump_if_false_idx = len(self.bytecode.instructions)
        self._emit(Opcode.JUMP_IF_FALSE, 0)
        
        for stmt in node.body:
            self.visit(stmt)
            
        # Jump back to start_idx
        offset = start_idx - len(self.bytecode.instructions)
        self._emit(Opcode.JUMP, offset)
        
        # Patch JUMP_IF_FALSE
        self.bytecode.instructions[jump_if_false_idx].operand = len(self.bytecode.instructions) - jump_if_false_idx
        
    def visit_TaskNode(self, node: TaskNode):
        # Compile task body in a new compiler context
        task_compiler = AAYUCompiler(filename=self.filename)
        task_bytecode = task_compiler.compile(ProgramNode(node.body))
        
        # Ensure the bytecode ends with a RETURN
        if not task_bytecode.instructions or task_bytecode.instructions[-1].opcode != Opcode.RETURN:
            none_idx = task_compiler._add_constant(None)
            task_compiler._emit(Opcode.LOAD_CONST, none_idx)
            task_compiler._emit(Opcode.RETURN)
            
        task_bytecode.parameters = node.parameters
        task_bytecode.name = node.name
        
        # Add to parent constant pool and emit code to register the task variable
        const_idx = self._add_constant(task_bytecode)
        name_idx = self._add_name(node.name)
        
        self._emit(Opcode.LOAD_CONST, const_idx)
        self._emit(Opcode.STORE_VAR, name_idx)
        
    def visit_RunNode(self, node: RunNode):
        name_idx = self._add_name(node.name)
        self._emit(Opcode.LOAD_VAR, name_idx)
        # Push arguments to stack
        for arg in node.arguments:
            self.visit(arg)
            
        # Load the task object

        
        # Call task with number of arguments as operand
        self._emit(Opcode.CALL_TASK, len(node.arguments))

    def visit_AssignmentNode(self, node: AssignmentNode):
        if isinstance(node.target, VariableNode):
            self.visit(node.value)
            idx = self._add_name(node.target.name)
            self._emit(Opcode.STORE_VAR, idx)
        else:
            raise NotImplementedError("Only variable assignment is supported in the VM compiler.")

    def visit_ReturnNode(self, node: ReturnNode):
        if node.value:
            self.visit(node.value)
        else:
            self._emit(Opcode.LOAD_CONST, self._add_constant(None))
        self._emit(Opcode.RETURN)

    def visit_ListDeclarationNode(self, node: ListDeclarationNode):
        self._emit(Opcode.MAKE_LIST, 0)
        idx = self._add_name(node.name)
        self._emit(Opcode.STORE_VAR, idx)

    def visit_ListInitializationNode(self, node: ListInitializationNode):
        self.visit(node.value)
        idx = self._add_name(node.name)
        self._emit(Opcode.STORE_VAR, idx)

    def visit_AddToListNode(self, node: AddToListNode):
        self.visit(node.item)
        idx = self._add_name(node.list_name)
        self._emit(Opcode.LOAD_VAR, idx)
        self._emit(Opcode.LIST_APPEND)
        self._emit(Opcode.POP)

    def visit_MapDeclarationNode(self, node: MapDeclarationNode):
        self._emit(Opcode.MAKE_MAP, 0)
        idx = self._add_name(node.name)
        self._emit(Opcode.STORE_VAR, idx)

    def visit_SetInMapNode(self, node: SetInMapNode):
        self.visit(node.value)
        self.visit(node.key)
        idx = self._add_name(node.map_name)
        self._emit(Opcode.LOAD_VAR, idx)
        self._emit(Opcode.MAP_SET)

    def visit_GetFromMapNode(self, node: GetFromMapNode):
        self.visit(node.key)
        idx = self._add_name(node.map_name)
        self._emit(Opcode.LOAD_VAR, idx)
        self._emit(Opcode.MAP_GET)

    def visit_EntityDeclarationNode(self, node: EntityDeclarationNode):
        fn_idx = self._add_name("db_register_entity")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        self.entity_registry[node.name] = node.fields

        name_idx = self._add_constant(node.name)
        self._emit(Opcode.LOAD_CONST, name_idx)

        fields_idx = self._add_constant(node.fields)
        self._emit(Opcode.LOAD_CONST, fields_idx)
        

        
        self._emit(Opcode.CALL_TASK, 2)
        self._emit(Opcode.POP)

    def visit_CreateEntityNode(self, node: CreateEntityNode):
        fn_idx = self._add_name("db_create")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        name_idx = self._add_constant(node.entity_name)
        self._emit(Opcode.LOAD_CONST, name_idx)
        
        map_idx = self._add_name(node.data_map)
        self._emit(Opcode.LOAD_VAR, map_idx)
        

        
        self._emit(Opcode.CALL_TASK, 2)
        self._emit(Opcode.POP)

    def visit_FindEntityNode(self, node: FindEntityNode):
        fn_idx = self._add_name("db_find")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        name_idx = self._add_constant(node.entity_name)
        self._emit(Opcode.LOAD_CONST, name_idx)
        
        field_idx = self._add_constant(node.condition_field)
        self._emit(Opcode.LOAD_CONST, field_idx)
        
        if node.condition_value:
            self.visit(node.condition_value)
        else:
            self._emit(Opcode.LOAD_CONST, self._add_constant(None))
            

        
        self._emit(Opcode.CALL_TASK, 3)

    def visit_UpdateEntityNode(self, node: UpdateEntityNode):
        fn_idx = self._add_name("db_update")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        name_idx = self._add_constant(node.entity_name)
        self._emit(Opcode.LOAD_CONST, name_idx)
        
        field_idx = self._add_constant(node.condition_field)
        self._emit(Opcode.LOAD_CONST, field_idx)
        
        self.visit(node.condition_value)
        
        map_idx = self._add_name(node.data_map)
        self._emit(Opcode.LOAD_VAR, map_idx)
        

        
        self._emit(Opcode.CALL_TASK, 4)
        self._emit(Opcode.POP)

    def visit_DeleteEntityNode(self, node: DeleteEntityNode):
        fn_idx = self._add_name("db_delete")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        name_idx = self._add_constant(node.entity_name)
        self._emit(Opcode.LOAD_CONST, name_idx)
        
        field_idx = self._add_constant(node.condition_field)
        self._emit(Opcode.LOAD_CONST, field_idx)
        
        self.visit(node.condition_value)
        

        
        self._emit(Opcode.CALL_TASK, 3)
        self._emit(Opcode.POP)

    def visit_JsonSerializeNode(self, node: JsonSerializeNode):
        fn_idx = self._add_name("json_serialize")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        self.visit(node.data)
        

        
        self._emit(Opcode.CALL_TASK, 1)

    def visit_RenderExpressionNode(self, node: RenderExpressionNode):
        fn_idx = self._add_name("render_template")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        self.visit(node.template_path)
        
        if node.context_map_name:
            map_idx = self._add_name(node.context_map_name)
            self._emit(Opcode.LOAD_VAR, map_idx)
        else:
            self._emit(Opcode.LOAD_CONST, self._add_constant(None))
            

        self._emit(Opcode.CALL_TASK, 2)

    def visit_RouteNode(self, node: RouteNode):
        fn_idx = self._add_name("http_route")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        self.visit(node.path)
        method_idx = self._add_constant(node.method)
        self._emit(Opcode.LOAD_CONST, method_idx)
        handler_idx = self._add_constant(node.handler_name)
        self._emit(Opcode.LOAD_CONST, handler_idx)

        self._emit(Opcode.CALL_TASK, 3)
        self._emit(Opcode.POP)

    def visit_FormGetNode(self, node: FormGetNode):
        fn_idx = self._add_name("http_form_get")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        self.visit(node.key)
        idx = self._add_name(node.req_name)
        self._emit(Opcode.LOAD_VAR, idx)

        self._emit(Opcode.CALL_TASK, 2)

    def visit_ServeNode(self, node: ServeNode):
        fn_idx = self._add_name("http_serve")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        self.visit(node.port)
        if node.handler_name:
            idx = self._add_constant(node.handler_name)
            self._emit(Opcode.LOAD_CONST, idx)
        else:
            self._emit(Opcode.LOAD_CONST, self._add_constant(None))
            

        self._emit(Opcode.CALL_TASK, 2)
        self._emit(Opcode.POP)

    def visit_ForEachNode(self, node: ForEachNode):
        loop_id = self.loop_counter
        self.loop_counter += 1
        
        coll_name = f"_coll_{loop_id}"
        idx_name = f"_idx_{loop_id}"
        
        # 1. Evaluate collection and store it in _coll_{id}
        self.visit(node.collection)
        coll_idx = self._add_name(coll_name)
        self._emit(Opcode.STORE_VAR, coll_idx)
        
        # 2. Store 0.0 in _idx_{id}
        self._emit(Opcode.LOAD_CONST, self._add_constant(0.0))
        idx_idx = self._add_name(idx_name)
        self._emit(Opcode.STORE_VAR, idx_idx)
        
        # 3. Mark condition check index
        cond_ip = len(self.bytecode.instructions)
        
        # 4. Check index < len(collection)
        self._emit(Opcode.LOAD_VAR, idx_idx)
        
        len_fn_idx = self._add_name("collection_len")
        self._emit(Opcode.LOAD_VAR, len_fn_idx)
        self._emit(Opcode.LOAD_VAR, coll_idx)
        self._emit(Opcode.CALL_TASK, 1)
        
        self._emit(Opcode.LT)
        
        # 5. Jump if false placeholder
        jump_if_false_idx = len(self.bytecode.instructions)
        self._emit(Opcode.JUMP_IF_FALSE, 0)
        
        # 6. Fetch b = collection[index] and store in node.iterator
        self._emit(Opcode.LOAD_VAR, idx_idx)
        self._emit(Opcode.LOAD_VAR, coll_idx)
        self._emit(Opcode.MAP_GET)
        iterator_idx = self._add_name(node.iterator)
        self._emit(Opcode.STORE_VAR, iterator_idx)
        
        # 7. Compile loop body
        for stmt in node.body:
            self.visit(stmt)
            
        # 8. Increment index: index = index + 1
        self._emit(Opcode.LOAD_VAR, idx_idx)
        self._emit(Opcode.LOAD_CONST, self._add_constant(1.0))
        self._emit(Opcode.ADD)
        self._emit(Opcode.STORE_VAR, idx_idx)
        
        # 9. Jump backward to cond_ip
        offset = len(self.bytecode.instructions) - cond_ip
        self._emit(Opcode.JUMP_BACKWARD, offset)
        
        # 10. Patch condition check jump
        self.bytecode.instructions[jump_if_false_idx].operand = len(self.bytecode.instructions) - jump_if_false_idx

    def visit_CreateAccountNode(self, node: CreateAccountNode):
        fn_idx = self._add_name("auth_create_account")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        map_idx = self._add_name(node.data_map_name)
        self._emit(Opcode.LOAD_VAR, map_idx)

        self._emit(Opcode.CALL_TASK, 1)
        self._emit(Opcode.POP)

    def visit_LoginNode(self, node: LoginNode):
        fn_idx = self._add_name("auth_login")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        map_idx = self._add_name(node.user_map_name)
        self._emit(Opcode.LOAD_VAR, map_idx)

        self._emit(Opcode.CALL_TASK, 1)
        self._emit(Opcode.POP)

    def visit_LogoutNode(self, node: LogoutNode):
        fn_idx = self._add_name("auth_logout")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        req_idx = self._add_name(node.req_name)
        self._emit(Opcode.LOAD_VAR, req_idx)

        self._emit(Opcode.CALL_TASK, 1)
        self._emit(Opcode.POP)

    def visit_GuardSessionNode(self, node: GuardSessionNode):
        fn_idx = self._add_name("auth_guard_session")
        self._emit(Opcode.LOAD_VAR, fn_idx)

        self._emit(Opcode.CALL_TASK, 0)
        self._emit(Opcode.POP)
        self._emit(Opcode.POP)

    def visit_UIComponentNode(self, node: UIComponentNode):
        if not self.ui_generator:
            from ui_generator import UIGenerator
            self.ui_generator = UIGenerator(entity_registry=self.entity_registry)
        else:
            self.ui_generator.entity_registry = self.entity_registry
        self.ui_generator.register_component(node)

    def visit_UIPageNode(self, node: UIPageNode):
        if not self.ui_generator:
            from ui_generator import UIGenerator
            self.ui_generator = UIGenerator(entity_registry=self.entity_registry)
        else:
            self.ui_generator.entity_registry = self.entity_registry
        self.ui_generator.generate_page(node)

    def visit_RoleDefNode(self, node):
        fn_idx = self._add_name("db_register_role")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        name_idx = self._add_constant(node.name)
        self._emit(Opcode.LOAD_CONST, name_idx)
        

        self._emit(Opcode.CALL_TASK, 1)
        self._emit(Opcode.POP)

    def visit_AllowDefNode(self, node):
        fn_idx = self._add_name("db_register_permission")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        role_idx = self._add_constant(node.role)
        self._emit(Opcode.LOAD_CONST, role_idx)
        
        action_idx = self._add_constant(node.action)
        self._emit(Opcode.LOAD_CONST, action_idx)
        
        entity_idx = self._add_constant(node.target_entity)
        self._emit(Opcode.LOAD_CONST, entity_idx)
        

        self._emit(Opcode.CALL_TASK, 3)
        self._emit(Opcode.POP)

    def visit_WorkflowDefNode(self, node):
        fn_idx = self._add_name("db_register_workflow")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        name_idx = self._add_constant(node.name)
        self._emit(Opcode.LOAD_CONST, name_idx)
        
        entity_idx = self._add_constant(node.entity_name)
        self._emit(Opcode.LOAD_CONST, entity_idx)
        
        # Serialize steps as comma-separated string for MVP
        steps_str = ",".join([s.name for s in node.steps])
        steps_idx = self._add_constant(steps_str)
        self._emit(Opcode.LOAD_CONST, steps_idx)
        

        self._emit(Opcode.CALL_TASK, 3)
        self._emit(Opcode.POP)

    def visit_RelationDefNode(self, node):
        fn_idx = self._add_name("db_register_relation")
        self._emit(Opcode.LOAD_VAR, fn_idx)
        e1_idx = self._add_constant(node.entity1)
        self._emit(Opcode.LOAD_CONST, e1_idx)
        
        rel_type_idx = self._add_constant(node.rel_type)
        self._emit(Opcode.LOAD_CONST, rel_type_idx)
        
        e2_idx = self._add_constant(node.entity2)
        self._emit(Opcode.LOAD_CONST, e2_idx)
        

        self._emit(Opcode.CALL_TASK, 3)
        self._emit(Opcode.POP)

    def visit_CrudNode(self, node):
        from ast_nodes import (
            UIPageNode, UIElementNode, TextNode, VariableNode, 
            TaskNode, MapDeclarationNode, DeclarationNode, FindEntityNode, SetInMapNode, 
            ReturnNode, RenderExpressionNode, RouteNode, FormGetNode, CreateEntityNode
        )
        entity_name = node.entity_name
        page_name = f"{entity_name}Admin"
        
        # 1. UI Page
        page_node = UIPageNode(name=page_name, elements=[
            UIElementNode(element_type="dashboard", children=[
                UIElementNode(element_type="sidebar", children=[
                    UIElementNode(element_type="text", value=TextNode(f"{entity_name} Management"))
                ]),
                UIElementNode(element_type="column", children=[
                    UIElementNode(element_type="navbar"),
                    UIElementNode(element_type="row", children=[
                        UIElementNode(element_type="table", value=VariableNode(name=entity_name)),
                        UIElementNode(element_type="form", value=VariableNode(name=entity_name))
                    ])
                ])
            ])
        ])
        self.visit(page_node)
        
        # 2. GET Route Task
        get_task_name = f"__crud_get_{entity_name.lower()}"
        get_body = [
            MapDeclarationNode(name="context"),
            DeclarationNode(var_type="any", name="records", value=FindEntityNode(entity_name=entity_name)),
            SetInMapNode(key=TextNode(entity_name), value=VariableNode("records"), map_name="context"),
            ReturnNode(value=RenderExpressionNode(template_path=TextNode(page_name + ".html"), context_map_name="context"))
        ]
        self.visit(TaskNode(name=get_task_name, parameters=["req"], body=get_body))
        self.visit(RouteNode(path=TextNode(f"/{entity_name.lower()}s"), handler_name=get_task_name, method="GET"))
        
        # 3. POST Route Task
        post_task_name = f"__crud_post_{entity_name.lower()}"
        post_body = [
            MapDeclarationNode(name="data")
        ]
        
        if entity_name in self.entity_registry:
            for field in self.entity_registry[entity_name]:
                fname = field['name']
                if fname in ['created_at', 'updated_at', 'id']: continue
                post_body.append(DeclarationNode(var_type="any", name=f"val_{fname}", value=FormGetNode(key=TextNode(fname), req_name="req")))
                post_body.append(SetInMapNode(key=TextNode(fname), value=VariableNode(f"val_{fname}"), map_name="data"))
                
        post_body.append(CreateEntityNode(entity_name=entity_name, data_map="data"))
        
        # Re-render
        post_body.append(MapDeclarationNode(name="context"))
        post_body.append(DeclarationNode(var_type="any", name="records", value=FindEntityNode(entity_name=entity_name)))
        post_body.append(SetInMapNode(key=TextNode(entity_name), value=VariableNode("records"), map_name="context"))
        post_body.append(ReturnNode(value=RenderExpressionNode(template_path=TextNode(page_name + ".html"), context_map_name="context")))
        
        self.visit(TaskNode(name=post_task_name, parameters=["req"], body=post_body))
        self.visit(RouteNode(path=TextNode(f"/{entity_name.lower()}s/create"), handler_name=post_task_name, method="POST"))

        # 4. PUT Route Task
        put_task_name = f"__crud_put_{entity_name.lower()}"
        put_body = [
            MapDeclarationNode(name="data")
        ]
        if entity_name in self.entity_registry:
            for field in self.entity_registry[entity_name]:
                fname = field['name']
                if fname in ['created_at', 'updated_at', 'id']: continue
                put_body.append(DeclarationNode(var_type="any", name=f"val_{fname}", value=FormGetNode(key=TextNode(fname), req_name="req")))
                put_body.append(SetInMapNode(key=TextNode(fname), value=VariableNode(f"val_{fname}"), map_name="data"))
        
        put_body.append(DeclarationNode(var_type="any", name="id_val", value=FormGetNode(key=TextNode("id"), req_name="req")))
        put_body.append(UpdateEntityNode(entity_name=entity_name, condition_field="id", condition_value=VariableNode("id_val"), data_map="data"))
        
        put_body.append(MapDeclarationNode(name="context"))
        put_body.append(DeclarationNode(var_type="any", name="records", value=FindEntityNode(entity_name=entity_name)))
        put_body.append(SetInMapNode(key=TextNode(entity_name), value=VariableNode("records"), map_name="context"))
        put_body.append(ReturnNode(value=RenderExpressionNode(template_path=TextNode(page_name + ".html"), context_map_name="context")))
        
        self.visit(TaskNode(name=put_task_name, parameters=["req"], body=put_body))
        self.visit(RouteNode(path=TextNode(f"/{entity_name.lower()}s/update"), handler_name=put_task_name, method="PUT"))

        # 5. DELETE Route Task
        del_task_name = f"__crud_delete_{entity_name.lower()}"
        del_body = []
        del_body.append(DeclarationNode(var_type="any", name="id_val", value=FormGetNode(key=TextNode("id"), req_name="req")))
        del_body.append(DeleteEntityNode(entity_name=entity_name, condition_field="id", condition_value=VariableNode("id_val")))
        
        del_body.append(MapDeclarationNode(name="context"))
        del_body.append(DeclarationNode(var_type="any", name="records", value=FindEntityNode(entity_name=entity_name)))
        del_body.append(SetInMapNode(key=TextNode(entity_name), value=VariableNode("records"), map_name="context"))
        del_body.append(ReturnNode(value=RenderExpressionNode(template_path=TextNode(page_name + ".html"), context_map_name="context")))
        
        self.visit(TaskNode(name=del_task_name, parameters=["req"], body=del_body))
        self.visit(RouteNode(path=TextNode(f"/{entity_name.lower()}s/delete"), handler_name=del_task_name, method="DELETE"))


if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser
    code = '''
    text name is "Ayush".
    show name.
    '''
    lexer = Lexer(code)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    
    compiler = AAYUCompiler()
    bytecode = compiler.compile(ast)
    
    print(bytecode.format())

