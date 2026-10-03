import re

with open("compiler/bytecode/encoder.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('elif opcode == "ACTION_DECL":\n            return 3', 'elif opcode == "ACTION_DECL":\n            return 9')

with open("compiler/bytecode/encoder.py", "w", encoding="utf-8") as f:
    f.write(content)
