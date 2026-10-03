    def op_INIT_STATE(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        name = self.vm.constant_pool[idx]
        val = self.vm.value_stack.pop()
        if not self.vm.state_scopes:
            from runtime.vm.exceptions import KernelError
            raise KernelError(f"state_scopes is empty at IP {self.vm.registers.ip - 3}")
        current_scope = self.vm.state_scopes[-1]
        
        if name in ["type", "node", "child_type"]:
            print(f"[DEBUG INIT_STATE] Setting {name} to: {val} in scope id {id(current_scope)}")
            
        current_scope[name] = val
        return True

    def op_LOAD_STATE(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        name = self.vm.constant_pool[idx]
        val = None
        found = False
        for scope in reversed(self.vm.state_scopes):
            if name in scope:
                val = scope[name]
                if name in ["type", "node", "child_type"]:
                    print(f"[DEBUG LOAD_STATE] Found {name} = {val} in scope id {id(scope)}")
                found = True
                break
        if not found:
            if hasattr(self.vm, 'action_addresses') and name in self.vm.action_addresses:
                val = name
            else:
                val = None
            if name in ["type", "node", "child_type"]:
                print(f"[DEBUG LOAD_STATE] {name} NOT FOUND, defaulting to {val}")
        self.vm.value_stack.push(val)
        return True
