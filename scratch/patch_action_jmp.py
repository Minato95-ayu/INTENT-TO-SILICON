with open('compiler/bytecode/encoder.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_action = '''    def _encode_action_decl(self, node: LIRNode):
        \"\"\"ACTION_DECL [name, body_lir_nodes]
        Actions are stored and called via CALL.
        For RC1, we record the address for later CALL resolution.
        \"\"\"
        action_name = node.operands[0]
        self._action_addresses[action_name] = len(self.bytecode)

        # Encode body statements
        if len(node.operands) > 1:
            body_nodes = node.operands[1]
            if isinstance(body_nodes, list):
                for sub_node in body_nodes:
                    if isinstance(sub_node, LIRNode):
                        self._encode_node(sub_node)

        # Return from action
        self._emit(Opcode.RET, 0)'''

new_action = '''    def _encode_action_decl(self, node: LIRNode):
        action_name = node.operands[0]
        
        # Jump over the action body so it doesn't execute inline
        self._emit(Opcode.JMP, 0xFFFF)
        jmp_addr = len(self.bytecode) - 2 # The operand offset

        self._action_addresses[action_name] = len(self.bytecode)

        # Encode body statements
        if len(node.operands) > 1:
            body_nodes = node.operands[1]
            if isinstance(body_nodes, list):
                for sub_node in body_nodes:
                    if isinstance(sub_node, LIRNode):
                        self._encode_node(sub_node)

        # Return from action
        self._emit(Opcode.RET, 0)
        
        # Patch the JMP operand
        end_addr = len(self.bytecode)
        self.bytecode[jmp_addr] = (end_addr >> 8) & 0xFF
        self.bytecode[jmp_addr + 1] = end_addr & 0xFF'''

content = content.replace(old_action, new_action)

with open('compiler/bytecode/encoder.py', 'w', encoding='utf-8') as f:
    f.write(content)
