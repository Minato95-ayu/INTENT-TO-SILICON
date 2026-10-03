import sys

def patch():
    # 1. Add INIT_VAR to opcodes.py
    with open("compiler/bytecode/instructions.py", "r", encoding="utf-8") as f:
        content = f.read()
    if "INIT_VAR = 0x28" not in content:
        content = content.replace("CREATE_CLOSURE = 0x27", "CREATE_CLOSURE = 0x27\n    INIT_VAR = 0x28")
    with open("compiler/bytecode/instructions.py", "w", encoding="utf-8") as f:
        f.write(content)

    # 2. Add to encoder.py
    with open("compiler/bytecode/encoder.py", "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("self._emit(Opcode.INIT_STATE, name_idx)", "self._emit(Opcode.INIT_VAR, name_idx)")
    with open("compiler/bytecode/encoder.py", "w", encoding="utf-8") as f:
        f.write(content)

    # 3. Add to interpreter.py
    with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
        content = f.read()
    if "def op_INIT_VAR" not in content:
        new_op = """    def op_INIT_VAR(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        name = self.vm.constant_pool[idx]
        val = self.vm.value_stack.pop()
        if not self.vm.state_scopes:
            from runtime.vm.exceptions import KernelError
            raise KernelError(f"state_scopes is empty at IP {self.vm.registers.ip - 3}")
        current_scope = self.vm.state_scopes[-1]
        current_scope[name] = val
        self.vm.value_stack.push(val)
        return True
"""
        content = content.replace("    def op_INIT_STATE(self, opcode):", new_op + "\n    def op_INIT_STATE(self, opcode):")
    with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
        f.write(content)
        
patch()
