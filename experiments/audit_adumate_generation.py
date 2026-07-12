"""
=============================================================================
FILE: audit_adumate_generation.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import sys
import os
import shutil
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'prototype', 'compiler_v2'))

from blueprint_generator import BlueprintGenerator
from database_generator import DatabaseGenerator
from api_generator import APIGenerator
from frontend_generator import FrontendGenerator

def run_adumate_audit():
    print("=== Sprint 12: Adumate End-to-End Generation Audit ===")
    
    intent = "Student ecosystem app with: Library, Hostel, Jobs, Tutors, OTP Login, UPI Payment"
    print(f"\n[1] Input Intent:\n\"{intent}\"")
    
    # 1. Generate Blueprint
    bp_gen = BlueprintGenerator()
    blueprint = bp_gen.generate([intent])
    
    concepts = [c["concept"] for c in blueprint.get("_reasoning_concepts_matched", [])]
    print(f"\n[2] Extracted Concepts:\n{concepts}")
    
    # 2. Setup Output Dir
    output_dir = os.path.join(base_dir, 'generated_project')
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        
    db_dir = os.path.join(output_dir, 'database')
    api_dir = os.path.join(output_dir, 'backend', 'api')
    frontend_dir = os.path.join(output_dir, 'frontend', 'components')
    
    os.makedirs(db_dir, exist_ok=True)
    os.makedirs(api_dir, exist_ok=True)
    os.makedirs(frontend_dir, exist_ok=True)
    
    generated_files = []
    
    # 3. Database Synthesis
    print("\n[3] Synthesizing Database Schema...")
    db_gen = DatabaseGenerator()
    sql_schema = db_gen.generate_sql(blueprint.get("data_entities", []))
    
    schema_path = os.path.join(db_dir, 'schema.sql')
    with open(schema_path, 'w') as f:
        f.write(sql_schema)
    generated_files.append(schema_path)
    
    # 4. API Synthesis
    print("[4] Synthesizing CRUD APIs and Pydantic Schemas...")
    api_gen = APIGenerator()
    for entity in blueprint.get("data_entities", []):
        api_code = api_gen.generate_api_code(entity)
        api_path = os.path.join(api_dir, f"{entity}_api.py")
        with open(api_path, 'w') as f:
            f.write(api_code)
        generated_files.append(api_path)
        
    # 5. Frontend Synthesis
    print("[5] Synthesizing React Components...")
    fe_gen = FrontendGenerator()
    for module in blueprint.get("frontend_modules", []):
        fe_code = fe_gen.generate_component_code(module, blueprint.get("data_entities", []))
        
        # camel case naming
        name_camel = ''.join(x.title() for x in module.split('_'))
        fe_path = os.path.join(frontend_dir, f"{name_camel}.tsx")
        with open(fe_path, 'w') as f:
            f.write(fe_code)
        generated_files.append(fe_path)
        
    print("\n=== Audit Results ===")
    print(f"Total Source Code Files Synthesized: {len(generated_files)}")
    
    print("\n--- SAMPLE: SQL Schema (schema.sql snippet) ---")
    print("\n".join(sql_schema.split("\n")[:25]) + "\n...")
    
    print("\n--- SAMPLE: API Code (library_booking_api.py snippet) ---")
    lb_api = os.path.join(api_dir, 'library_booking_api.py')
    if os.path.exists(lb_api):
        with open(lb_api, 'r') as f:
            print("\n".join(f.read().split("\n")[:20]) + "\n...")
            
    print("\n--- SAMPLE: React Form (BookingForm.tsx snippet) ---")
    bf_tsx = os.path.join(frontend_dir, 'BookingForm.tsx')
    if os.path.exists(bf_tsx):
        with open(bf_tsx, 'r') as f:
            print("\n".join(f.read().split("\n")[:20]) + "\n...")
            
    print("\n[SUCCESS] Deterministic Code Synthesis Complete! Aayu built real software.")

if __name__ == "__main__":
    run_adumate_audit()
