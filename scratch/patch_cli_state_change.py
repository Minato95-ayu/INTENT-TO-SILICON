with open('tools/commands/run.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_render = '''        dispatcher = EventDispatcher(vm)
        if renderer_type == "console":
            renderer = ConsoleRenderer(dispatcher=dispatcher)
            renderer.render(vm.interpreter.render_tree)
            renderer.start_event_loop()
        else:
            renderer = TkinterRenderer(dispatcher=dispatcher)
            renderer.render(vm.interpreter.render_tree)
            renderer.start_event_loop()'''

new_render = '''        dispatcher = EventDispatcher(vm)
        if renderer_type == "console":
            renderer = ConsoleRenderer(dispatcher=dispatcher)
            
            def re_render_console():
                vm.call_action_by_name("__PAGE_START__")
                renderer.render(vm.interpreter.render_tree)
                
            dispatcher.on_state_changed = re_render_console
            renderer.render(vm.interpreter.render_tree)
            renderer.start_event_loop()
        else:
            renderer = TkinterRenderer(dispatcher=dispatcher)
            
            def re_render_tk():
                # Re-run page generation
                vm.call_action_by_name("__PAGE_START__")
                # Update UI
                renderer.render(vm.interpreter.render_tree)
                
            dispatcher.on_state_changed = re_render_tk
            renderer.render(vm.interpreter.render_tree)
            renderer.start_event_loop()'''

content = content.replace(old_render, new_render)

with open('tools/commands/run.py', 'w', encoding='utf-8') as f:
    f.write(content)
