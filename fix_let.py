import re
with open('compiler/ir/pipeline.py', 'r') as f:
    content = f.read()

replacement = """
    def _semantic_to_hir(self, node):
        if isinstance(node, SemanticStateDeclNode) or type(node).__name__ == "SemanticLetDeclNode":
            val_hir = self._semantic_to_hir(node.value)
            if isinstance(val_hir, HIRPrint): val_hir = HIRLoadConst(val_hir.value)
            return HIRStateDecl(node.name, val_hir)"""

content = content.replace("    def _semantic_to_hir(self, node):\n        if isinstance(node, SemanticStateDeclNode):", replacement)

with open('compiler/ir/pipeline.py', 'w') as f:
    f.write(content)
