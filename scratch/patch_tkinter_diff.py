with open('runtime/renderers/tkinter_renderer.py', 'r', encoding='utf-8') as f:
    content = f.read()

import_diff = "from aayu.runtime.ui.diff import DiffEngine\n"
if "DiffEngine" not in content:
    content = import_diff + content

old_init = '''    def __init__(self, dispatcher=None):
        self.dispatcher = dispatcher
        self.root = None
        self.registry = WidgetRegistry()'''

new_init = '''    def __init__(self, dispatcher=None):
        self.dispatcher = dispatcher
        self.root = None
        self.registry = WidgetRegistry()
        self.diff_engine = DiffEngine()
        self.widget_map = {} # path -> tk.Widget'''

content = content.replace(old_init, new_init)

old_render = '''    def render(self, tree: RenderTree):
        self.init_window()
        
        # Clear existing widgets if re-rendering entirely
        for widget in self.root.winfo_children():
            widget.destroy()
            
        if tree and tree.root:
            self._build_widget(tree.root, self.root)'''

new_render = '''    def render(self, tree: RenderTree):
        self.init_window()
        
        changes = self.diff_engine.diff(tree)
        
        if changes == "FULL_RENDER":
            for widget in self.root.winfo_children():
                widget.destroy()
            self.widget_map.clear()
            if tree and tree.root:
                self._build_widget(tree.root, self.root, path="root")
        else:
            self._apply_diff(changes)
            
    def _apply_diff(self, changes):
        for change in changes:
            if change["type"] == "UPDATE_PROPS":
                widget = self.widget_map.get(change["path"])
                if widget and "value" in change["props"]:
                    if isinstance(widget, ttk.Label) or isinstance(widget, ttk.Button):
                        widget.config(text=str(change["props"]["value"]))'''

content = content.replace(old_render, new_render)

old_build = '''    def _build_widget(self, node: RenderNode, parent: tk.Widget):
        widget = None
        if node.type == "Page":
            widget = self._render_page(node, parent)
        elif node.type == "Text":
            widget = self._render_text(node, parent)
        elif node.type == "Button":
            widget = self._render_button(node, parent)
        elif node.type == "Column":
            widget = self._render_column(node, parent)
            
        if widget:
            for child in node.children:
                self._build_widget(child, widget)'''

new_build = '''    def _build_widget(self, node: RenderNode, parent: tk.Widget, path: str):
        widget = None
        if node.type == "Page":
            widget = self._render_page(node, parent)
        elif node.type == "Text":
            widget = self._render_text(node, parent)
        elif node.type == "Button":
            widget = self._render_button(node, parent)
        elif node.type == "Column":
            widget = self._render_column(node, parent)
            
        if widget:
            self.widget_map[path] = widget
            for i, child in enumerate(node.children):
                self._build_widget(child, widget, f"{path}.{i}")'''

content = content.replace(old_build, new_build)

with open('runtime/renderers/tkinter_renderer.py', 'w', encoding='utf-8') as f:
    f.write(content)
