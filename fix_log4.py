import re

with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("def op_STORE_STATE", "def op_STORE_STATE_orig")

new_code = """
    def op_STORE_STATE(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        name = self.vm.constant_pool[idx]
        print(f"STORE_STATE {name} in {self.vm.state_scopes}")
        return self.op_STORE_STATE_orig(opcode)
"""
content += new_code

with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
    f.write(content)
