"""
=============================================================================
FILE: test_v2_regression.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import json
import os
import sys

# Add compiler_v2 to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prototype', 'compiler_v2'))
from aayu.compiler.v2.compiler import CompilerV2

def test_regression():
    c = CompilerV2()
    
    with open('../data/intent_ir_examples_50.json', 'r') as f:
        gold_data = json.load(f)
        
    with open('../data/unseen_examples_20.json', 'r') as f:
        unseen_data = json.load(f)
        
    all_data = gold_data + unseen_data
    
    passed = 0
    negated_emotion_passed = 0
    negated_emotion_total = 0
    
    print("Running IR Regression Tests on V2 Compiler...")
    
    for item in all_data:
        expected = item['intent_ir']
        predicted = c.process(item['input'])
        
        # Track negated emotion specific tests
        if "dar nahi" in item['input'] or "bot se mujhe koi problem nahi" in item['input']:
            negated_emotion_total += 1
            if predicted['primary_problem'] is None:
                negated_emotion_passed += 1
                
        if expected['primary_problem'] == predicted['primary_problem'] and expected['module'] == predicted['module']:
            passed += 1
        else:
            print(f"FAILED on '{item['input']}'")
            print(f"Expected: {expected['primary_problem']}")
            print(f"Got: {predicted['primary_problem']}")
            
    print(f"\nTotal Passed: {passed} / {len(all_data)}")
    if negated_emotion_total > 0:
        print(f"Negated Emotion Accuracy: {(negated_emotion_passed/negated_emotion_total)*100:.1f}%")
    
if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
    test_regression()
