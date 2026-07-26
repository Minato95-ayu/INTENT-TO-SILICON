from runtime.ui.render_tree import RenderTree

class RendererInterface:
    def render(self, tree: RenderTree):
        raise NotImplementedError("Renderer must implement render()")
        
    def init_window(self):
        pass
        
    def start_event_loop(self):
        pass
