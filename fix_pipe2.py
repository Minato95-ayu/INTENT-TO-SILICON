
import os

with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
    pipe_code = f.read()

hir_to_mir = """        elif isinstance(node, SemanticInsertNode):
            fields_hir = {}
            for k, v in node.fields.items():
                val_hir = self._semantic_to_hir(v)
                if isinstance(val_hir, HIRPrint): val_hir = HIRLoadConst(val_hir.value)
                fields_hir[k] = val_hir
            return HIRInsert(node.model_name, fields_hir)"""

pipe_code = pipe_code.replace("""        elif isinstance(node, SemanticInsertNode):
            fields_hir = {k: self._semantic_to_hir(v) for k, v in node.fields.items()}
            return HIRInsert(node.model_name, fields_hir)""", hir_to_mir)

with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
    f.write(pipe_code)
print("Pipeline Patched properly again!")

