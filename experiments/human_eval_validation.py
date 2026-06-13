import csv
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'prototype'))

from nlp_engine import process_single_input, load_libraries

def compute_cohens_kappa(human_labels, system_labels, categories):
    """
    Computes simple Agreement % and Cohen's Kappa for 2 raters.
    """
    if len(human_labels) != len(system_labels) or len(human_labels) == 0:
        return 0.0, 0.0

    n = len(human_labels)
    agreements = sum(1 for h, s in zip(human_labels, system_labels) if h == s)
    p_o = agreements / n  # Observed agreement
    
    # Calculate expected agreement (P_e)
    p_e = 0
    for cat in categories:
        h_count = human_labels.count(cat)
        s_count = system_labels.count(cat)
        p_e += (h_count / n) * (s_count / n)
        
    if p_e == 1:
        kappa = 1.0
    else:
        kappa = (p_o - p_e) / (1 - p_e)
        
    return p_o * 100, kappa

def validate_human_eval():
    csv_path = os.path.join(base_dir, 'data', 'human_eval_template.csv')
    
    if not os.path.exists(csv_path):
        print(f"Error: Could not find {csv_path}")
        return
        
    human_labels = []
    system_labels = []
    phrases = []
    
    func_lib, emotion_lib = load_libraries()
    categories = list(emotion_lib.keys())
    categories.append("unknown")
    
    missing_labels = 0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            h_label = row.get('human_label', '').strip().lower()
            if not h_label:
                missing_labels += 1
                continue
                
            metrics = process_single_input(row['phrase'], func_lib, emotion_lib, headless_reply="1")
            
            # System label is the first matched emotion, or 'unknown'
            s_label = "unknown"
            if metrics.get("matched_emotions"):
                s_label = metrics["matched_emotions"][0].lower()
                
            human_labels.append(h_label)
            system_labels.append(s_label)
            phrases.append(row['phrase'])
            
    if missing_labels > 0:
        print(f"WARNING: {missing_labels} phrases are missing human labels. Please fill the 'human_label' column via Google Forms.")
        if len(human_labels) == 0:
            print("No human labels found. Cannot compute metrics. Aborting.")
            return

    print("==================================================")
    print(" HUMAN EVALUATION VALIDATION REPORT")
    print("==================================================")
    print(f"Total Phrases Evaluated: {len(human_labels)}")
    
    agreement_pct, kappa = compute_cohens_kappa(human_labels, system_labels, categories)
    
    print(f"Human-System Agreement % : {agreement_pct:.2f}%")
    print(f"Cohen's Kappa Score      : {kappa:.3f}")
    
    # Interpretation
    interpretation = "Poor"
    if kappa > 0.8: interpretation = "Almost Perfect"
    elif kappa > 0.6: interpretation = "Substantial"
    elif kappa > 0.4: interpretation = "Moderate"
    elif kappa > 0.2: interpretation = "Fair"
    elif kappa > 0.0: interpretation = "Slight"
    
    print(f"Agreement Interpretation : {interpretation}")
    print("==================================================")
    
if __name__ == "__main__":
    validate_human_eval()
