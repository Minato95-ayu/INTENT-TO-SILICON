import re

with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
"""        elif type(node).__name__ == "SemanticLetDeclNode":
            val_hir = self._semantic_to_hir(node.value)
            if isinstance(val_hir, HIRPrint): val_hir = HIRLoadConst(val_hir.value)
            return HIRAssignment(node.name, val_hir)""",
"""        elif type(node).__name__ == "SemanticLetDeclNode":
            val_hir = self._semantic_to_hir(node.value)
            if isinstance(val_hir, HIRPrint): val_hir = HIRLoadConst(val_hir.value)
            return HIRStateDecl(node.name, val_hir)"""
)

with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
    f.write(content)
