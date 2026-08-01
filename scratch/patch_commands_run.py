with open('tools/commands/run.py', 'r', encoding='utf-8') as f:
    content = f.read()

import_str = "from aayu.runtime.renderers.console import ConsoleRenderer\n"
if "ConsoleRenderer" not in content:
    content = import_str + content

old_run = '''        vm.run()
        print("[AAYU] Execution completed successfully.")'''

new_run = '''        vm.run()
        
        # Render the UI tree using Console Renderer
        renderer = ConsoleRenderer()
        renderer.render(vm.interpreter.render_tree)
        
        print("[AAYU] Execution completed successfully.")'''

content = content.replace(old_run, new_run)

with open('tools/commands/run.py', 'w', encoding='utf-8') as f:
    f.write(content)
