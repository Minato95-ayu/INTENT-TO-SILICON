with open('runtime/vm/vm.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_call = '''    def call_action_by_name(self, action_name: str):
        if action_name in self.action_addresses:
            target_ip = self.action_addresses[action_name]
            # Save current IP if we were executing?'''

new_call = '''    def call_action_by_name(self, action_name: str):
        if action_name in self.action_addresses:
            target_ip = self.action_addresses[action_name]
            
            if action_name == "__PAGE_START__":
                self.interpreter.node_stack.clear()
                
            # Save current IP if we were executing?'''

content = content.replace(old_call, new_call)

with open('runtime/vm/vm.py', 'w', encoding='utf-8') as f:
    f.write(content)
