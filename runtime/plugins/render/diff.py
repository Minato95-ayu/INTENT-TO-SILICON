from typing import Dict, List, Any
from .commands import RenderCommand, CMD_CREATE, CMD_REMOVE, CMD_UPDATE_PROPS

class DiffEngine:
    """
    O(N) Diff Engine.
    Compares two logical UI trees using Hash Maps of node IDs.
    Yields minimal Atomic Render Commands.
    """
    def __init__(self):
        pass
        
    def _flatten_tree(self, node, node_map: Dict[str, Any]):
        if not node: return
        
        node_map[node.id] = {
            "type": node.__class__.__name__,
            "props": dict(node.props),
            "parent_id": node.parent.id if node.parent else None,
            "children_ids": [c.id for c in node.children]
        }
        for child in node.children:
            self._flatten_tree(child, node_map)

    def compute(self, old_tree, new_tree) -> List[RenderCommand]:
        commands = []
        
        old_map = {}
        new_map = {}
        
        self._flatten_tree(old_tree, old_map)
        self._flatten_tree(new_tree, new_map)
        
        # Detect Deletes
        for node_id in old_map:
            if node_id not in new_map:
                commands.append(RenderCommand(CMD_REMOVE, node_id))
                
        # Detect Creates and Updates
        for node_id, new_node in new_map.items():
            if node_id not in old_map:
                commands.append(RenderCommand(CMD_CREATE, node_id, payload={
                    "type": new_node["type"],
                    "props": new_node["props"],
                    "parent_id": new_node["parent_id"]
                }))
            else:
                old_node = old_map[node_id]
                # Shallow compare props
                if old_node["props"] != new_node["props"]:
                    commands.append(RenderCommand(CMD_UPDATE_PROPS, node_id, payload={"props": new_node["props"]}))
                    
        return commands
