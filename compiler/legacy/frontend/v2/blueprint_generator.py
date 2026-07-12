"""
=============================================================================
FILE: blueprint_generator.py
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
import re

class BlueprintGenerator:
    def __init__(self):
        self.templates = {}
        self.concept_modules = {}
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        try:
            with open(os.path.join(base_dir, 'dictionary', 'blueprint_templates.json'), 'r') as f:
                self.templates = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load blueprint_templates.json: {e}")
            
        try:
            with open(os.path.join(base_dir, 'dictionary', 'concept_modules.json'), 'r') as f:
                self.concept_modules = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load concept_modules.json: {e}")

    def generate(self, input_intents):
        """
        Takes a list of candidate resolutions or a high-level application intent string.
        Extracts atomic concepts and aggregates their architectural requirements into a unified System Blueprint.
        """
        if not input_intents:
            return {}
            
        blueprint = {
            "frontend_modules": set(),
            "backend_modules": set(),
            "data_entities": set(),
            "external_integrations": set()
        }
        
        # Convert input to list if it's a single string
        if isinstance(input_intents, str):
            input_intents = [input_intents]
            
        extracted_concepts = set()
        
        for item in input_intents:
            item_lower = item.lower()
            
            # 1. Exact Template Match (Legacy fallback for explicit rules)
            template = self.templates.get(item)
            if template:
                blueprint["frontend_modules"].update(template.get("frontend_modules", []))
                blueprint["backend_modules"].update(template.get("backend_modules", []))
                blueprint["data_entities"].update(template.get("data_entities", []))
                blueprint["external_integrations"].update(template.get("external_integrations", []))
                continue
                
            # 2. Concept-Based Aggregation
            words = re.findall(r'\b\w+\b', item_lower)
            for word in words:
                if word in self.concept_modules:
                    extracted_concepts.add(word)
                    concept_arch = self.concept_modules[word]
                    blueprint["frontend_modules"].update(concept_arch.get("frontend_modules", []))
                    blueprint["backend_modules"].update(concept_arch.get("backend_modules", []))
                    blueprint["data_entities"].update(concept_arch.get("data_entities", []))
                    blueprint["external_integrations"].update(concept_arch.get("external_integrations", []))
                    
        # Secure By Default (Aayu Baseline Security)
        blueprint["backend_modules"].update([
            "authentication_service", 
            "authorization_middleware", 
            "input_validation_layer",
            "rate_limiter",
            "audit_logger"
        ])
        blueprint["data_entities"].add("security_audit_log")
        blueprint["external_integrations"].add("kms_encryption")

        # Optional: Keep track of reasoning logic
        blueprint["_reasoning_concepts_matched"] = sorted([
            {"concept": c, "weight": self.concept_modules[c].get("weight", 1.0)} 
            for c in extracted_concepts
        ], key=lambda x: x["weight"], reverse=True)
                
        return {
            "frontend_modules": sorted(list(blueprint["frontend_modules"])),
            "backend_modules": sorted(list(blueprint["backend_modules"])),
            "data_entities": sorted(list(blueprint["data_entities"])),
            "external_integrations": sorted(list(blueprint["external_integrations"])),
            "_reasoning_concepts_matched": blueprint["_reasoning_concepts_matched"]
        }
