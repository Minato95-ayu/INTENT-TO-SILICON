import re

with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
    content = f.read()

# In op_CALL
content = content.replace(
    'self.vm.call_stack.push((self.vm.registers.ip + 3, False, returns, args, base_depth))',
    'self.vm.call_stack.push((self.vm.registers.ip + 3, False, returns, args, base_depth, len(self.vm.state.scopes)))'
)

# In op_CALL_COMPONENT
content = content.replace(
    'self.vm.call_stack.push((self.vm.registers.ip + 3, True, 0, 1, base_depth))',
    'self.vm.call_stack.push((self.vm.registers.ip + 3, True, 0, 1, base_depth, len(self.vm.state.scopes)))'
)

# In op_RET and op_RETURN_VALUE, they need to unpack the 6th element and restore scopes.
with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
    f.write(content)
