import tkinter as tk
from typing import List, Tuple
from aayu.runtime.renderers.base import RendererInterface
from aayu.runtime.ui.display_list import DisplayList, DrawRect, DrawText, RegisterClickArea, DrawRoundedRect, DrawImage, DrawIcon
from aayu.runtime.events.queue import EventQueue, MouseClick

class TkinterRenderer(RendererInterface):
    def __init__(self, event_queue: EventQueue):
        super().__init__(event_queue)
        self.root = None
        self.canvas = None
        self.click_areas: List[Tuple[float, float, float, float, str]] = []
        
    def initialize(self):
        self.root = tk.Tk()
        self.root.title("AAYU Rendering Engine")
        self.root.geometry("800x600")
        
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        self.canvas.bind("<Button-1>", self._on_click)
        
        # We need a custom main loop or we use update()
        # For our architecture, we control the loop from the outside.
        
    def render(self, display_list: DisplayList):
        if not self.canvas:
            return
            
        self.canvas.delete("all")
        self.click_areas.clear()
        
        for cmd in display_list.commands:
            if isinstance(cmd, DrawRect):
                self.canvas.create_rectangle(
                    cmd.x, cmd.y, cmd.x + cmd.width, cmd.y + cmd.height,
                    fill=cmd.color, outline=""
                )
            elif isinstance(cmd, DrawRoundedRect):
                # Tkinter doesn't have native rounded rects on Canvas easily without polygons.
                # Approximate with a normal rectangle for v1, or draw overlapping shapes.
                self.canvas.create_rectangle(
                    cmd.x, cmd.y, cmd.x + cmd.width, cmd.y + cmd.height,
                    fill=cmd.color, outline=""
                )
            elif isinstance(cmd, DrawText):
                font = (cmd.font_family, cmd.font_size, "bold" if cmd.bold else "normal")
                self.canvas.create_text(
                    cmd.x, cmd.y, text=cmd.text, font=font, fill=cmd.color, anchor=tk.NW
                )
            elif isinstance(cmd, RegisterClickArea):
                self.click_areas.append((cmd.x, cmd.y, cmd.width, cmd.height, cmd.action_name))
                
    def _on_click(self, event):
        x, y = event.x, event.y
        # Push raw click event
        self.event_queue.push(MouseClick(x, y, 1))
        
        # Also resolve click areas for the VM
        # Wait, the VM shouldn't resolve click areas if we want true decoupling.
        # But for V1, we can pass a synthetic ActionEvent or let the renderer trigger the action.
        # Actually, let's just trigger the action via a generic ActionEvent in the queue.
        # But wait, we don't have ActionEvent in our Event list.
        # Let's just push it to the queue as a custom event, or maybe the VM listens to MouseClick 
        # and checking the HitTest itself?
        # The DisplayList was built by LayoutEngine, so Renderer has the ClickAreas.
        # Let's push a custom attribute to MouseClick for V1, or just let Renderer handle hit testing.
        
        for cx, cy, cw, ch, action in reversed(self.click_areas):
            if cx <= x <= cx + cw and cy <= y <= cy + ch:
                from aayu.runtime.events.queue import ActionEvent
                self.event_queue.push(ActionEvent(action))
                break
                
    def process_events(self):
        if self.root:
            self.root.update_idletasks()
            self.root.update()
            
    def present(self):
        # In Tkinter, update() does the present
        if self.root:
            self.root.update()
            
    def shutdown(self):
        if self.root:
            self.root.destroy()
            self.root = None
