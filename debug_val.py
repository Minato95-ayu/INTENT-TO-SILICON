
import re
with open("runtime/vm/validator.py", "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("new_depth = depth", "new_depth = depth\n            from runtime.vm.instructions import opcode_to_str\n            print(f\"[VAL TRACE] ip={ip} {opcode_to_str(opcode)} {old_depth} -> {new_depth}\")".replace("old_depth", "depth"))

with open("runtime/vm/validator.py", "w", encoding="utf-8") as f:
    f.write(code)

