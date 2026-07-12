"""
=============================================================================
FILE: formatter.py
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
from compiler.frontend.passes.base import BasePass
from compiler.frontend.compiler_context import CompilerContext

class AAYUFormatter(BasePass):
    def __init__(self, indent_size=4):
        super().__init__("AAYU Formatter")
        self.indent_size = indent_size
        self.indent_level = 0
        
    def _indent(self) -> str:
        return " " * (self.indent_size * self.indent_level)
        
    def format(self, node: Node) -> str:
        if not node:
            return ""
        return self.visit(node)
        
    def visit(self, node: Node) -> str:
        if node is None:
            return ""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: Node) -> str:
        return f"/* UNFORMATTED NODE: {type(node).__name__} */"

    def visit_ProgramNode(self, node: ProgramNode) -> str:
        return "\n".join(self.visit(stmt) for stmt in node.statements).strip() + "\n"
        
    def visit_BlockNode(self, node: BlockNode) -> str:
        lines = []
        for stmt in node.statements:
            formatted = self.visit(stmt)
            if formatted:
                lines.append(f"{self._indent()}{formatted}")
        return "\n".join(lines)
        
    def visit_DeclarationNode(self, node: DeclarationNode) -> str:
        # let x is 5. or let x: Number is 5.
        base = f"{node.var_type} {node.name}"
        if getattr(node, 'type_annotation', None):
            base += f": {self.visit(node.type_annotation)}"
        val = self.visit(node.value)
        return f"{base} is {val}."
        
    def visit_AssignmentNode(self, node: AssignmentNode) -> str:
        target = self.visit(node.target)
        val = self.visit(node.value)
        return f"{target} is {val}."

    def visit_VariableNode(self, node: VariableNode) -> str:
        return node.name

    def visit_NumberNode(self, node: NumberNode) -> str:
        # Formatting floats without trailing .0 if integer
        if node.value == int(node.value):
            return str(int(node.value))
        return str(node.value)

    def visit_TextNode(self, node: TextNode) -> str:
        return f'"{node.value}"'

    def visit_LogicalExpressionNode(self, node: LogicalExpressionNode) -> str:
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"{left} {node.operator} {right}"

    def visit_BinaryExpressionNode(self, node: BinaryExpressionNode) -> str:
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"{left} {node.operator} {right}"

    def visit_UnaryExpressionNode(self, node: UnaryExpressionNode) -> str:
        right = self.visit(node.right)
        if node.operator.isalpha():
            return f"{node.operator} {right}"
        return f"{node.operator}{right}"

    def visit_ShowNode(self, node: ShowNode) -> str:
        return f"show {self.visit(node.expression)}."

    def visit_FunctionDeclNode(self, node: FunctionDeclNode) -> str:
        params = []
        for p in node.parameters:
            if isinstance(p, tuple) and len(p) == 2:
                params.append(f"{p[0]}: {self.visit(p[1])}")
            else:
                params.append(str(p))
        param_str = ", ".join(params)
        
        type_params = ""
        if getattr(node, 'type_parameters', []):
            type_params = f"<{', '.join(node.type_parameters)}>"
            
        ret_type = ""
        if getattr(node, 'return_type', None):
            ret_type = f": {self.visit(node.return_type)}"
            
        vis = "export " if node.is_exported else ""
        header = f"{vis}function {node.name}{type_params}({param_str}){ret_type}"
        
        self.indent_level += 1
        body_str = ""
        for stmt in node.body:
            body_str += f"\n{self._indent()}{self.visit(stmt)}"
        self.indent_level -= 1
        
        return f"{header}{body_str}\n{self._indent()}end."

    def visit_ReturnNode(self, node: ReturnNode) -> str:
        return f"return {self.visit(node.value)}."
        
    def visit_IfNode(self, node: IfNode) -> str:
        cond = self.visit(node.condition)
        out = f"if {cond}."
        
        self.indent_level += 1
        for stmt in node.body:
            out += f"\n{self._indent()}{self.visit(stmt)}"
        self.indent_level -= 1
        
        if node.else_body:
            out += f"\n{self._indent()}else."
            self.indent_level += 1
            for stmt in node.else_body:
                out += f"\n{self._indent()}{self.visit(stmt)}"
            self.indent_level -= 1
            
        out += f"\n{self._indent()}end."
        return out
        
    def visit_WhileNode(self, node: WhileNode) -> str:
        cond = self.visit(node.condition)
        out = f"while {cond}."
        
        self.indent_level += 1
        for stmt in node.body:
            out += f"\n{self._indent()}{self.visit(stmt)}"
        self.indent_level -= 1
        
        out += f"\n{self._indent()}end."
        return out
        
    def visit_TaskNode(self, node: TaskNode) -> str:
        param_str = ", ".join(node.parameters)
        out = f"task {node.name}({param_str})"
        self.indent_level += 1
        for stmt in node.body:
            out += f"\n{self._indent()}{self.visit(stmt)}"
        self.indent_level -= 1
        out += f"\n{self._indent()}end."
        return out

    def visit_RunNode(self, node: RunNode) -> str:
        args = ", ".join(self.visit(a) for a in node.arguments)
        target = f"{node.module_name}.{node.name}" if node.module_name else node.name
        return f"run {target}({args})."

    # Type Nodes support
    def visit_NamedTypeNode(self, node) -> str:
        return node.name

    def visit_PrimitiveTypeNode(self, node) -> str:
        return node.name

    def visit_GenericTypeNode(self, node) -> str:
        params = ", ".join(self.visit(p) for p in node.type_args)
        return f"{self.visit(node.base_type)}<{params}>"

    def visit_RepeatNode(self, node: RepeatNode) -> str:
        count = self.visit(node.count)
        out = f"repeat {count} times."
        self.indent_level += 1
        for stmt in node.body:
            out += f"\n{self._indent()}{self.visit(stmt)}"
        self.indent_level -= 1
        out += f"\n{self._indent()}end."
        return out

    def visit_ForRangeNode(self, node: ForRangeNode) -> str:
        start = self.visit(node.start)
        end = self.visit(node.end)
        out = f"for {node.iterator} in {start}..{end}."
        self.indent_level += 1
        for stmt in node.body:
            out += f"\n{self._indent()}{self.visit(stmt)}"
        self.indent_level -= 1
        out += f"\n{self._indent()}end."
        return out

    def visit_ForEachNode(self, node: ForEachNode) -> str:
        coll = self.visit(node.collection)
        out = f"for {node.iterator} in {coll}."
        self.indent_level += 1
        for stmt in node.body:
            out += f"\n{self._indent()}{self.visit(stmt)}"
        self.indent_level -= 1
        out += f"\n{self._indent()}end."
        return out

    def visit_BuiltinFunctionNode(self, node: BuiltinFunctionNode) -> str:
        args = ", ".join(self.visit(a) for a in node.arguments)
        return f"{node.name}({args})."

    def visit_ListDeclarationNode(self, node: ListDeclarationNode) -> str:
        elements = ", ".join(self.visit(e) for e in node.elements)
        return f"list {node.name} is [{elements}]."

    def visit_MapDeclarationNode(self, node: MapDeclarationNode) -> str:
        return f"map {node.name}."

    def visit_AddToListNode(self, node: AddToListNode) -> str:
        item = self.visit(node.item)
        return f"add {item} to {node.list_name}."

    def visit_SetInMapNode(self, node: SetInMapNode) -> str:
        key = self.visit(node.key)
        val = self.visit(node.value)
        return f"set {key} to {val} in {node.map_name}."

    def visit_GetFromMapNode(self, node: GetFromMapNode) -> str:
        key = self.visit(node.key)
        return f"{node.map_name}[{key}]"

    def visit_UseNode(self, node: UseNode) -> str:
        return f"use {node.module}."

    def visit_ExportNode(self, node: ExportNode) -> str:
        # If the inner declaration is already handled with 'export' prefix, we just return it.
        # Otherwise, prefix it.
        inner = self.visit(node.declaration)
        if not inner.startswith("export "):
            return f"export {inner}"
        return inner

    def visit_RecordDeclarationNode(self, node: RecordDeclarationNode) -> str:
        type_params = ""
        if node.type_parameters:
            type_params = f"<{', '.join(node.type_parameters)}>"
        fields = " and ".join(node.fields)
        return f"record {node.name}{type_params} has {fields}."

    def visit_InstanceDeclarationNode(self, node: InstanceDeclarationNode) -> str:
        props = []
        for k, v in node.properties.items():
            props.append(f"{k}: {self.visit(v)}")
        prop_str = ", ".join(props)
        return f"create {node.type_name} {node.name} with {prop_str}."

    def visit_PropertyAccessNode(self, node: PropertyAccessNode) -> str:
        obj = self.visit(node.object_expr)
        return f"{obj}'s {node.property_name}"

    def visit_MethodCallNode(self, node: MethodCallNode) -> str:
        obj = self.visit(node.object_expr)
        args = ", ".join(self.visit(a) for a in node.arguments)
        return f"{obj}'s {node.method_name}({args})"

    def visit_InterfaceDeclNode(self, node: InterfaceDeclNode) -> str:
        type_params = ""
        if getattr(node, 'type_parameters', []):
            type_params = f"<{', '.join(node.type_parameters)}>"
        
        vis = "export " if node.is_exported else ""
        out = f"{vis}interface {node.name}{type_params}."
        self.indent_level += 1
        for m in node.methods:
            out += f"\n{self._indent()}{self.visit(m)}"
        self.indent_level -= 1
        out += f"\n{self._indent()}end."
        return out

    def visit_InterfaceMethodNode(self, node: InterfaceMethodNode) -> str:
        params = []
        for p in node.parameters:
            params.append(f"{p[0]}: {self.visit(p[1])}")
        param_str = ", ".join(params)
        ret_type = ""
        if node.return_type:
            ret_type = f": {self.visit(node.return_type)}"
        return f"function {node.name}({param_str}){ret_type}."

    def visit_ExtensionDeclNode(self, node: ExtensionDeclNode) -> str:
        type_params = ""
        if getattr(node, 'type_parameters', []):
            type_params = f"<{', '.join(node.type_parameters)}>"
        
        if node.interface_name:
            out = f"extend {node.target_type}{type_params} with {node.interface_name}."
        else:
            out = f"extend {node.target_type}{type_params}."
            
        self.indent_level += 1
        for m in node.methods:
            out += f"\n{self._indent()}{self.visit(m)}"
        self.indent_level -= 1
        out += f"\n{self._indent()}end."
        return out

    def visit_ThrowNode(self, node: ThrowNode) -> str:
        return f"throw {self.visit(node.exception)}."

    def visit_PanicNode(self, node: PanicNode) -> str:
        return f"panic {self.visit(node.message)}."

    def visit_TryNode(self, node: TryNode) -> str:
        out = "try."
        self.indent_level += 1
        for stmt in node.body:
            out += f"\n{self._indent()}{self.visit(stmt)}"
        self.indent_level -= 1
        
        for catch in node.catches:
            out += f"\n{self._indent()}{self.visit(catch)}"
            
        if node.finally_block:
            out += f"\n{self._indent()}{self.visit(node.finally_block)}"
            
        out += f"\n{self._indent()}end."
        return out

    def visit_CatchNode(self, node: CatchNode) -> str:
        out = f"catch {node.exception_type} as {node.variable_name}."
        self.indent_level += 1
        for stmt in node.body:
            out += f"\n{self._indent()}{self.visit(stmt)}"
        self.indent_level -= 1
        return out

    def visit_FinallyNode(self, node: FinallyNode) -> str:
        out = "finally."
        self.indent_level += 1
        for stmt in node.body:
            out += f"\n{self._indent()}{self.visit(stmt)}"
        self.indent_level -= 1
        return out

    def visit_AssertNode(self, node: AssertNode) -> str:
        msg = f", {self.visit(node.message)}" if node.message else ""
        return f"assert {self.visit(node.condition)}{msg}."
