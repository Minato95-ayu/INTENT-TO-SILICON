with open('tools/commands/run.py', 'r', encoding='utf-8') as f:
    content = f.read()

import_str = "from aayu.runtime.renderers.console import ConsoleRenderer\n"
if "ConsoleRenderer" not in content:
    content = import_str + content

old_run = '''        vm.execute()
        
        print("[AAYU] Execution completed successfully.")'''

new_run = '''        vm.execute()
        
        renderer = ConsoleRenderer()
        renderer.render(vm.interpreter.render_tree)
        
        print("[AAYU] Execution completed successfully.")'''

content = content.replace(old_run, new_run)

with open('tools/commands/run.py', 'w', encoding='utf-8') as f:
    f.write(content)
