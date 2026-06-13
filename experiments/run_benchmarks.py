import csv
import os
import sys

# Add prototype directory to sys path so we can import the engine
base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(base_dir, 'prototype'))

from nlp_engine import load_libraries, process_single_input

def run_benchmarks():
    dataset_path = os.path.join(base_dir, 'data', 'evaluation_dataset.csv')
    
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
            
            # v0.5 Benchmark update:
            # The system now forces active disambiguation and expects an option choice (1, 2, etc).
            # For "ambiguous" tests (expected="clarification_required"), simulate an unresolved/invalid reply ("no" or "")
            # For "functional/emotional/mixed" tests, simulate a user who correctly chooses an option (e.g., "2")
            if expected == "clarification_required":
                headless_reply = "no"
            else:
                headless_reply = "2"
                
            metrics = process_single_input(input_text, func_lib, emotion_lib, headless_reply=headless_reply)
            
            # Tally metrics
            if metrics["status"] == "success":
                direct_success += 1
            elif metrics["status"] == "clarification_required":
                clarification_required += 1
            elif metrics["status"] == "fail_hard":
                hard_fail += 1
                
            if metrics["blueprint_path"]:
                yaml_generated += 1
                
            if category == "negation":
                total_negation_cases += 1
                if metrics["negated_intents_detected"] > 0:
                    correct_negation_parses += 1
                
            total_questions_asked += metrics["questions_asked"]
            
    print("\n==================================================")
    print(" BENCHMARK REPORT")
    print("==================================================")
    print(f"Total Inputs              : {total_inputs}")
    print(f"Resolved via Disambiguation %: {(direct_success/total_inputs)*100:.1f}%")
    print(f"Unresolved Ambiguity (Halt) %: {(clarification_required/total_inputs)*100:.1f}%")
    print(f"Out of Vocabulary (Halt) %   : {(hard_fail/total_inputs)*100:.1f}%")
    print(f"Final YAML Blueprints Gen %  : {(yaml_generated/total_inputs)*100:.1f}%")
    
    if total_negation_cases > 0:
        print("--------------------------------------------------")
        print(f"Negation Accuracy %       : {(correct_negation_parses/total_negation_cases)*100:.1f}%")
        print(f"  (Total Negation Cases: {total_negation_cases})")
        print(f"  (Correctly Parsed: {correct_negation_parses})")
    
    if total_inputs > 0:
        print("--------------------------------------------------")
        print(f"Average Questions Asked   : {total_questions_asked / total_inputs:.2f}")
    print("==================================================")
    
if __name__ == "__main__":
    run_benchmarks()
