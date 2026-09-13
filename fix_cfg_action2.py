import re
with open("compiler/ir/cfg_builder.py", "r") as f:
    content = f.read()

content = content.replace("action_cfg = CFG()", "action_cfg = CFG(hir.name)")

with open("compiler/ir/cfg_builder.py", "w") as f:
    f.write(content)
