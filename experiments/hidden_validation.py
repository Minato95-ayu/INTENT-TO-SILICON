import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prototype', 'compiler_v2'))
from compiler import CompilerV2

def run_benchmark():
    c = CompilerV2()
    
    with open('../data/hidden_examples_20.json', 'r') as f:
        data = json.load(f)
        
    total = len(data)
    prob_correct = 0
    mod_correct = 0
    
    print("====================================")
    print("HIDDEN INPUT VALIDATION BENCHMARK")
    print("====================================\n")
    
    for item in data:
        expected = item['intent_ir']
        predicted = c.process(item['input'])
        
        if expected['primary_problem'] == predicted['primary_problem']:
            prob_correct += 1
            
        if expected['module'] == predicted['module']:
            mod_correct += 1
            
    prob_acc = (prob_correct / total) * 100
    mod_acc = (mod_correct / total) * 100
    
    print(f"Total Hidden Examples: {total}\n")
    print(f"Problem Accuracy:        {prob_acc:.1f}%")
    print(f"Module Accuracy:         {mod_acc:.1f}%")
    
    overall = (prob_acc + mod_acc) / 2
    print(f"\nOverall Hidden Score:    {overall:.1f}%")
    print("====================================")

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
    run_benchmark()
