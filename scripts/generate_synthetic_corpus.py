"""
=============================================================================
FILE: generate_synthetic_corpus.py
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
import random

def generate_synthetic_variations(real_phrase, category, num_variations):
    """
    Simulates a synthetic augmentation pipeline.
    In a production setting, this would call an LLM (e.g., GPT-4 / Gemini) 
    to generate high-quality augmentations based on the real seed phrase.
    For this benchmark, we apply programmatic rule-based expansions.
    """
    augmentations = []
    
    # Simple rule-based synonym / phrasing variations
    prefixes = ["Yaar ", "Bhai ", "Please fix this: ", "Issue: ", "Bug: ", "", ""]
    suffixes = [" jaldi", " immediately", " asap", "...", "!", " yaar", ""]
    synonyms = {
        "paise": ["amount", "payment", "money", "rupaye", "funds"],
        "kat gaye": ["deduct ho gaya", "cut gaya", "chala gaya", "debit ho gaya"],
        "kaha click karu": ["kidhar jau", "button kahan hai", "option kidhar hai"],
        "safe": ["secure", "private", "protected"],
        "blank screen": ["safed screen", "white screen", "kuch nahi dikh raha", "render fail"],
        "fail": ["atak gaya", "stuck", "error de raha hai"]
    }
    
    for _ in range(num_variations):
        new_phrase = real_phrase.lower()
        for key, syn_list in synonyms.items():
            if key in new_phrase:
                new_phrase = new_phrase.replace(key, random.choice(syn_list))
                
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        
        final_phrase = f"{prefix}{new_phrase}{suffix}".strip()
        # Fallback if too similar
        if final_phrase == real_phrase:
            final_phrase = final_phrase + random.choice([" hamesha aise hota hai", " kya bakwas hai", " please help"])
            
        augmentations.append(final_phrase)
        
    return augmentations

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_csv_path = os.path.join(base_dir, 'data', 'corpus_v1_real.csv')
    hybrid_csv_path = os.path.join(base_dir, 'data', 'corpus_v1_hybrid_1000.csv')
    
    real_phrases = []
    
    # 1. Read real phrases
    if os.path.exists(real_csv_path):
        with open(real_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                real_phrases.append(row)
    else:
        print(f"Error: {real_csv_path} not found. Please provide real phrases first.")
        return

    # 2. Calculate how many variations needed per real phrase to hit 500 synthetic
    num_real = len(real_phrases)
    if num_real == 0:
        print("No real phrases found in the template.")
        return
        
    target_synthetic = 500
    variations_per_phrase = (target_synthetic // num_real) + 1
    
    synthetic_phrases = []
    syn_id = num_real + 1
    
    for row in real_phrases:
        variations = generate_synthetic_variations(row['phrase'], row['category'], variations_per_phrase)
        for var in variations:
            if len(synthetic_phrases) < target_synthetic:
                synthetic_phrases.append({
                    'id': syn_id,
                    'phrase': var,
                    'category': row['category'],
                    'source': 'synthetic_augmentation'
                })
                syn_id += 1

    # 3. Combine into hybrid corpus
    hybrid_corpus = real_phrases + synthetic_phrases
    
    # Save hybrid corpus
    fieldnames = ['id', 'phrase', 'category', 'source', 'proof_app_name', 'proof_rating', 'proof_date']
    with open(hybrid_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(hybrid_corpus)
        
    print(f"Hybrid Corpus Generated successfully!")
    print(f"Total Real Phrases: {len(real_phrases)}")
    print(f"Total Synthetic Phrases: {len(synthetic_phrases)}")
    print(f"Total Hybrid Corpus Size: {len(hybrid_corpus)} -> Saved to {hybrid_csv_path}")

if __name__ == "__main__":
    main()
