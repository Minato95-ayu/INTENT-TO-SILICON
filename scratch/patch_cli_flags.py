with open('tools/commands/run.py', 'r', encoding='utf-8') as f:
    content = f.read()

import_str = "from aayu.runtime.renderers.tkinter_renderer import TkinterRenderer\n"
if "TkinterRenderer" not in content:
    content = import_str + content

# Patch argument parsing
old_args = '''def handle(args):
    target = args[0] if len(args) > 0 else "main.aayu"
    if not os.path.exists(target):'''

new_args = '''def handle(args):
    renderer_type = "tk"
    target = "main.aayu"
    
    for arg in args:
        if arg == "--console":
            renderer_type = "console"
        elif arg.startswith("--renderer="):
            renderer_type = arg.split("=")[1]
        elif not arg.startswith("-"):
            target = arg

    if not os.path.exists(target):'''

content = content.replace(old_args, new_args)

# Patch renderer selection
old_render = '''        renderer = ConsoleRenderer()
        renderer.render(vm.interpreter.render_tree)
        
        print("[AAYU] Execution completed successfully.")'''

new_render = '''        
        if renderer_type == "console":
            renderer = ConsoleRenderer()
            renderer.render(vm.interpreter.render_tree)
            renderer.start_event_loop()
        else:
            renderer = TkinterRenderer()
            renderer.render(vm.interpreter.render_tree)
            renderer.start_event_loop()
            
        print("[AAYU] Execution completed successfully.")'''

content = content.replace(old_render, new_render)

with open('tools/commands/run.py', 'w', encoding='utf-8') as f:
    f.write(content)
