
path = "D:/intent-to-silicon-research/INTENT-TO-SILICON/compiler/ir/pipeline.py"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

old_code = """                if page_name == "App":
                    mir_list.append(MIRInstruction("MARK_PAGE_START", []))
                    mir_list.append(MIRInstruction("MARK_BLOCK_START", []))
                    for child in hir.children:
                        self._hir_to_mir(child, mir_list)
                    mir_list.append(MIRInstruction(f"INIT_{hir.w_type.upper()}", [hir.props]))
                else:"""

new_code = """                if page_name == "App":
                    body_mir = []
                    body_mir.append(MIRInstruction("MARK_BLOCK_START", []))
                    for child in hir.children:
                        self._hir_to_mir(child, body_mir)
                    body_mir.append(MIRInstruction(f"INIT_{hir.w_type.upper()}", [hir.props]))
                    mir_list.append(MIRInstruction("ACTION_DECL", ["__PAGE_START__", body_mir]))
                else:"""

if old_code in c:
    c = c.replace(old_code, new_code)
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Successfully patched pipeline.py for page App")
else:
    print("Could not find old code in pipeline.py")

