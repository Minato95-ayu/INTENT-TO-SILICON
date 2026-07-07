"""
=============================================================================
FILE: patch_vm_lines.py
PURPOSE: Fixes or patches existing code
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles fixes or patches existing code.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import re

vm_path = r"prototype\language\runtime\vm\vm.py"
with open(vm_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_loop = False
replaced = False

for i, line in enumerate(lines):
    if "while current_frame.ip < len(current_frame.bytecode.instructions):" in line:
        in_loop = True
        new_lines.append(line)
        new_lines.append("""            instruction = current_frame.bytecode.instructions[current_frame.ip]
            opcode = instruction.opcode
            operand = instruction.operand
            
            self.instruction_count += 1
            if self.instruction_count > 1000000:
                self._raise_runtime_error("Maximum instruction limit exceeded")

            from .handlers import dispatch
            from ..values.null import NullValue
            if opcode == Opcode.RETURN:
                if len(self.frames) == 1:
                    self.return_value = current_frame.stack.pop() if current_frame.stack else NullValue()
                    break
                else:
                    ret_val = current_frame.stack.pop() if current_frame.stack else NullValue()
                    self.memory.pop_frame()
                    self.frames.pop()
                    current_frame = self.frames[-1]
                    current_frame.stack.append(ret_val)
                    continue
                    
            handled_jump = dispatch(opcode, operand, current_frame, self)
            if not handled_jump:
                current_frame.ip += 1
""")
    elif in_loop:
        if "except Exception as e:" in line:
            in_loop = False
            new_lines.append("        " + line.lstrip())
    else:
        new_lines.append(line)

with open(vm_path, "w", encoding="utf-8") as f:
    f.write("".join(new_lines))
print("Patched vm.py using lines!")
