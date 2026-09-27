with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('MIRInstruction("SET_STATE", [hir.catch_var])', 'MIRInstruction("STORE_VAR", [hir.catch_var])')

with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Patched SET_STATE to STORE_VAR")
