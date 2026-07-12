"""
=============================================================================
FILE: unseen_validation.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prototype', 'compiler_v2'))
from compiler.frontend.compiler import CompilerV2

def run_benchmark():
    c = CompilerV2()
    
    with open('../data/unseen_examples_50.json', 'r') as f:
        data = json.load(f)
        
    total = len(data)
    prob_correct = 0
    mod_correct = 0
    neg_total = 0
    neg_passed = 0
    
    print("====================================")
    print("UNSEEN INPUT VALIDATION BENCHMARK")
    print("====================================\n")
    
    for item in data:
        expected = item['intent_ir']
        predicted = c.process(item['input'])
        
        if expected['primary_problem'] == predicted['primary_problem']:
            prob_correct += 1
            
        if expected['module'] == predicted['module']:
            mod_correct += 1
            
        # Check negated emotion
        if "nahi" in item['input'] and expected['primary_problem'] is None:
            neg_total += 1
            if predicted['primary_problem'] is None:
                neg_passed += 1
            
    prob_acc = (prob_correct / total) * 100
    mod_acc = (mod_correct / total) * 100
    neg_acc = (neg_passed / neg_total * 100) if neg_total > 0 else 0
    
    print(f"Total Examples: {total}\n")
    print(f"Problem Accuracy:        {prob_acc:.1f}%")
    print(f"Module Accuracy:         {mod_acc:.1f}%")
    if neg_total > 0:
        print(f"Negation Accuracy:       {neg_acc:.1f}%")
    
    overall = (prob_acc + mod_acc) / 2
    print(f"\nOverall Unseen Score:    {overall:.1f}%")
    print("====================================")

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
    run_benchmark()
