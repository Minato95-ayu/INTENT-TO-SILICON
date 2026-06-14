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

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prototype.compiler_v2.lexer import Lexer
from prototype.compiler_v2.parser import AayuParser
from prototype.compiler_v2.semantic_analyzer import SemanticAnalyzer
from prototype.compiler_v2.ir_generator import IRGenerator
from prototype.compiler_v2.schema_generator import SchemaGenerator
from prototype.compiler_v2.sql_generator import SQLGenerator
from prototype.compiler_v2.sqlalchemy_generator import SQLAlchemyGenerator

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

        # 4. ORM Compilation & Execution
        orm_code = SQLAlchemyGenerator().generate(schema)
        
        temp_file = os.path.join(os.path.dirname(__file__), f"_release_{name.lower()}.py")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(orm_code)
            
        spec = importlib.util.spec_from_file_location(f"models_{name}", temp_file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[f"models_{name}"] = module
        spec.loader.exec_module(module)
        print("  [PASS] ORM Code Generated & Imported")
        
        # 5. Bootstrap Database
        engine = create_engine("sqlite:///:memory:")
        module.Base.metadata.create_all(engine)
        
        inspector = inspect(engine)
        tables = set(inspector.get_table_names())
        print(f"  [PASS] Database Bootstrapped Successfully with tables: {tables}")
        
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
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
