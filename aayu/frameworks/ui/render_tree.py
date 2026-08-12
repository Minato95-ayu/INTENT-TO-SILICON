from typing import Dict, List, Any, Optional

import uuid

class RenderNode:
    def __init__(self, node_type: str, node_id: Optional[str] = None, props: Optional[Dict[str, Any]] = None, style: Optional[Dict[str, Any]] = None, bindings: Optional[Dict[str, Any]] = None, layout_hints: Optional[Dict[str, Any]] = None, key: Optional[str] = None, parent_id: Optional[str] = None):
        self.id = node_id or str(uuid.uuid4())
        self.type = node_type
        self.props = props or {}
        self.style = style or {}
        self.stateBinding = bindings or {}
        self.layoutHints = layout_hints or {}
        self.key = key or self.props.get("key")
        self.parent_id = parent_id
        self.children: List['RenderNode'] = []
    
    def add_child(self, child: 'RenderNode'):
        child.parent_id = self.id
        self.children.append(child)
        
    def clone(self) -> 'RenderNode':
        """Deep clone for immutability during diffing"""
        cloned = RenderNode(
            self.type, 
            node_id=self.id, 
            props=dict(self.props), 
            style=dict(self.style), 
            bindings=dict(self.stateBinding), 
            layout_hints=dict(self.layoutHints),
            key=self.key,
            parent_id=self.parent_id
        )
        cloned.children = [c.clone() for c in self.children]
        return cloned
        
    def __repr__(self):
        return f"<RenderNode {self.type} id={self.id}>"

class RenderTree:
    def __init__(self, root: Optional[RenderNode] = None):
        self.root = root
        self.current_route = None

    def dispatch_navigation(self, route):
        self.current_route = route
