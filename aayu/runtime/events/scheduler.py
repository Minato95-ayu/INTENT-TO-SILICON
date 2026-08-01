import time
from typing import Callable

class FrameScheduler:
    """
    Manages frame rendering frequency to hit ~60 FPS.
    Groups multiple state changes/events into a single render pass.
    """
    def __init__(self, fps: int = 60):
        self.fps = fps
        self.frame_time = 1.0 / fps
        self.last_frame_time = time.time()
        self._frame_callbacks = []
        self._dirty = False
        
    def request_frame(self, callback: Callable):
        """Request a callback to run on the next frame."""
        self._frame_callbacks.append(callback)
        
    def schedule_render(self):
        """Mark the frame as dirty, requiring a render pass."""
        self._dirty = True
        
    def tick(self, render_func: Callable):
        """
        Called in the main event loop. Triggers a render pass if dirty
        and the frame time has elapsed.
        """
        current_time = time.time()
        elapsed = current_time - self.last_frame_time
        
        if elapsed >= self.frame_time:
            # Execute scheduled callbacks (like animations)
            callbacks = self._frame_callbacks
            self._frame_callbacks = []
            for cb in callbacks:
                cb()
                
            # Render if dirty
            if self._dirty:
                render_func()
                self._dirty = False
                
            self.last_frame_time = current_time
        else:
            # Sleep remainder of frame time to avoid burning CPU
            time.sleep(max(0, self.frame_time - elapsed))
