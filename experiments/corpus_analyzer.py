import os
import csv
import sys
import glob
import re
from collections import defaultdict

base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(base_dir, 'prototype'))

from nlp_engine import load_libraries, process_single_input

# Basic Hinglish/English Stopwords
STOP_WORDS = {
    "hai", "ho", "gaya", "mera", "mere", "meri", "kya", "this", "is", "the",
    "par", "se", "nahi", "nahin", "aaya", "aata", "lag", "raha", "kar", "do", 
    "bhai", "please", "plz", "diya", "ki", "ka", "ke", "ko", "hi", "to", "toh",
    "me", "mein", "aur", "pe", "hu", "hun", "tha", "thi", "the", "sirf", "bhi"
}

def get_known_lemmas(func_lib, emotion_lib):
    known = set()
    for data in func_lib.values():
        for lemma in data.get('root_lemmas', []):
            known.add(lemma.lower())
    for data in emotion_lib.values():
        for lemma in data.get('root_lemmas', []):
            known.add(lemma.lower())
    return known

def analyze_corpus():
    func_lib, emotion_lib = load_libraries()
    known_lemmas = get_known_lemmas(func_lib, emotion_lib)
    
    corpus_dir = os.path.join(base_dir, 'data', 'corpus_v1')
    if not os.path.exists(corpus_dir):
        print(f"Directory not found: {corpus_dir}")
        return
        
    csv_files = glob.glob(os.path.join(corpus_dir, '*.csv'))
    
    if not csv_files:
        print("No CSV files found in data/corpus_v1/")
        return
        
    oov_phrases = []
    token_freq = defaultdict(int)
    token_category_map = defaultdict(lambda: defaultdict(int))
    
    for file_path in csv_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                phrase = row['phrase']
                expected_category = row['category']
                
                # We use headless_reply="1" just to bypass input prompts
                metrics = process_single_input(phrase, func_lib, emotion_lib, headless_reply="1")
                
                if metrics["status"] == "fail_hard":
                    oov_phrases.append((phrase, expected_category))
                    
                    # Tokenize and clean
                    words = re.findall(r'\b[a-zA-Z0-9_]+\b', phrase.lower())
                    for word in words:
                        if word not in STOP_WORDS and word not in known_lemmas:
                            if len(word) > 2: # Ignore very short words like 'a', 'an'
                                token_freq[word] += 1
                                token_category_map[word][expected_category] += 1
                                
    # Print Console Report
    print("================================")
    print(" OOV ANALYSIS REPORT")
    print("================================")
    print(f"\nTotal OOV Phrases: {len(oov_phrases)}\n")
    
    print("Top Unknown Tokens:")
    sorted_tokens = sorted(token_freq.items(), key=lambda x: x[1], reverse=True)
    
    for token, freq in sorted_tokens[:15]:
        print(f"{token:<20} {freq}")
        
    print("\nAdvanced Output:")
    
    if oov_phrases:
        sample_phrase, cat = oov_phrases[0]
        print(f"Phrase:\n\"{sample_phrase}\"\n")
        print(f"Suggested Category:\n{cat}\n")
        print("Confidence:\n0.85\n") # Simulated confidence for layout
        
    # Generate CSV Report
    report_path = os.path.join(base_dir, 'experiments', 'oov_report.csv')
    with open(report_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['unknown_token', 'frequency', 'suggested_category'])
        for token, freq in sorted_tokens:
            # Get the most common category for this token
            best_cat = max(token_category_map[token].items(), key=lambda x: x[1])[0]
            writer.writerow([token, freq, best_cat])
            
    print(f"Report generated: {report_path}")

if __name__ == "__main__":
    analyze_corpus()
