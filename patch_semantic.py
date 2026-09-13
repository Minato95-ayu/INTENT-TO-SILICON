
import sys
with open("compiler/semantic/analyzer.py", "r", encoding="utf-8") as f:
    content = f.read()

import_ast = "from compiler.ast.nodes import ("
import_new = "from compiler.ast.nodes import (InsertNode, FindNode, RespondNode, "
content = content.replace(import_ast, import_new)

sem_imports = "from .nodes import ("
sem_new = "from .nodes import (SemanticInsertNode, SemanticFindNode, SemanticRespondNode, "
content = content.replace(sem_imports, sem_new)

parse_node = """    def _analyze_node(self, node):"""
new_parse = """    def _analyze_node(self, node):
        if isinstance(node, InsertNode):
            fields = {k: self._analyze_node(v) for k, v in node.fields.items()}
            return SemanticInsertNode(node.model_name, fields)
        if isinstance(node, FindNode):
            return SemanticFindNode(node.model_name)
        if isinstance(node, RespondNode):
            return SemanticRespondNode(self._analyze_node(node.value))
"""
content = content.replace(parse_node, new_parse)

with open("compiler/semantic/analyzer.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Semantic analyzer Patched!")

with open("compiler/semantic/nodes.py", "r", encoding="utf-8") as f:
    node_content = f.read()

node_new = """
@dataclass(frozen=True)
class SemanticInsertNode(SemanticNode):
    model_name: str
    fields: dict
@dataclass(frozen=True)
class SemanticFindNode(SemanticNode):
    model_name: str
@dataclass(frozen=True)
class SemanticRespondNode(SemanticNode):
    value: SemanticNode
"""
node_content = node_content + node_new
with open("compiler/semantic/nodes.py", "w", encoding="utf-8") as f:
    f.write(node_content)

