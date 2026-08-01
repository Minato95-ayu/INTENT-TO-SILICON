import re
import time

with open('runtime/vm/interpreter.py', 'r', encoding='utf-8') as f:
    base_content = f.read()

missing_opcodes = """
            elif opcode == Opcode.CREATE_MODEL:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                model_name = self.vm.value_stack.pop()
                fields = self.vm.constant_pool[idx]
                self.vm.database.create_model(model_name, fields)
                
            elif opcode == Opcode.REGISTER_ROUTE:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                path = self.vm.value_stack.pop()
                methods_meta = self.vm.constant_pool[idx]
                self.vm.api_router.register_route(path, methods_meta)
                self.vm.api_router.start()
                
            elif opcode == Opcode.CHECK_AUTH:
                self.vm.registers.ip += 3
                # Check for authToken in the current state scope
                token = None
                if self.vm.state_scopes:
                    # We search from top to bottom
                    for scope in reversed(self.vm.state_scopes):
                        if "authToken" in scope.variables:
                            token = scope.variables["authToken"]
                            break
                
                if not token:
                    raise KernelError("Unauthorized: Missing auth token", self.vm.registers.ip)
                    
                from aayu.runtime.stdlib.modules.auth_lib import verify_jwt
                payload = verify_jwt(token)
                if not payload:
                    raise KernelError("Unauthorized: Invalid or expired auth token", self.vm.registers.ip)
                    
                # Inject req_user into the local scope so the action can use it
                if self.vm.state_scopes:
                    self.vm.state_scopes[-1]["req_user"] = payload
                else:
                    self.vm.state["req_user"] = payload
"""

with open('scratch/interpreter_diff.txt', 'r', encoding='utf-8') as f:
    diff_lines = f.readlines()

diff_opcodes = []
for line in diff_lines:
    if line.startswith('+'):
        if 'self.vm.state_scopes[-1]["req_user"] = payload' in line: continue
        if 'self.vm.state["req_user"] = payload' in line: continue
        if 'else:' in line and 'req_user' not in line: pass
        diff_opcodes.append(line[1:])

diff_opcodes_fixed = []
for line in diff_opcodes:
    diff_opcodes_fixed.append("    " + line)
diff_opcodes_str = "".join(diff_opcodes_fixed)

exception_opcodes = """
            elif opcode == Opcode.SETUP_EXCEPT:
                offset = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                if not hasattr(self.vm, 'block_stack'):
                    from aayu.runtime.vm.stack import Stack
                    self.vm.block_stack = Stack(max_depth=64)
                self.vm.block_stack.push({
                    "type": "TRY",
                    "handler_ip": offset,
                    "stack_depth": self.vm.value_stack.depth()
                })
                
            elif opcode == Opcode.POP_EXCEPT:
                self.vm.registers.ip += 1
                if hasattr(self.vm, 'block_stack') and self.vm.block_stack.depth() > 0:
                    block = self.vm.block_stack.pop()
                    if block["type"] != "TRY":
                        raise KernelError("POP_EXCEPT called but top block is not TRY")
                        
            elif opcode == Opcode.THROW:
                self.vm.registers.ip += 1
                exc = self.vm.value_stack.pop()
                handled = False
                if hasattr(self.vm, 'block_stack'):
                    while self.vm.block_stack.depth() > 0:
                        block = self.vm.block_stack.pop()
                        if block["type"] == "TRY":
                            while self.vm.value_stack.depth() > block["stack_depth"]:
                                self.vm.value_stack.pop()
                            self.vm.value_stack.push(exc)
                            self.vm.registers.ip = block["handler_ip"]
                            handled = True
                            break
                if not handled:
                    raise KernelError(f"Unhandled AAYU Exception: {exc}")
                    
            elif opcode == Opcode.RETHROW:
                self.vm.registers.ip += 1
                exc = self.vm.value_stack.pop()
                handled = False
                if hasattr(self.vm, 'block_stack'):
                    while self.vm.block_stack.depth() > 0:
                        block = self.vm.block_stack.pop()
                        if block["type"] == "TRY":
                            while self.vm.value_stack.depth() > block["stack_depth"]:
                                self.vm.value_stack.pop()
                            self.vm.value_stack.push(exc)
                            self.vm.registers.ip = block["handler_ip"]
                            handled = True
                            break
                if not handled:
                    raise KernelError(f"Unhandled AAYU Exception: {exc}")
"""

insert_marker = "            elif opcode == Opcode.DISPATCH:"
parts = base_content.split(insert_marker)
new_content = parts[0] + missing_opcodes + diff_opcodes_str + exception_opcodes + "\n" + insert_marker + parts[1]

with open('runtime/vm/interpreter_rebuilt.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print("Successfully rebuilt interpreter.py!")
