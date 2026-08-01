from aayu.compiler.semantic.nodes import (
    SemanticProgramNode, SemanticStateDeclNode, SemanticLiteralNode,
    SemanticAssignmentNode, SemanticWidgetNode, SemanticImportNode,
    SemanticActionDeclNode, SemanticActionCallNode, SemanticIdentifierNode,
    SemanticIfNode, SemanticForNode, SemanticBinaryOpNode,
    SemanticModelDeclNode, SemanticRouteNode, SemanticReturnNode, SemanticMethodNode,
    SemanticNode
)
from aayu.compiler.semantic.errors import TypeError

class TypeChecker:
    def __init__(self):
        self.current_function_return = None
        
    def check(self, ast: SemanticProgramNode):
        for stmt in ast.statements:
            self._check_node(stmt)
            
    def _check_node(self, node: SemanticNode):
        if node is None:
            return
            
        if isinstance(node, SemanticStateDeclNode):
            self._check_node(node.value)
            
        elif isinstance(node, SemanticAssignmentNode):
            self._check_node(node.value)
            
            # Simple check for simple variable assignments
            if "." not in node.target:
                sym = node.scope.resolve(node.target)
                if sym:
                    if sym.data_type != "Any" and getattr(node.value, "data_type", "Any") != "Any":
                        if sym.data_type != getattr(node.value, "data_type", "Any"):
                            raise TypeError(
                                expected=sym.data_type,
                                received=getattr(node.value, "data_type", "Any"),
                                line=node.line,
                                column=node.column,
                                hint=f"Cannot assign {getattr(node.value, 'data_type', 'Any')} to {sym.data_type} variable '{node.target}'. Did you mean to cast it?"
                            )
            else:
                # Model dot-access assignment (e.g., user.age = "hello")
                pass
                
        elif isinstance(node, SemanticBinaryOpNode):
            self._check_node(node.left)
            self._check_node(node.right)
            
            lt = getattr(node.left, "data_type", "Any")
            rt = getattr(node.right, "data_type", "Any")
            op = node.op
            
            if lt != "Any" and rt != "Any":
                if op in ["+", "-", "*", "/", "%", ">", "<", ">=", "<="]:
                    if lt not in ["Integer", "Float"] and lt != "String":
                        raise TypeError(expected="Number or String", received=lt, line=node.line, column=node.column)
                    if rt not in ["Integer", "Float"] and rt != "String":
                        raise TypeError(expected="Number or String", received=rt, line=node.line, column=node.column)
                    
                    if (lt == "String" or rt == "String") and op != "+":
                        raise TypeError(expected="Number", received="String", line=node.line, column=node.column, hint="Only + is supported for strings.")
                            
                elif op in ["&&", "||", "!"]:
                    if lt != "Boolean" and op != "!":
                        raise TypeError(expected="Boolean", received=lt, line=node.line, column=node.column)
                    if rt != "Boolean":
                        raise TypeError(expected="Boolean", received=rt, line=node.line, column=node.column)
                        
        elif isinstance(node, SemanticWidgetNode):
            for child in node.children:
                self._check_node(child)
                
            wtype = node.widget_type.lower()
            if wtype == "image":
                if node.children and len(node.children) > 0:
                    child = node.children[0]
                    c_dt = getattr(child, "data_type", "Any")
                    if c_dt != "String" and c_dt != "Any":
                        raise TypeError(expected="String", received=c_dt, line=node.line, column=node.column, hint=f"Image expects String path, got {c_dt}.")
                        
        elif isinstance(node, SemanticActionDeclNode):
            prev_ret = self.current_function_return
            self.current_function_return = "Any" 
            for stmt in node.statements:
                self._check_node(stmt)
            self.current_function_return = prev_ret
            
        elif isinstance(node, SemanticRouteNode):
            for method in node.methods:
                for stmt in method.body:
                    self._check_node(stmt)
                    
        elif isinstance(node, SemanticReturnNode):
            self._check_node(node.value)
            val_dt = getattr(node.value, "data_type", "Any")
            if self.current_function_return and self.current_function_return != "Any":
                if val_dt != "Any" and val_dt != self.current_function_return:
                    raise TypeError(expected=self.current_function_return, received=val_dt, line=node.line, column=node.column)
                    
        elif isinstance(node, SemanticIfNode):
            self._check_node(node.condition)
            c_dt = getattr(node.condition, "data_type", "Any")
            if c_dt != "Any" and c_dt != "Boolean":
                 raise TypeError(expected="Boolean", received=c_dt, line=node.line, column=node.column, hint="If condition must be a Boolean.")
            for stmt in node.then_branch:
                self._check_node(stmt)
            if node.else_branch:
                for stmt in node.else_branch:
                    self._check_node(stmt)
                    
        elif isinstance(node, SemanticForNode):
            self._check_node(node.iterable)
            i_dt = getattr(node.iterable, "data_type", "Any")
            if i_dt != "Any" and not i_dt.startswith("List"):
                 raise TypeError(expected="List", received=i_dt, line=node.line, column=node.column, hint="For loop iterable must be a List.")
            for stmt in node.body:
                self._check_node(stmt)
                
        elif hasattr(node, "statements"):
            for stmt in getattr(node, "statements"):
                self._check_node(stmt)
