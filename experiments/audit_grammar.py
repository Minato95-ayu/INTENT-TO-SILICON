"""
Aayu Grammar Audit (Sprint 20)

Tests the Intent → Lock → Grammar pipeline.
Verifies that ResolvedIntent maps losslessly to .aayu ADL syntax.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.clarification_engine import ClarificationEngine
from prototype.compiler_v2.grammar_generator import GrammarGenerator


def run_audit():
    print("\n" + "=" * 60)
    print("  AAYU GRAMMAR GENERATION AUDIT (SPRINT 20)")
    print("=" * 60)

    engine = ClarificationEngine()
    generator = GrammarGenerator()

    test_cases = [
        {
            "name": "Test 1: Adumate (Student Ecosystem)",
            "intent": "Student Ecosystem with Hostel, Jobs, Library, Payments",
            "system_name": "Adumate",
            "answers": {
                "integration": "shared",
                "authentication": "otp",
                "book_catalog": "api",
                "room_allocation": "automated",
                "job_listing": "admin",
                "payments": "yes",
                "notifications": "yes"
            },
            "expected_domains": ["education", "employment", "housing", "library"],
            "expected_shared": ["student"]
        },
        {
            "name": "Test 2: Hospital Management",
            "intent": "Hospital management system",
            "system_name": "HospitalManagement",
            "answers": {
                "authentication": "mfa",
                "compliance": "hipaa",
                "telemedicine": "webrtc",
                "payments": "insurance"
            },
            "expected_domains": ["healthcare"],
            "expected_shared": []
        },
        {
            "name": "Test 3: Marketplace + Logistics",
            "intent": "Marketplace + Logistics + Payments",
            "system_name": "OnlineMarketplace",
            "answers": {
                "integration": "integrated",
                "seller": "kyc",
                "logistics": "platform",
                "payments": "yes"
            },
            "expected_domains": ["logistics", "marketplace", "payments"],
            "expected_shared": []
        }
    ]

    all_passed = True

    for test in test_cases:
        print(f"\n--- {test['name']} ---")
        print(f"INPUT: \"{test['intent']}\"")

        # 1. Analyze
        result = engine.analyze([], test["intent"])

        # 2. Resolve (simulate locked intent with answers)
        resolved = engine.resolve(test["intent"], test["answers"], [])

        # 3. Generate Grammar
        aayu_code = generator.generate(resolved, result, test["system_name"])

        print(f"\n--- Generated .aayu ---")
        print(aayu_code)

        # 4. Validate
        passed = True

        # Check domains
        for d in test["expected_domains"]:
            if f"  {d}" not in aayu_code:
                print(f"  FAIL: Expected domain '{d}' not found in output")
                passed = False

        # Check shared
        for s in test["expected_shared"]:
            if f"shared:" not in aayu_code or f"  {s}" not in aayu_code:
                print(f"  FAIL: Expected shared entity '{s}' not found")
                passed = False

        # Check system name
        if f"system {test['system_name']}" not in aayu_code:
            print(f"  FAIL: System name '{test['system_name']}' not found")
            passed = False

        if passed:
            print(f"=> TEST VERDICT: SUCCESS")
        else:
            print(f"=> TEST VERDICT: FAILED")
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("  ALL TESTS PASSED")
    else:
        print("  SOME TESTS FAILED")
    print("=" * 60)


if __name__ == "__main__":
    run_audit()
