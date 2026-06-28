import uuid
from typing import Dict, Any, List, Optional
from brainos.storage import StorageAPI
from brainos.models import VALID_NODE_TYPES, VALID_EDGE_RELATIONS

class GraphEngine:
    def __init__(self, storage: StorageAPI):
        self.storage = storage

    def setup(self):
        self.storage.setup()

    def create_node(self, node_type: str, name: str, data: Optional[Dict[str, Any]] = None) -> str:
        """Create a new node in the graph. Returns node_id."""
        if node_type not in VALID_NODE_TYPES:
            raise ValueError(f"Invalid node type '{node_type}'. Valid types: {VALID_NODE_TYPES}")

        # First check if node with same name exists (simplified for v0.1)
        existing = self.storage.get_node_by_name(name)
        if existing and existing["type"] == node_type:
            # Update data instead
            merged_data = existing["data"]
            if data:
                merged_data.update(data)
            self.storage.add_node(existing["id"], node_type, name, merged_data)
            return existing["id"]

        node_id = str(uuid.uuid4())
        self.storage.add_node(node_id, node_type, name, data or {})
        return node_id

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        return self.storage.get_node(node_id)
        
    def get_node_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        return self.storage.get_node_by_name(name)

    def create_edge(self, from_node: str, to_node: str, relation: str, weight: float = 1.0) -> str:
        """Create a directed edge between two nodes. Returns edge_id."""
        if relation not in VALID_EDGE_RELATIONS:
            raise ValueError(f"Invalid edge relation '{relation}'. Valid relations: {VALID_EDGE_RELATIONS}")
            
        # We can add checks to prevent duplicates
        existing = self.storage.get_edges(from_node=from_node, to_node=to_node, relation=relation)
        if existing:
            return existing[0]["id"]
            
        edge_id = str(uuid.uuid4())
        self.storage.add_edge(edge_id, from_node, to_node, relation, weight)
        return edge_id

    def traverse(self, start_node_id: str, direction: str = "out", relation: Optional[str] = None, max_depth: int = 10) -> List[Dict[str, Any]]:
        """
        Traverse the graph from a starting node.
        direction: "out" (from_node == start_node), "in" (to_node == start_node), or "both"
        Returns a list of paths/edges or nodes (simplified to return edges for now).
        """
        visited_nodes = set()
        visited_edges = set()
        queue = [(start_node_id, 0)]
        results = []

        while queue:
            current_node, depth = queue.pop(0)
            if depth >= max_depth:
                continue
                
            if current_node in visited_nodes:
                continue
            visited_nodes.add(current_node)
            
            # Get outgoing edges
            if direction in ("out", "both"):
                edges = self.storage.get_edges(from_node=current_node, relation=relation)
                for edge in edges:
                    if edge["id"] not in visited_edges:
                        visited_edges.add(edge["id"])
                        results.append(edge)
                        queue.append((edge["to_node"], depth + 1))
                        
            # Get incoming edges
            if direction in ("in", "both"):
                edges = self.storage.get_edges(to_node=current_node, relation=relation)
                for edge in edges:
                    if edge["id"] not in visited_edges:
                        visited_edges.add(edge["id"])
                        results.append(edge)
                        queue.append((edge["from_node"], depth + 1))
                        
        return results

    def impact_analysis(self, node_name: str) -> Dict[str, Any]:
        """
        Custom traversal logic for impact analysis.
        Follows 'depends_on' (inbound) and 'implements' (outbound) and 'freezes' (inbound) etc.
        For v0.1, we'll just track anything that points to this node with depends_on, or blocks this node.
        """
        node = self.get_node_by_name(node_name)
        if not node:
            return {"error": f"Node '{node_name}' not found."}
            
        # Find all nodes that depend on this node
        # A -> depends_on -> B (this node)
        # Therefore, changes to B impact A.
        impacted_edges = self.traverse(node["id"], direction="in", relation="depends_on")
        
        # Also find all nodes that this node implements (if we change this node, what does it break?)
        # Wait, if A -> implements -> B, and we change B, A is affected.
        implements_edges = self.traverse(node["id"], direction="in", relation="implements")
        
        all_edges = impacted_edges + implements_edges
        
        affected_nodes = []
        for edge in all_edges:
            # Since direction="in", the affected node is from_node
            affected = self.get_node(edge["from_node"])
            if affected and affected["id"] != node["id"]:
                affected_nodes.append(affected)
                
        # Deduplicate
        seen = set()
        unique_affected = []
        for n in affected_nodes:
            if n["id"] not in seen:
                seen.add(n["id"])
                unique_affected.append(n)
                
        return {
            "target": node,
            "affected": unique_affected,
            "edges": all_edges
        }
