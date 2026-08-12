from aayu.compiler.semantic.nodes import (
    SemanticProgramNode, SemanticStateDeclNode, SemanticLiteralNode,
    SemanticAssignmentNode, SemanticWidgetNode, SemanticImportNode,
    SemanticActionDeclNode, SemanticActionCallNode, SemanticIdentifierNode,
    SemanticIfNode, SemanticForNode, SemanticBinaryOpNode,
    SemanticModelDeclNode, SemanticRouteNode, SemanticReturnNode, SemanticMethodNode,
    SemanticNode
)
from aayu.compiler.semantic.errors import TypeError
from aayu.compiler.semantic.types import (
    Type, PrimitiveType, UnionType, OptionalType,
    T_INT, T_FLOAT, T_STRING, T_BOOL, T_ANY
)

class TypeChecker:
    def __init__(self):
        self.current_function_return = None
        
    def check(self, ast: SemanticProgramNode):
        for stmt in ast.statements:
            self._check_node(stmt)
            
    def _get_type(self, node) -> Type:
        # Assuming node.data_type is already populated with Type objects by type_pass
        if hasattr(node, "data_type") and isinstance(node.data_type, Type):
            return node.data_type
        return T_ANY
            
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
                    sym_type = sym.data_type if isinstance(sym.data_type, Type) else T_ANY
                    val_type = self._get_type(node.value)
                    
                    if sym_type != T_ANY and val_type != T_ANY:
                        if not val_type.is_assignable_to(sym_type):
                            raise TypeError(
                                expected=str(sym_type),
                                received=str(val_type),
                                line=node.line,
                                column=node.column,
                                hint=f"Cannot assign {val_type} to {sym_type} variable '{node.target}'. Did you mean to cast it?"
                            )
            else:
                # Model dot-access assignment
                pass
                
        elif isinstance(node, SemanticBinaryOpNode):
            self._check_node(node.left)
            self._check_node(node.right)
            
            lt = self._get_type(node.left)
            rt = self._get_type(node.right)
            op = node.op
            
            if lt != T_ANY and rt != T_ANY:
                if op in ["+", "-", "*", "/", "%", ">", "<", ">=", "<="]:
                    num_str_union = UnionType(T_INT, T_FLOAT, T_STRING)
                    if not lt.is_assignable_to(num_str_union):
                        raise TypeError(expected="Number or String", received=str(lt), line=node.line, column=node.column)
                    if not rt.is_assignable_to(num_str_union):
                        raise TypeError(expected="Number or String", received=str(rt), line=node.line, column=node.column)
                    
                    if (lt.is_assignable_to(T_STRING) or rt.is_assignable_to(T_STRING)) and op != "+":
                        raise TypeError(expected="Number", received="String", line=node.line, column=node.column, hint="Only + is supported for strings.")
                            
                elif op in ["&&", "||", "!"]:
                    if not lt.is_assignable_to(T_BOOL) and op != "!":
                        raise TypeError(expected="Bool", received=str(lt), line=node.line, column=node.column)
                    if not rt.is_assignable_to(T_BOOL) and op != "!":
                        raise TypeError(expected="Bool", received=str(rt), line=node.line, column=node.column)
                        
        elif isinstance(node, SemanticWidgetNode):
            for child in node.children:
                self._check_node(child)
                
            wtype = node.widget_type.lower()
            if wtype == "image":
                if node.children and len(node.children) > 0:
                    child = node.children[0]
                    c_dt = self._get_type(child)
                    if not c_dt.is_assignable_to(T_STRING) and c_dt != T_ANY:
                        raise TypeError(expected="String", received=str(c_dt), line=node.line, column=node.column, hint=f"Image expects String path, got {c_dt}.")
                        
        elif isinstance(node, SemanticActionDeclNode):
            prev_ret = self.current_function_return
            self.current_function_return = T_ANY 
            for stmt in node.statements:
                self._check_node(stmt)
            self.current_function_return = prev_ret
            
        elif isinstance(node, SemanticRouteNode):
            for method in node.methods:
                for stmt in method.body:
                    self._check_node(stmt)
                    
        elif isinstance(node, SemanticReturnNode):
            self._check_node(node.value)
            val_dt = self._get_type(node.value)
            if self.current_function_return and self.current_function_return != T_ANY:
                if val_dt != T_ANY and not val_dt.is_assignable_to(self.current_function_return):
                    raise TypeError(expected=str(self.current_function_return), received=str(val_dt), line=node.line, column=node.column)
                    
        elif isinstance(node, SemanticIfNode):
            self._check_node(node.condition)
            c_dt = self._get_type(node.condition)
            if c_dt != T_ANY and not c_dt.is_assignable_to(T_BOOL):
                 raise TypeError(expected="Bool", received=str(c_dt), line=node.line, column=node.column, hint="If condition must be a Boolean.")
            for stmt in node.then_branch:
                self._check_node(stmt)
            if node.else_branch:
                for stmt in node.else_branch:
                    self._check_node(stmt)
                    
        elif isinstance(node, SemanticForNode):
            self._check_node(node.iterable)
            # Future: Update this when List/Array types are implemented
            for stmt in node.body:
                self._check_node(stmt)
                
        elif hasattr(node, "statements"):
            for stmt in getattr(node, "statements"):
                self._check_node(stmt)
