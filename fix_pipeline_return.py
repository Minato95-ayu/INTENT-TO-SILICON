import re
with open("compiler/ir/pipeline.py", "r") as f:
    content = f.read()

replacement = """        elif isinstance(node, SemanticReturnNode):
            val_hir = self._semantic_to_hir(node.value)
            if isinstance(val_hir, HIRPrint): val_hir = HIRLoadConst(val_hir.value)
            return HIRReturn(val_hir)"""

content = re.sub(r'        elif isinstance\(node, SemanticReturnNode\):\n\s*val_hir = self\._semantic_to_hir\(node\.value\)\n\s*return HIRReturn\(val_hir\)', replacement, content)
with open("compiler/ir/pipeline.py", "w") as f:
    f.write(content)
