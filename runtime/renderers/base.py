from typing import Optional
from runtime.ui.display_list import DisplayList
from runtime.events.queue import EventQueue

class RendererInterface:
    def __init__(self, event_queue: EventQueue):
        self.event_queue = event_queue
        
    def initialize(self):
        """Initialize the rendering context (e.g., window, canvas)"""
        pass
        
    def render(self, display_list: DisplayList):
        """Draw the display list to the screen"""
        pass
        
    def resize(self, width: float, height: float):
        """Handle resize events"""
        pass
        
    def process_events(self):
        """Poll and process OS events, pushing them to the EventQueue"""
        pass
        
    def present(self):
        """Swap buffers or update the screen"""
        pass
        
    def shutdown(self):
        """Clean up resources"""
        pass
