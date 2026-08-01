import re

with open('runtime/vm/interpreter.py', 'r') as f:
    content = f.read()

content = content.replace('opcode = self.vm.decoder.fetch8(self.vm.registers.ip)', 'opcode = self.vm.decoder.fetch8(self.vm.registers.ip)\n        from aayu.runtime.vm.instructions import Opcode\n        print("[DEBUG] Executing:", Opcode.opcode_to_str(opcode))')

with open('runtime/vm/interpreter.py', 'w') as f:
    f.write(content)
