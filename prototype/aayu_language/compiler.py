from ast_nodes import *
from ir import Opcode, Instruction, Bytecode

class AAYUCompiler:
    def __init__(self):
        self.bytecode = Bytecode()
        
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
        self.bytecode.instructions.append(Instruction(opcode, operand))
        
    def compile(self, node: Node) -> Bytecode:
        self.visit(node)
        return self.bytecode
        
    def visit(self, node: Node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
        
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
        task_compiler = AAYUCompiler()
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
