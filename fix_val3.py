import sys

def patch():
    with open("runtime/vm/validator.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Add INIT_VAR to Opcode class in validator.py
    if "INIT_VAR = 0x28" not in content:
        content = content.replace("CREATE_CLOSURE = 0x27", "CREATE_CLOSURE = 0x27\n    INIT_VAR = 0x28")
        
    # Remove duplicate INIT_VAR in the validator list
    content = content.replace("Opcode.INIT_VAR, Opcode.INIT_VAR,", "Opcode.INIT_VAR,")
    
    with open("runtime/vm/validator.py", "w", encoding="utf-8") as f:
        f.write(content)

patch()
