"""
Aayu Schema Audit (Sprint 26)

Validates the translation of IRModel to SchemaModel.
Ensures correct database relationships and shared entity normalization.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.lexer import Lexer
from prototype.compiler_v2.parser import AayuParser
from prototype.compiler_v2.semantic_analyzer import SemanticAnalyzer
from prototype.compiler_v2.ir_generator import IRGenerator
from prototype.compiler_v2.schema_generator import SchemaGenerator

def compile_to_schema(source: str):
    lexer = Lexer(source)
    parser = AayuParser(lexer.tokenize())
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    result = analyzer.analyze(ast)
    if not result.valid:
        raise Exception(f"Semantic errors found: {result.errors}")
        
    ir_model = IRGenerator().generate(ast)
    schema_model = SchemaGenerator().generate(ir_model)
    return schema_model

def print_schema(schema):
    for table in schema.tables:
        print(f"Table: {table.name}")
        for col in table.columns:
            props = []
            if col.is_primary_key: props.append("PK")
            if col.is_foreign_key: props.append(f"FK -> {col.references_table}")
            if col.is_unique: props.append("UNIQUE")
            prop_str = f" [{' '.join(props)}]" if props else ""
            print(f"  - {col.name} ({col.type}){prop_str}")

def run_audit():
    print("\n" + "=" * 60)
    print("  AAYU SCHEMA COMPILER AUDIT (SPRINT 26)")
    print("=" * 60)

    all_passed = True

    # Test 1: Hospital (one_to_many)
    print("\n--- Test 1: Hospital (one_to_many) ---")
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
        schema = compile_to_schema(source_1)
        print_schema(schema)
        
        appt_table = schema.get_table("appointment")
        if appt_table:
            has_patient_fk = any(c.name == "patient_id" and c.is_foreign_key for c in appt_table.columns)
            has_doctor_fk = any(c.name == "doctor_id" and c.is_foreign_key for c in appt_table.columns)
            if has_patient_fk and has_doctor_fk:
                print("=> TEST VERDICT: SUCCESS")
            else:
                print("=> TEST VERDICT: FAILED (Missing FKs)")
                all_passed = False
        else:
            print("=> TEST VERDICT: FAILED (appointment table missing)")
            all_passed = False
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        all_passed = False


    # Test 2: Marketplace (many_to_many)
    print("\n--- Test 2: Marketplace (many_to_many junction) ---")
    source_2 = """system Marketplace

entities:
  product (resource)
  order (transaction)

relations:
  product -> order (many_to_many)
"""
    try:
        schema = compile_to_schema(source_2)
        print_schema(schema)
        
        junction = schema.get_table("product_order")
        if junction:
            has_prod_fk = any(c.name == "product_id" for c in junction.columns)
            has_order_fk = any(c.name == "order_id" for c in junction.columns)
            if has_prod_fk and has_order_fk:
                print("=> TEST VERDICT: SUCCESS")
            else:
                print("=> TEST VERDICT: FAILED (Junction missing correct FKs)")
                all_passed = False
        else:
            print("=> TEST VERDICT: FAILED (product_order junction table missing)")
            all_passed = False
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        all_passed = False


    # Test 3: Adumate (one_to_one)
    print("\n--- Test 3: Adumate (one_to_one UNIQUE) ---")
    source_3 = """system Adumate

entities:
  student (actor)
  room_allocation (transaction)

relations:
  student -> room_allocation (one_to_one)
"""
    try:
        schema = compile_to_schema(source_3)
        print_schema(schema)
        
        room_table = schema.get_table("room_allocation")
        if room_table:
            has_unique_fk = any(c.name == "student_id" and c.is_foreign_key and c.is_unique for c in room_table.columns)
            if has_unique_fk:
                print("=> TEST VERDICT: SUCCESS")
            else:
                print("=> TEST VERDICT: FAILED (Missing unique FK)")
                all_passed = False
        else:
            print("=> TEST VERDICT: FAILED (room_allocation table missing)")
            all_passed = False
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        all_passed = False


    # Test 4: Shared Entity Normalization
    print("\n--- Test 4: Shared Entity (Only ONE table) ---")
    source_4 = """system MultiDomain

domains:
  edu
  housing

shared:
  student (actor)

entities:
  course
  room

relations:
  student -> course (one_to_many)
  student -> room (one_to_many)
"""
    try:
        schema = compile_to_schema(source_4)
        print_schema(schema)
        
        student_tables = [t for t in schema.tables if t.name == "student"]
        if len(student_tables) == 1:
            print("=> TEST VERDICT: SUCCESS")
        else:
            print(f"=> TEST VERDICT: FAILED (Found {len(student_tables)} student tables, expected exactly 1)")
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
