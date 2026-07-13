import re

with open('compiler/semantic/nodes.py', 'r') as f:
    content = f.read()

semantic_import = """
@dataclass(frozen=True)
class SemanticImportNode(SemanticASTNode):
    module: str
"""

if "class SemanticImportNode" not in content:
    content += "\n" + semantic_import

with open('compiler/semantic/nodes.py', 'w') as f:
    f.write(content)
print("Updated nodes.py in semantic")
