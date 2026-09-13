
import os

with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
    pipe_code = f.read()

# Add HIR nodes
if "class HIRInsert" not in pipe_code:
    hir_nodes = """
class HIRInsert(HIRNode):
    def __init__(self, model_name, fields):
        self.model_name = model_name
        self.fields = fields
class HIRFind(HIRNode):
    def __init__(self, model_name):
        self.model_name = model_name
class HIRRespond(HIRNode):
    def __init__(self, value):
        self.value = value
"""
    pipe_code = pipe_code.replace("class HIRRethrow(HIRNode):", "class HIRRethrow(HIRNode):\n    pass" + hir_nodes)

# Semantic to HIR
sem_to_hir = """        elif isinstance(node, SemanticInsertNode):
            fields_hir = {k: self._semantic_to_hir(v) for k, v in node.fields.items()}
            return HIRInsert(node.model_name, fields_hir)
        elif isinstance(node, SemanticFindNode):
            return HIRFind(node.model_name)
        elif isinstance(node, SemanticRespondNode):
            return HIRRespond(self._semantic_to_hir(node.value))"""
pipe_code = pipe_code.replace("elif isinstance(node, SemanticReturnNode):", sem_to_hir + "\n        elif isinstance(node, SemanticReturnNode):")

# HIR to MIR
hir_to_mir = """        elif isinstance(hir_node, HIRInsert):
            for k, v in hir_node.fields.items():
                self._hir_to_mir(v, mir_list)
                mir_list.append(MIRInstruction("PUSH_CONST", [k]))
            mir_list.append(MIRInstruction("DB_INSERT", [hir_node.model_name, len(hir_node.fields)]))
        elif isinstance(hir_node, HIRFind):
            mir_list.append(MIRInstruction("DB_FIND", [hir_node.model_name]))
        elif isinstance(hir_node, HIRRespond):
            self._hir_to_mir(hir_node.value, mir_list)
            mir_list.append(MIRInstruction("RESPOND", []))"""
pipe_code = pipe_code.replace("elif isinstance(hir_node, HIRReturn):", hir_to_mir + "\n        elif isinstance(hir_node, HIRReturn):")

with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
    f.write(pipe_code)
print("Pipeline Patched for CRUD Linkage!")

