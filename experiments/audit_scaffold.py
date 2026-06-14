"""
Aayu Project Scaffolding Audit (Sprint 30)

Validates that Aayu can successfully package a runnable application folder structure.
Tests imports and runs real HTTP requests against the modular codebase.
"""

import os
import sys
import shutil

# Ensure prototype is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.lexer import Lexer
from prototype.compiler_v2.parser import AayuParser
from prototype.compiler_v2.semantic_analyzer import SemanticAnalyzer
from prototype.compiler_v2.ir_generator import IRGenerator
from prototype.compiler_v2.schema_generator import SchemaGenerator
from prototype.compiler_v2.app_packager import AppPackager

def execute_scaffold_test(name: str, source: str) -> bool:
    print(f"\\n--- Running Scaffold Audit for {name} ---")
    try:
        # 1. Front-End
        tokens = Lexer(source).tokenize()
        ast = AayuParser(tokens).parse()
        sem_result = SemanticAnalyzer().analyze(ast)
        if not sem_result.valid:
            print(f"  [FAIL] Semantic Analysis Failed: {sem_result.errors}")
            return False

        # 2. Intermediate Representation
        ir = IRGenerator().generate(ast)
        schema = SchemaGenerator().generate(ir)
        
        # 3. Scaffold Application
        app_dir = os.path.join(os.path.dirname(__file__), f"generated_{name.lower()}_app")
        if os.path.exists(app_dir):
            shutil.rmtree(app_dir)
            
        packager = AppPackager(app_dir)
        packager.package(schema)
        
        # Assert files exist
        expected_files = [
            "__init__.py", "database.py", "models.py", "schemas.py", 
            "main.py", "requirements.txt", "README.md"
        ]
        for f in expected_files:
            if not os.path.exists(os.path.join(app_dir, f)):
                print(f"  [FAIL] Missing expected file: {f}")
                return False
                
        if not os.path.exists(os.path.join(app_dir, "routers", "__init__.py")):
            print("  [FAIL] Missing routers directory or __init__.py")
            return False
            
        print(f"  [PASS] Application successfully scaffolded to {app_dir}")
        
        # 4. Dynamic Import Test
        # Add experiments directory to path so we can import the generated package
        experiments_dir = os.path.dirname(__file__)
        if experiments_dir not in sys.path:
            sys.path.insert(0, experiments_dir)
            
        module_name = f"generated_{name.lower()}_app.main"
        try:
            import importlib
            main_module = importlib.import_module(module_name)
        except Exception as e:
            print(f"  [FAIL] IMPORT ERROR: {type(e).__name__}: {e}")
            return False
            
        print("  [PASS] Successfully imported main.app with all internal relative dependencies")
        
        # 5. FastAPI TestClient Validation
        from fastapi.testclient import TestClient
        client = TestClient(main_module.app)
        
        # Health check
        res = client.get("/")
        if res.status_code != 200 or res.json() != {"status": "ok"}:
            print(f"  [FAIL] GET / healthcheck failed: {res.status_code}")
            return False
        print("  [PASS] GET / Health Check -> 200 OK")
        
        # Find test entity
        entity_to_test = None
        for table_name in ["patient", "student", "product"]:
            if hasattr(main_module.models, "".join(x.title() for x in table_name.split("_"))):
                entity_to_test = table_name
                break
                
        if not entity_to_test:
            print("  [PASS] No standard entities found to test HTTP CRUD, but code compiled successfully.")
            return True
            
        print(f"\\n  Testing HTTP Endpoints for: {entity_to_test}")
        
        # POST
        post_res = client.post(f"/{entity_to_test}/", json={})
        if post_res.status_code != 200:
            print(f"  [FAIL] POST /{entity_to_test}/ returned {post_res.status_code}")
            return False
        created_id = post_res.json()["id"]
        print(f"  [PASS] POST /{entity_to_test}/ -> 200 OK")
        
        # GET List
        get_list = client.get(f"/{entity_to_test}/")
        if get_list.status_code != 200:
            print(f"  [FAIL] GET /{entity_to_test}/ returned {get_list.status_code}")
            return False
        print(f"  [PASS] GET /{entity_to_test}/ -> 200 OK")
        
        # PUT
        put_res = client.put(f"/{entity_to_test}/{created_id}", json={})
        if put_res.status_code != 200:
            print(f"  [FAIL] PUT /{entity_to_test}/{{id}} returned {put_res.status_code}")
            return False
        print(f"  [PASS] PUT /{entity_to_test}/{{id}} -> 200 OK")
        
        # DELETE
        del_res = client.delete(f"/{entity_to_test}/{created_id}")
        if del_res.status_code != 200:
            print(f"  [FAIL] DELETE /{entity_to_test}/{{id}} returned {del_res.status_code}")
            return False
        print(f"  [PASS] DELETE /{entity_to_test}/{{id}} -> 200 OK")

        return True
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"  [FAIL] PIPELINE CRASH: {type(e).__name__}: {e}")
        return False

def run_audit():
    print("\\n" + "=" * 60)
    print("  AAYU PROJECT SCAFFOLDING AUDIT (SPRINT 30)")
    print("=" * 60)

    all_passed = True

    source = """system Hospital
entities:
  patient (actor)
  doctor (actor)
"""
    if execute_scaffold_test("Hospital", source):
        print("=> TEST VERDICT: SUCCESS")
    else:
        print("=> TEST VERDICT: FAILED")
        all_passed = False

    print("\\n" + "=" * 60)
    if all_passed:
        print("  ALL TESTS PASSED. RUNNABLE APPLICATION SCAFFOLDING VERIFIED!")
    else:
        print("  SOME TESTS FAILED")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
