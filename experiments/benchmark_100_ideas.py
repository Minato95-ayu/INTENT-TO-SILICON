"""
=============================================================================
FILE: benchmark_100_ideas.py
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
import json
import random

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'prototype', 'compiler_v2'))

from blueprint_generator import BlueprintGenerator
from clarification_engine import ClarificationEngine

def generate_ideas():
    domains = [
        "education", "healthcare", "agriculture", "finance", "logistics", 
        "government", "ecommerce", "social", "ai", "cybersecurity", "marketplace"
    ]
    
    modifiers = [
        "platform for", "app for", "ecosystem for", "dashboard for", 
        "network for", "system for", "aggregator for"
    ]
    
    ideas = []
    # Generate exactly 100 deterministic ideas for reproducibility
    random.seed(42)
    for _ in range(100):
        d1 = random.choice(domains)
        d2 = random.choice(domains)
        while d2 == d1:
            d2 = random.choice(domains)
        mod = random.choice(modifiers)
        idea = f"{d1} {mod} {d2}"
        ideas.append(idea)
    return ideas

def run_benchmark():
    bp_gen = BlueprintGenerator()
    cl_eng = ClarificationEngine()
    
    ideas = generate_ideas()
    
    stats = {
        "total_ideas": len(ideas),
        "blueprint_generated": 0,
        "concepts_detected": 0,
        "clarification_needed": 0,
        "total_questions_asked": 0
    }
    
    print("=== Aayu 100-Idea Benchmark Verification ===\n")
    
    for i, idea in enumerate(ideas, 1):
        # 1. Blueprint Generation & Concept Detection
        blueprint = bp_gen.generate([idea])
        extracted_concepts = [c["concept"] for c in blueprint.get("_reasoning_concepts_matched", [])]
        
        has_blueprint = len(blueprint.get("frontend_modules", [])) > 0
        has_concepts = len(extracted_concepts) > 0
        
        if has_blueprint: stats["blueprint_generated"] += 1
        if has_concepts: stats["concepts_detected"] += 1
            
        # 2. Clarification Engine
        questions = cl_eng.analyze(extracted_concepts, idea)
        needs_clarification = len(questions) > 0
        
        if needs_clarification:
            stats["clarification_needed"] += 1
            stats["total_questions_asked"] += len(questions)
            
        # Print a sample of 5 ideas to keep output clean
        if i <= 5:
            print(f"Idea #{i}: '{idea}'")
            print(f"  Concepts Detected: {extracted_concepts}")
            print(f"  Modules Generated: {len(blueprint['frontend_modules'])} Frontend, {len(blueprint['backend_modules'])} Backend")
            if questions:
                print(f"  Clarification Qs: {questions[:2]}") # Print first 2
            else:
                print("  Clarification Qs: None")
            print()
            
    print("--- Benchmark Results ---")
    print(f"Total Ideas Tested:       {stats['total_ideas']}")
    print(f"Concepts Detected:        {stats['concepts_detected']} / {stats['total_ideas']} ({(stats['concepts_detected']/stats['total_ideas'])*100:.1f}%)")
    print(f"Blueprint Generated:      {stats['blueprint_generated']} / {stats['total_ideas']} ({(stats['blueprint_generated']/stats['total_ideas'])*100:.1f}%)")
    print(f"Clarification Triggered:  {stats['clarification_needed']} / {stats['total_ideas']} ({(stats['clarification_needed']/stats['total_ideas'])*100:.1f}%)")
    print(f"Total Questions Asked:    {stats['total_questions_asked']}")
    print("\n[SUCCESS] Missing Information Detection Engine & Benchmark Complete!")

if __name__ == "__main__":
    run_benchmark()
