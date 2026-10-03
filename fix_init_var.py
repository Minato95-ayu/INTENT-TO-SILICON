import sys

def patch():
    with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
        content = f.read()

    target = """        current_scope = self.vm.state_scopes[-1]
        current_scope[name] = val
        self.vm.value_stack.push(val)
        return True"""
        
    new_target = """        current_scope = self.vm.state_scopes[-1]
        current_scope[name] = val
        return True"""

    if target in content:
        content = content.replace(target, new_target)
        with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
            f.write(content)
        print("Patched op_INIT_VAR to not push!")
    else:
        print("Target not found!")

patch()
