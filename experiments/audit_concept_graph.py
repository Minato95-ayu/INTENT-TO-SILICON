"""
=============================================================================
FILE: audit_concept_graph.py
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
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.clarification_engine import ClarificationEngine

def run_audit():
    print("\n" + "="*60)
    print("  AAYU CONCEPT GRAPH AUDIT (SPRINT 17)")
    print("="*60)

    engine = ClarificationEngine()

    test_cases = [
        {
            "name": "Test 1: Pure Inference",
            "intent": "Hospital app",
            "extracted_concepts": [],
            "answers": {}
        },
        {
            "name": "Test 2: Implicit Domain Match",
            "intent": "School management system",
            "extracted_concepts": [],
            "answers": {}
        },
        {
            "name": "Test 3: Deep Dependency Inference",
            "intent": "Hospital app with insurance",
            "extracted_concepts": ["insurance"],
            "answers": {}
        },
        {
            "name": "Test 4: Multi-Domain Detection",
            "intent": "Hospital and Pharmacy platform",
            "extracted_concepts": [],
            "answers": {
                "integration": "Integrated workflow"
            }
        },
        {
            "name": "Test 5: Over-generation Prevention",
            "intent": "Hospital information portal",
            "extracted_concepts": [],
            "answers": {}
        },
        {
            "name": "Test B: Recursive Expansion Verify",
            "intent": "Hospital app with billing",
            "extracted_concepts": ["billing"],
            "answers": {}
        },
        {
            "name": "Test C: Cross-domain dependency sanity",
            "intent": "Education platform with payments",
            "extracted_concepts": ["payments"],
            "answers": {}
        },
        {
            "name": "Test D: Cycle Protection Verify",
            "intent": "Cycle test domain",
            "extracted_concepts": ["cycle_a"],
            "answers": {}
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n--- {test['name']} ---")
        print(f"INPUT: \"{test['intent']}\"")
        
        # Phase 1 & 2: Analyze
        result = engine.analyze(test.get('extracted_concepts', []), test['intent'])
        
        print(f"DETECTED DOMAINS: {result.detected_domains}")
        print(f"INFERRED CONCEPTS: {result.inferred_concepts}")
        print(f"QUESTIONS GENERATED: {len(result.questions)}")
        for q in result.questions:
            print(f"  [{q['concept']}] {q['question']}")
            
        # Phase 3: Resolve
        resolved = engine.resolve(test['intent'], test['answers'], test.get('extracted_concepts', []))
        
        print("\nRESOLVED INTENT STATE:")
        print(f"  Detected:  {resolved.detected}")
        print(f"  Inferred:  {resolved.inferred}")
        print(f"  Confirmed: {resolved.confirmed}")
        
        locked = engine.lock_intent(resolved)
        print(f"  Locked String: {locked}")

if __name__ == "__main__":
    run_audit()
