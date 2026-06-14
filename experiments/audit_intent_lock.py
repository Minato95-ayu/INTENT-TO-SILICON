import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.clarification_engine import ClarificationEngine
from prototype.compiler_v2.intent_validator import IntentValidator
from prototype.compiler_v2.intent_completeness_engine import IntentState

def run_audit():
    print("\n" + "="*60)
    print("  AAYU INTENT COMPLETENESS AUDIT (SPRINT 18)")
    print("="*60)

    engine = ClarificationEngine()
    validator = IntentValidator()

    test_cases = [
        {
            "name": "Test 1: PARTIAL (Missing Required Concepts)",
            "intent": "Hospital app",
            "extracted_concepts": [],
            "answers": {},
            "expected_state": IntentState.PARTIAL
        },
        {
            "name": "Test 2: LOCKED (Missing Critical Implementation Details)",
            "intent": "Hospital app",
            "extracted_concepts": [],
            "answers": {
                "payments": "Insurance claim integration chahiye ya direct patient payment?"
            },
            "expected_state": IntentState.LOCKED
        },
        {
            "name": "Test 3: GENERATION_READY (All Decisions Made)",
            "intent": "Hospital app",
            "extracted_concepts": [],
            "answers": {
                "payments": "yes",
                "telemedicine": "webrtc",
                "authentication": "otp"
            },
            "expected_state": IntentState.GENERATION_READY
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n--- {test['name']} ---")
        print(f"INPUT: \"{test['intent']}\"")
        
        # Analyze
        result = engine.analyze(test.get('extracted_concepts', []), test['intent'])
        
        # Resolve
        resolved = engine.resolve(test['intent'], test['answers'], test.get('extracted_concepts', []))
        
        # Validate (Completeness)
        validation_result = validator.validate(result, resolved)
        
        print(f"STATE: {validation_result.state.name}")
        print(f"BLOCKING ITEMS: {validation_result.blocking_items}")
        
        if validation_result.is_valid:
            print("=> COMPILER STATUS: PASS (GENERATION SAFE)")
        else:
            print("=> COMPILER STATUS: FAIL (GENERATION BLOCKED)")
            for e in validation_result.errors:
                print(f"   Error: {e}")
                
        if validation_result.state == test['expected_state']:
            print("=> TEST VERDICT: SUCCESS")
        else:
            print(f"=> TEST VERDICT: FAILED (Expected {test['expected_state'].name})")

if __name__ == "__main__":
    run_audit()
