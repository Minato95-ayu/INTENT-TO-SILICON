with open('runtime/vm/vm.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_load = '''    def load(self, bytecode, constant_pool=None):
        self.constant_pool = constant_pool or []
        Validator.validate(bytecode, self.constant_pool)
        self.decoder = Decoder(bytecode, self.constant_pool)
        self.registers.reset()'''

new_load = '''    def load(self, bytecode, constant_pool=None, action_addresses=None):
        self.constant_pool = constant_pool or []
        self.action_addresses = action_addresses or {}
        Validator.validate(bytecode, self.constant_pool)
        self.decoder = Decoder(bytecode, self.constant_pool)
        self.registers.reset()
        
    def call_action_by_name(self, action_name: str):
        if action_name in self.action_addresses:
            target_ip = self.action_addresses[action_name]
            # Save current IP if we were executing?
            # Actually, GUI event runs independently. Let's just push current IP to call_stack and run interpreter?
            # Wait, the interpreter loop is likely HALTED!
            # So we just set IP to target, and call self.interpreter.run()
            # But wait, Interpreter might need to stop when it hits RET if the call stack is empty!
            self.call_stack.push(self.registers.ip)
            self.registers.ip = target_ip
            self.execute()
        else:
            print(f"[VM] Error: Action '{action_name}' not found.")'''

content = content.replace(old_load, new_load)

with open('runtime/vm/vm.py', 'w', encoding='utf-8') as f:
    f.write(content)
