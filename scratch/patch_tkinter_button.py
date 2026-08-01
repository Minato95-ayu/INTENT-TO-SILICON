with open('runtime/renderers/tkinter_renderer.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_button = '''    def _render_button(self, node: RenderNode, parent_widget: tk.Widget) -> tk.Widget:
        text_val = str(node.props.get("value", "Button"))
        btn = ttk.Button(parent_widget, text=text_val)
        btn.pack(anchor=tk.W, pady=5)
        return btn'''

new_button = '''    def _render_button(self, node: RenderNode, parent_widget: tk.Widget) -> tk.Widget:
        text_val = str(node.props.get("value", "Button"))
        
        def on_click():
            action_name = node.props.get("onClick")
            if action_name and self.dispatcher:
                self.dispatcher.dispatch(action_name)
                # Re-render the tree after dispatch because state might have changed!
                # Wait, we need a diff engine or just re-render root?
                # For now, just re-render root:
                # Actually, wait, re-rendering entirely might lose focus. We will implement diff engine next.
                # For now, let's call re-render.
                # Wait, re-render creates a new RenderTree? No, VM needs to regenerate the RenderTree!
                # Ah! VM needs to be re-executed from PAGE start to generate a NEW RenderTree!
                # Wait, we'll handle re-rendering in the dispatcher.
                
        btn = ttk.Button(parent_widget, text=text_val, command=on_click)
        btn.pack(anchor=tk.W, pady=5)
        return btn'''

content = content.replace(old_button, new_button)

with open('runtime/renderers/tkinter_renderer.py', 'w', encoding='utf-8') as f:
    f.write(content)
