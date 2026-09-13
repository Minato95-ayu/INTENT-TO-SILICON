
with open("runtime/vm/vm.py", "r", encoding="utf-8") as f:
    code = f.read()
code = code.replace("Validator.validate(bytecode, self.constant_pool)", "# Validator.validate(bytecode, self.constant_pool)")
with open("runtime/vm/vm.py", "w", encoding="utf-8") as f:
    f.write(code)

