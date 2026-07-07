"""
=============================================================================
FILE: aayu_ir.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import json
import os

class AayuIRBuilder:
    def __init__(self):
        self.mapping = {}
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        try:
            with open(os.path.join(base_dir, 'dictionary', 'aayu_ir_mapping.json'), 'r') as f:
                self.mapping = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load aayu_ir_mapping.json: {e}")

    def build(self, intent_ir):
        """
        Converts Intent IR to Aayu IR.
        """
        if not intent_ir or not intent_ir.get('module') or not intent_ir.get('primary_problem'):
            return None
            
        module = intent_ir['module']
        problem = intent_ir['primary_problem']
        
        module_mapping = self.mapping.get(module, {})
        aayu_mapping = module_mapping.get(problem)
        
        if not aayu_mapping:
            return None
            
        return {
            "domain": module,
            "event": aayu_mapping["event"],
            "condition": aayu_mapping["condition"],
            "action": aayu_mapping["action"],
            "confidence": intent_ir.get("confidence_score", 0.0)
        }
