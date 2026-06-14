"""
Aayu Semantic Audit (Sprint 23)

Validates that the Semantic Analyzer correctly enforces architectural logic on ASTs.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.lexer import Lexer
from prototype.compiler_v2.parser import AayuParser
from prototype.compiler_v2.semantic_analyzer import SemanticAnalyzer

def run_test(name: str, source: str, expected_valid: bool = True, expected_warnings: bool = False):
    print(f"\n--- {name} ---")
    
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
        
    for warn in result.warnings:
        print(f"  WARNING: {warn.message} (Line {warn.line})")
        
    if expected_warnings and not result.warnings:
        print(f"  FAIL: Expected warnings but none were emitted.")
        passed = False
        
    if passed:
        print("=> TEST VERDICT: SUCCESS")
    else:
        print("=> TEST VERDICT: FAILED")
        
    return passed

def run_audit():
    print("\n" + "=" * 60)
    print("  AAYU SEMANTIC AUDIT (SPRINT 23)")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    examples_dir = os.path.join(base_dir, "grammar_examples")

    all_passed = True

    # Test 1: Valid architecture (hospital.aayu)
    with open(os.path.join(examples_dir, "hospital.aayu"), "r") as f:
        passed = run_test("Test 1: Valid architecture", f.read(), expected_valid=True)
        all_passed = all_passed and passed

    # Test 2: Undefined Entity Reference
    source_2 = """system Test

entities:
  doctor

relations:
  doctor -> patient
"""
    passed = run_test("Test 2: Undefined Entity Reference", source_2, expected_valid=False)
    all_passed = all_passed and passed

    # Test 3: Duplicate Entity/Domain
    source_3 = """system Test

domains:
  healthcare
  healthcare

entities:
  student
  student
"""
    passed = run_test("Test 3: Duplicate Entity/Domain", source_3, expected_valid=False)
    all_passed = all_passed and passed

    # Test 4: Shared vs Local Collision
    source_4 = """system Test

shared:
  student

entities:
  student
"""
    passed = run_test("Test 4: Shared vs Local Collision", source_4, expected_valid=False)
    all_passed = all_passed and passed

    # Test 5: Empty System
    source_5 = """system Empty"""
    passed = run_test("Test 5: Empty System", source_5, expected_valid=False)
    all_passed = all_passed and passed

    # Test 6: Orphan Entity (Warning)
    source_6 = """system Test

entities:
  doctor
  patient
  room

relations:
  doctor -> patient
"""
    passed = run_test("Test 6: Orphan Entity (Warning)", source_6, expected_valid=True, expected_warnings=True)
    all_passed = all_passed and passed

    print("\n" + "=" * 60)
    if all_passed:
        print("  ALL TESTS PASSED")
    else:
        print("  SOME TESTS FAILED")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
