import re

with open('runtime/vm/interpreter.py', 'r') as f:
    content = f.read()

old_code = '''        elif opcode == Opcode.OP_ASYNC_CALL:
            self.vm.registers.ip += 3
            # AWAIT is currently synchronous in this interpreter implementation
            pass'''
new_code = '''        elif opcode == Opcode.OP_ASYNC_CALL:
            # Opcode.OP_ASYNC_CALL num_args
            # Stack top has: argN, argN-1, ... arg1, name_idx
            num_args = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
            self.vm.registers.ip += 3
            
            args = []
            for _ in range(num_args):
                args.insert(0, self.vm.value_stack.pop())
            
            name_idx = self.vm.value_stack.pop()
            func_name = self.vm.constant_pool[name_idx]
            
            from aayu.runtime.stdlib.stdlib import StdLib
            stdlib = StdLib(self.vm)
            
            # Find function in registry
            if func_name in stdlib.registry.functions:
                func = stdlib.registry.functions[func_name]
                result = func(*args)
                self.vm.value_stack.push(result)
            else:
                print(f"[VM Warning] Unresolved native function call: {func_name}")
                self.vm.value_stack.push(None)'''

content = content.replace(old_code, new_code)
with open('runtime/vm/interpreter.py', 'w') as f:
    f.write(content)
