with open('runtime/renderers/console.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_loop = '''    def start_event_loop(self):
        print("=== Simulating Click on 'Increment' ===")
        if self.dispatcher:
            self.dispatcher.dispatch("Increment")'''

new_loop = '''    def start_event_loop(self):
        pass'''

content = content.replace(old_loop, new_loop)

with open('runtime/renderers/console.py', 'w', encoding='utf-8') as f:
    f.write(content)
