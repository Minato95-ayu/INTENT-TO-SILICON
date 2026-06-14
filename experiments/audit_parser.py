"""
Aayu Parser Audit (Sprint 22)

Validates that the Parser successfully converts Token Streams into AayuAST structures,
enforces strict order, and gracefully emits ParserErrors with line/col metadata.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.lexer import Lexer
from prototype.compiler_v2.parser import AayuParser, ParserError

def print_ast(ast):
    print(f"AayuAST(")
    print(f"    system=SystemNode('{ast.system.name}'),")
    
    if ast.domains:
        print(f"    domains=[")
        for d in ast.domains:
            print(f"        DomainNode('{d.name}', line={d.line}, col={d.column}),")
        print(f"    ],")
        
    if ast.shared:
        print(f"    shared=[")
        for s in ast.shared:
            print(f"        SharedNode('{s.name}'),")
        print(f"    ],")
        
    if ast.entities:
        print(f"    entities=[")
        for e in ast.entities:
            print(f"        EntityNode('{e.name}'),")
        print(f"    ],")
        
    if ast.relations:
        print(f"    relations=[")
        for r in ast.relations:
            print(f"        RelationNode(src='{r.source}', tgt='{r.target}'),")
        print(f"    ]")
        
    print(f")")

def run_test(name: str, source: str, expected_error: bool = False):
    print(f"\n--- {name} ---")
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = AayuParser(tokens)
        ast = parser.parse()
        
        if expected_error:
            print("=> TEST VERDICT: FAILED (Expected a ParserError, but parsing succeeded!)")
            return False
            
        print_ast(ast)
        print("=> TEST VERDICT: SUCCESS (Valid AST)")
        return True
        
    except ParserError as e:
        if expected_error:
            print(f"Caught Expected {e}")
            print("=> TEST VERDICT: SUCCESS")
            return True
        else:
            print(f"Unexpected {e}")
            print("=> TEST VERDICT: FAILED")
            return False

def run_audit():
    print("\n" + "=" * 60)
    print("  AAYU PARSER AUDIT (SPRINT 22)")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    examples_dir = os.path.join(base_dir, "grammar_examples")

    all_passed = True

    # Test 1: hospital.aayu
    with open(os.path.join(examples_dir, "hospital.aayu"), "r") as f:
        passed = run_test("Test 1: hospital.aayu", f.read(), expected_error=False)
        all_passed = all_passed and passed

    # Test 2: adumate.aayu
    with open(os.path.join(examples_dir, "adumate.aayu"), "r") as f:
        passed = run_test("Test 2: adumate.aayu", f.read(), expected_error=False)
        all_passed = all_passed and passed

    # Test 3: Missing colon
    source_3 = """system Hospital

domains
  healthcare
"""
    passed = run_test("Test 3: Missing colon", source_3, expected_error=True)
    all_passed = all_passed and passed

    # Test 4: Broken relation
    source_4 = """system Hospital

domains:
  healthcare

entities:
  doctor
  patient

relations:
  doctor -
  patient
"""
    passed = run_test("Test 4: Broken relation", source_4, expected_error=True)
    all_passed = all_passed and passed

    # Test 5: Unknown / Out of order section
    source_5 = """system Hospital

entities:
  patient

domains:
  healthcare
"""
    passed = run_test("Test 5: Out of order section", source_5, expected_error=True)
    all_passed = all_passed and passed

    print("\n" + "=" * 60)
    if all_passed:
        print("  ALL TESTS PASSED")
    else:
        print("  SOME TESTS FAILED")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
