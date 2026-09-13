
import os

with open("compiler/bytecode/encoder.py", "r", encoding="utf-8") as f:
    enc_code = f.read()

enc_patch = """        elif node.opcode == "DB_INSERT":
            idx = self._get_or_add_const(node.operands[0])
            instructions.append(Instruction("DB_INSERT", idx, node.operands[1]))
        elif node.opcode == "DB_FIND":
            idx = self._get_or_add_const(node.operands[0])
            instructions.append(Instruction("DB_FIND", idx))
        elif node.opcode == "RESPOND":
            instructions.append(Instruction("RESPOND"))"""
enc_code = enc_code.replace("elif node.opcode == \"RETURN_VALUE\":", enc_patch + "\n        elif node.opcode == \"RETURN_VALUE\":")

with open("compiler/bytecode/encoder.py", "w", encoding="utf-8") as f:
    f.write(enc_code)
print("Encoder Patched!")

