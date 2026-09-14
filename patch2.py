import re

with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
    content = f.read()

helper = """    def _needs_pop(self, stmt):
        from compiler.ir.hir import HIRActionCall, HIRInsert, HIRFind, HIRBinaryOp, HIRLoadVar, HIRLoadConst, HIRArrayNode, HIRSubscript, HIRDictionary, HIRAwait
        return isinstance(stmt, (HIRActionCall, HIRInsert, HIRFind, HIRBinaryOp, HIRLoadVar, HIRLoadConst, HIRArrayNode, HIRSubscript, HIRDictionary, HIRAwait))
"""

if "_needs_pop" not in content:
    content = content.replace("class IRPipeline:\n", "class IRPipeline:\n" + helper)

# In HIRActionDecl
content = content.replace("if isinstance(stmt, HIRActionCall):\n                    body_mir.append(MIRInstruction(\"POP\", []))", 
                          "if self._needs_pop(stmt):\n                    body_mir.append(MIRInstruction(\"POP\", []))")

# In HIRRoute
content = content.replace("if isinstance(stmt, HIRActionCall):\n                        body_mir.append(MIRInstruction(\"POP\", []))", 
                          "if self._needs_pop(stmt):\n                        body_mir.append(MIRInstruction(\"POP\", []))")

# In HIRIf - then_branch
if "for stmt in hir.then_branch:\n                self._hir_to_mir(stmt, mir_list)\n            mir_list.append(MIRInstruction(\"JUMP\", [end_label]))" in content:
    content = content.replace(
        "for stmt in hir.then_branch:\n                self._hir_to_mir(stmt, mir_list)\n            mir_list.append(MIRInstruction(\"JUMP\", [end_label]))",
        "for stmt in hir.then_branch:\n                self._hir_to_mir(stmt, mir_list)\n                if self._needs_pop(stmt):\n                    mir_list.append(MIRInstruction(\"POP\", []))\n            mir_list.append(MIRInstruction(\"JUMP\", [end_label]))"
    )

# In HIRIf - else_branch
if "for stmt in hir.else_branch:\n                    self._hir_to_mir(stmt, mir_list)\n            mir_list.append(MIRInstruction(\"LABEL\", [end_label]))" in content:
    content = content.replace(
        "for stmt in hir.else_branch:\n                    self._hir_to_mir(stmt, mir_list)\n            mir_list.append(MIRInstruction(\"LABEL\", [end_label]))",
        "for stmt in hir.else_branch:\n                    self._hir_to_mir(stmt, mir_list)\n                    if self._needs_pop(stmt):\n                        mir_list.append(MIRInstruction(\"POP\", []))\n            mir_list.append(MIRInstruction(\"LABEL\", [end_label]))"
    )

# In HIRFor
if "for stmt in hir.body:\n                self._hir_to_mir(stmt, mir_list)\n            # Increment index" in content:
    content = content.replace(
        "for stmt in hir.body:\n                self._hir_to_mir(stmt, mir_list)\n            # Increment index",
        "for stmt in hir.body:\n                self._hir_to_mir(stmt, mir_list)\n                if self._needs_pop(stmt):\n                    mir_list.append(MIRInstruction(\"POP\", []))\n            # Increment index"
    )

# In HIRLifecycle
if "for stmt in hir.body:\n                self._hir_to_mir(stmt, body_mir)\n            mir_list.append(MIRInstruction(\"DECLARE_LIFECYCLE\", [hir.hook, body_mir]))" in content:
    content = content.replace(
        "for stmt in hir.body:\n                self._hir_to_mir(stmt, body_mir)\n            mir_list.append(MIRInstruction(\"DECLARE_LIFECYCLE\", [hir.hook, body_mir]))",
        "for stmt in hir.body:\n                self._hir_to_mir(stmt, body_mir)\n                if self._needs_pop(stmt):\n                    body_mir.append(MIRInstruction(\"POP\", []))\n            mir_list.append(MIRInstruction(\"DECLARE_LIFECYCLE\", [hir.hook, body_mir]))"
    )

with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
    f.write(content)
print("done replacing")
