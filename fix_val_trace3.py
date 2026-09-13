
import os
with open("runtime/vm/validator.py", "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace(
    "            if new_depth != old_depth:",
    """            from runtime.vm.instructions import opcode_to_str
            print(f"[VAL TRACE] ip={ip} {opcode_to_str(opcode)} {old_depth} -> {new_depth}")
            if new_depth != old_depth:"""
)

with open("runtime/vm/validator.py", "w", encoding="utf-8") as f:
    f.write(code)

