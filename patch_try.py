with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
    text = f.read()

target = """        if func_name in stdlib.registry.functions:
            func = stdlib.registry.functions[func_name]
            result = func(args, self.vm)
            self.vm.value_stack.push(result)
        elif isinstance(func_name, str) and (external := stdlib.registry.lookup_external(func_name)):"""

replacement = """        if func_name in stdlib.registry.functions:
            func = stdlib.registry.functions[func_name]
            try:
                result = func(args, self.vm)
                self.vm.value_stack.push(result)
            except Exception as e:
                self._throw_exception(KernelError(str(e)))
                return True
        elif isinstance(func_name, str) and (external := stdlib.registry.lookup_external(func_name)):"""

text = text.replace(target, replacement)

with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Added exception handling to OP_ASYNC_CALL")
