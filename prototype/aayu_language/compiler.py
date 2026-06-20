from ast_nodes import *
from ir import Opcode, Instruction, Bytecode

class AAYUCompiler:
    def __init__(self, filename: str = ""):
        self.bytecode = Bytecode()
        self.loop_counter = 0
        self.filename = filename
        self.current_line = None
        
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
            Instruction(opcode, operand, line=self.current_line, file=self.filename)
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
        
    def generic_visit(self, node: Node):
        raise NotImplementedError(f"No visit_{type(node).__name__} method defined in compiler")
        
    def visit_ProgramNode(self, node: ProgramNode):
        for stmt in node.statements:
            self.visit(stmt)
            
    def visit_NumberNode(self, node: NumberNode):
        idx = self._add_constant(node.value)
        self._emit(Opcode.LOAD_CONST, idx)
        
    def visit_TextNode(self, node: TextNode):
        idx = self._add_constant(node.value)
        self._emit(Opcode.LOAD_CONST, idx)
        
    def visit_VariableNode(self, node: VariableNode):
        idx = self._add_name(node.name)
        self._emit(Opcode.LOAD_NAME, idx)
        
    def visit_DeclarationNode(self, node: DeclarationNode):
        self.visit(node.value)
        idx = self._add_name(node.name)
        self._emit(Opcode.STORE_NAME, idx)
        
    def visit_ShowNode(self, node: ShowNode):
        self.visit(node.expression)
        self._emit(Opcode.PRINT)
        
    def visit_BinaryExpressionNode(self, node: BinaryExpressionNode):
        self.visit(node.left)
        self.visit(node.right)
        
        if node.operator == '+':
            self._emit(Opcode.ADD)
        elif node.operator == '-':
            self._emit(Opcode.SUB)
        elif node.operator == '*':
            self._emit(Opcode.MUL)
        elif node.operator == '/':
            self._emit(Opcode.DIV)
        elif node.operator in ('is', 'equals', 'equal to', '=='):
            self._emit(Opcode.EQUAL)
        elif node.operator == '>':
            self._emit(Opcode.GREATER)
        elif node.operator == '<':
            self._emit(Opcode.LESS)
            
    def visit_IfNode(self, node: IfNode):
        self.visit(node.condition)
        
        # Emit JUMP_IF_FALSE with placeholder
        jump_if_false_idx = len(self.bytecode.instructions)
        self._emit(Opcode.JUMP_IF_FALSE, 0)
        
        for stmt in node.body:
            self.visit(stmt)
            
        if node.else_body:
            jump_forward_idx = len(self.bytecode.instructions)
            self._emit(Opcode.JUMP_FORWARD, 0)
            
            # Patch JUMP_IF_FALSE to jump here
            self.bytecode.instructions[jump_if_false_idx].operand = len(self.bytecode.instructions) - jump_if_false_idx
            
            for stmt in node.else_body:
                self.visit(stmt)
                
            # Patch JUMP_FORWARD to jump here
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
        offset = len(self.bytecode.instructions) - start_idx
        self._emit(Opcode.JUMP_BACKWARD, offset)
        
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
        self._emit(Opcode.STORE_NAME, name_idx)
        
    def visit_RunNode(self, node: RunNode):
        # Push arguments to stack
        for arg in node.arguments:
            self.visit(arg)
            
        # Load the task object
        name_idx = self._add_name(node.name)
        self._emit(Opcode.LOAD_NAME, name_idx)
        
        # Call task with number of arguments as operand
        self._emit(Opcode.CALL_TASK, len(node.arguments))

    def visit_AssignmentNode(self, node: AssignmentNode):
        if isinstance(node.target, VariableNode):
            self.visit(node.value)
            idx = self._add_name(node.target.name)
            self._emit(Opcode.STORE_NAME, idx)
        else:
            raise NotImplementedError("Only variable assignment is supported in the VM compiler.")

    def visit_ReturnNode(self, node: ReturnNode):
        if node.value:
            self.visit(node.value)
        else:
            self._emit(Opcode.LOAD_CONST, self._add_constant(None))
        self._emit(Opcode.RETURN)

    def visit_ListDeclarationNode(self, node: ListDeclarationNode):
        self._emit(Opcode.BUILD_LIST, 0)
        idx = self._add_name(node.name)
        self._emit(Opcode.STORE_NAME, idx)

    def visit_ListInitializationNode(self, node: ListInitializationNode):
        self.visit(node.value)
        idx = self._add_name(node.name)
        self._emit(Opcode.STORE_NAME, idx)

    def visit_AddToListNode(self, node: AddToListNode):
        self.visit(node.item)
        idx = self._add_name(node.list_name)
        self._emit(Opcode.LOAD_NAME, idx)
        self._emit(Opcode.ADD_TO_LIST)
        self._emit(Opcode.POP)

    def visit_MapDeclarationNode(self, node: MapDeclarationNode):
        self._emit(Opcode.BUILD_MAP, 0)
        idx = self._add_name(node.name)
        self._emit(Opcode.STORE_NAME, idx)

    def visit_SetInMapNode(self, node: SetInMapNode):
        self.visit(node.value)
        self.visit(node.key)
        idx = self._add_name(node.map_name)
        self._emit(Opcode.LOAD_NAME, idx)
        self._emit(Opcode.MAP_SET)

    def visit_GetFromMapNode(self, node: GetFromMapNode):
        self.visit(node.key)
        idx = self._add_name(node.map_name)
        self._emit(Opcode.LOAD_NAME, idx)
        self._emit(Opcode.GET_ITEM)

    def visit_EntityDeclarationNode(self, node: EntityDeclarationNode):
        name_idx = self._add_constant(node.name)
        self._emit(Opcode.LOAD_CONST, name_idx)

        fields_idx = self._add_constant(node.fields)
        self._emit(Opcode.LOAD_CONST, fields_idx)
        
        fn_idx = self._add_name("db_register_entity")
        self._emit(Opcode.LOAD_NAME, fn_idx)
        
        self._emit(Opcode.CALL_TASK, 2)
        self._emit(Opcode.POP)

    def visit_CreateEntityNode(self, node: CreateEntityNode):
        name_idx = self._add_constant(node.entity_name)
        self._emit(Opcode.LOAD_CONST, name_idx)
        
        map_idx = self._add_name(node.data_map)
        self._emit(Opcode.LOAD_NAME, map_idx)
        
        fn_idx = self._add_name("db_create")
        self._emit(Opcode.LOAD_NAME, fn_idx)
        
        self._emit(Opcode.CALL_TASK, 2)
        self._emit(Opcode.POP)

    def visit_FindEntityNode(self, node: FindEntityNode):
        name_idx = self._add_constant(node.entity_name)
        self._emit(Opcode.LOAD_CONST, name_idx)
        
        field_idx = self._add_constant(node.condition_field)
        self._emit(Opcode.LOAD_CONST, field_idx)
        
        if node.condition_value:
            self.visit(node.condition_value)
        else:
            self._emit(Opcode.LOAD_CONST, self._add_constant(None))
            
        fn_idx = self._add_name("db_find")
        self._emit(Opcode.LOAD_NAME, fn_idx)
        
        self._emit(Opcode.CALL_TASK, 3)

    def visit_UpdateEntityNode(self, node: UpdateEntityNode):
        name_idx = self._add_constant(node.entity_name)
        self._emit(Opcode.LOAD_CONST, name_idx)
        
        field_idx = self._add_constant(node.condition_field)
        self._emit(Opcode.LOAD_CONST, field_idx)
        
        self.visit(node.condition_value)
        
        map_idx = self._add_name(node.data_map)
        self._emit(Opcode.LOAD_NAME, map_idx)
        
        fn_idx = self._add_name("db_update")
        self._emit(Opcode.LOAD_NAME, fn_idx)
        
        self._emit(Opcode.CALL_TASK, 4)
        self._emit(Opcode.POP)

    def visit_DeleteEntityNode(self, node: DeleteEntityNode):
        name_idx = self._add_constant(node.entity_name)
        self._emit(Opcode.LOAD_CONST, name_idx)
        
        field_idx = self._add_constant(node.condition_field)
        self._emit(Opcode.LOAD_CONST, field_idx)
        
        self.visit(node.condition_value)
        
        fn_idx = self._add_name("db_delete")
        self._emit(Opcode.LOAD_NAME, fn_idx)
        
        self._emit(Opcode.CALL_TASK, 3)
        self._emit(Opcode.POP)

    def visit_JsonSerializeNode(self, node: JsonSerializeNode):
        self.visit(node.data)
        
        fn_idx = self._add_name("json_serialize")
        self._emit(Opcode.LOAD_NAME, fn_idx)
        
        self._emit(Opcode.CALL_TASK, 1)

    def visit_RenderExpressionNode(self, node: RenderExpressionNode):
        self.visit(node.template_path)
        
        if node.context_map_name:
            map_idx = self._add_name(node.context_map_name)
            self._emit(Opcode.LOAD_NAME, map_idx)
        else:
            self._emit(Opcode.LOAD_CONST, self._add_constant(None))
            
        fn_idx = self._add_name("render_template")
        self._emit(Opcode.LOAD_NAME, fn_idx)
        
        self._emit(Opcode.CALL_TASK, 2)

    def visit_RouteNode(self, node: RouteNode):
        self.visit(node.path)
        method_idx = self._add_constant(node.method)
        self._emit(Opcode.LOAD_CONST, method_idx)
        handler_idx = self._add_constant(node.handler_name)
        self._emit(Opcode.LOAD_CONST, handler_idx)
        fn_idx = self._add_name("http_route")
        self._emit(Opcode.LOAD_NAME, fn_idx)
        self._emit(Opcode.CALL_TASK, 3)
        self._emit(Opcode.POP)

    def visit_FormGetNode(self, node: FormGetNode):
        self.visit(node.key)
        idx = self._add_name(node.req_name)
        self._emit(Opcode.LOAD_NAME, idx)
        fn_idx = self._add_name("http_form_get")
        self._emit(Opcode.LOAD_NAME, fn_idx)
        self._emit(Opcode.CALL_TASK, 2)

    def visit_ServeNode(self, node: ServeNode):
        self.visit(node.port)
        if node.handler_name:
            idx = self._add_constant(node.handler_name)
            self._emit(Opcode.LOAD_CONST, idx)
        else:
            self._emit(Opcode.LOAD_CONST, self._add_constant(None))
            
        fn_idx = self._add_name("http_serve")
        self._emit(Opcode.LOAD_NAME, fn_idx)
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
        self._emit(Opcode.STORE_NAME, coll_idx)
        
        # 2. Store 0.0 in _idx_{id}
        self._emit(Opcode.LOAD_CONST, self._add_constant(0.0))
        idx_idx = self._add_name(idx_name)
        self._emit(Opcode.STORE_NAME, idx_idx)
        
        # 3. Mark condition check index
        cond_ip = len(self.bytecode.instructions)
        
        # 4. Check index < len(collection)
        self._emit(Opcode.LOAD_NAME, idx_idx)
        self._emit(Opcode.LOAD_NAME, coll_idx)
        len_fn_idx = self._add_name("collection_len")
        self._emit(Opcode.LOAD_NAME, len_fn_idx)
        self._emit(Opcode.CALL_TASK, 1)
        self._emit(Opcode.LESS)
        
        # 5. Jump if false placeholder
        jump_if_false_idx = len(self.bytecode.instructions)
        self._emit(Opcode.JUMP_IF_FALSE, 0)
        
        # 6. Fetch b = collection[index] and store in node.iterator
        self._emit(Opcode.LOAD_NAME, idx_idx)
        self._emit(Opcode.LOAD_NAME, coll_idx)
        self._emit(Opcode.GET_ITEM)
        iterator_idx = self._add_name(node.iterator)
        self._emit(Opcode.STORE_NAME, iterator_idx)
        
        # 7. Compile loop body
        for stmt in node.body:
            self.visit(stmt)
            
        # 8. Increment index: index = index + 1
        self._emit(Opcode.LOAD_NAME, idx_idx)
        self._emit(Opcode.LOAD_CONST, self._add_constant(1.0))
        self._emit(Opcode.ADD)
        self._emit(Opcode.STORE_NAME, idx_idx)
        
        # 9. Jump backward to cond_ip
        offset = len(self.bytecode.instructions) - cond_ip
        self._emit(Opcode.JUMP_BACKWARD, offset)
        
        # 10. Patch condition check jump
        self.bytecode.instructions[jump_if_false_idx].operand = len(self.bytecode.instructions) - jump_if_false_idx

    def visit_CreateAccountNode(self, node: CreateAccountNode):
        map_idx = self._add_name(node.data_map_name)
        self._emit(Opcode.LOAD_NAME, map_idx)
        fn_idx = self._add_name("auth_create_account")
        self._emit(Opcode.LOAD_NAME, fn_idx)
        self._emit(Opcode.CALL_TASK, 1)
        self._emit(Opcode.POP)

    def visit_LoginNode(self, node: LoginNode):
        map_idx = self._add_name(node.user_map_name)
        self._emit(Opcode.LOAD_NAME, map_idx)
        fn_idx = self._add_name("auth_login")
        self._emit(Opcode.LOAD_NAME, fn_idx)
        self._emit(Opcode.CALL_TASK, 1)
        self._emit(Opcode.POP)

    def visit_LogoutNode(self, node: LogoutNode):
        req_idx = self._add_name(node.req_name)
        self._emit(Opcode.LOAD_NAME, req_idx)
        fn_idx = self._add_name("auth_logout")
        self._emit(Opcode.LOAD_NAME, fn_idx)
        self._emit(Opcode.CALL_TASK, 1)
        self._emit(Opcode.POP)

    def visit_GuardSessionNode(self, node: GuardSessionNode):
        fn_idx = self._add_name("auth_guard_session")
        self._emit(Opcode.LOAD_NAME, fn_idx)
        self._emit(Opcode.CALL_TASK, 0)
        self._emit(Opcode.POP)




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
