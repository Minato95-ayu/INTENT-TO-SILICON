import sys

def patch():
    with open("runtime/vm/validator.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Find INIT_STATE and add INIT_VAR with the SAME popping behavior as INIT_COMPONENT_STATE (it pops and pushes back, so net = 0)
    # Actually wait. Let me see what INIT_STATE does in validator.
    if "elif opcode == Opcode.INIT_VAR:" not in content:
        content = content.replace(
            "elif opcode == Opcode.INIT_COMPONENT_STATE:",
            "elif opcode in [Opcode.INIT_COMPONENT_STATE, Opcode.INIT_VAR]:"
        )
    with open("runtime/vm/validator.py", "w", encoding="utf-8") as f:
        f.write(content)

patch()
