import json
from typing import Dict, Any, List
from .graph import GraphEngine

class ContextEngine:
    def __init__(self, graph: GraphEngine):
        self.graph = graph

    def generate_bundle(self, target_node_name: str) -> Dict[str, Any]:
        """
        Generate a standardized Context Bundle for a given target node (e.g. a Task or Component).
        """
        target_node = self.graph.get_node_by_name(target_node_name)
        if not target_node:
            return {"error": f"Node '{target_node_name}' not found."}
            
        # Standard format
        bundle = {
            "project": "BrainOS Application", # Hardcoded for v0.1
            "target": target_node,
            "decisions": [],
            "components": [],
            "issues": [],
            "files": []
        }
        
        # Traverse graph to find related context
        # For v0.1 we just do a breadth-first search of depth 2 to collect related nodes
        edges = self.graph.traverse(target_node["id"], direction="both", max_depth=2)
        
        visited_nodes = {target_node["id"]}
        
        for edge in edges:
            for node_id in (edge["from_node"], edge["to_node"]):
                if node_id not in visited_nodes:
                    visited_nodes.add(node_id)
                    node = self.graph.get_node(node_id)
                    if not node:
                        continue
                        
                    n_type = node.get("type", "").lower()
                    if n_type == "decision":
                        bundle["decisions"].append(node)
                    elif n_type in ("component", "module"):
                        bundle["components"].append(node)
                    elif n_type == "issue":
                        bundle["issues"].append(node)
                    elif n_type == "file":
                        bundle["files"].append(node)
                        
        return bundle
        
    def export_bundle(self, target_node_name: str, out_json: str = "bundle.json"):
        bundle = self.generate_bundle(target_node_name)
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(bundle, f, indent=2)
        return bundle
