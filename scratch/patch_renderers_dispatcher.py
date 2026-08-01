with open('runtime/renderers/console.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("class ConsoleRenderer(RendererInterface):", "class ConsoleRenderer(RendererInterface):\n    def __init__(self, dispatcher=None):\n        self.dispatcher = dispatcher")

with open('runtime/renderers/console.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('runtime/renderers/tkinter_renderer.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("    def __init__(self):", "    def __init__(self, dispatcher=None):\n        self.dispatcher = dispatcher")

with open('runtime/renderers/tkinter_renderer.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('tools/commands/run.py', 'r', encoding='utf-8') as f:
    content = f.read()

import_dispatcher = "from aayu.runtime.ui.events import EventDispatcher\n"
if "EventDispatcher" not in content:
    content = import_dispatcher + content

old_render = '''        if renderer_type == "console":
            renderer = ConsoleRenderer()
            renderer.render(vm.interpreter.render_tree)
            renderer.start_event_loop()
        else:
            renderer = TkinterRenderer()
            renderer.render(vm.interpreter.render_tree)
            renderer.start_event_loop()'''

new_render = '''        dispatcher = EventDispatcher(vm)
        if renderer_type == "console":
            renderer = ConsoleRenderer(dispatcher=dispatcher)
            renderer.render(vm.interpreter.render_tree)
            renderer.start_event_loop()
        else:
            renderer = TkinterRenderer(dispatcher=dispatcher)
            renderer.render(vm.interpreter.render_tree)
            renderer.start_event_loop()'''

content = content.replace(old_render, new_render)

with open('tools/commands/run.py', 'w', encoding='utf-8') as f:
    f.write(content)
