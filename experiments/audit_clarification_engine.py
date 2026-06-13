"""
Aayu Clarification Engine — Full Pipeline Audit

Demonstrates the complete flow:
    Vague Intent → Concept Extraction → Gap Detection →
    Clarification Questions → Simulated Answers →
    Intent Lock → Intent Validation → Blueprint → Schema → CRUD → Build

Usage:
    python experiments/audit_clarification_engine.py
    python experiments/audit_clarification_engine.py "Mujhe hospital app banana hai"
"""

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
from clarification_engine import ClarificationEngine, ClarificationResult, ResolvedIntent
from intent_validator import IntentValidator


# ============================================================
# SIMULATED ANSWERS
# In Sprint 16, answers are hardcoded for deterministic testing.
# Sprint 16.1 will add stdin-based interactive input.
# ============================================================
SIMULATED_ANSWERS = {
    # Domain clarification (when intent is too vague to detect domain)
    "domain": "healthcare",
    # Healthcare domain
    "authentication": "yes",
    "compliance": "yes",
    "telemedicine": "no",
    "payments": "yes",
    # Education domain
    "notifications": "yes",
    "content_delivery": "no",
    # Agriculture domain
    "localization": "yes",
    "offline_support": "no",
    # Logistics domain
    "tracking": "yes",
    "routing": "no",
    # Generic
    "fraud_detection": "no",
    "accessibility": "no",
    "shipping": "no",
    "inventory": "no",
    "moderation": "no",
    "media_storage": "no",
    "model_hosting": "no",
    "cost_control": "no",
    "data_privacy": "no",
    "audit_logging": "no",
    "escrow": "no",
    "reviews": "no",
    "search": "no",
}


def print_section(title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def run_clarification_audit():
    # ---- Step 0: Get Intent ----
    if len(sys.argv) > 1:
        raw_intent = sys.argv[1]
    else:
        raw_intent = "Mujhe hospital app banana hai"

    print_section("AAYU CLARIFICATION ENGINE AUDIT")

    print(f"\nINPUT INTENT:")
    print(f'  "{raw_intent}"')

    # ---- Step 1: Initial Blueprint (from vague intent) ----
    print_section("PHASE 1: CONCEPT EXTRACTION")

    bp_gen = BlueprintGenerator()
    initial_blueprint = bp_gen.generate([raw_intent])
    concepts = [c["concept"] for c in initial_blueprint.get("_reasoning_concepts_matched", [])]

    print(f"\nEXTRACTED CONCEPTS:")
    for c in concepts:
        print(f"  • {c}")

    # ---- Step 2: Clarification Analysis ----
    print_section("PHASE 2: GAP DETECTION & CLARIFICATION")

    clarification_engine = ClarificationEngine()
    clarification_result = clarification_engine.analyze(concepts, raw_intent)

    print(f"\nDOMAIN: {clarification_engine._extract_domain(raw_intent)}")
    print(f"\nDETECTED CONCEPTS: {clarification_result.detected_concepts}")
    print(f"MISSING CONCEPTS:  {clarification_result.missing_concepts}")

    print(f"\nCONFIDENCE SCORES:")
    for concept, score in sorted(clarification_result.confidence.items(), key=lambda x: x[1], reverse=True):
        bar = "#" * int(score * 20) + "." * (20 - int(score * 20))
        print(f"  {concept:25s} [{bar}] {score:.2f}")

    print(f"\nIS COMPLETE: {clarification_result.is_complete}")

    if clarification_result.is_complete:
        print("\n[OK] No clarification needed. Intent is already complete.")
    else:
        print(f"\nQUESTIONS ({len(clarification_result.questions)}):")
        for i, q in enumerate(clarification_result.questions, 1):
            print(f"  {i}. [{q['concept']}] {q['question']}")

    # ---- Step 3: Resolve with Simulated Answers ----
    print_section("PHASE 3: INTENT RESOLUTION")

    # Only answer the questions that were asked
    answers = {}
    for q in clarification_result.questions:
        concept = q["concept"]
        answer = SIMULATED_ANSWERS.get(concept, "no")
        answers[concept] = answer
        print(f"  Q: {q['question']}")
        print(f"  A: {answer}")
        print()

    resolved = clarification_engine.resolve(raw_intent, answers)

    print(f"RESOLVED INTENT:")
    print(f"  Domain:   {resolved.domain}")
    print(f"  Entities: {resolved.entities}")
    print(f"  Features: {resolved.features}")

    # ---- Step 4: Lock Intent ----
    print_section("PHASE 4: INTENT LOCK")

    locked_intent = clarification_engine.lock_intent(resolved)
    print(f"\nLOCKED INTENT:")
    print(f'  "{locked_intent}"')

    # ---- Step 5: Intent Validation ----
    print_section("PHASE 5: INTENT VALIDATION")

    validator = IntentValidator()
    validation = validator.validate(clarification_result, resolved)

    if validation.is_valid:
        print("\n[PASS] Intent Validation: PASSED")
    else:
        print("\n[FAIL] Intent Validation: FAILED")
        for e in validation.errors:
            print(f"  ERROR: {e}")
        sys.exit(1)

    if validation.warnings:
        for w in validation.warnings:
            print(f"  WARNING: {w}")

    # ---- Step 6: Full Pipeline (Blueprint -> Schema -> CRUD -> Build) ----
    print_section("PHASE 6: COMPILATION PIPELINE")

    print(f'\nCompiling locked intent: "{locked_intent}"')

    # Re-generate blueprint from locked intent
    blueprint = bp_gen.generate([locked_intent])
    locked_concepts = [c["concept"] for c in blueprint.get("_reasoning_concepts_matched", [])]

    print(f"\nBLUEPRINT CONCEPTS: {locked_concepts}")
    print(f"DATA ENTITIES:      {blueprint.get('data_entities', [])}")

    # Generate Manifest
    manifest_gen = ManifestGenerator()
    manifest_yaml = manifest_gen.generate(locked_intent, blueprint, locked_concepts)

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
    print("\n[Schema Synthesis]...")
    schema_syn = SchemaSynthesizer(output_dir)
    data_entities = blueprint.get("data_entities", [])
    resolved_schema = schema_syn.synthesize(data_entities)
    print(f"  Resolved {len(resolved_schema)} entities")
    status_schema = "PASS"

    # Backend Synthesis
    print("\n[Backend Synthesis]...")
    db_gen = DatabaseGenerator()
    api_gen = APIGenerator()
    rt_gen = RuntimeGenerator()

    with open(os.path.join(backend_dir, 'database.py'), 'w') as f:
        f.write(db_gen.generate_database_setup())
    with open(os.path.join(backend_dir, 'models.py'), 'w') as f:
        f.write(db_gen.generate_models(resolved_schema))
    with open(os.path.join(backend_dir, 'schemas.py'), 'w') as f:
        f.write(api_gen.generate_schemas(resolved_schema))
    for entity in data_entities:
        with open(os.path.join(routers_dir, f"{entity}_api.py"), 'w') as f:
            f.write(api_gen.generate_api_code(entity))
    main_code, reqs = rt_gen.generate_backend_runtime(data_entities)
    with open(os.path.join(backend_dir, 'main.py'), 'w') as f:
        f.write(main_code)
    with open(os.path.join(backend_dir, 'requirements.txt'), 'w') as f:
        f.write(reqs)

    # Frontend Synthesis
    print("[Frontend Synthesis]...")
    fe_gen = FrontendGenerator()
    for module in blueprint.get("frontend_modules", []):
        fe_code = fe_gen.generate_component_code(module, data_entities, resolved_schema)
        name_camel = ''.join(x.title() for x in module.split('_'))
        with open(os.path.join(components_dir, f"{name_camel}.tsx"), 'w') as f:
            f.write(fe_code)
    pj, vc, tc, main_tsx, app_tsx, index_html = rt_gen.generate_frontend_runtime(blueprint.get("frontend_modules", []))
    with open(os.path.join(frontend_dir, 'package.json'), 'w') as f: f.write(pj)
    with open(os.path.join(frontend_dir, 'vite.config.ts'), 'w') as f: f.write(vc)
    with open(os.path.join(frontend_dir, 'tsconfig.json'), 'w') as f: f.write(tc)
    with open(os.path.join(frontend_dir, 'index.html'), 'w') as f: f.write(index_html)
    with open(os.path.join(src_dir, 'main.tsx'), 'w') as f: f.write(main_tsx)
    with open(os.path.join(src_dir, 'App.tsx'), 'w') as f: f.write(app_tsx)

    # ---- Step 7: Verification ----
    print_section("PHASE 7: VERIFICATION")

    # File existence checks
    checks = {
        'main.py': os.path.join(backend_dir, 'main.py'),
        'models.py': os.path.join(backend_dir, 'models.py'),
        'database.py': os.path.join(backend_dir, 'database.py'),
        'schemas.py': os.path.join(backend_dir, 'schemas.py'),
        'package.json': os.path.join(frontend_dir, 'package.json'),
        'index.html': os.path.join(frontend_dir, 'index.html'),
    }

    all_pass = True
    for name, path in checks.items():
        exists = os.path.exists(path)
        status = "PASS" if exists else "FAIL"
        if not exists:
            all_pass = False
        print(f"  {name:20s} {status}")

    # Python compile check
    print(f"\n  Python Compile Check:")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "py_compile", os.path.join(backend_dir, 'main.py')],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"    main.py compile:   PASS")
    except subprocess.CalledProcessError:
        print(f"    main.py compile:   FAIL")
        all_pass = False

    # ---- Final Summary ----
    print_section("FINAL AUDIT SUMMARY")

    print(f"""
  Input:          "{raw_intent}"
  Domain:         {resolved.domain}
  Questions:      {len(clarification_result.questions)}
  Answers:        {len(answers)}
  Locked Intent:  "{locked_intent}"
  Entities:       {len(data_entities)}
  Validation:     {"PASS" if validation.is_valid else "FAIL"}
  Schema:         {status_schema}
  Compile:        {"PASS" if all_pass else "FAIL"}
""")

    if all_pass:
        print("  [PASS] CLARIFICATION ENGINE AUDIT: ALL CHECKS PASSED")
    else:
        print("  [FAIL] CLARIFICATION ENGINE AUDIT: SOME CHECKS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    run_clarification_audit()
