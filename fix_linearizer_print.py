import re
with open("compiler/ir/linearizer.py", "r") as f:
    content = f.read()

replacement = """                elif inst.opcode == "NEXT_ITEM":
                    push_value(inst.operands[0])
                    mir_list.append(MIRInstruction("NEXT_ITEM", []))
                    pop_to_value(inst.result)
                    
                elif inst.opcode == "PRINT":
                    push_value(inst.operands[0])
                    mir_list.append(MIRInstruction("OP_ASYNC_CALL", ["print", 1]))"""

content = re.sub(r'                elif inst\.opcode == "NEXT_ITEM":\n.*?pop_to_value\(inst\.result\)', replacement, content, flags=re.DOTALL)
with open("compiler/ir/linearizer.py", "w") as f:
    f.write(content)
