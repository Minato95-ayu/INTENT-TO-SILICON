import re

with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("def op_ENTER_SCOPE", "def op_ENTER_SCOPE_orig")

new_code = """
    def op_ENTER_SCOPE(self, opcode):
        print(f"ENTER_SCOPE (ip={self.vm.registers.ip}) -> len {len(self.vm.state_scopes) + 1}")
        return self.op_ENTER_SCOPE_orig(opcode)
"""
content += new_code

content = content.replace("def op_EXIT_SCOPE", "def op_EXIT_SCOPE_orig")

new_code = """
    def op_EXIT_SCOPE(self, opcode):
        print(f"EXIT_SCOPE (ip={self.vm.registers.ip}) -> len {len(self.vm.state_scopes) - 1}")
        return self.op_EXIT_SCOPE_orig(opcode)
"""
content += new_code

with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
    f.write(content)
