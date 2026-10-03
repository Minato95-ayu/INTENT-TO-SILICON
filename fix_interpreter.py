import re

with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix missing return True
new_code = """
        if func_name in stdlib.registry.functions:
            func = stdlib.registry.functions[func_name]
            try:
                result = func(args, self.vm)
                self.vm.value_stack.push(result)
                return True
            except Exception as e:
"""

content = content.replace("""        if func_name in stdlib.registry.functions:
            func = stdlib.registry.functions[func_name]
            try:
                result = func(args, self.vm)
                self.vm.value_stack.push(result)
            except Exception as e:""", new_code)

with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
    f.write(content)
