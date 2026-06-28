from typing import Dict, Any, List
from .graph import GraphEngine

class DecisionEngine:
    def __init__(self, graph: GraphEngine):
        self.graph = graph

    def freeze(self, decision_name: str) -> str:
        """Mark a decision as frozen."""
        return self.graph.create_node("Decision", decision_name, {"status": "Frozen"})

    def check_conflict(self, target_node_name: str) -> Dict[str, Any]:
        """
        Check if modifying the target node violates any frozen decisions.
        We do this by running an impact analysis (reverse). 
        Wait, if we modify a component, does it violate a decision?
        If Decision -> freezes -> Component.
        So if we are modifying Component, we check inbound 'freezes' edges.
        """
        node = self.graph.get_node_by_name(target_node_name)
        if not node:
            return {"conflict": False}

        # Find all incoming 'freezes' edges to this node
        freezes_edges = self.graph.traverse(node["id"], direction="in", relation="freezes")
        
        conflicting_decisions = []
        for edge in freezes_edges:
            decision_node = self.graph.get_node(edge["from_node"])
            if decision_node and decision_node.get("data", {}).get("status") == "Frozen":
                conflicting_decisions.append(decision_node)
                
        if conflicting_decisions:
            # We found a conflict! Let's also run impact analysis to show what else is affected.
            impact = self.graph.impact_analysis(target_node_name)
            return {
                "conflict": True,
                "decisions": conflicting_decisions,
                "impact": impact.get("affected", [])
            }
            
        return {"conflict": False}
