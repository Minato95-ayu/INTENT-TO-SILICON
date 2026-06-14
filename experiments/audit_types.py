"""
Aayu Type System Audit (Sprint 24)

Validates that Lexer, Parser, and Semantic Analyzer correctly handle 
optional inline types like `patient (actor)` and `doctor -> patient (one_to_many)`.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.lexer import Lexer
from prototype.compiler_v2.parser import AayuParser
from prototype.compiler_v2.semantic_analyzer import SemanticAnalyzer

def run_test(name: str, source: str, expected_valid: bool = True):
    print(f"\n--- {name} ---")
    
    try:
        # 1. Lexing
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # 2. Parsing
        parser = AayuParser(tokens)
        ast = parser.parse()
        
        # 3. Semantic Analysis
        analyzer = SemanticAnalyzer()
        result = analyzer.analyze(ast)
        
        passed = True
        
        if result.valid != expected_valid:
            print(f"  FAIL: Expected valid={expected_valid}, got valid={result.valid}")
            passed = False
            
        for err in result.errors:
            print(f"  ERROR: {err.message} (Line {err.line})")
            
        if passed:
            print("=> TEST VERDICT: SUCCESS")
        else:
            print("=> TEST VERDICT: FAILED")
            
        return passed
        
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        print("=> TEST VERDICT: FAILED (CRASH)")
        return False

def run_audit():
    print("\n" + "=" * 60)
    print("  AAYU TYPE SYSTEM AUDIT (SPRINT 24)")
    print("=" * 60)

    all_passed = True

    # Test 1: Valid typed entities and relations
    source_1 = """system Hospital

entities:
  patient (actor)
  appointment (transaction)

relations:
  patient -> appointment (one_to_many)
"""
    passed = run_test("Test 1: Valid typed entities and relations", source_1, expected_valid=True)
    all_passed = all_passed and passed

    # Test 2: Backward compatibility (untyped)
    source_2 = """system Hospital

entities:
  patient
  appointment

relations:
  patient -> appointment
"""
    passed = run_test("Test 2: Backward compatibility (untyped)", source_2, expected_valid=True)
    all_passed = all_passed and passed

    # Test 3: Invalid entity type
    source_3 = """system Hospital

entities:
  patient (integer)
  appointment

relations:
  patient -> appointment
"""
    passed = run_test("Test 3: Invalid entity type ('integer')", source_3, expected_valid=False)
    all_passed = all_passed and passed

    # Test 4: Invalid relation type
    source_4 = """system Hospital

entities:
  patient
  appointment

relations:
  patient -> appointment (one_to_infinity)
"""
    passed = run_test("Test 4: Invalid relation type ('one_to_infinity')", source_4, expected_valid=False)
    all_passed = all_passed and passed

    print("\n" + "=" * 60)
    if all_passed:
        print("  ALL TESTS PASSED")
    else:
        print("  SOME TESTS FAILED")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
