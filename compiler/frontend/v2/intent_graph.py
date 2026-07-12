"""
=============================================================================
FILE: intent_graph.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import json

class IntentGraphBuilder:
    def __init__(self):
        self.dependencies = {}
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        try:
            with open(os.path.join(base_dir, 'dictionary', 'domain_dependencies.json'), 'r') as f:
                self.dependencies = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load domain_dependencies.json: {e}")

    def build_graph(self, intents):
        """
        Takes a list of IntentIR dicts and returns a topologically sorted list 
        of Intent Nodes based on domain dependencies.
        """
        if not intents:
            return []
            
        # Filter out unknown intents
        valid_intents = [i for i in intents if i.get("primary_problem") is not None]
        if not valid_intents:
            return []

        # Create nodes
        nodes = []
        for intent in valid_intents:
            domain = intent.get("module")
            # Build dependencies for this specific node
            # A node depends on another domain if its domain depends on that domain
            node_deps = self.dependencies.get(domain, [])
            
            nodes.append({
                "domain": domain,
                "problem": intent.get("primary_problem"),
                "depends_on": node_deps,
                "intent_ir": intent
            })
            
        # Topological Sort
        sorted_nodes = []
        visited = set()
        temp_visited = set()

        def visit(node):
            node_id = f"{node['domain']}_{node['problem']}"
            if node_id in temp_visited:
                # Cycle detected, just ignore for simplicity
                return
            if node_id in visited:
                return
                
            temp_visited.add(node_id)
            
            # Visit dependencies first
            for dep_domain in node["depends_on"]:
                # Find all nodes in the current list that match the dependency domain
                for other_node in nodes:
                    if other_node["domain"] == dep_domain:
                        visit(other_node)
                        
            temp_visited.remove(node_id)
            visited.add(node_id)
            sorted_nodes.append(node)

        for node in nodes:
            visit(node)
            
        return sorted_nodes
