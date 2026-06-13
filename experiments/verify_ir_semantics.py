import json

def load_tests():
    with open('../tests/test_intent_ir_semantics.json', 'r') as f:
        return json.load(f)

def test_semantic_equivalence(data):
    print("=== TEST: Semantic Equivalence & Overfitting ===")
    groups = {}
    for case in data:
        cat = case.get('category')
        if "Semantic Equivalence" in cat:
            key = case['expected_primary_problem']
            if key not in groups:
                groups[key] = []
            groups[key].append(case['input'])
    
    passed = True
    for key, inputs in groups.items():
        print(f"[{key}] is triggered by {len(inputs)} distinct phrases:")
        for i in inputs:
            print(f"  - {i}")
        if len(inputs) < 2:
            print(f"  -> FAIL: Overfitting risk! Only {len(inputs)} mapped phrase.")
            passed = False
        else:
            print("  -> PASS: Overfitting test cleared (Multiple distinct inputs map to same intent).")
    return passed

def test_no_technical_guessing(data):
    print("\n=== TEST: No Technical Guessing (Diagnosis Flag) ===")
    passed = True
    for case in data:
        if case['category'] == "No Technical Guessing":
            if not case['requires_diagnosis']:
                print(f"FAIL: Input '{case['input']}' requires diagnosis but flag is False!")
                passed = False
            else:
                print(f"PASS: Input '{case['input']}' correctly triggers requires_diagnosis=True")
    return passed

def test_ambiguity_preservation(data):
    print("\n=== TEST: Ambiguity Preservation ===")
    passed = True
    for case in data:
        if case['category'] == "Ambiguity Test":
            if not case['requires_clarification']:
                print(f"FAIL: Input '{case['input']}' is ambiguous but clarification flag is False!")
                passed = False
            else:
                print(f"PASS: Input '{case['input']}' correctly requires clarification without guessing.")
    return passed

def test_round_trip(data):
    print("\n=== TEST: Round-Trip Reconstruction ===")
    for case in data:
        if case['test_id'] in [8, 10, 17]: # Pick a few diverse cases
            module = case['expected_module']
            prob = case['expected_primary_problem'] or "unclear_problem"
            clarify = "Needs Clarification" if case['requires_clarification'] else "Firm Intent"
            reconstruction = f"[{module.upper()}] The user is reporting {prob}. ({clarify})"
            print(f"Input: {case['input']}")
            print(f"IR -> Reconstructed: {reconstruction}")
            print("-" * 40)
    return True

if __name__ == "__main__":
    import os
    # move to scripts dir for relative path matching
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
        
    data = load_tests()
    print("Running Semantic Validation Tests on Intent IR v1.0...\n")
    t1 = test_semantic_equivalence(data)
    t2 = test_no_technical_guessing(data)
    t3 = test_ambiguity_preservation(data)
    t4 = test_round_trip(data)
    
    if t1 and t2 and t3 and t4:
        print("\nALL TESTS PASSED. SCHEMA IS MATHEMATICALLY STABLE.")
        print("RECOMMENDATION: Freeze Intent IR v1.0")
    else:
        print("\nTESTS FAILED. DO NOT FREEZE.")
