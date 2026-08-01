import re

with open('compiler/semantic/analyzer.py', 'r') as f:
    content = f.read()

# Add ImportNode
content = content.replace(
    'AssignmentNode, WidgetNode',
    'AssignmentNode, WidgetNode, ImportNode'
)

# Add SemanticImportNode
# But first, I need to create it in nodes.py, let's just use SemanticLiteralNode for now, or add SemanticImportNode
content = content.replace(
    'SemanticAssignmentNode, SemanticWidgetNode',
    'SemanticAssignmentNode, SemanticWidgetNode\nfrom compiler.semantic.nodes import SemanticImportNode'
)

# Modify __init__ to track visited modules
init_method = """    def __init__(self, visiting_modules=None):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.visiting_modules = visiting_modules or set()"""

content = re.sub(
    r'def __init__\(self\):\n.*?self\.current_scope = self\.global_scope',
    init_method,
    content,
    flags=re.DOTALL
)

# Add ImportNode handling
import_handler = """        elif isinstance(node, ImportNode):
            return self._analyze_import(node)"""

content = content.replace(
    'elif isinstance(node, WidgetNode):\n            return self._analyze_widget(node)',
    'elif isinstance(node, WidgetNode):\n            return self._analyze_widget(node)\n' + import_handler
)

# Add _analyze_import method
analyze_import_method = """
    def _analyze_import(self, node: ImportNode):
        from aayu.compiler.errors import CompilerError
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
"""

content += analyze_import_method

with open('compiler/semantic/analyzer.py', 'w') as f:
    f.write(content)
print("Updated analyzer.py")
