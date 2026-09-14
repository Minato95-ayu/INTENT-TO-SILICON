import re

with open("runtime/vm/vm.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("self.heap = Heap()", "self.heap = Heap()\n        self.heap.set_vm(self)")

with open("runtime/vm/vm.py", "w", encoding="utf-8") as f:
    f.write(content)
print("vm.py updated")
