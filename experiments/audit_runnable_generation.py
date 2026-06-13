import sys
import os
import shutil
import subprocess

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'prototype', 'compiler_v2'))

from blueprint_generator import BlueprintGenerator
from manifest_generator import ManifestGenerator
from schema_synthesizer import SchemaSynthesizer
from database_generator import DatabaseGenerator
from api_generator import APIGenerator
from frontend_generator import FrontendGenerator
from runtime_generator import RuntimeGenerator

def run_runnable_audit():
    print("=== Production Runtime Generation Audit ===")
    
    if len(sys.argv) > 1:
        intent = sys.argv[1]
    else:
        intent = "Student ecosystem app with: Library, Hostel, Jobs, Tutors, OTP Login, UPI Payment"
        
    print(f"\n[1] Input Intent:\n\"{intent}\"")
    
    bp_gen = BlueprintGenerator()
    blueprint = bp_gen.generate([intent])
    concepts = [c["concept"] for c in blueprint.get("_reasoning_concepts_matched", [])]
    
    # Generate Manifest
    print("\n[2] Generating Application Manifest...")
    manifest_gen = ManifestGenerator()
    manifest_yaml = manifest_gen.generate(intent, blueprint, concepts)
    
    # Setup Output Dir
    output_dir = os.path.join(base_dir, 'generated_project')
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        
    backend_dir = os.path.join(output_dir, 'backend')
    routers_dir = os.path.join(backend_dir, 'routers')
    frontend_dir = os.path.join(output_dir, 'frontend')
    src_dir = os.path.join(frontend_dir, 'src')
    components_dir = os.path.join(src_dir, 'components')
    
    os.makedirs(routers_dir, exist_ok=True)
    os.makedirs(components_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, 'manifest.yaml'), 'w') as f:
        f.write(manifest_yaml)
    
    # Schema Synthesis
    print("\n[3] Synthesizing Schema from Domain Ontology...")
    schema_syn = SchemaSynthesizer(output_dir)
    data_entities = blueprint.get("data_entities", [])
    resolved_schema = schema_syn.synthesize(data_entities)
    
    # Backend Synthesis
    print("\n[4] Synthesizing Backend (SQLAlchemy + FastAPI)...")
    db_gen = DatabaseGenerator()
    api_gen = APIGenerator()
    rt_gen = RuntimeGenerator()
    
    # DB Setup
    with open(os.path.join(backend_dir, 'database.py'), 'w') as f:
        f.write(db_gen.generate_database_setup())
        
    # DB Models
    with open(os.path.join(backend_dir, 'models.py'), 'w') as f:
        f.write(db_gen.generate_models(resolved_schema))
        
    # Pydantic Schemas
    with open(os.path.join(backend_dir, 'schemas.py'), 'w') as f:
        f.write(api_gen.generate_schemas(resolved_schema))
        
    # API Routers
    for entity in data_entities:
        with open(os.path.join(routers_dir, f"{entity}_api.py"), 'w') as f:
            f.write(api_gen.generate_api_code(entity))
            
    # Main.py & Requirements
    main_code, reqs = rt_gen.generate_backend_runtime(blueprint.get("data_entities", []))
    with open(os.path.join(backend_dir, 'main.py'), 'w') as f:
        f.write(main_code)
    with open(os.path.join(backend_dir, 'requirements.txt'), 'w') as f:
        f.write(reqs)
        
    # Frontend Synthesis
    print("\n[5] Synthesizing Frontend (React + Vite)...")
    fe_gen = FrontendGenerator()
    for module in blueprint.get("frontend_modules", []):
        fe_code = fe_gen.generate_component_code(module, data_entities, resolved_schema)
        name_camel = ''.join(x.title() for x in module.split('_'))
        with open(os.path.join(components_dir, f"{name_camel}.tsx"), 'w') as f:
            f.write(fe_code)
            
    # Frontend Scaffolding
    pj, vc, tc, main_tsx, app_tsx, index_html = rt_gen.generate_frontend_runtime(blueprint.get("frontend_modules", []))
    with open(os.path.join(frontend_dir, 'package.json'), 'w') as f: f.write(pj)
    with open(os.path.join(frontend_dir, 'vite.config.ts'), 'w') as f: f.write(vc)
    with open(os.path.join(frontend_dir, 'tsconfig.json'), 'w') as f: f.write(tc)
    with open(os.path.join(frontend_dir, 'index.html'), 'w') as f: f.write(index_html)
    with open(os.path.join(src_dir, 'main.tsx'), 'w') as f: f.write(main_tsx)
    with open(os.path.join(src_dir, 'App.tsx'), 'w') as f: f.write(app_tsx)
    
    print("\n=== Success Criteria Checks ===")
    
    checks = [
        os.path.join(backend_dir, 'main.py'),
        os.path.join(backend_dir, 'models.py'),
        os.path.join(backend_dir, 'database.py'),
        os.path.join(frontend_dir, 'package.json')
    ]
    
    for c in checks:
        exists = os.path.exists(c)
        status = "PASS" if exists else "FAIL"
        print(f"{os.path.basename(c)} exists: {status}")
        
    # Compile Check
    print("\nRunning `python -m py_compile main.py`...")
    try:
        subprocess.check_call([sys.executable, "-m", "py_compile", os.path.join(backend_dir, 'main.py')])
        print("Compile Check: PASS")
    except subprocess.CalledProcessError:
        print("Compile Check: FAIL")

if __name__ == "__main__":
    run_runnable_audit()
