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
    
    metrics = {
        "valid_inputs": 0,
        "oov_failures": 0,
        "emotion_total": 0,
        "emotion_correct": 0,
        "negation_total": 0,
        "negation_correct": 0,
        "total_questions_asked": 0,
        "inputs_with_questions": 0
    }
    
    results_log = []
    
    for item in dataset:
        phrase = item["phrase"]
        expected = item["expected_category"]
        test_type = item.get("type", "functional")
        negated_expected = item.get("negated", None)
        
        # We pass headless_reply="1" so it auto-selects option 1 if clarification triggers
        result = process_single_input(phrase, func_lib, emotion_lib, headless_reply="1")
        
        status = result["status"]
        q_asked = result.get("questions_asked", 0)
        
        is_correct = False
        actual_output = ""
        
        if test_type == "oov":
            if status == "fail_hard":
                is_correct = True
                actual_output = "safe_halt (Expected)"
            else:
                actual_output = "FAILED_HALT"
        else:
            metrics["valid_inputs"] += 1
            if status == "fail_hard":
                metrics["oov_failures"] += 1
                actual_output = "OOV_FAILURE"
            else:
                metrics["inputs_with_questions"] += 1
                metrics["total_questions_asked"] += q_asked
                
                matched_funcs = result.get("matched_func_categories", [])
                matched_emotions = result.get("matched_emotions", [])
                negated_funcs = result.get("negated_func_categories", [])
                
                if test_type == "emotion":
                    metrics["emotion_total"] += 1
                    if expected in matched_emotions:
                        metrics["emotion_correct"] += 1
                        is_correct = True
                    actual_output = f"E:{matched_emotions} F:{matched_funcs}"
                        
                elif test_type == "negation":
                    metrics["negation_total"] += 1
                    if negated_expected in negated_funcs and expected in matched_funcs:
                        metrics["negation_correct"] += 1
                        is_correct = True
                    actual_output = f"Matched:{matched_funcs} Negated:{negated_funcs}"
                        
                else: # functional or low_confidence
                    if expected in matched_funcs:
                        is_correct = True
                    actual_output = f"Matched:{matched_funcs}"
                    
        results_log.append({
            "phrase": phrase,
            "type": test_type,
            "expected": expected,
            "actual": actual_output,
            "is_correct": is_correct,
            "questions": q_asked
        })
        
    # Generate Report
    oov_rate = (metrics["oov_failures"] / metrics["valid_inputs"]) * 100 if metrics["valid_inputs"] > 0 else 0
    emotion_acc = (metrics["emotion_correct"] / metrics["emotion_total"]) * 100 if metrics["emotion_total"] > 0 else 0
    negation_acc = (metrics["negation_correct"] / metrics["negation_total"]) * 100 if metrics["negation_total"] > 0 else 0
    avg_questions = metrics["total_questions_asked"] / metrics["inputs_with_questions"] if metrics["inputs_with_questions"] > 0 else 0
    
    report_md = f"""# NLP Engine Aggressive Benchmark Report (v2.0)

## Targets Evaluation
- **Target 1: OOV Rate < 5%** -> Actual: **{oov_rate:.1f}%** (Failures: {metrics["oov_failures"]}/{metrics["valid_inputs"]})
- **Target 2: Pain Point Accuracy > 90%** -> Actual: **{emotion_acc:.1f}%** ({metrics["emotion_correct"]}/{metrics["emotion_total"]})
- **Target 3: Avg Questions > 2.0** -> Actual: **{avg_questions:.2f}** (Total Qs: {metrics["total_questions_asked"]} / Inputs: {metrics["inputs_with_questions"]})
- **Target 4: Negation Accuracy > 95%** -> Actual: **{negation_acc:.1f}%** ({metrics["negation_correct"]}/{metrics["negation_total"]})

## Detailed Logs
| Phrase | Type | Expected | Actual | Pass | Qs |
| --- | --- | --- | --- | --- | --- |
"""
    for log in results_log:
        pass_str = "✅" if log["is_correct"] else "❌"
        report_md += f"| {log['phrase']} | {log['type']} | {log['expected']} | {log['actual']} | {pass_str} | {log['questions']} |\n"
        
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
        
    print(f"Benchmark complete! Results saved to {report_path}")
    print(f"OOV: {oov_rate:.1f}% | Emotion: {emotion_acc:.1f}% | Negation: {negation_acc:.1f}% | Avg Qs: {avg_questions:.2f}")

if __name__ == "__main__":
    run_benchmark()
