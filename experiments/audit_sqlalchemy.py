"""
Aayu SQLAlchemy Audit (Sprint 28)

Validates the translation of SchemaModel to executable Python SQLAlchemy Models.
Writes the generated models to a temporary module, imports them, and bootstraps an SQLite database.
"""

import os
import sys
import importlib.util
from sqlalchemy import create_engine, inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.lexer import Lexer
from prototype.compiler_v2.parser import AayuParser
from prototype.compiler_v2.semantic_analyzer import SemanticAnalyzer
from prototype.compiler_v2.ir_generator import IRGenerator
from prototype.compiler_v2.schema_generator import SchemaGenerator
from prototype.compiler_v2.sqlalchemy_generator import SQLAlchemyGenerator

def compile_to_orm_code(source: str) -> str:
    lexer = Lexer(source)
    parser = AayuParser(lexer.tokenize())
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    result = analyzer.analyze(ast)
    if not result.valid:
        raise Exception(f"Semantic errors found: {result.errors}")
        
    ir_model = IRGenerator().generate(ast)
    schema_model = SchemaGenerator().generate(ir_model)
    orm_code = SQLAlchemyGenerator().generate(schema_model)
    return orm_code

def execute_orm(orm_code: str, expected_tables: set, module_name: str) -> bool:
    print("--- Generated SQLAlchemy Models ---")
    for line in orm_code.split('\\n'):
        if line.strip():
            print(f"  {line}")
    print("-" * 33)
    
    # 1. Write to temporary file
    temp_file = os.path.join(os.path.dirname(__file__), f"_{module_name}.py")
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(orm_code)
            
        # 2. Dynamically import the module to catch SyntaxErrors
        spec = importlib.util.spec_from_file_location(module_name, temp_file)
        orm_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = orm_module
        try:
            spec.loader.exec_module(orm_module)
        except Exception as e:
            print(f"  PYTHON IMPORT ERROR: {type(e).__name__}: {e}")
            return False
            
        Base = orm_module.Base
        
        # 3. Create SQLite memory database and create tables
        engine = create_engine("sqlite:///:memory:")
        try:
            Base.metadata.create_all(engine)
        except Exception as e:
            print(f"  SQLALCHEMY CREATE_ALL ERROR: {type(e).__name__}: {e}")
            return False
            
        # 4. Verify tables exist via SQLAlchemy inspector
        inspector = inspect(engine)
        actual_tables = set(inspector.get_table_names())
        
        if actual_tables == expected_tables:
            print(f"  VERIFICATION: Verified {len(actual_tables)} tables via SQLAlchemy Inspector: {actual_tables}")
            return True
        else:
            print(f"  VERIFICATION FAILED: Expected tables {expected_tables}, but database has {actual_tables}")
            return False
            
    finally:
        # Cleanup temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if module_name in sys.modules:
            del sys.modules[module_name]

def run_audit():
    print("\\n" + "=" * 60)
    print("  AAYU SQLALCHEMY ORM AUDIT (SPRINT 28)")
    print("=" * 60)

    all_passed = True

    # Test 1: Hospital
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
        orm_code = compile_to_orm_code(source_1)
        expected_tables = {"patient", "doctor", "appointment"}
        if execute_orm(orm_code, expected_tables, "temp_hospital"):
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
        orm_code = compile_to_orm_code(source_2)
        expected_tables = {"product", "order", "product_order"}
        if execute_orm(orm_code, expected_tables, "temp_marketplace"):
            print("=> TEST VERDICT: SUCCESS")
        else:
            print("=> TEST VERDICT: FAILED")
            all_passed = False
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        all_passed = False


    # Test 3: Adumate
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
        orm_code = compile_to_orm_code(source_3)
        expected_tables = {"student", "room_allocation"}
        if execute_orm(orm_code, expected_tables, "temp_adumate"):
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
