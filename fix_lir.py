
import os

with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
    pipe_code = f.read()

lir_patch = """        elif mir.opcode == "DECLARE_LIFECYCLE":
            body_lir = []
            for sub_mir in mir.operands[1]:
                self._mir_to_lir(sub_mir, body_lir)
            lir_list.append(LIRNode("DECLARE_LIFECYCLE", [mir.operands[0], body_lir]))
        elif mir.opcode in ("DB_INSERT", "DB_FIND", "RESPOND"):
            lir_list.append(LIRNode(mir.opcode, mir.operands))"""

pipe_code = pipe_code.replace("""        elif mir.opcode == "DECLARE_LIFECYCLE":
            body_lir = []
            for sub_mir in mir.operands[1]:
                self._mir_to_lir(sub_mir, body_lir)
            lir_list.append(LIRNode("DECLARE_LIFECYCLE", [mir.operands[0], body_lir]))""", lir_patch)

with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
    f.write(pipe_code)
print("LIR Patched!")

