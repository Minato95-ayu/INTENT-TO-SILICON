"""
=============================================================================
FILE: create_human_eval_template.py
PURPOSE: Generates project components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles generates project components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import csv
import random
import os

def create_template():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    corpus_dir = os.path.join(base_dir, 'data', 'corpus_v1')
    
    categories = [
        "payment_anxiety",
        "otp_failure",
        "navigation_confusion",
        "performance_frustration"
    ]
    
    selected_phrases = []
    
    # 1. Select 10 from each category
    for cat in categories:
        file_path = os.path.join(corpus_dir, f"{cat}.csv")
        phrases = []
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    phrases.append((row['phrase'], cat))
        
        # Pick 10
        if phrases:
            sampled = random.sample(phrases, min(10, len(phrases)))
            selected_phrases.extend(sampled)
            
    # 2. Add 10 Mixed / Ambiguous phrases
    mixed_phrases = [
        ("app bahut slow hai aur refund nahi aaya", "mixed"),
        ("OTP fail ho raha hai kaha click karu", "mixed"),
        ("payment stuck hai, setting hidden hai", "mixed"),
        ("video upload crash ho gaya mera 500 ud gaya", "mixed"),
        ("samajh nahi aa raha paise wapas kaise lu", "mixed"),
        ("login invalid hai, order cancel ho gaya", "mixed"),
        ("customer care ka number kidhar hai fraud app", "mixed"),
        ("loading loading... otp hi nahi aata", "mixed"),
        ("menu nahi mil raha, payment fail dikha raha hai", "mixed"),
        ("double charge ho gaya aur phone hang kar raha hai", "mixed")
    ]
    
    selected_phrases.extend(mixed_phrases)
    
    # Shuffle the 50 phrases so it's a blind test
    random.shuffle(selected_phrases)
    
    output_path = os.path.join(base_dir, 'data', 'human_eval_template.csv')
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['phrase', 'actual_category', 'human_label'])
        for p, cat in selected_phrases:
            # We keep actual_category for the validation script to know the truth/source
            writer.writerow([p, cat, ''])
            
    print(f"Created template at {output_path} with {len(selected_phrases)} phrases.")

if __name__ == "__main__":
    create_template()
