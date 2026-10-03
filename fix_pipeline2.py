import sys

def patch():
    with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
        content = f.read()

    old_lir = """        if mir.opcode == "INIT_STATE":
            # INIT_STATE [name] -> STATE_INIT [name]
            lir_list.append(LIRNode("STATE_INIT", [mir.operands[0]]))
        elif mir.opcode == "SET_STATE":"""
    new_lir = """        if mir.opcode == "INIT_STATE":
            # INIT_STATE [name] -> STATE_INIT [name]
            lir_list.append(LIRNode("STATE_INIT", [mir.operands[0]]))
        elif mir.opcode == "INIT_VAR":
            lir_list.append(LIRNode("INIT_VAR", [mir.operands[0]]))
        elif mir.opcode == "SET_STATE":"""
        
    content = content.replace(old_lir, new_lir)

    with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
        f.write(content)

patch()
