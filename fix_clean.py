import sys

def patch():
    with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Remove INIT_STATE print
    target1 = """        if name in ["type", "node", "child_type"]:
            print(f"[DEBUG INIT_STATE] Setting {name} to: {val} in scope id {id(current_scope)}")
            
        current_scope[name] = val"""
    new_target1 = "        current_scope[name] = val"

    # Remove LOAD_STATE print
    target2 = """            if name in ["type", "node", "child_type"]:
                print(f"[DEBUG LOAD_STATE] Found {name} = {val} in scope id {id(scope)}")
            self.vm.value_stack.push(val)"""
    new_target2 = "            self.vm.value_stack.push(val)"

    content = content.replace(target1, new_target1)
    content = content.replace(target2, new_target2)

    with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Cleaned up debug prints!")

patch()
