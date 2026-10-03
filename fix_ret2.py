import re

with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("len(self.vm.state.scopes)", "len(self.vm.state_scopes)")
content = content.replace("self.vm.state.scopes.pop()", "self.vm.state_scopes.pop()")
content = content.replace("hasattr(self.vm.state, 'scopes')", "hasattr(self.vm, 'state_scopes')")

with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
    f.write(content)
