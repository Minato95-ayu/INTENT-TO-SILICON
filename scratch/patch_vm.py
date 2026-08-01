
with open("runtime/vm/vm.py", "r") as f:
    code = f.read()

code = code.replace("not self.value_stack.is_empty()", "self.value_stack.depth() > 0")

with open("runtime/vm/vm.py", "w") as f:
    f.write(code)

