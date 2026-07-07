"""
=============================================================================
FILE: test_blueprint_generator.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import sys
import os
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'prototype', 'compiler_v2'))

from blueprint_generator import BlueprintGenerator

def run_blueprint_test():
    generator = BlueprintGenerator()
    
    print("=== Aayu Blueprint Generator Verification ===")
    
    # Example 1: Blueprint from a Workflow Resolution
    print("\n--- Test 1: Generate Blueprint for a Specific Resolution ---")
    resolutions = ["refund_flow", "create_callback_ticket"]
    print(f"Input Candidate Resolutions: {resolutions}")
    blueprint_1 = generator.generate(resolutions)
    print("Generated Architecture Blueprint:")
    print(json.dumps(blueprint_1, indent=2))
    
    # Example 2: Blueprint from High-Level Application Intent
    print("\n--- Test 2: Generate Blueprint for an Entire Application ---")
    app_intent = ["library_booking", "hostel_booking"]
    print(f"Input App Intents: {app_intent}")
    blueprint_2 = generator.generate(app_intent)
    print("Generated Architecture Blueprint:")
    print(json.dumps(blueprint_2, indent=2))

if __name__ == "__main__":
    run_blueprint_test()
