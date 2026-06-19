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
        elif node.operator == 'is' or node.operator == 'equals' or node.operator == 'equal to':
            self._emit(Opcode.EQUAL)
            
    def visit_IfNode(self, node: IfNode):
        self.visit(node.condition)
        
        # Emit JUMP_IF_FALSE with placeholder
        jump_if_false_idx = len(self.bytecode.instructions)
        self._emit(Opcode.JUMP_IF_FALSE, 0)
        
        for stmt in node.then_branch:
            self.visit(stmt)
            
        if node.else_branch:
            jump_forward_idx = len(self.bytecode.instructions)
            self._emit(Opcode.JUMP_FORWARD, 0)
            
            # Patch JUMP_IF_FALSE to jump here
            self.bytecode.instructions[jump_if_false_idx].operand = len(self.bytecode.instructions) - jump_if_false_idx - 1
            
            for stmt in node.else_branch:
                self.visit(stmt)
                
            # Patch JUMP_FORWARD to jump here
            self.bytecode.instructions[jump_forward_idx].operand = len(self.bytecode.instructions) - jump_forward_idx - 1
        else:
            # Patch JUMP_IF_FALSE to jump here
            self.bytecode.instructions[jump_if_false_idx].operand = len(self.bytecode.instructions) - jump_if_false_idx - 1

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
        self.bytecode.instructions[jump_if_false_idx].operand = len(self.bytecode.instructions) - jump_if_false_idx - 1
        
    def visit_TaskNode(self, node: TaskNode):
        # In a real compiler, we would probably compile tasks into separate bytecode objects
        # or store the jump location. For V1, we'll keep it simple: we skip compiling tasks inline
        # unless they are explicitly called, or we compile them but jump over them.
        
        jump_over_idx = len(self.bytecode.instructions)
        self._emit(Opcode.JUMP_FORWARD, 0)
        
        # Remember where this task starts
        # For a full implementation, we'd store this in a task table
        task_start_idx = len(self.bytecode.instructions)
        
        for stmt in node.body:
            self.visit(stmt)
            
        self._emit(Opcode.RETURN)
        
        # Patch JUMP_FORWARD
        self.bytecode.instructions[jump_over_idx].operand = len(self.bytecode.instructions) - jump_over_idx - 1

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
