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
    
    total_tests = 0
    passed_tests = 0
    total_ambiguity_reduced = 0
    
    print("==================================================")
    print(" INTENT-TO-SILICON : Benchmarking Suite v1.0")
    print("==================================================")
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_tests += 1
            input_text = row['input_text']
            expected = row['expected_outcome']
            
            # Run headless processing (assume user always confirms "yes/2" for disambiguation)
            metrics = process_single_input(input_text, func_lib, emotion_lib, headless_reply="yes")
            
            # Evaluate Status
            status_match = metrics["status"] == expected
            if status_match:
                passed_tests += 1
                
            # Evaluate Ambiguity Reduction (Experiment 2)
            if metrics["status"] == "Success":
                ambiguity_reduced = metrics["initial_ambiguity_count"] # number of vague concepts locked into 1 spec per category
                total_ambiguity_reduced += ambiguity_reduced
            
            print(f"Test {row['id']}: '{input_text[:30]}...'")
            print(f"  -> Expected: {expected} | Got: {metrics['status']}")
            if metrics["blueprint_path"]:
                print(f"  -> Generated: {os.path.basename(metrics['blueprint_path'])}")
            print("-" * 40)
            
    print("\n==================================================")
    print(" BENCHMARK RESULTS")
    print("==================================================")
    print(f"Total Requests Processed : {total_tests}")
    print(f"Accuracy Rate            : {(passed_tests/total_tests)*100:.1f}%")
    if passed_tests > 0:
        print(f"Average Ambiguity Locked : {total_ambiguity_reduced / passed_tests:.2f} concepts locked per successful intent.")
    print("==================================================")
    
if __name__ == "__main__":
    run_benchmarks()
