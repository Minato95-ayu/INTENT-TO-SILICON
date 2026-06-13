import sys
import os
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'prototype', 'compiler_v2'))

from compiler import CompilerV2

def run_tests():
    c = CompilerV2()
    print("=== Aayu Compiler v0.1 Verification ===\n")
    
    test_cases = [
        {
            "name": "Test 1 & 2: Base Wording to Python Code",
            "input": "paise kat gaye par order nahi bana"
        },
        {
            "name": "Test 3: Unseen Wording Generalization",
            "input": "money deduct ho gaya lekin order create nahi hua"
        }
    ]
    
    for tc in test_cases:
        print(f"[{tc['name']}]")
        print(f"Input: {tc['input']}")
        res = c.process(tc['input'])
        
        print("Aayu IR:")
        print(json.dumps(res['aayu_ir'], indent=2))
        
        print("\nGenerated Python:")
        print(res['code'])
        print("-" * 40 + "\n")

if __name__ == "__main__":
    run_tests()
