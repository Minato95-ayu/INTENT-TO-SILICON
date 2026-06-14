"""
Aayu Full Stack Audit (Sprint 31)

Validates that Aayu can package a runnable Full Stack application
and that the generated React+Vite frontend successfully builds.
"""

import os
import sys
import shutil
import subprocess

# Ensure prototype is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.lexer import Lexer
from prototype.compiler_v2.parser import AayuParser
from prototype.compiler_v2.semantic_analyzer import SemanticAnalyzer
from prototype.compiler_v2.ir_generator import IRGenerator
from prototype.compiler_v2.schema_generator import SchemaGenerator
from prototype.compiler_v2.app_packager import AppPackager

def execute_frontend_test(name: str, source: str) -> bool:
    print(f"\\n--- Running Full Stack Audit for {name} ---")
    try:
        # 1. Front-End Compile
        tokens = Lexer(source).tokenize()
        ast = AayuParser(tokens).parse()
        sem_result = SemanticAnalyzer().analyze(ast)
        if not sem_result.valid:
            print(f"  [FAIL] Semantic Analysis Failed")
            return False

        # 2. Schema
        ir = IRGenerator().generate(ast)
        schema = SchemaGenerator().generate(ir)
        
        # 3. Scaffold Full Stack Application
        app_dir = os.path.join(os.path.dirname(__file__), f"generated_{name.lower()}_app")
        if os.path.exists(app_dir):
            shutil.rmtree(app_dir)
            
        packager = AppPackager(app_dir)
        packager.package(schema)
        
        print(f"  [PASS] Full Stack Application scaffolded to {app_dir}")
        
        frontend_dir = os.path.join(app_dir, "frontend")
        
        # Assert frontend files exist
        expected_files = [
            "package.json", "vite.config.ts", "tsconfig.json", "index.html", 
            "src/main.tsx", "src/App.tsx", "src/services/api.ts"
        ]
        for f in expected_files:
            if not os.path.exists(os.path.join(frontend_dir, f)):
                print(f"  [FAIL] Missing expected frontend file: {f}")
                return False
                
        print("  [PASS] Frontend structural verification passed.")
        
        # 4. NPM Install
        print("  Running 'npm install'...")
        install_res = subprocess.run(["npm", "install"], cwd=frontend_dir, capture_output=True, text=True, shell=True)
        if install_res.returncode != 0:
            print(f"  [FAIL] npm install failed:\\n{install_res.stderr}")
            return False
        print("  [PASS] npm install succeeded.")
        
        # 5. NPM Build
        print("  Running 'npm run build'...")
        build_res = subprocess.run(["npm", "run", "build"], cwd=frontend_dir, capture_output=True, text=True, shell=True)
        if build_res.returncode != 0:
            print(f"  [FAIL] npm run build failed:\\n{build_res.stderr}")
            return False
        print("  [PASS] npm run build succeeded. Syntactic and structural validation of React/TS frontend confirmed.")

        return True
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"  [FAIL] PIPELINE CRASH: {type(e).__name__}: {e}")
        return False

def run_audit():
    print("\\n" + "=" * 60)
    print("  AAYU FULL STACK AUDIT (SPRINT 31)")
    print("=" * 60)

    all_passed = True

    source = """system Hospital
entities:
  patient (actor)
  doctor (actor)
"""
    if execute_frontend_test("Hospital", source):
        print("=> TEST VERDICT: SUCCESS")
    else:
        print("=> TEST VERDICT: FAILED")
        all_passed = False

    print("\\n" + "=" * 60)
    if all_passed:
        print("  ALL TESTS PASSED. INTENT TO FULL STACK BUILD VERIFIED!")
    else:
        print("  SOME TESTS FAILED")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
