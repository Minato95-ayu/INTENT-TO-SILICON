from typing import List, Optional
from runtime.ui.render_tree import RenderNode

class RenderObject:
    """
    Represents a node in the layout tree that bridges layout math and painting.
    Caches intrinsic sizes and bounding boxes.
    """
    def __init__(self, render_node: RenderNode):
        self.render_node = render_node
        self.x: float = 0.0
        self.y: float = 0.0
        self.width: float = 0.0
        self.height: float = 0.0
        self.intrinsic_width: Optional[float] = None
        self.intrinsic_height: Optional[float] = None
        self.children: List['RenderObject'] = []
        
    def add_child(self, child: 'RenderObject'):
        self.children.append(child)
