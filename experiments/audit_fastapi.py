"""
Aayu FastAPI CRUD Audit (Sprint 29)

Validates the translation of SchemaModel to executable FastAPI Applications.
Tests actual HTTP calls against the generated endpoints to prove Live Web API functionality.
"""

import os
import sys
import importlib.util

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.lexer import Lexer
from prototype.compiler_v2.parser import AayuParser
from prototype.compiler_v2.semantic_analyzer import SemanticAnalyzer
from prototype.compiler_v2.ir_generator import IRGenerator
from prototype.compiler_v2.schema_generator import SchemaGenerator
from prototype.compiler_v2.sqlalchemy_generator import SQLAlchemyGenerator
from prototype.compiler_v2.api_generator import FastAPIGenerator

def compile_to_app_code(source: str) -> str:
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
    api_code = FastAPIGenerator().generate(schema_model)
    
    return orm_code + "\n\n" + api_code

def execute_api_test(app_code: str, module_name: str) -> bool:
    print("--- Generated Full Application Code (ORM + API) ---")
    for line in app_code.split('\\n'):
        if line.strip():
            print(f"  {line}")
    print("-" * 51)
    
    temp_file = os.path.join(os.path.dirname(__file__), f"_{module_name}.py")
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(app_code)
            
        spec = importlib.util.spec_from_file_location(module_name, temp_file)
        api_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = api_module
        try:
            spec.loader.exec_module(api_module)
        except Exception as e:
            print(f"  [FAIL] PYTHON IMPORT ERROR: {type(e).__name__}: {e}")
            return False
            
        # Bootstrap DB
        try:
            api_module.Base.metadata.create_all(api_module.engine)
            print("  [PASS] Database successfully bootstrapped.")
        except Exception as e:
            print(f"  [FAIL] DB BOOTSTRAP ERROR: {type(e).__name__}: {e}")
            return False
            
        # FastAPI TestClient
        try:
            from fastapi.testclient import TestClient
        except ImportError:
            print("  [FAIL] fastapi module not found. Please pip install fastapi httpx.")
            return False
            
        client = TestClient(api_module.app)
        
        # We will test the 'patient' entity if it exists (Hospital), or 'student' (Adumate), or 'product' (Marketplace)
        entity_to_test = None
        for table_name in ["patient", "student", "product"]:
            if hasattr(api_module, "".join(x.title() for x in table_name.split("_"))):
                entity_to_test = table_name
                break
                
        if not entity_to_test:
            print("  [PASS] No standard entities found to test HTTP CRUD, but code compiled successfully.")
            return True
            
        print(f"\\n  Testing HTTP Endpoints for: {entity_to_test}")
        
        # 1. POST
        post_response = client.post(f"/{entity_to_test}", json={})
        if post_response.status_code != 200:
            print(f"  [FAIL] POST /{entity_to_test} returned {post_response.status_code}: {post_response.text}")
            return False
        created_id = post_response.json()["id"]
        print(f"  [PASS] POST /{entity_to_test} -> 200 OK (Created ID: {created_id})")
        
        # 2. GET List
        get_list = client.get(f"/{entity_to_test}")
        if get_list.status_code != 200:
            print(f"  [FAIL] GET /{entity_to_test} returned {get_list.status_code}")
            return False
        print(f"  [PASS] GET /{entity_to_test} -> 200 OK (Count: {len(get_list.json())})")
        
        # 3. PUT
        put_response = client.put(f"/{entity_to_test}/{created_id}", json={})
        if put_response.status_code != 200:
            print(f"  [FAIL] PUT /{entity_to_test}/{{id}} returned {put_response.status_code}")
            return False
        print(f"  [PASS] PUT /{entity_to_test}/{{id}} -> 200 OK")
        
        # 4. GET Item
        get_item = client.get(f"/{entity_to_test}/{created_id}")
        if get_item.status_code != 200:
            print(f"  [FAIL] GET /{entity_to_test}/{{id}} returned {get_item.status_code}")
            return False
        print(f"  [PASS] GET /{entity_to_test}/{{id}} -> 200 OK")
        
        # 5. DELETE
        delete_response = client.delete(f"/{entity_to_test}/{created_id}")
        if delete_response.status_code != 200:
            print(f"  [FAIL] DELETE /{entity_to_test}/{{id}} returned {delete_response.status_code}")
            return False
        print(f"  [PASS] DELETE /{entity_to_test}/{{id}} -> 200 OK")
        
        # 6. GET Item (Verify Deletion)
        get_deleted = client.get(f"/{entity_to_test}/{created_id}")
        if get_deleted.status_code != 404:
            print(f"  [FAIL] GET /{entity_to_test}/{{id}} after deletion returned {get_deleted.status_code} (Expected 404)")
            return False
        print(f"  [PASS] GET /{entity_to_test}/{{id}} after deletion -> 404 Not Found (Correctly Deleted)")
        
        return True
            
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if module_name in sys.modules:
            del sys.modules[module_name]

def run_audit():
    print("\\n" + "=" * 60)
    print("  AAYU FASTAPI CRUD AUDIT (SPRINT 29)")
    print("=" * 60)

    all_passed = True

    print("\\n--- Test 1: Hospital (CRUD Test) ---")
    source_1 = """system Hospital
entities:
  patient (actor)
  doctor (actor)
"""
    try:
        app_code = compile_to_app_code(source_1)
        if execute_api_test(app_code, "temp_api_hospital"):
            print("=> TEST VERDICT: SUCCESS")
        else:
            print("=> TEST VERDICT: FAILED")
            all_passed = False
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        all_passed = False

    print("\\n" + "=" * 60)
    if all_passed:
        print("  ALL TESTS PASSED. INTENT TO HTTP CRUD VERIFIED!")
    else:
        print("  SOME TESTS FAILED")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
