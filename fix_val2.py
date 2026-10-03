import sys

def patch():
    with open("runtime/vm/validator.py", "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace(
        "Opcode.INIT_COMPONENT_STATE, \nOpcode.CREATE_MODEL",
        "Opcode.INIT_COMPONENT_STATE, Opcode.INIT_VAR, \nOpcode.CREATE_MODEL"
    )
    # just in case
    content = content.replace(
        "Opcode.INIT_COMPONENT_STATE, Opcode.CREATE_MODEL",
        "Opcode.INIT_COMPONENT_STATE, Opcode.INIT_VAR, Opcode.CREATE_MODEL"
    )
    with open("runtime/vm/validator.py", "w", encoding="utf-8") as f:
        f.write(content)

patch()
