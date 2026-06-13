import sys
import os
import json
import shutil

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'prototype', 'compiler_v2'))

from blueprint_generator import BlueprintGenerator
from skeleton_generator import SkeletonGenerator

def test_adumate_skeleton():
    print("=== Aayu Sprint 11: Skeleton Generator Test ===")
    
    intent = "Adumate Student Ecosystem"
    print(f"\nInput Intent: {intent}")
    
    # 1. Generate Blueprint
    bp_gen = BlueprintGenerator()
    blueprint = bp_gen.generate([intent])
    
    print(f"\nExtracted Concepts: {[c['concept'] for c in blueprint['_reasoning_concepts_matched']]}")
    
    # 2. Clean up previous generated project
    output_dir = os.path.join(base_dir, 'generated_project')
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        
    # 3. Generate Skeleton
    sk_gen = SkeletonGenerator()
    generated_files = sk_gen.generate(blueprint, output_dir)
    
    print("\nGenerated Skeleton Files:")
    for filepath in sorted(generated_files):
        # Print relative path for cleaner output
        rel_path = os.path.relpath(filepath, base_dir)
        print(f"  - {rel_path}")
        
    # Check if files have content
    print("\nSample Content (schema.sql):")
    schema_path = os.path.join(output_dir, 'database', 'schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r') as f:
            print(f.read()[:200] + "...\n")
            
    print("\nSample Content (frontend page):")
    # pick the first frontend file
    for f in generated_files:
        if 'frontend' in f and f.endswith('.tsx'):
            with open(f, 'r') as fp:
                print(f"[{os.path.basename(f)}]")
                print(fp.read())
            break
            
    print("[SUCCESS] Skeleton generation pipeline is working.")

if __name__ == "__main__":
    test_adumate_skeleton()
