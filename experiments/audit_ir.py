"""
Aayu IR Audit (Sprint 25)

Validates the translation of AayuAST to the Deterministic IRModel.
Ensures that shared entities are correctly merged and syntax noise is discarded.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.lexer import Lexer
from prototype.compiler_v2.parser import AayuParser
from prototype.compiler_v2.semantic_analyzer import SemanticAnalyzer
from prototype.compiler_v2.ir_generator import IRGenerator

def print_ir(model):
    print(f"IRModel(system='{model.system_name}')")
    
    if model.domains:
        print("  Domains:")
        for d in model.domains:
            print(f"    - {d.name}")
            
    if model.entities:
        print("  Entities:")
        for e in model.entities:
            kind_str = f" [category={e.category}]" if e.category else ""
            shared_str = " (SHARED)" if e.is_shared else ""
            print(f"    - {e.name}{kind_str}{shared_str}")
            
    if model.relationships:
        print("  Relationships:")
        for r in model.relationships:
            card_str = f" [cardinality={r.cardinality}]" if r.cardinality else ""
            print(f"    - {r.source} -> {r.target}{card_str}")

def compile_to_ir(source: str):
    lexer = Lexer(source)
    parser = AayuParser(lexer.tokenize())
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    result = analyzer.analyze(ast)
    if not result.valid:
        raise Exception("Semantic errors found in test source")
        
    generator = IRGenerator()
    return generator.generate(ast)

def run_audit():
    print("\n" + "=" * 60)
    print("  AAYU DETERMINISTIC IR AUDIT (SPRINT 25)")
    print("=" * 60)

    all_passed = True

    # Test 1: Hospital (2 actors, 1 transaction, 2 relationships)
    print("\n--- Test 1: Hospital ---")
    source_1 = """system Hospital

entities:
  patient (actor)
  doctor (actor)
  appointment (transaction)

relations:
  patient -> appointment (one_to_many)
  doctor -> appointment (one_to_many)
"""
    try:
        model = compile_to_ir(source_1)
        print_ir(model)
        
        actors = [e for e in model.entities if e.category == "actor"]
        txs = [e for e in model.entities if e.category == "transaction"]
        if len(actors) == 2 and len(txs) == 1 and len(model.relationships) == 2:
            print("=> TEST VERDICT: SUCCESS")
        else:
            print("=> TEST VERDICT: FAILED (Count mismatch)")
            all_passed = False
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        all_passed = False

    # Test 2: Marketplace
    print("\n--- Test 2: Marketplace ---")
    source_2 = """system Marketplace

entities:
  seller (actor)
  buyer (actor)
  product (resource)
  order (transaction)

relations:
  seller -> product (one_to_many)
  buyer -> order (one_to_many)
  product -> order (many_to_many)
"""
    try:
        model = compile_to_ir(source_2)
        print_ir(model)
        
        expected_names = {"seller", "buyer", "product", "order"}
        actual_names = {e.name for e in model.entities}
        if actual_names == expected_names:
            print("=> TEST VERDICT: SUCCESS")
        else:
            print("=> TEST VERDICT: FAILED (Missing entities)")
            all_passed = False
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        all_passed = False

    # Test 3: Adumate (Shared student)
    print("\n--- Test 3: Adumate ---")
    source_3 = """system Adumate

domains:
  education
  housing

shared:
  student (actor)

entities:
  enrollment (transaction)
  room_allocation (transaction)

relations:
  student -> enrollment (one_to_many)
  student -> room_allocation (one_to_one)
"""
    try:
        model = compile_to_ir(source_3)
        print_ir(model)
        
        student_node = next((e for e in model.entities if e.name == "student"), None)
        if student_node and student_node.is_shared and student_node.category == "actor":
            print("=> TEST VERDICT: SUCCESS (Shared entity normalized perfectly)")
        else:
            print("=> TEST VERDICT: FAILED (Shared entity mapping incorrect)")
            all_passed = False
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("  ALL TESTS PASSED")
    else:
        print("  SOME TESTS FAILED")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
