with open('compiler/ir/pipeline.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''            if hir.w_type.lower() == "text" and hir.children:
                for child in hir.children:
                    if isinstance(child, HIRLoadVar):
                        mir_list.append(MIRInstruction("LOAD_VAR", [child.name]))
                        mir_list.append(MIRInstruction("PRINT_STACK", []))
                    else:
                        self._hir_to_mir(child, mir_list)
                return'''

new_code = '''            if hir.w_type.lower() == "text" and hir.children:
                for child in hir.children:
                    if isinstance(child, HIRLoadVar):
                        mir_list.append(MIRInstruction("LOAD_VAR", [child.name]))
                        mir_list.append(MIRInstruction("INIT_TEXT", []))
                    else:
                        self._hir_to_mir(child, mir_list)
                return'''

content = content.replace(old_code, new_code)

with open('compiler/ir/pipeline.py', 'w', encoding='utf-8') as f:
    f.write(content)
