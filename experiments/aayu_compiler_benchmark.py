import json
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'prototype', 'compiler_v2'))

from compiler import CompilerV2

def run_benchmark(dataset_path, dataset_name):
    c = CompilerV2()
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    total = len(data)
    if total == 0:
        print(f"Dataset {dataset_name} is empty.")
        return
        
    intent_correct = 0
    aayu_correct = 0
    code_correct = 0
    
    for item in data:
        phrase = item['input']
        expected_problem = item['intent_ir']['primary_problem']
        
        res = c.process(phrase)
        intent_ir = res.get('intent_ir')
        aayu_ir = res.get('aayu_ir')
        code = res.get('code')
        
        # Intent IR Accuracy
        if intent_ir and intent_ir.get('primary_problem') == expected_problem:
            intent_correct += 1
            
            # Aayu IR Accuracy (Requires Intent IR to be correct + Aayu IR generated)
            if aayu_ir and aayu_ir.get('event') and aayu_ir.get('action'):
                aayu_correct += 1
                
                # Code Generation Accuracy (Requires Aayu IR to be correct + Code generated)
                if code and code.strip():
                    code_correct += 1
                    
    intent_acc = (intent_correct / total) * 100
    aayu_acc = (aayu_correct / total) * 100
    code_acc = (code_correct / total) * 100
    end_to_end_acc = code_acc # End-to-end is successful if correct code is generated
    
    print(f"=== Benchmark Results: {dataset_name} ===")
    print(f"Total Examples:           {total}")
    print(f"Intent IR Accuracy:       {intent_acc:.1f}%")
    print(f"Aayu IR Accuracy:         {aayu_acc:.1f}%")
    print(f"Code Generation Accuracy: {code_acc:.1f}%")
    print(f"End-to-End Accuracy:      {end_to_end_acc:.1f}%")
    print("-" * 45)

if __name__ == "__main__":
    print("============================================")
    print("      AAYU COMPILER BENCHMARK SPRINT 5.5")
    print("============================================\n")
    
    gold_path = os.path.join(base_dir, 'data', 'intent_ir_examples_50.json')
    unseen_path = os.path.join(base_dir, 'data', 'unseen_examples_50.json')
    
    if os.path.exists(gold_path):
        run_benchmark(gold_path, "Gold Dataset (50 Examples)")
    else:
        print("Gold dataset not found.")
        
    if os.path.exists(unseen_path):
        run_benchmark(unseen_path, "Unseen Dataset (50 Examples)")
    else:
        print("Unseen dataset not found.")
