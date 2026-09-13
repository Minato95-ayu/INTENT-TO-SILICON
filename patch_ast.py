
import sys
content = open("compiler/ast/nodes.py").read()

new_nodes = """
@dataclass(frozen=True)
class InsertNode(ASTNode):
    model_name: str
    fields: dict

@dataclass(frozen=True)
class FindNode(ASTNode):
    model_name: str

@dataclass(frozen=True)
class RespondNode(ASTNode):
    value: ASTNode
"""

content = content.replace("class ReturnNode(ASTNode):", new_nodes + "\n@dataclass(frozen=True)\nclass ReturnNode(ASTNode):")
with open("compiler/ast/nodes.py", "w") as f:
    f.write(content)
print("Patched!")

