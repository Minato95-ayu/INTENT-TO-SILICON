from runtime.renderers.base import RendererInterface
from runtime.ui.display_list import DisplayList
from runtime.events.queue import EventQueue

class ConsoleRenderer(RendererInterface):
    def __init__(self, event_queue: EventQueue):
        super().__init__(event_queue)
        
    def initialize(self):
        pass
        
    def render(self, display_list: DisplayList):
        print("=== Console Display List ===")
        for cmd in display_list.commands:
            print(f"- {cmd}")
        print("============================")
        
    def process_events(self):
        pass
        
    def present(self):
        pass
        
    def shutdown(self):
        pass
