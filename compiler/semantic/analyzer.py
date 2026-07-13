from compiler.ast.nodes import (
    ProgramNode, StateDeclarationNode, LiteralNode,
    AssignmentNode, WidgetNode, ImportNode,
    ActionDeclarationNode, ActionCallNode, IdentifierNode,
    AppDeclarationNode, RunNode
)
from compiler.semantic.symbols import SymbolTable, Symbol
from compiler.semantic.errors import SemanticError
from compiler.semantic.nodes import (
    SemanticProgramNode, SemanticStateDeclNode, SemanticLiteralNode,
    SemanticAssignmentNode, SemanticWidgetNode, SemanticImportNode,
    SemanticActionDeclNode, SemanticActionCallNode, SemanticIdentifierNode
)

class SemanticAnalyzer:
    def __init__(self, visiting_modules=None):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.visiting_modules = visiting_modules or set()

    def analyze(self, ast: ProgramNode) -> SemanticProgramNode:
        statements = []
        for stmt in ast.statements:
            result = self._analyze_node(stmt)
            if result is not None:
                statements.append(result)
            
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
        elif isinstance(node, ImportNode):
            return self._analyze_import(node)
        elif isinstance(node, ActionDeclarationNode):
            return self._analyze_action_decl(node)
        elif isinstance(node, ActionCallNode):
            return self._analyze_action_call(node)
        elif isinstance(node, IdentifierNode):
            return self._analyze_identifier(node)
        elif isinstance(node, AppDeclarationNode):
            # App declaration is metadata — pass through as-is
            return None
        elif isinstance(node, RunNode):
            # Run is a control marker — skip in semantic analysis
            return None
        else:
            raise SemanticError(f"Unknown node type: {type(node).__name__}", getattr(node, 'line', 0), getattr(node, 'column', 0))

    def _analyze_action_decl(self, node: ActionDeclarationNode):
        statements = []
        for stmt in node.statements:
            statements.append(self._analyze_node(stmt))
        return SemanticActionDeclNode(
            line=node.line, column=node.column, scope=self.current_scope,
            name=node.name, statements=statements
        )

    def _analyze_action_call(self, node: ActionCallNode):
        args = []
        for a in node.args:
            args.append(self._analyze_node(a))
        return SemanticActionCallNode(
            line=node.line, column=node.column, scope=self.current_scope,
            name=node.name, args=args
        )

    def _analyze_identifier(self, node: IdentifierNode):
        return SemanticIdentifierNode(
            line=node.line, column=node.column, scope=self.current_scope,
            name=node.name
        )

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

    def _analyze_import(self, node: ImportNode):
        from compiler.errors import CompilerError
        if node.module in self.visiting_modules:
            raise CompilerError(f"Import cycle detected: '{node.module}'", node.line, getattr(node, 'column', 0))
            
        self.visiting_modules.add(node.module)
        # In a real compiler, we would load and parse the module here, and run SemanticAnalyzer recursively
        # For now, we just track the cycle.
        return SemanticImportNode(
            line=node.line,
            column=getattr(node, 'column', 0),
            scope=self.current_scope,
            module=node.module
        )
