import json
import os

def create_expected_outputs():
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
        
    with open('../data/intent_ir_examples_50.json', 'r') as f:
        data = json.load(f)
        
    expected = []
    for d in data:
        expected.append({
            "input": d['input'],
            "expected_module": d['intent_ir']['module'],
            "expected_problem": d['intent_ir']['primary_problem'],
            "requires_clarification": d['intent_ir']['requires_clarification'],
            "requires_diagnosis": d['intent_ir']['requires_diagnosis']
        })
        
    with open('../data/intent_ir_expected_outputs.json', 'w') as f:
        json.dump(expected, f, indent=2)
    print("Created ../data/intent_ir_expected_outputs.json")

if __name__ == "__main__":
    create_expected_outputs()
