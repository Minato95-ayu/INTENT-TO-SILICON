import sys

def patch():
    with open("compiler/bytecode/encoder.py", "r", encoding="utf-8") as f:
        content = f.read()

    # _encode_node
    if "elif opcode == \"INIT_VAR\":" not in content:
        old_encode = """        if opcode == "STATE_INIT":
            self._encode_state_init(node)"""
        new_encode = """        if opcode == "STATE_INIT":
            self._encode_state_init(node)
        elif opcode == "INIT_VAR":
            self._encode_init_var(node)"""
        content = content.replace(old_encode, new_encode)
        
    # _encode_init_var
    if "def _encode_init_var" not in content:
        old_fn = """    def _encode_state_init(self, node: LIRNode):"""
        new_fn = """    def _encode_init_var(self, node: LIRNode):
        name = node.operands[0]
        name_idx = self.pool.add(name)
        self._emit(Opcode.INIT_STATE, name_idx)

    def _encode_state_init(self, node: LIRNode):"""
        content = content.replace(old_fn, new_fn)

    with open("compiler/bytecode/encoder.py", "w", encoding="utf-8") as f:
        f.write(content)

patch()
