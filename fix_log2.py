import re

with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("while len(self.vm.state_scopes) > base_scope_depth:", """print(f"Popping scopes from {len(self.vm.state_scopes)} to {base_scope_depth}")
                while len(self.vm.state_scopes) > base_scope_depth:""")

with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
    f.write(content)
