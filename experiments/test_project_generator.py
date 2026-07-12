"""
=============================================================================
FILE: test_project_generator.py
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

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'prototype', 'compiler_v2'))

from blueprint_generator import BlueprintGenerator
from project_generator import ProjectGenerator

def print_tree(directory, prefix=""):
    """Recursively prints a directory tree."""
    if not os.path.exists(directory):
        return
        
    items = sorted(os.listdir(directory))
    for i, item in enumerate(items):
        path = os.path.join(directory, item)
        is_last = (i == len(items) - 1)
        connector = "\\-- " if is_last else "|-- "
        print(f"{prefix}{connector}{item}")
        
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "|   ")
            print_tree(path, new_prefix)

def run_project_test():
    bp_gen = BlueprintGenerator()
    proj_gen = ProjectGenerator()
    
    print("=== Aayu Project Generator Verification ===")
    app_intent = ["library_booking", "hostel_booking"]
    print(f"Input App Intents: {app_intent}")
    
    blueprint = bp_gen.generate(app_intent)
    
    out_dir = os.path.join(base_dir, "generated_project")
    proj_gen.generate_project(blueprint, out_dir)
    
    print("\n[SUCCESS] Project physical structure generated!")
    print(f"Location: {out_dir}\n")
    
    print("=== Directory Tree ===")
    print("generated_project/")
    print_tree(out_dir)

if __name__ == "__main__":
    run_project_test()
