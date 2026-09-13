
import os

with open("runtime/vm/validator.py", "r", encoding="utf-8") as f:
    val_code = f.read()

patch = """            if opcode in (Opcode.REGISTER_ROUTE, Opcode.CHECK_AUTH, Opcode.SETUP_EXCEPT, Opcode.POP_EXCEPT, Opcode.SETUP_FINALLY, Opcode.EXEC_FINALLY):
                pass
            elif opcode == Opcode.DB_INSERT:
                idx = (bytecode[ip+1] << 8) | bytecode[ip+2]
                num_fields = constant_pool[idx]["fields_count"]
                new_depth -= (num_fields * 2)
            elif opcode == Opcode.DB_FIND:
                new_depth += 1
            elif opcode == Opcode.RESPOND:
                new_depth -= 1

            if new_depth != old_depth:
                from runtime.vm.instructions import opcode_to_str
                print(f"[VAL TRACE] ip={ip} {opcode_to_str(opcode)} {old_depth} -> {new_depth}")
"""

import re
val_code = re.sub(r"            elif opcode in \(Opcode\.REGISTER_ROUTE.*?new_depth -= 1", patch, val_code, flags=re.DOTALL)

with open("runtime/vm/validator.py", "w", encoding="utf-8") as f:
    f.write(val_code)
print("Validator trace added!")

