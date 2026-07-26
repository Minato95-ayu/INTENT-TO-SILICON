class DiffEngine:
    def __init__(self):
        self.old_tree = None

    def diff(self, new_tree):
        if not self.old_tree:
            self.old_tree = new_tree
            return "FULL_RENDER"
            
        changes = self._compare_nodes(self.old_tree.root, new_tree.root)
        self.old_tree = new_tree
        return changes
        
    def _compare_nodes(self, old_node, new_node, path="root"):
        changes = []
        if old_node.type != new_node.type:
            changes.append({"type": "REPLACE", "path": path, "node": new_node})
            return changes
            
        if old_node.props != new_node.props:
            changes.append({"type": "UPDATE_PROPS", "path": path, "props": new_node.props})
            
        # Compare children (simple index-based for now)
        old_len = len(old_node.children)
        new_len = len(new_node.children)
        
        for i in range(min(old_len, new_len)):
            changes.extend(self._compare_nodes(old_node.children[i], new_node.children[i], f"{path}.{i}"))
            
        if new_len > old_len:
            for i in range(old_len, new_len):
                changes.append({"type": "ADD_CHILD", "path": path, "node": new_node.children[i]})
        elif old_len > new_len:
            for i in range(new_len, old_len):
                changes.append({"type": "REMOVE_CHILD", "path": f"{path}.{i}"})
                
        return changes
