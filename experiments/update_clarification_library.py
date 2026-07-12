"""
=============================================================================
FILE: update_clarification_library.py
PURPOSE: Updates system components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles updates system components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import json
import os

base_dir = os.path.dirname(os.path.dirname(__file__))
filepath = os.path.join(base_dir, 'dictionary', 'clarification_library.json')

with open(filepath, 'r') as f:
    data = json.load(f)

# Rules for mapping
# Telemedicine, payments, notifications, content_delivery, localization, offline_support
# tracking, routing, compliance, accessibility, shipping, inventory, media_sharing,
# threat_intel, vulnerability_report

def categorize(concept):
    if concept in ["authentication", "telemedicine", "tracking", "routing", "shipping", "media_sharing"]:
        return "implementation", "critical", None
    elif concept in ["payments", "inventory", "threat_intel", "vulnerability_report", "localization", "offline_support"]:
        return "feature", "critical", None
    elif concept in ["compliance", "accessibility", "fraud_detection"]:
        return "implementation", "optional", "default"
    elif concept in ["notifications", "content_delivery"]:
        return "implementation", "optional", "default"
    else:
        return "feature", "optional", None

for domain, content in data.items():
    if not isinstance(content, dict) or "questions" not in content:
        continue
    
    new_questions = {}
    for concept, text in content["questions"].items():
        if isinstance(text, dict):
            new_questions[concept] = text
            continue
            
        t, p, d = categorize(concept)
        obj = {
            "question": text,
            "type": t,
            "priority": p
        }
        if d:
            if concept == "notifications":
                obj["default"] = "email"
            elif concept == "compliance":
                obj["default"] = "gdpr"
            elif concept == "accessibility":
                obj["default"] = "wcag"
            elif concept == "fraud_detection":
                obj["default"] = "basic_rules"
            elif concept == "content_delivery":
                obj["default"] = "cdn"
                
        new_questions[concept] = obj
        
    content["questions"] = new_questions

with open(filepath, 'w') as f:
    json.dump(data, f, indent=2)
