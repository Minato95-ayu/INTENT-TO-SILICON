import csv
import os
import random

def generate_100k_hybrid():
    print("Generating 50K Synthetic Augmentations for 100K Hybrid Corpus...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_csv_path = os.path.join(base_dir, 'data', 'corpus_v1_real_50k.csv')
    hybrid_csv_path = os.path.join(base_dir, 'data', 'corpus_v1_hybrid_100k.csv')
    
    real_phrases = []
    
    if not os.path.exists(real_csv_path):
        print(f"Error: {real_csv_path} not found.")
        return

    # Read 50K real phrases
    with open(real_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            real_phrases.append(row)

    print(f"Loaded {len(real_phrases)} real phrases.")
    
    synthetic_phrases = []
    
    # Fast programmatic generation (1 variant per real phrase)
    prefixes = ["Bug: ", "Issue - ", "Fix this: ", "Please fix: ", "Error: ", "", "", ""]
    suffixes = [" asap", " immediately", "...", " yaar", "!", ""]
    
    # Very fast replace logic for large data
    for i, row in enumerate(real_phrases):
        orig = str(row.get('phrase', '')).lower()
        
        # Simple augmentations
        prefix = prefixes[i % len(prefixes)]
        suffix = suffixes[i % len(suffixes)]
        
        var = f"{prefix}{orig}{suffix}".strip()
        if var == orig:
            var = orig + " (bug reported)"
            
        synthetic_phrases.append({
            'id': 50000 + i + 1,
            'phrase': var,
            'category': 'unknown',
            'source': 'synthetic_augmentation',
            'proof_app_name': row.get('proof_app_name', ''),
            'proof_rating': row.get('proof_rating', ''),
            'proof_date': row.get('proof_date', '')
        })
        
        if len(synthetic_phrases) >= 50000:
            break

    # Combine into 100K Hybrid
    hybrid_corpus = real_phrases + synthetic_phrases
    
    print("Saving to CSV...")
    # Use pandas for faster save
    import pandas as pd
    df = pd.DataFrame(hybrid_corpus)
    df.to_csv(hybrid_csv_path, index=False)
        
    print(f"SUCCESS: Hybrid Corpus Generated!")
    print(f"Total Real Phrases: {len(real_phrases)}")
    print(f"Total Synthetic Phrases: {len(synthetic_phrases)}")
    print(f"Total Hybrid Corpus Size: {len(hybrid_corpus)} -> Saved to {hybrid_csv_path}")

if __name__ == "__main__":
    generate_100k_hybrid()
