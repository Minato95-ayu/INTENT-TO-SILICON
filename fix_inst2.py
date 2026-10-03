import sys

def patch():
    with open("runtime/vm/instructions.py", "r", encoding="utf-8") as f:
        content = f.read()

    if "INIT_VAR = 0x28" not in content:
        content = content.replace("CREATE_CLOSURE = 0x8A", "CREATE_CLOSURE = 0x8A\n    INIT_VAR = 0x28")
        
    with open("runtime/vm/instructions.py", "w", encoding="utf-8") as f:
        f.write(content)

patch()
