import sys

def patch():
    with open("runtime/vm/instructions.py", "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("INIT_VAR = 0x28", "INIT_VAR = 0x8B")
        
    with open("runtime/vm/instructions.py", "w", encoding="utf-8") as f:
        f.write(content)

patch()
