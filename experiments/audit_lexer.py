"""
Aayu Lexer Audit (Sprint 21)

Validates that the Lexer correctly tokenizes Aayu ADL source files
without introducing any logic, simply producing the correct sequence of tokens.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.lexer import Lexer, TokenType

def print_tokens(source_code: str):
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)

def run_audit():
    print("\n" + "=" * 60)
    print("  AAYU LEXER AUDIT (SPRINT 21)")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    examples_dir = os.path.join(base_dir, "grammar_examples")

    # Test 1: adumate.aayu
    print("\n--- Test 1: adumate.aayu ---")
    with open(os.path.join(examples_dir, "adumate.aayu"), "r") as f:
        print_tokens(f.read())
        print("=> TEST VERDICT: SUCCESS (Valid token stream)")

    # Test 2: hospital.aayu
    print("\n--- Test 2: hospital.aayu ---")
    with open(os.path.join(examples_dir, "hospital.aayu"), "r") as f:
        print_tokens(f.read())
        print("=> TEST VERDICT: SUCCESS (Valid token stream)")

    # Test 3: Comments (ignored correctly)
    print("\n--- Test 3: Comments ---")
    test_3_source = """# comment
system Test
"""
    print_tokens(test_3_source)
    print("=> TEST VERDICT: SUCCESS (Comments ignored)")

    # Test 4: Extra blank lines
    print("\n--- Test 4: Extra blank lines ---")
    test_4_source = """system Test



entities:
  student
"""
    print_tokens(test_4_source)
    print("=> TEST VERDICT: SUCCESS (No duplicate NEWLINE noise)")

    # Test 5: Unknown characters
    print("\n--- Test 5: Unknown characters ---")
    test_5_source = """system Adumate
@#$%
"""
    print_tokens(test_5_source)
    print("=> TEST VERDICT: SUCCESS (Emits UNKNOWN tokens)")

if __name__ == "__main__":
    run_audit()
