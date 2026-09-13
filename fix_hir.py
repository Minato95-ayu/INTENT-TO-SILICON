
import os

with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
    pipe_code = f.read()

hir_to_mir = """        elif isinstance(hir, HIRInsert):
            for k, v in hir.fields.items():
                self._hir_to_mir(v, mir_list)
                mir_list.append(MIRInstruction("PUSH_CONST", [k]))
            mir_list.append(MIRInstruction("DB_INSERT", [hir.model_name, len(hir.fields)]))
            mir_list.append(MIRInstruction("PUSH_CONST", [0])) # Dummy push to balance stack
        elif isinstance(hir, HIRFind):
            mir_list.append(MIRInstruction("DB_FIND", [hir.model_name]))
        elif isinstance(hir, HIRRespond):
            self._hir_to_mir(hir.value, mir_list)
            mir_list.append(MIRInstruction("RESPOND", []))"""

pipe_code = pipe_code.replace("elif isinstance(hir, HIRReturn):", hir_to_mir + "\n        elif isinstance(hir, HIRReturn):")

with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
    f.write(pipe_code)
print("Pipeline Patched properly!")

