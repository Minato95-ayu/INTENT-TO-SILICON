"""
=============================================================================
FILE: audit_cross_domain.py
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
    print("  AAYU CROSS-DOMAIN STRESS TEST AUDIT (SPRINT 19)")
    print("="*60)

    engine = ClarificationEngine()

    test_cases = [
        {
            "name": "Test 1: Healthcare Ecosystem",
            "intent": "Hospital + Pharmacy + Insurance",
            "expected_domains": ["healthcare", "pharmacy", "insurance"]
        },
        {
            "name": "Test 2: Adumate-Style Student Ecosystem",
            "intent": "Student Ecosystem with Hostel, Jobs, Library, Payments, Mentorship",
            "expected_domains": ["education", "housing", "employment", "library"]
        },
        {
            "name": "Test 3: Commerce Ecosystem",
            "intent": "Marketplace + Logistics + Payments",
            "expected_domains": ["marketplace", "logistics", "payments"]
        },
        {
            "name": "Test 4: Pure Insurance Ecosystem",
            "intent": "Insurance Claim Management Platform",
            "expected_domains": ["insurance"]
        },
        {
            "name": "Test 5: Pure Payments Ecosystem",
            "intent": "Digital Payments Platform",
            "expected_domains": ["payments"]
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n--- {test['name']} ---")
        print(f"INPUT: \"{test['intent']}\"")
        
        # Analyze
        result = engine.analyze([], test['intent'])
        
        detected = result.detected_domains
        print(f"DETECTED DOMAINS: {detected}")
        
        # Check expected
        missing = [d for d in test['expected_domains'] if d not in detected]
        extra = [d for d in detected if d not in test['expected_domains']]
        
        # Print structured integration question if present
        integration_q = next((q for q in result.questions if q["concept"] == "integration"), None)
        if integration_q:
            print(f"INTEGRATION QUESTION: {integration_q['question']}")
            
        if not missing and not extra:
            print("=> TEST VERDICT: SUCCESS")
        else:
            print(f"=> TEST VERDICT: FAILED")
            if missing:
                print(f"   Missing expected domains: {missing}")
            if extra:
                print(f"   Unexpected domains detected: {extra}")

if __name__ == "__main__":
    run_audit()
