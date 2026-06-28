from ast_nodes import *
from typing import List, Union

class LoweringPass:
    def __init__(self):
        self.counter = 0

    def lower(self, program: ProgramNode) -> ProgramNode:
        program.statements = self._lower_list(program.statements)
        return program

    def _lower_list(self, nodes: List[Node]) -> List[Node]:
        result = []
        for node in nodes:
            lowered = self.visit(node)
            if isinstance(lowered, list):
                result.extend(lowered)
            elif lowered is not None:
                result.append(lowered)
        return result

    def visit(self, node: Node) -> Union[Node, List[Node]]:
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: Node) -> Node:
        # Recursively visit children
        for field_name, value in node.__dict__.items():
            if isinstance(value, list) and all(isinstance(v, Node) for v in value):
                setattr(node, field_name, self._lower_list(value))
            elif isinstance(value, Node):
                setattr(node, field_name, self.visit(value))
        return node

    def visit_RepeatNode(self, node: RepeatNode) -> List[Node]:
        self.counter += 1
        var_name = f"__repeat_{self.counter}"
        
        # let __repeat_X = count
        init = DeclarationNode(var_type="number", name=var_name, value=self.visit(node.count))
        if hasattr(node, 'line'):
            init.line = node.line
        
        # __repeat_X > 0
        cond = BinaryExpressionNode(
            left=VariableNode(name=var_name),
            operator="GREATER",
            right=NumberNode(value=0.0)
        )
        if hasattr(node, 'line'):
            cond.line = node.line
        
        # __repeat_X = __repeat_X - 1
        decrement = AssignmentNode(
            target=VariableNode(name=var_name),
            value=BinaryExpressionNode(
                left=VariableNode(name=var_name),
                operator="MINUS",
                right=NumberNode(value=1.0)
            )
        )
        if hasattr(node, 'line'):
            decrement.line = node.line
        
        body = self._lower_list(node.body)
        body.append(decrement)
        
        while_node = WhileNode(condition=cond, body=body)
        if hasattr(node, 'line'):
            while_node.line = node.line
        
        return [init, while_node]

    def visit_ForRangeNode(self, node: ForRangeNode) -> List[Node]:
        # let i = start
        init = DeclarationNode(var_type="number", name=node.iterator, value=self.visit(node.start))
        if hasattr(node, 'line'):
            init.line = node.line
        
        end_plus_one = BinaryExpressionNode(
            left=self.visit(node.end),
            operator="PLUS",
            right=NumberNode(value=1.0)
        )
        
        cond = BinaryExpressionNode(
            left=VariableNode(name=node.iterator),
            operator="LESS",
            right=end_plus_one
        )
        if hasattr(node, 'line'):
            cond.line = node.line
            
        # i = i + 1
        increment = AssignmentNode(
            target=VariableNode(name=node.iterator),
            value=BinaryExpressionNode(
                left=VariableNode(name=node.iterator),
                operator="PLUS",
                right=NumberNode(value=1.0)
            )
        )
        if hasattr(node, 'line'):
            increment.line = node.line
            
        body = self._lower_list(node.body)
        body.append(increment)
        
        while_node = WhileNode(condition=cond, body=body)
        if hasattr(node, 'line'):
            while_node.line = node.line
            
        return [init, while_node]
