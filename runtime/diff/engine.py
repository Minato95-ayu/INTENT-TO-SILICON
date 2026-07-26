from typing import Optional
from runtime.ui.render_tree import RenderNode, RenderTree

class DiffEngine:
    """
    V1 Diff Engine: Does a simple deep comparison of the old and new RenderTrees.
    Returns True if any changes occurred requiring a layout and paint phase.
    """
    def diff(self, old_tree: Optional[RenderTree], new_tree: RenderTree) -> bool:
        if not old_tree or not old_tree.root:
            return True
        if not new_tree or not new_tree.root:
            return True
            
        return self._diff_node(old_tree.root, new_tree.root)
        
    def _diff_node(self, old_node: RenderNode, new_node: RenderNode) -> bool:
        if old_node.type != new_node.type:
            return True
            
        # Optional: Key matching for strict list reconciliation (V2)
        if old_node.key != new_node.key:
            return True
            
        # Props comparison
        if old_node.props != new_node.props:
            return True
            
        # Style comparison
        if old_node.style != new_node.style:
            return True
            
        # Children comparison
        if len(old_node.children) != len(new_node.children):
            return True
            
        for old_child, new_child in zip(old_node.children, new_node.children):
            if self._diff_node(old_child, new_child):
                return True
                
        return False
