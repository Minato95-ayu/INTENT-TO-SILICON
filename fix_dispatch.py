import sys

def patch():
    with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
        content = f.read()

    target = "        self.dispatch_table[Opcode.INIT_COMPONENT_STATE] = self.op_INIT_COMPONENT_STATE"
    new_target = "        self.dispatch_table[Opcode.INIT_COMPONENT_STATE] = self.op_INIT_COMPONENT_STATE\n        self.dispatch_table[Opcode.INIT_VAR] = self.op_INIT_VAR"

    if target in content and "self.dispatch_table[Opcode.INIT_VAR]" not in content:
        content = content.replace(target, new_target)
        with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
            f.write(content)
        print("Patched interpreter dispatch table!")
    else:
        print("Target not found or already patched!")

patch()
