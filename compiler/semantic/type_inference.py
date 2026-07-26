
from compiler.semantic.nodes import (
    SemanticProgramNode, SemanticStateDeclNode, SemanticLiteralNode,
    SemanticAssignmentNode, SemanticWidgetNode, SemanticImportNode,
    SemanticActionDeclNode, SemanticActionCallNode, SemanticIdentifierNode,
    SemanticIfNode, SemanticForNode, SemanticBinaryOpNode,
    SemanticModelNode, SemanticRouteNode, SemanticReturnNode, SemanticMethodNode,
    SemanticNode
)

class TypeInference:
    def __init__(self):
        pass
        
    def infer(self, ast: SemanticProgramNode) -> SemanticProgramNode:
        for stmt in ast.statements:
            self._infer_node(stmt)
        ast.data_type = "Void"
        return ast
        
    def _infer_node(self, node: SemanticNode) -> str:
        if node is None:
            return "Void"
            
        data_type = "Any"
        
        if isinstance(node, SemanticLiteralNode):
            if node.type_name == "number":
                # Very simple integer/float distinction
                if "." in str(node.value):
                    data_type = "Float"
                else:
                    data_type = "Integer"
            elif node.type_name == "string":
                data_type = "String"
            elif node.type_name == "boolean":
                data_type = "Boolean"
            elif node.type_name == "list":
                # Infer list type based on first element
                if isinstance(node.value, list) and len(node.value) > 0:
                    first_val = node.value[0]
                    # We might need to map raw values back to types, but literal arrays store raw vals
                    if isinstance(first_val, int): data_type = "List<Integer>"
                    elif isinstance(first_val, str): data_type = "List<String>"
                    elif isinstance(first_val, float): data_type = "List<Float>"
                    else: data_type = "List<Any>"
                else:
                    data_type = "List<Any>"
                    
        elif isinstance(node, SemanticIdentifierNode):
            sym = node.scope.resolve(node.name)
            if sym:
                data_type = sym.data_type
            else:
                data_type = "Any"
                
        elif isinstance(node, SemanticStateDeclNode):
            val_type = self._infer_node(node.value)
            sym = node.scope.resolve(node.name)
            if sym:
                sym.data_type = val_type
            data_type = "Void"
            
        elif isinstance(node, SemanticAssignmentNode):
            self._infer_node(node.value)
            data_type = "Void"
            
        elif isinstance(node, SemanticBinaryOpNode):
            left_type = self._infer_node(node.left)
            right_type = self._infer_node(node.right)
            
            if node.op in ["==", "!=", ">", "<", ">=", "<="]:
                data_type = "Boolean"
            elif left_type == right_type:
                data_type = left_type
            elif "Float" in [left_type, right_type]:
                data_type = "Float"
            else:
                data_type = "Any"
                
        elif isinstance(node, SemanticActionDeclNode):
            for stmt in node.statements:
                self._infer_node(stmt)
            sym = node.scope.parent.resolve(node.name) if node.scope.parent else None
            if sym:
                sym.data_type = "Function"
                sym.is_function = True
            data_type = "Void"
            
        elif isinstance(node, SemanticActionCallNode):
            for arg in node.args:
                self._infer_node(arg)
            data_type = "Any" # Function return types not fully implemented yet
            
        elif isinstance(node, SemanticWidgetNode):
            for child in node.children:
                self._infer_node(child)
            data_type = "Widget"
            
        elif isinstance(node, SemanticIfNode):
            self._infer_node(node.condition)
            for stmt in node.then_branch:
                self._infer_node(stmt)
            if node.else_branch:
                for stmt in node.else_branch:
                    self._infer_node(stmt)
            data_type = "Void"
            
        elif isinstance(node, SemanticForNode):
            self._infer_node(node.iterable)
            for stmt in node.body:
                self._infer_node(stmt)
            data_type = "Void"
            
        elif isinstance(node, SemanticModelNode):
            sym = node.scope.parent.resolve(node.name) if node.scope.parent else None
            if sym:
                sym.data_type = "Model"
            data_type = "Void"
            
        elif isinstance(node, SemanticRouteNode):
            for method in node.methods:
                for stmt in method.body:
                    self._infer_node(stmt)
            data_type = "Void"
            
        elif isinstance(node, SemanticReturnNode):
            self._infer_node(node.value)
            data_type = "Void"
            
        node.data_type = data_type
        return data_type
