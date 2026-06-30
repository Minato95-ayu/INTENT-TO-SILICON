import os

vm_path = r"prototype\language\runtime\vm\vm.py"
with open(vm_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_loop = False

for line in lines:
    if "while self.frames:" in line:
        in_loop = True
        new_lines.append(line)
        new_lines.append("""                self.instruction_count += 1
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
""")
    elif in_loop:
        if "except Exception as e:" in line:
            in_loop = False
            new_lines.append("        " + line.lstrip())
    else:
        new_lines.append(line)

with open(vm_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("Manually replaced vm loop by lines!")
