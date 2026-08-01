import os

nodes_add = """
@dataclass(frozen=True)
class SemanticIdentifierNode(SemanticNode):
    name: str

@dataclass(frozen=True)
class SemanticActionDeclNode(SemanticNode):
    name: str
    statements: List[SemanticNode]

@dataclass(frozen=True)
class SemanticActionCallNode(SemanticNode):
    name: str
    args: List[SemanticNode]
"""

with open("compiler/semantic/nodes.py", "a") as f:
    f.write(nodes_add)

import_add = """from aayu.compiler.ast.nodes import (
    ProgramNode, StateDeclarationNode, LiteralNode,
    AssignmentNode, WidgetNode, ImportNode,
    ActionDeclarationNode, ActionCallNode, IdentifierNode
)"""
nodes_import_add = """from aayu.compiler.semantic.nodes import (
    SemanticProgramNode, SemanticStateDeclNode, SemanticLiteralNode,
    SemanticAssignmentNode, SemanticWidgetNode, SemanticImportNode,
    SemanticActionDeclNode, SemanticActionCallNode, SemanticIdentifierNode
)"""

analyzer_patch = """
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
"""

with open("compiler/semantic/analyzer.py", "r") as f:
    text = f.read()

# Replace ast imports
text = text.replace("""from aayu.compiler.ast.nodes import (
    ProgramNode, StateDeclarationNode, LiteralNode,
    AssignmentNode, WidgetNode, ImportNode
)""", import_add)

# Replace semantic nodes imports
text = text.replace("""from aayu.compiler.semantic.nodes import (
    SemanticProgramNode, SemanticStateDeclNode, SemanticLiteralNode,
    SemanticAssignmentNode, SemanticWidgetNode, SemanticImportNode
)""", nodes_import_add)

# Replace analyze_node and add the new methods
import re
text = re.sub(
    r"    def _analyze_node\(self, node\):.*?    def _analyze_state_decl", 
    analyzer_patch + "\n    def _analyze_state_decl", 
    text, flags=re.DOTALL
)

with open("compiler/semantic/analyzer.py", "w") as f:
    f.write(text)
