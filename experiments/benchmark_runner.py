import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from prototype.nlp_engine import process_single_input, load_libraries

def run_benchmark():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    dataset_path = os.path.join(base_dir, 'data', 'mock_pain_points_dataset.json')
    report_path = os.path.join(base_dir, 'experiments', 'benchmark_report.md')
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
        
    func_lib, emotion_lib = load_libraries()
    
    total = len(dataset)
    correct_intent = 0
    correct_safe_halt = 0
    safe_halt_total = 0
    clarification_triggered = 0
    
    results_log = []
    
    for item in dataset:
        phrase = item["phrase"]
        expected = item["expected_intent"]
        
        # We pass headless_reply="1" so it auto-selects option 1 if clarification triggers
        metrics = process_single_input(phrase, func_lib, emotion_lib, headless_reply="1")
        
        status = metrics["status"]
        pain_points = metrics.get("pain_points", [])
        
        # Evaluate
        is_correct = False
        
        if expected == "safe_halt":
            safe_halt_total += 1
            if status == "fail_hard":
                correct_safe_halt += 1
                is_correct = True
        else:
            if status == "success" and expected in pain_points:
                correct_intent += 1
                clarification_triggered += 1  # In v0.8, successful intent extraction means clarification was triggered and resolved
                is_correct = True
                
        results_log.append({
            "phrase": phrase,
            "expected": expected,
            "actual": pain_points if pain_points else status,
            "is_correct": is_correct
        })
        
    # Generate Report
    accuracy = (correct_intent / (total - safe_halt_total)) * 100 if (total - safe_halt_total) > 0 else 0
    safe_halt_accuracy = (correct_safe_halt / safe_halt_total) * 100 if safe_halt_total > 0 else 0
    
    report_md = f"""# NLP Engine Benchmark Report (v0.9)

## Summary
- **Total Phrases Tested**: {total}
- **Intent Recognition Accuracy**: {accuracy:.1f}% ({correct_intent}/{total - safe_halt_total})
- **Safe Halt (OOV) Accuracy**: {safe_halt_accuracy:.1f}% ({correct_safe_halt}/{safe_halt_total})
- **Clarification Trigger Rate**: {clarification_triggered} times triggered correctly.

## Detailed Logs
| Phrase | Expected | Actual | Pass |
| --- | --- | --- | --- |
"""
    for log in results_log:
        pass_str = "✅" if log["is_correct"] else "❌"
        actual_str = str(log["actual"])
        report_md += f"| {log['phrase']} | {log['expected']} | {actual_str} | {pass_str} |\n"
        
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
        
    print(f"Benchmark complete! Accuracy: {accuracy:.1f}%. Report saved to {report_path}")

if __name__ == "__main__":
    run_benchmark()
