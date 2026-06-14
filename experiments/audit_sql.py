"""
Aayu SQL Audit (Sprint 27)

Validates the translation of SchemaModel to executable SQLite DDL.
Executes the generated SQL in an in-memory database to prove architectural correctness.
"""

import os
import sys
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.lexer import Lexer
from prototype.compiler_v2.parser import AayuParser
from prototype.compiler_v2.semantic_analyzer import SemanticAnalyzer
from prototype.compiler_v2.ir_generator import IRGenerator
from prototype.compiler_v2.schema_generator import SchemaGenerator
from prototype.compiler_v2.sql_generator import SQLGenerator

def compile_to_sql(source: str) -> str:
    lexer = Lexer(source)
    parser = AayuParser(lexer.tokenize())
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    result = analyzer.analyze(ast)
    if not result.valid:
        raise Exception(f"Semantic errors found: {result.errors}")
        
    ir_model = IRGenerator().generate(ast)
    schema_model = SchemaGenerator().generate(ir_model)
    sql = SQLGenerator().generate(schema_model)
    return sql

def execute_sql(sql: str, expected_tables: set) -> bool:
    print("--- Generated SQL ---")
    for line in sql.split('\\n'):
        if line.strip():
            print(f"  {line}")
    print("-" * 21)
    
    try:
        # 1. Connect to in-memory database
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        
        # 2. Execute the entire DDL script
        cursor.executescript(sql)
        
        # 3. Verify tables were actually created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        actual_tables = {t[0] for t in tables}
        # Ignore SQLite internal tables if any
        actual_tables = {t for t in actual_tables if not t.startswith("sqlite_")}
        
        if actual_tables == expected_tables:
            print(f"  VERIFICATION: Verified {len(actual_tables)} tables in sqlite_master: {actual_tables}")
            return True
        else:
            print(f"  VERIFICATION FAILED: Expected tables {expected_tables}, but database has {actual_tables}")
            return False
            
    except sqlite3.Error as e:
        print(f"  SQLITE EXECUTION ERROR: {e}")
        return False
    finally:
        conn.close()

def run_audit():
    print("\\n" + "=" * 60)
    print("  AAYU SQL COMPILER AUDIT (SPRINT 27)")
    print("=" * 60)

    all_passed = True

    # Test 1: Hospital (one_to_many)
    print("\\n--- Test 1: Hospital ---")
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
        sql = compile_to_sql(source_1)
        expected_tables = {"patient", "doctor", "appointment"}
        if execute_sql(sql, expected_tables):
            print("=> TEST VERDICT: SUCCESS")
        else:
            print("=> TEST VERDICT: FAILED")
            all_passed = False
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        all_passed = False


    # Test 2: Marketplace (many_to_many junction)
    print("\\n--- Test 2: Marketplace ---")
    source_2 = """system Marketplace

entities:
  product (resource)
  order (transaction)

relations:
  product -> order (many_to_many)
"""
    try:
        sql = compile_to_sql(source_2)
        expected_tables = {"product", "order", "product_order"}
        if execute_sql(sql, expected_tables):
            print("=> TEST VERDICT: SUCCESS")
        else:
            print("=> TEST VERDICT: FAILED")
            all_passed = False
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        all_passed = False


    # Test 3: Adumate (one_to_one UNIQUE)
    print("\\n--- Test 3: Adumate ---")
    source_3 = """system Adumate

domains:
  edu
  housing

shared:
  student (actor)

entities:
  room_allocation (transaction)

relations:
  student -> room_allocation (one_to_one)
"""
    try:
        sql = compile_to_sql(source_3)
        expected_tables = {"student", "room_allocation"}
        if execute_sql(sql, expected_tables):
            print("=> TEST VERDICT: SUCCESS")
        else:
            print("=> TEST VERDICT: FAILED")
            all_passed = False
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        all_passed = False

    print("\\n" + "=" * 60)
    if all_passed:
        print("  ALL TESTS PASSED")
    else:
        print("  SOME TESTS FAILED")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
