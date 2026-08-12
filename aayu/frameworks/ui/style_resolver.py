from aayu.runtime.ui.render_tree import RenderNode
from typing import Dict, Any

class StyleResolver:
    """
    Resolves inherited styles (e.g. font family, text color) across the RenderTree.
    """
    def resolve(self, root: RenderNode):
        self._traverse(root, {})
        
    def _traverse(self, node: RenderNode, parent_styles: Dict[str, Any]):
        # Combine parent styles with current node's styles
        # Node's explicit styles override inherited ones
        resolved_styles = dict(parent_styles)
        resolved_styles.update(node.style)
        
        # We only want to inherit certain properties (e.g., color, font-family)
        inheritable = {}
        if "color" in resolved_styles:
            inheritable["color"] = resolved_styles["color"]
        if "fontFamily" in resolved_styles:
            inheritable["fontFamily"] = resolved_styles["fontFamily"]
            
        # Update node's resolved style (V1: we just mutate the node's style dict)
        # Note: in a pure immutable tree, we'd return a new node here.
        node.style = resolved_styles
        
        for child in node.children:
            self._traverse(child, inheritable)
