
import os

with open("runtime/vm/validator.py", "r", encoding="utf-8") as f:
    val_code = f.read()

patch = """            elif opcode == Opcode.DB_INSERT:
                num_fields = (bytecode[ip+3] << 8) | bytecode[ip+4]
                new_depth -= (num_fields * 2)
            elif opcode == Opcode.DB_FIND:
                new_depth += 1
            elif opcode == Opcode.RESPOND:
                new_depth -= 1"""

val_code = val_code.replace("pass # Assuming 0 delta", "pass\n" + patch)

with open("runtime/vm/validator.py", "w", encoding="utf-8") as f:
    f.write(val_code)
print("Validator Patched!")

