import sys
import os
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'prototype', 'compiler_v2'))

from blueprint_generator import BlueprintGenerator

def run_audit():
    generator = BlueprintGenerator()
    
    print("=== Aayu Blueprint Generalization Audit ===")
    
    test_cases = [
        "Adumate student ecosystem app",
        "AI powered hospital management platform",
        "Freelancer marketplace for college students",
        "Smart agriculture advisory platform"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Novel Project {i} ---")
        print(f"Input: \"{test_case}\"")
        blueprint = generator.generate([test_case])
        print("Generated Architecture Blueprint:")
        print(json.dumps(blueprint, indent=2))

if __name__ == "__main__":
    run_audit()
