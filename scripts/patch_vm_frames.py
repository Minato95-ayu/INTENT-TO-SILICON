"""
=============================================================================
FILE: patch_vm_frames.py
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
    vm_content = f.read()

pattern = r'            while self\.frames:.*?            except Exception as e:'
replacement = """            while self.frames:
                self.instruction_count += 1
                if self.instruction_count > 1000000:
                    self._raise_runtime_error("Maximum instruction limit exceeded")
                    
                current_frame = self.frames[-1]
                
                if current_frame.ip >= len(current_frame.bytecode.instructions):
                    self.frames.pop()
                    self.memory.pop_frame()
                    continue
                    
                instruction = current_frame.bytecode.instructions[current_frame.ip]
                opcode = instruction.opcode
                operand = instruction.operand
                
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
                        if self.frames:
                            current_frame = self.frames[-1]
                            current_frame.stack.append(ret_val)
                        continue
                        
                handled_jump = dispatch(opcode, operand, current_frame, self)
                if not handled_jump:
                    current_frame.ip += 1

        except Exception as e:"""

new_content = re.sub(pattern, replacement, vm_content, flags=re.DOTALL)

with open(vm_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Replaced vm loop!")
