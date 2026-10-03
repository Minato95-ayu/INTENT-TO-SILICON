import re

with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('MIRInstruction("STORE_STATE", [hir.name])', 'MIRInstruction("INIT_STATE", [hir.name])')

with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
    f.write(content)
