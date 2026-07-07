"""
=============================================================================
FILE: generate_expected_outputs.py
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

def create_expected_outputs():
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
        
    with open('../data/intent_ir_examples_50.json', 'r') as f:
        data = json.load(f)
        
    expected = []
    for d in data:
        expected.append({
            "input": d['input'],
            "expected_module": d['intent_ir']['module'],
            "expected_problem": d['intent_ir']['primary_problem'],
            "requires_clarification": d['intent_ir']['requires_clarification'],
            "requires_diagnosis": d['intent_ir']['requires_diagnosis']
        })
        
    with open('../data/intent_ir_expected_outputs.json', 'w') as f:
        json.dump(expected, f, indent=2)
    print("Created ../data/intent_ir_expected_outputs.json")

if __name__ == "__main__":
    create_expected_outputs()
