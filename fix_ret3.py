import re

with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("if hasattr(self.vm, 'state') and hasattr(self.vm, 'state_scopes'):", "if hasattr(self.vm, 'state_scopes'):")

with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
    f.write(content)
