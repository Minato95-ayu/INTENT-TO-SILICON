import re

with open('runtime/vm/interpreter.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('is_comp = self.vm.call_stack.frames[-1][1]', 'is_comp = self.vm.call_stack.frames[-1][1]\n            print("INIT_STATE name:", name, "val:", val, "is_comp:", is_comp)')

with open('runtime/vm/interpreter.py', 'w', encoding='utf-8') as f:
    f.write(text)
