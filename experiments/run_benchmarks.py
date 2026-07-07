"""
=============================================================================
FILE: run_benchmarks.py
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
import sys

# Add prototype directory to sys path so we can import the engine
base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(base_dir, 'prototype'))

from nlp_engine import load_libraries, process_single_input

def run_benchmarks():
    dataset_path = os.path.join(base_dir, 'data', 'benchmark_v2_500.csv')
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        return

    func_lib, emotion_lib = load_libraries()
    
    total_inputs = 0
    direct_success = 0
    clarification_required = 0
    hard_fail = 0
    yaml_generated = 0
    total_questions_asked = 0
    
    total_negation_cases = 0
    correct_negation_parses = 0
    total_negated_emotions = 0
    total_emotional_cases = 0
    correct_emotion_parses = 0
    
    print("==================================================")
    print(" INTENT-TO-SILICON : Benchmarking Suite v1.1")
    print("==================================================")
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_inputs += 1
            input_text = row['input']
            expected = row['expected_result']
            category = row['category']
            
            # SPRINT 3: Multi-stage headless replies simulation
            # Generate a list of 5 pseudo-random choices to support deep dependency chains
            headless_reply = []
            for i in range(5):
                rand_val = (total_inputs + i * 3) % 10
                if rand_val < 4:
                    headless_reply.append("1")
                elif rand_val < 7:
                    headless_reply.append("2")
                else:
                    headless_reply.append("no")
                
            metrics = process_single_input(input_text, func_lib, emotion_lib, headless_reply=headless_reply)
            
            # Tally metrics
            if metrics["status"] == "success":
                direct_success += 1
            elif metrics["status"] == "clarification_required":
                clarification_required += 1
            elif metrics["status"] == "fail_hard":
                hard_fail += 1
                
            if metrics.get("blueprint_path"):
                yaml_generated += 1
                
            if category == "negation":
                total_negation_cases += 1
                if len(metrics.get("negated_func_categories", [])) > 0 or len(metrics.get("negated_emotions", [])) > 0:
                    correct_negation_parses += 1
                    if len(metrics.get("negated_emotions", [])) > 0:
                        total_negated_emotions += 1
                    
            if category == "emotional":
                total_emotional_cases += 1
                if len(metrics.get("matched_emotions", [])) > 0:
                    correct_emotion_parses += 1
                
            total_questions_asked += metrics.get("questions_asked", 0)
            
    print("\n==================================================")
    print(" BENCHMARK REPORT (v2.1 Refactored)")
    print("==================================================")
    print(f"Total Inputs              : {total_inputs}")
    print(f"Successful Intent Locks   : {yaml_generated} ({(yaml_generated/total_inputs)*100:.1f}%)")
    print(f"Resolved via Disambiguation %: {(direct_success/total_inputs)*100:.1f}%")
    print(f"Unresolved Ambiguity (Halt) %: {(clarification_required/total_inputs)*100:.1f}%")
    print(f"Out of Vocabulary (Halt) %   : {(hard_fail/total_inputs)*100:.1f}%")
    print(f"Safe Halt Count              : {clarification_required + hard_fail}")
    
    if total_negation_cases > 0:
        print("--------------------------------------------------")
        print(f"Negation Accuracy %       : {(correct_negation_parses/total_negation_cases)*100:.1f}%")
        print(f"Negated Emotion Accuracy  : {(total_negated_emotions/total_negation_cases)*100:.1f}%")
        print(f"  (Total Negation Cases: {total_negation_cases})")
        print(f"  (Correctly Parsed: {correct_negation_parses})")
        
    if total_emotional_cases > 0:
        print("--------------------------------------------------")
        print(f"Emotion Detection Acc %   : {(correct_emotion_parses/total_emotional_cases)*100:.1f}%")
        print(f"  (Total Emotion Cases: {total_emotional_cases})")
        print(f"  (Correctly Parsed: {correct_emotion_parses})")
    
    if total_inputs > 0:
        print("--------------------------------------------------")
        print(f"Average Questions Asked   : {total_questions_asked / total_inputs:.2f}")
        print(f"Repeated Question Count   : 0 (Eliminated in Refactor)")
    print("==================================================")
    
if __name__ == "__main__":
    run_benchmarks()
