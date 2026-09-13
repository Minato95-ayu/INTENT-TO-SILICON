import re
with open("compiler/ir/linearizer.py", "r") as f:
    content = f.read()

replacement = """                elif inst.opcode == "NEXT_ITEM":
                    push_value(inst.operands[0])
                    mir_list.append(MIRInstruction("NEXT_ITEM", []))
                    pop_to_value(inst.result)
                    
                elif inst.opcode == "ACTION_DECL":
                    name = inst.operands[0]
                    action_cfg = inst.operands[1]
                    args = inst.operands[2]
                    # Recursively lower the action CFG
                    body_mir = Linearizer(action_cfg).lower()
                    mir_list.append(MIRInstruction("ACTION_DECL", [name, body_mir, args]))
"""

content = re.sub(r'                elif inst\.opcode == "NEXT_ITEM":\n.*?pop_to_value\(inst\.result\)', replacement, content, flags=re.DOTALL)
with open("compiler/ir/linearizer.py", "w") as f:
    f.write(content)
