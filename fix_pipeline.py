# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

with open('compiler/ir/pipeline.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_while = '''        elif type(hir).__name__ == "HIRWhile":
            import uuid
            uid = uuid.uuid4().hex[:8]
            start_label = f"while_start_{uid}"
            end_label = f"while_end_{uid}"
            
            mir_list.append(MIRInstruction("LABEL", [start_label]))
            self._hir_to_mir(hir.condition, mir_list)
            mir_list.append(MIRInstruction("JUMP_IF_FALSE", [end_label]))
            
            for stmt in hir.body:
                self._hir_to_mir(stmt, mir_list)
                if self._needs_pop(stmt):
                    mir_list.append(MIRInstruction("POP", []))
                    
            mir_list.append(MIRInstruction("JUMP", [start_label]))
            mir_list.append(MIRInstruction("LABEL", [end_label]))'''

new_while = '''        elif type(hir).__name__ == "HIRWhile":
            import uuid
            uid = uuid.uuid4().hex[:8]
            start_label = f"while_start_{uid}"
            end_label = f"while_end_{uid}"
            
            mir_list.append(MIRInstruction("LABEL", [start_label]))
            self._hir_to_mir(hir.condition, mir_list)
            mir_list.append(MIRInstruction("JUMP_IF_FALSE", [end_label]))
            
            mir_list.append(MIRInstruction("ENTER_SCOPE", []))
            for stmt in hir.body:
                self._hir_to_mir(stmt, mir_list)
                if self._needs_pop(stmt):
                    mir_list.append(MIRInstruction("POP", []))
            mir_list.append(MIRInstruction("EXIT_SCOPE", []))
                    
            mir_list.append(MIRInstruction("JUMP", [start_label]))
            mir_list.append(MIRInstruction("LABEL", [end_label]))'''

c = c.replace(old_while, new_while)

with open('compiler/ir/pipeline.py', 'w', encoding='utf-8') as f:
    f.write(c)
