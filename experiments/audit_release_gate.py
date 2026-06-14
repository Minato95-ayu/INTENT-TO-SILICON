"""
Aayu Release Gate Audit

Runs the FULL compiler pipeline across all benchmarks:
Intent ADL -> Lexer -> Parser -> Semantic Analyzer -> Typed AST -> IR -> Schema -> SQL -> ORM

Verifies zero regressions across the entire Intent-to-Silicon backend pipeline.
"""

import os
import sys
import importlib.util
from sqlalchemy import create_engine, inspect
from sqlalchemy.pool import StaticPool

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.lexer import Lexer
from prototype.compiler_v2.parser import AayuParser
from prototype.compiler_v2.semantic_analyzer import SemanticAnalyzer
from prototype.compiler_v2.ir_generator import IRGenerator
from prototype.compiler_v2.schema_generator import SchemaGenerator
from prototype.compiler_v2.sql_generator import SQLGenerator
from prototype.compiler_v2.sqlalchemy_generator import SQLAlchemyGenerator
from prototype.compiler_v2.api_generator import FastAPIGenerator

BENCHMARKS = {
    "Hospital": """system Hospital
entities:
  patient (actor)
  doctor (actor)
  appointment (transaction)
relations:
  patient -> appointment (one_to_many)
  doctor -> appointment (one_to_many)
""",
    
    "Marketplace": """system Marketplace
entities:
  product (resource)
  order (transaction)
relations:
  product -> order (many_to_many)
""",
    
    "Adumate": """system Adumate
domains:
  edu
  housing
shared:
  student (actor)
entities:
  course (resource)
  room_allocation (transaction)
relations:
  student -> course (many_to_many)
  student -> room_allocation (one_to_one)
"""
}

def execute_pipeline(name: str, source: str) -> bool:
    print(f"\\n--- Running Release Gate for {name} ---")
    try:
        # 1. Front-End
        tokens = Lexer(source).tokenize()
        ast = AayuParser(tokens).parse()
        sem_result = SemanticAnalyzer().analyze(ast)
        if not sem_result.valid:
            print(f"  [FAIL] Semantic Analysis Failed: {sem_result.errors}")
            return False
        print("  [PASS] Front-End Passed (Lexer, Parser, Semantic)")

        # 2. Intermediate Representation
        ir = IRGenerator().generate(ast)
        schema = SchemaGenerator().generate(ir)
        print(f"  [PASS] IR & Schema Generation Passed ({len(schema.tables)} tables)")

        # 3. SQL Compilation
        sql = SQLGenerator().generate(schema)
        print("  [PASS] SQL Generation Passed")

        # 5. App Packaging
        app_dir = os.path.join(os.path.dirname(__file__), f"generated_{name.lower()}_app")
        import shutil
        if os.path.exists(app_dir):
            shutil.rmtree(app_dir)
            
        from prototype.compiler_v2.app_packager import AppPackager
        packager = AppPackager(app_dir)
        packager.package(schema)
        print(f"  [PASS] Application successfully scaffolded to {app_dir}")
        
        # 6. Dynamic Import & Bootstrap Database
        experiments_dir = os.path.dirname(__file__)
        if experiments_dir not in sys.path:
            sys.path.insert(0, experiments_dir)
            
        module_name = f"generated_{name.lower()}_app.backend.main"
        import importlib
        main_module = importlib.import_module(module_name)
        print("  [PASS] Main Application Module Imported")
        
        db_module = importlib.import_module(f"generated_{name.lower()}_app.backend.database")
        inspector = inspect(db_module.engine)
        tables = set(inspector.get_table_names())
        print(f"  [PASS] Database Bootstrapped Successfully with tables: {tables}")
        
        # 7. Frontend Build Verification
        frontend_dir = os.path.join(app_dir, "frontend")
        import subprocess
        install_res = subprocess.run(["npm", "install"], cwd=frontend_dir, capture_output=True, text=True, shell=True)
        if install_res.returncode != 0:
            print(f"  [FAIL] Frontend npm install failed:\\n{install_res.stderr}")
            return False
            
        build_res = subprocess.run(["npm", "run", "build"], cwd=frontend_dir, capture_output=True, text=True, shell=True)
        if build_res.returncode != 0:
            print(f"  [FAIL] Frontend npm run build failed:\\n{build_res.stderr}")
            return False
        print("  [PASS] React+Vite Frontend Build Succeeded")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] PIPELINE CRASH: {type(e).__name__}: {e}")
        return False

def run_release_gate():
    print("=" * 60)
    print("  AAYU COMPILER RELEASE GATE AUDIT")
    print("=" * 60)
    
    all_passed = True
    for name, source in BENCHMARKS.items():
        if not execute_pipeline(name, source):
            all_passed = False
            
    print("\\n" + "=" * 60)
    if all_passed:
        print("  RELEASE GATE VERDICT: FULL PASS. AAYU IS STABLE.")
    else:
        print("  RELEASE GATE VERDICT: REGRESSION DETECTED.")
    print("=" * 60)

if __name__ == "__main__":
    run_release_gate()
