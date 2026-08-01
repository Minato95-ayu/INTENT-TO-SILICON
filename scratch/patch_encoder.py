import re

with open('compiler/bytecode/encoder.py', 'r') as f:
    content = f.read()

old_code = '''        elif opcode == "OP_ASYNC_CALL":
            self._emit(Opcode.OP_ASYNC_CALL, 0)'''
new_code = '''        elif opcode == "OP_ASYNC_CALL":
            name = node.operands[0]
            num_args = node.operands[1]
            name_idx = self.pool.add(name)
            self._emit(Opcode.PUSH_CONST, name_idx)
            self._emit(Opcode.OP_ASYNC_CALL, num_args)'''

content = content.replace(old_code, new_code)
with open('compiler/bytecode/encoder.py', 'w') as f:
    f.write(content)
