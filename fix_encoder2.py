import sys

def patch():
    with open("compiler/bytecode/encoder.py", "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace(
        "opcode not in [\"INIT_STATE\"]",
        "opcode not in [\"INIT_STATE\", \"INIT_VAR\"]"
    )
        
    with open("compiler/bytecode/encoder.py", "w", encoding="utf-8") as f:
        f.write(content)

patch()
