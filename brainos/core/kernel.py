from typing import Dict, Any, List
from .graph import GraphEngine

class MemoryManager:
    def __init__(self, graph: GraphEngine):
        self.graph = graph

    def set_dna(self, rule_name: str, content: str) -> str:
        """Stores a piece of Project DNA as a 'Rule' node."""
        return self.graph.create_node("Rule", rule_name, {"content": content})

    def get_dna(self) -> List[Dict[str, Any]]:
        """Retrieves all Project DNA (Rules)."""
        return self.graph.storage.get_nodes_by_type("Rule")
