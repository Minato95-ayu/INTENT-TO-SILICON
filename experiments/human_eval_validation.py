"""
=============================================================================
FILE: human_eval_validation.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import csv
import sys
from collections import Counter

base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(base_dir, 'prototype'))

from nlp_engine import load_libraries, process_single_input

def calculate_cohens_kappa(rater1, rater2):
    """Calculate Cohen's Kappa score manually to avoid external dependencies."""
    if len(rater1) != len(rater2):
        raise ValueError("Raters must have the same number of evaluations.")
        
    n = len(rater1)
    
    # Observed agreement
    agreements = sum(1 for r1, r2 in zip(rater1, rater2) if r1 == r2)
    po = agreements / n
    
    # Expected agreement
    counts1 = Counter(rater1)
    counts2 = Counter(rater2)
    
    pe = 0
    categories = set(rater1).union(set(rater2))
    for cat in categories:
        pe += (counts1[cat] / n) * (counts2[cat] / n)
        
    if 1 - pe == 0:
        return 1.0 # Perfect agreement, avoid division by zero
        
    kappa = (po - pe) / (1 - pe)
    return kappa

def validate_human_eval():
    func_lib, emotion_lib = load_libraries()
    
    data_path = os.path.join(base_dir, 'data', 'mock_human_responses.csv')
    if not os.path.exists(data_path):
        print(f"File not found: {data_path}")
        return
        
    human_labels = []
    system_labels = []
    actual_labels = []
    
    with open(data_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            phrase = row['phrase']
            actual = row['actual_category']
            human = row['human_label']
            
            # Get System Label
            metrics = process_single_input(phrase, func_lib, emotion_lib, headless_reply="1")
            
            if metrics["status"] == "fail_hard":
                system = "fail_hard"
            elif metrics.get("matched_emotions"):
                system = metrics["matched_emotions"][0]
            elif metrics.get("matched_func_categories"):
                system = metrics["matched_func_categories"][0]
            else:
                system = "fail_hard"
                
            if human != system:
                print(f"Mismatch! Phrase: '{phrase}' | Human: {human} | System: {system}")
            
            human_labels.append(human)
            system_labels.append(system)
            actual_labels.append(actual)
            
    # Calculate Human vs Actual (excluding 'mixed')
    human_correct = 0
    non_mixed = 0
    for h, a in zip(human_labels, actual_labels):
        if a != "mixed":
            non_mixed += 1
            if h == a:
                human_correct += 1
    human_agreement = (human_correct / non_mixed) * 100 if non_mixed > 0 else 0
    
    # Calculate System vs Human
    system_correct = sum(1 for h, s in zip(human_labels, system_labels) if h == s)
    system_agreement = (system_correct / len(human_labels)) * 100
    
    # Calculate Cohen's Kappa (System vs Human)
    kappa = calculate_cohens_kappa(human_labels, system_labels)
    
    print("========================================")
    print(" HUMAN EVALUATION VALIDATION REPORT")
    print("========================================")
    print(f"\nTotal Phrases Evaluated: {len(human_labels)}")
    print(f"Human Agreement (vs Ground Truth): {human_agreement:.1f}%")
    print(f"System Agreement (vs Human Label): {system_agreement:.1f}%")
    print(f"Cohen Kappa Score                : {kappa:.2f}")
    
    print("\nInterpretation for Paper:")
    if kappa > 0.8:
        print("-> Excellent Agreement: System perfectly mirrors human intent interpretation.")
    elif kappa > 0.6:
        print("-> Substantial Agreement: System strongly aligns with human interpretation. Ready for publication!")
    else:
        print("-> Moderate/Weak Agreement: More taxonomy refinement needed.")
        
    print("========================================")

if __name__ == "__main__":
    validate_human_eval()
