with open('runtime/vm/interpreter.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('self.vm.registers.ip += 1', 'self.vm.registers.ip += 3')

with open('runtime/vm/interpreter.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('runtime/vm/validator.py', 'r', encoding='utf-8') as f:
    val_content = f.read()

# in validator.py, instead of doing different ip += 3 or ip += 1, just do ip += 3 for all.
# Actually I'll just replace 'ip += 1' with 'ip += 3' since the loop has else: ip += 1
val_content = val_content.replace('ip += 1', 'ip += 3')

with open('runtime/vm/validator.py', 'w', encoding='utf-8') as f:
    f.write(val_content)
