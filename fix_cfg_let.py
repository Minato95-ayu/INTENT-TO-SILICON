import re
with open('compiler/ir/cfg_builder.py', 'r') as f:
    content = f.read()

replacement = """
        elif isinstance(hir, HIRLoadVar):
            if hir.name == "true": return self._emit("CONST", [True])
            if hir.name == "false": return self._emit("CONST", [False])
            if hir.name == "null": return self._emit("CONST", [None])
            return self._emit("LOAD_VAR", [hir.name])"""

content = re.sub(r'\n\s*elif isinstance\(hir, HIRLoadVar\):\n\s*return self\._emit\("LOAD_VAR", \[hir\.name\]\)', replacement, content, flags=re.DOTALL)

with open('compiler/ir/cfg_builder.py', 'w') as f:
    f.write(content)
