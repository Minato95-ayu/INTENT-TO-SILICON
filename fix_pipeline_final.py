import sys

def patch():
    with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
        content = f.read()

    target = "lir_list.append(LIRNode(\"STATE_INIT\", [mir.operands[0]]))\n        elif mir.opcode == \"SET_STATE\":"
    
    new_target = "lir_list.append(LIRNode(\"STATE_INIT\", [mir.operands[0]]))\n        elif mir.opcode == \"INIT_VAR\":\n            lir_list.append(LIRNode(\"INIT_VAR\", [mir.operands[0]]))\n        elif mir.opcode == \"SET_STATE\":"

    if target in content:
        content = content.replace(target, new_target)
        with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
            f.write(content)
        print("Patched successfully!")
    else:
        print("Target not found!")

patch()
