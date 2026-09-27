with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('MIRInstruction("STORE_VAR", [hir.catch_var])', 'MIRInstruction("SET_STATE", [hir.catch_var])')

with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Reverted to SET_STATE")
