import sys

def patch():
    with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Import
    if "HIRLetDecl," not in content:
        content = content.replace("HIRStateDecl,", "HIRStateDecl, HIRLetDecl,")
        
    # _hir_to_mir
    if "elif isinstance(hir, HIRLetDecl):" not in content:
        old_mir = """        if isinstance(hir, HIRStateDecl):
            self._hir_to_mir(hir.value, mir_list)
            mir_list.append(MIRInstruction("INIT_STATE", [hir.name]))"""
        new_mir = """        if isinstance(hir, HIRStateDecl):
            self._hir_to_mir(hir.value, mir_list)
            mir_list.append(MIRInstruction("INIT_STATE", [hir.name]))
        elif isinstance(hir, HIRLetDecl):
            self._hir_to_mir(hir.value, mir_list)
            mir_list.append(MIRInstruction("INIT_VAR", [hir.name]))"""
        content = content.replace(old_mir, new_mir)

    # _mir_to_lir
    if "elif mir.opcode == \"INIT_VAR\":" not in content:
        old_lir = """        if mir.opcode == "INIT_STATE":
            # INIT_STATE [name] -> STATE_INIT [name]
            lir_list.append(LIRNode("STATE_INIT", [mir.operands[0]]))"""
        new_lir = """        if mir.opcode == "INIT_STATE":
            # INIT_STATE [name] -> STATE_INIT [name]
            lir_list.append(LIRNode("STATE_INIT", [mir.operands[0]]))
        elif mir.opcode == "INIT_VAR":
            lir_list.append(LIRNode("INIT_VAR", [mir.operands[0]]))"""
        content = content.replace(old_lir, new_lir)

    with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
        f.write(content)

patch()
