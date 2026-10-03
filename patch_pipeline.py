import re

with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Change signature
content = content.replace("def _hir_to_mir(self, hir, mir_list: list):", "def _hir_to_mir(self, hir, mir_list: list, is_expr: bool = False):")

# 2. Add POP for action calls
call_action_target = """        elif isinstance(hir, HIRActionCall):
            for arg in hir.args:
                self._hir_to_mir(arg, mir_list)
            # IMPORTANT ROUTING LOGIC:
            # If the function name has '.' (method) or '::' (namespace), OR it is in our built-in list,
            # we compile it to OP_ASYNC_CALL which triggers native Python execution.
            # Otherwise, we assume it is a user-defined AAYU action and compile it to CALL_ACTION.
            if "." in hir.name or "::" in hir.name or hir.name in ["print", "type", "float", "int", "input", "core::input", "typeof"]:
                mir_list.append(MIRInstruction("OP_ASYNC_CALL", [hir.name, len(hir.args)]))
            else:
                mir_list.append(MIRInstruction("CALL_ACTION", [hir.name, len(hir.args)]))"""

call_action_replacement = """        elif isinstance(hir, HIRActionCall):
            for arg in hir.args:
                self._hir_to_mir(arg, mir_list, is_expr=True)
            # IMPORTANT ROUTING LOGIC:
            # If the function name has '.' (method) or '::' (namespace), OR it is in our built-in list,
            # we compile it to OP_ASYNC_CALL which triggers native Python execution.
            # Otherwise, we assume it is a user-defined AAYU action and compile it to CALL_ACTION.
            if "." in hir.name or "::" in hir.name or hir.name in ["print", "type", "float", "int", "input", "core::input", "typeof"]:
                mir_list.append(MIRInstruction("OP_ASYNC_CALL", [hir.name, len(hir.args)]))
            else:
                mir_list.append(MIRInstruction("CALL_ACTION", [hir.name, len(hir.args)]))
            if not is_expr:
                mir_list.append(MIRInstruction("POP", []))"""

content = content.replace(call_action_target, call_action_replacement)

# 3. Replace _hir_to_mir calls that evaluate expressions
content = content.replace("self._hir_to_mir(hir.value, mir_list)", "self._hir_to_mir(hir.value, mir_list, is_expr=True)")
content = content.replace("self._hir_to_mir(hir.left, mir_list)", "self._hir_to_mir(hir.left, mir_list, is_expr=True)")
content = content.replace("self._hir_to_mir(hir.right, mir_list)", "self._hir_to_mir(hir.right, mir_list, is_expr=True)")
content = content.replace("self._hir_to_mir(hir.condition, mir_list)", "self._hir_to_mir(hir.condition, mir_list, is_expr=True)")
content = content.replace("self._hir_to_mir(hir.iterable, mir_list)", "self._hir_to_mir(hir.iterable, mir_list, is_expr=True)")
content = content.replace("self._hir_to_mir(elem, mir_list)", "self._hir_to_mir(elem, mir_list, is_expr=True)")
content = content.replace("self._hir_to_mir(v, mir_list)", "self._hir_to_mir(v, mir_list, is_expr=True)")

# 4. Patch ACTION_DECL in _mir_to_lir
action_decl_target = """            body_lir.append(LIRNode("RET", []))
            args = mir.operands[2] if len(mir.operands) > 2 else []
            lir_list.append(LIRNode("ACTION_DECL", [mir.operands[0], body_lir, args]))"""

action_decl_replacement = """            body_lir.append(LIRNode("PUSH_CONST", [None]))
            body_lir.append(LIRNode("RETURN_VALUE", []))
            args = mir.operands[2] if len(mir.operands) > 2 else []
            lir_list.append(LIRNode("ACTION_DECL", [mir.operands[0], body_lir, args]))"""

content = content.replace(action_decl_target, action_decl_replacement)

with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Pipeline patched successfully!")
