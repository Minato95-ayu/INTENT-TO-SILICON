import re

with open('runtime/vm/interpreter.py', 'r') as f:
    content = f.read()

old_code = '''            from aayu.runtime.stdlib.stdlib import StdLib
            stdlib = StdLib(self.vm)
            
            # Find function in registry
            if func_name in stdlib.registry.functions:
                func = stdlib.registry.functions[func_name]
                result = func(*args)
                self.vm.value_stack.push(result)
            else:
                print(f"[VM Warning] Unresolved native function call: {func_name}")
                self.vm.value_stack.push(None)'''

new_code = '''            stdlib = self.vm.stdlib
            
            # Find function in registry
            if func_name in stdlib.registry.functions:
                func = stdlib.registry.functions[func_name]
                result = func(args, self.vm)
                self.vm.value_stack.push(result)
            else:
                print(f"[VM Warning] Unresolved native function call: {func_name}")
                self.vm.value_stack.push(None)'''

content = content.replace(old_code, new_code)

with open('runtime/vm/interpreter.py', 'w') as f:
    f.write(content)
