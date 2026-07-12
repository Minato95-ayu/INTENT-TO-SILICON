"""
=============================================================================
FILE: concept_graph_engine.py
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
from typing import List, Dict, Set, Tuple

class ConceptGraphEngine:
    def __init__(self):
        self.graph = {}
        self.load_graph()

    def load_graph(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        graph_path = os.path.join(base_dir, 'dictionary', 'concept_graph.json')
        try:
            with open(graph_path, 'r') as f:
                self.graph = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load concept_graph.json: {e}")

    def expand(self, explicit_concepts: List[str]) -> Tuple[Set[str], Set[str]]:
        """
        Recursively expands the explicit concepts through 'requires' edges.
        Also gathers 'optional' concepts from the expanded nodes.
        
        Args:
            explicit_concepts: The domains and concepts explicitly found in user intent.
            
        Returns:
            (inferred_requires, optional_concepts)
        """
        visited = set()
        
        def traverse(node):
            if node in visited:
                return
            visited.add(node)
            
            node_data = self.graph.get(node, {})
            # Only recursively traverse "requires"
            for child in node_data.get("requires", []):
                traverse(child)
                
        for concept in explicit_concepts:
            traverse(concept)
            
        # Collect optional concepts for all visited nodes
        optionals = set()
        for node in visited:
            node_data = self.graph.get(node, {})
            for opt in node_data.get("optional", []):
                # Only consider it optional if it hasn't been required/inferred already
                if opt not in visited:
                    optionals.add(opt)
                    
        return visited, optionals
