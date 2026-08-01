with open('runtime/vm/interpreter.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("props = self.vm.value_stack.pop()\n                print(f'POPPED WIDGET PROPS: {props!r}')", "props = self.vm.value_stack.pop()")

with open('runtime/vm/interpreter.py', 'w', encoding='utf-8') as f:
    f.write(content)
