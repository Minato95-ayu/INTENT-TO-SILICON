with open('compiler/ir/pipeline.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''            # First recursively process children
            for child in hir.children:'''

new_code = '''            if hir.w_type.lower() == "page":
                mir_list.append(MIRInstruction("MARK_PAGE_START", []))
            # First recursively process children
            for child in hir.children:'''

content = content.replace(old_code, new_code)

old_lir = '''        elif mir.opcode.startswith("INIT_"):
            # INIT_TEXT, INIT_BUTTON, etc. ? BUILD_*'''

new_lir = '''        elif mir.opcode == "MARK_PAGE_START":
            lir_list.append(LIRNode("MARK_PAGE_START", []))
        elif mir.opcode.startswith("INIT_"):
            # INIT_TEXT, INIT_BUTTON, etc. ? BUILD_*'''

content = content.replace(old_lir, new_lir)

with open('compiler/ir/pipeline.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('compiler/bytecode/encoder.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_enc = '''    def _encode_node(self, node: LIRNode):
        \"\"\"Dispatch a single LIR node to the appropriate encoder.\"\"\"
        opcode = node.opcode'''

new_enc = '''    def _encode_node(self, node: LIRNode):
        \"\"\"Dispatch a single LIR node to the appropriate encoder.\"\"\"
        opcode = node.opcode
        
        if opcode == "MARK_PAGE_START":
            self._action_addresses["__PAGE_START__"] = len(self.bytecode)
            return'''

content = content.replace(old_enc, new_enc)

with open('compiler/bytecode/encoder.py', 'w', encoding='utf-8') as f:
    f.write(content)
