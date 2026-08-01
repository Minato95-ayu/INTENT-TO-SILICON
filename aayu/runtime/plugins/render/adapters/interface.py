from typing import List
from ..commands import RenderCommand

class NativeAdapter:
    """Base interface for Platform Render Adapters."""
    def initialize(self):
        pass
        
    def render_batch(self, commands: List[RenderCommand]):
        raise NotImplementedError("Adapters must implement render_batch")
        
    def shutdown(self):
        pass
