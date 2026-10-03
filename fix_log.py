import re

with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("def op_INIT_STATE", "def op_INIT_STATE_orig")

new_code = """
    def op_INIT_STATE(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        name = self.vm.constant_pool[idx]
        print(f"INIT_STATE {name} in scope len {len(self.vm.state_scopes)}")
        return self.op_INIT_STATE_orig(opcode)
"""
content += new_code

with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
    f.write(content)
