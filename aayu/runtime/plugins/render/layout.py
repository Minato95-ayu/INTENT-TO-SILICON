from typing import Dict, Any

class LayoutEngine:
    """
    Deterministic layout calculator.
    Computes X/Y and Width/Height without CSS complexity.
    """
    def __init__(self):
        pass
        
    def compute(self, node, current_x: int = 0, current_y: int = 0) -> Dict[str, Dict[str, int]]:
        """
        Returns a map of node_id -> {x, y, width, height}
        """
        boxes = {}
        
        node_type = node.__class__.__name__
        layout_type = node.props.get("type", "Column")
        padding = node.props.get("padding", 0)
        
        # Calculate for children first to determine parent size if it's dynamic
        child_boxes = {}
        cx = current_x + padding
        cy = current_y + padding
        
        max_child_w = 0
        max_child_h = 0
        
        for child in node.children:
            cw = child.props.get("width", 0)
            ch = child.props.get("height", 0)
            
            c_boxes = self.compute(child, cx, cy)
            child_boxes.update(c_boxes)
            
            # Use calculated dimensions if child was a container itself
            if child.id in c_boxes:
                cw = c_boxes[child.id]["width"]
                ch = c_boxes[child.id]["height"]
                
            if layout_type == "Row":
                cx += cw
                max_child_h = max(max_child_h, ch)
            elif layout_type == "Column":
                cy += ch
                max_child_w = max(max_child_w, cw)
            elif layout_type == "Stack":
                max_child_w = max(max_child_w, cw)
                max_child_h = max(max_child_h, ch)
                
        boxes.update(child_boxes)
        
        # Calculate self size
        my_w = node.props.get("width")
        my_h = node.props.get("height")
        
        if my_w is None:
            if layout_type == "Row":
                my_w = (cx - current_x) + padding
            else:
                my_w = max_child_w + (padding * 2)
                
        if my_h is None:
            if layout_type == "Column":
                my_h = (cy - current_y) + padding
            else:
                my_h = max_child_h + (padding * 2)
                
        boxes[node.id] = {
            "x": current_x,
            "y": current_y,
            "width": my_w,
            "height": my_h
        }
        
        return boxes
