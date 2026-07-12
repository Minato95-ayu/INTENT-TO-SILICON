"""
=============================================================================
FILE: resolution_engine.py
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
import yaml

class ResolutionEngine:
    def __init__(self):
        self.resolutions = {}
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        try:
            with open(os.path.join(base_dir, 'dictionary', 'resolutions.json'), 'r') as f:
                self.resolutions = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load resolutions.json: {e}")

    def generate_candidates(self, workflow_yaml):
        """
        Takes a Semantic Workflow YAML string, parses it, and attaches 
        candidate resolutions for each step.
        Returns a list of dicts representing the resolution reasoning.
        """
        if not workflow_yaml:
            return []
            
        try:
            workflow_data = yaml.safe_load(workflow_yaml)
            steps = workflow_data.get("workflow", [])
        except Exception:
            steps = []
            
        resolutions_plan = []
        
        for step in steps:
            domain = step.get("domain")
            issue = step.get("issue")
            candidates = self.resolutions.get(issue, ["log_error", "route_to_human"])
            
            resolutions_plan.append({
                "domain": domain,
                "issue": issue,
                "candidate_resolutions": candidates
            })
            
        return resolutions_plan
