from compiler.ast.nodes import (
    ProgramNode, StateDeclarationNode, LiteralNode,
    AssignmentNode, WidgetNode
)
from compiler.semantic.symbols import SymbolTable, Symbol
from compiler.semantic.errors import SemanticError
from compiler.semantic.nodes import (
    SemanticProgramNode, SemanticStateDeclNode, SemanticLiteralNode,
    SemanticAssignmentNode, SemanticWidgetNode
)

class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope

    def analyze(self, ast: ProgramNode) -> SemanticProgramNode:
        statements = []
        for stmt in ast.statements:
            statements.append(self._analyze_node(stmt))
            
        return SemanticProgramNode(
            line=ast.line,
            column=ast.column,
            scope=self.global_scope,
            statements=statements
        )

    def _analyze_node(self, node):
        if isinstance(node, StateDeclarationNode):
            return self._analyze_state_decl(node)
        elif isinstance(node, AssignmentNode):
            return self._analyze_assignment(node)
        elif isinstance(node, LiteralNode):
            return self._analyze_literal(node)
        elif isinstance(node, WidgetNode):
            return self._analyze_widget(node)
        else:
            raise SemanticError(f"Unknown node type: {type(node).__name__}", getattr(node, 'line', 0), getattr(node, 'column', 0))

    def _analyze_state_decl(self, node: StateDeclarationNode):
        if self.current_scope.resolve(node.name) is not None:
            raise SemanticError(f"Duplicate declaration of '{node.name}'", node.line, node.column)
            
        sym = Symbol(node.name, "state")
        self.current_scope.define(sym)
        
        val_node = self._analyze_node(node.value)
        return SemanticStateDeclNode(
            line=node.line,
            column=node.column,
            scope=self.current_scope,
            name=node.name,
            value=val_node
        )

    def _analyze_assignment(self, node: AssignmentNode):
        if self.current_scope.resolve(node.target) is None:
            raise SemanticError(f"Undefined variable '{node.target}'", node.line, node.column)
            
        val_node = self._analyze_node(node.value)
        return SemanticAssignmentNode(
            line=node.line,
            column=node.column,
            scope=self.current_scope,
            target=node.target,
            value=val_node
        )

    def _analyze_literal(self, node: LiteralNode):
        t_name = "number" if str(node.value).isdigit() else "string"
        return SemanticLiteralNode(
            line=node.line,
            column=node.column,
            scope=self.current_scope,
            value=node.value,
            type_name=t_name
        )

    def _analyze_widget(self, node: WidgetNode):
        # We can validate widget types here
        children = []
        for c in node.children:
            children.append(self._analyze_node(c))
            
        return SemanticWidgetNode(
            line=node.line,
            column=node.column,
            scope=self.current_scope,
            widget_type=node.widget_type,
            props=node.props,
            children=children
        )
