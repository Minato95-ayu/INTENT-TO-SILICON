import os
import re

vm_path = r"prototype\language\runtime\vm\vm.py"
with open(vm_path, "r", encoding="utf-8") as f:
    vm_content = f.read()

# Replace the giant if-else block
start_str = "            self.instruction_count += 1"
end_str = "            except Exception as e:"

start_idx = vm_content.find(start_str)
end_idx = vm_content.find(end_str)

if start_idx != -1 and end_idx != -1:
    new_loop = """            self.instruction_count += 1
            if self.instruction_count > 1000000:
                self._raise_runtime_error("Maximum instruction limit exceeded")

            try:
                from .handlers import dispatch
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
                
"""
    # The end_idx points to `            except Exception as e:`.
    # Let's keep it.
    vm_content = vm_content[:start_idx] + new_loop + vm_content[end_idx:]
    with open(vm_path, "w", encoding="utf-8") as f:
        f.write(vm_content)
    print("Patched vm loop!")
else:
    print("Could not find bounds.")
