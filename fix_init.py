    def op_INIT_STATE(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        name = self.vm.constant_pool[idx]
        val = self.vm.value_stack.pop()
        if not self.vm.state_scopes:
            from runtime.vm.exceptions import KernelError
            raise KernelError(f"state_scopes is empty at IP {self.vm.registers.ip - 3}")
        current_scope = self.vm.state_scopes[-1]
        
        # DEBUG
        if name == "node":
            print(f"[DEBUG INIT_STATE] node. val is {type(val)}: {val}")
            
        current_scope[name] = val
        return True
