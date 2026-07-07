"""
=============================================================================
FILE: constraint_resolver.py
PURPOSE: ConstraintResolver for Intent Engine v2
=============================================================================
"""

from typing import Dict, Any

class ConstraintResolver:
    def __init__(self):
        pass
        
    def resolve(self, enriched_graph: Dict[str, Any]) -> Dict[str, Any]:
        resolved = enriched_graph.copy()
        
        # Check constraints (e.g. can't deploy without a backend)
        entities = resolved.get("entities", [])
        actions = resolved.get("actions", [])
        
        if "deploy" in actions and "api" not in entities:
            # Infer an API is needed if they want to deploy something like a CRM
            if "crm" in entities:
                resolved["entities"].append("api")
                
        return resolved
