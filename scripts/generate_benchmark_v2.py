"""
=============================================================================
FILE: generate_benchmark_v2.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import csv
import os
import random

def generate_benchmark_v2():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hybrid_path = os.path.join(base_dir, 'data', 'corpus_v1_hybrid_100k.csv')
    benchmark_path = os.path.join(base_dir, 'data', 'benchmark_v2_500.csv')

    # Base sets to draw from
    functional = [
        "mujhe scalable e-commerce app chahiye", "payment integration ke sath website", 
        "realtime chat app bana do", "fast database hona chahiye", "microservices lagani hain"
    ]
    ambiguous = [
        "ekdum mast app banao", "idea hai startup ka", "viral hona chahiye",
        "best app chahiye duniya ki", "next level cheez banani hai"
    ]
    negation = [
        "mujhe sql nahi chahiye mongodb use karo", "slow nahi hona chahiye", 
        "no downtime acceptable", "payment fail na ho", "backend pe nodejs mat use karna"
    ]
    
    # Try to load real pain points from hybrid corpus
    pain_points = []
    if os.path.exists(hybrid_path):
        with open(hybrid_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pain_points.append(row['phrase'])
                
    if len(pain_points) < 100:
        pain_points.extend([
            "paise kat gaye refund do", "app bar bar hang ho rahi hai", 
            "data chori hone ka dar hai", "kaha click karu samajh nahi aa raha",
            "slow load ho raha hai"
        ] * 20)

    benchmark_cases = []
    case_id = 1
    
    # 1. 100 Functional
    for i in range(100):
        benchmark_cases.append({
            "id": case_id, "input": random.choice(functional) + f" {i}", 
            "category": "functional", "source": "benchmark_v2_generator", "expected_result": "success"
        })
        case_id += 1

    # 2. 100 Ambiguous
    for i in range(100):
        benchmark_cases.append({
            "id": case_id, "input": random.choice(ambiguous) + f" {i}", 
            "category": "ambiguous", "source": "benchmark_v2_generator", "expected_result": "clarification_required"
        })
        case_id += 1

    # 3. 100 Negation
    for i in range(100):
        benchmark_cases.append({
            "id": case_id, "input": random.choice(negation) + f" {i}", 
            "category": "negation", "source": "benchmark_v2_generator", "expected_result": "success"
        })
        case_id += 1

    # 4. 100 Pain Point (Emotional)
    for i in range(100):
        benchmark_cases.append({
            "id": case_id, "input": pain_points[i % len(pain_points)], 
            "category": "emotional", "source": "corpus_v1_hybrid", "expected_result": "clarification_required"
        })
        case_id += 1

    # 5. 100 Mixed (Functional + Negation + Emotion)
    mixed = [
        "payment system chahiye par fraud ka dar hai", 
        "e-commerce app banao jo kabhi hang na ho",
        "scalable database chahiye kyunki slow UI bohot pareshan karti hai"
    ]
    for i in range(100):
        benchmark_cases.append({
            "id": case_id, "input": random.choice(mixed) + f" {i}", 
            "category": "mixed", "source": "benchmark_v2_generator", "expected_result": "clarification_required"
        })
        case_id += 1

    with open(benchmark_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'input', 'category', 'source', 'expected_result'])
        writer.writeheader()
        writer.writerows(benchmark_cases)

    print(f"Benchmark v2 successfully generated with 500 perfectly balanced cases at {benchmark_path}")

if __name__ == "__main__":
    generate_benchmark_v2()
