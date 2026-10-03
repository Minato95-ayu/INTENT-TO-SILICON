import sys
from compiler.ir.hir import HIRNode

class HIRLetDecl(HIRNode):
    def __init__(self, name: str, value):
        self.name = name
        self.value = value
        self.line = -1

    def __repr__(self):
        return f"HIRLetDecl(name={self.name!r}, value={self.value!r})"

def patch_hir():
    with open("compiler/ir/hir.py", "r", encoding="utf-8") as f:
        content = f.read()
    if "class HIRLetDecl" not in content:
        new_class = """
@dataclass
class HIRLetDecl(HIRNode):
    name: str
    value: Any

"""
        content = content.replace("@dataclass\nclass HIRStateDecl(HIRNode):", new_class + "@dataclass\nclass HIRStateDecl(HIRNode):")
        with open("compiler/ir/hir.py", "w", encoding="utf-8") as f:
            f.write(content)
            
patch_hir()
