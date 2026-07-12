"""
=============================================================================
FILE: lowering.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from compiler.frontend.ast_nodes import *
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

    def visit_RepeatNode(self, node: RepeatNode) -> Node:
        self.counter += 1
        var_name = f"__repeat_{self.counter}"
        
        # let __repeat_X = count
        init = DeclarationNode(var_type="number", name=var_name, value=self.visit(node.count))
        if hasattr(node, 'line'):
            init.line = node.line
        
        # __repeat_X > 0
        cond = BinaryExpressionNode(
            left=VariableNode(name=var_name),
            operator=">",
            right=NumberNode(value=0.0)
        )
        if hasattr(node, 'line'):
            cond.line = node.line
        
        # __repeat_X = __repeat_X - 1
        decrement = AssignmentNode(
            target=VariableNode(name=var_name),
            value=BinaryExpressionNode(
                left=VariableNode(name=var_name),
                operator="-",
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
        
        return BlockNode(statements=[init, while_node])

    def visit_ForRangeNode(self, node: ForRangeNode) -> Node:
        # let i = start
        init = DeclarationNode(var_type="number", name=node.iterator, value=self.visit(node.start))
        if hasattr(node, 'line'):
            init.line = node.line
        
        end_plus_one = BinaryExpressionNode(
            left=self.visit(node.end),
            operator="+",
            right=NumberNode(value=1.0)
        )
        
        cond = BinaryExpressionNode(
            left=VariableNode(name=node.iterator),
            operator="<",
            right=end_plus_one
        )
        if hasattr(node, 'line'):
            cond.line = node.line
            
        # i = i + 1
        increment = AssignmentNode(
            target=VariableNode(name=node.iterator),
            value=BinaryExpressionNode(
                left=VariableNode(name=node.iterator),
                operator="+",
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
            
        return BlockNode(statements=[init, while_node])

    def visit_MethodCallNode(self, node: MethodCallNode) -> Node:
        # Check if this is a module call (e.g. math.add)
        is_module_call = False
        if hasattr(node.object_node, 'symbol'):
            from compiler.frontend.resolver.symbols import ModuleSymbol
            if isinstance(node.object_node.symbol, ModuleSymbol):
                is_module_call = True
                
        if is_module_call:
            # For module calls, we find the exported function symbol inside the module
            mod_sym = node.object_node.symbol
            func_sym = mod_sym.module_table.lookup(node.method_name)
            if not func_sym or not func_sym.is_exported:
                raise Exception(f"Cannot access private or undefined symbol '{node.method_name}' in module '{mod_sym.name}'")
                
            transformed_args = [self.visit(a) for a in node.arguments]
            call_node = BuiltinFunctionNode(name=node.method_name, arguments=transformed_args)
            call_node.symbol = func_sym
            if hasattr(node, 'line'):
                call_node.line = node.line
            return call_node
            
        # Standard object method call
        new_name = f"__method_{node.method_name}"
        # Transform object and arguments
        transformed_obj = self.visit(node.object_node)
        transformed_args = [self.visit(a) for a in node.arguments]
        
        all_args = [transformed_obj] + transformed_args
        
        call_node = BuiltinFunctionNode(name=new_name, arguments=all_args)
        if hasattr(node, 'line'):
            call_node.line = node.line
        return call_node

    def visit_ShowNode(self, node: ShowNode) -> Node:
        # Lower 'show expr.' to 'print(expr)'
        transformed_val = self.visit(node.value)
        call_node = BuiltinFunctionNode(name="print", arguments=[transformed_val])
        if hasattr(node, 'line'):
            call_node.line = node.line
        return call_node
