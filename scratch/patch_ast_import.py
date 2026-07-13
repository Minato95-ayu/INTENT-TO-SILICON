import re

with open('compiler/ast/nodes.py', 'r') as f:
    content = f.read()

import_node = """
@dataclass(frozen=True)
class ImportNode(ASTNode):
    module: str
"""

if "class ImportNode" not in content:
    content += "\n" + import_node

with open('compiler/ast/nodes.py', 'w') as f:
    f.write(content)
print("Updated nodes.py")
