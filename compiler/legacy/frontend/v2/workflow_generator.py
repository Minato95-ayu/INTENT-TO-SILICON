"""
=============================================================================
FILE: workflow_generator.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import yaml

class SemanticWorkflowGenerator:
    def generate(self, intent_graph_nodes):
        """
        Takes a topologically sorted list of intent nodes and generates
        a semantic YAML workflow.
        """
        if not intent_graph_nodes:
            return ""
            
        workflow = {"workflow": []}
        
        for node in intent_graph_nodes:
            step = {
                "domain": node["domain"],
                "issue": node["problem"]
            }
            workflow["workflow"].append(step)
            
        # Dump to YAML format
        # sort_keys=False preserves the topological order
        return yaml.dump(workflow, sort_keys=False, default_flow_style=False)
