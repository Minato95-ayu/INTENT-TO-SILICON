"""
=============================================================================
FILE: generate_payment_corpus.py
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
import random
import os

def generate_payment_phrases(count=100):
    subjects = [
        "mere paise", "account se paise", "amount", "payment", 
        "500 rupees", "mera refund", "double charge", "bank se", "wallet se"
    ]
    
    actions = [
        "kat gaye", "deduct ho gaya", "fail ho gaya", "ud gaye",
        "nahi aaya", "stuck ho gaya", "pending hai", "wapas nahi aaya",
        "cancel ho gaya par kat gaya"
    ]
    
    complaints = [
        "bakwas app", "fraud hai", "scam", "customer care kaha hai", 
        "order nahi dikh raha", "koi reply nahi", "wapas do",
        "app delete kar dunga", "1 star", "help me"
    ]
    
    sources = ["playstore", "reddit", "twitter", "quora"]
    category = "payment_anxiety"
    
    phrases = []
    
    # Generate combinations
    for _ in range(count):
        sub = random.choice(subjects)
        act = random.choice(actions)
        comp = random.choice(complaints)
        
        # Sometimes don't include complaint
        if random.random() > 0.3:
            phrase = f"{sub} {act} {comp}"
        else:
            phrase = f"{sub} {act}"
            
        # Add random english mix occasionally
        if random.random() > 0.8:
            phrase += " this is worst"
        
        source = random.choice(sources)
        phrases.append([phrase.strip(), source, category])
        
    return phrases

if __name__ == "__main__":
    phrases = generate_payment_phrases(100)
    
    # Ensure directory exists
    os.makedirs(os.path.join("data", "corpus_v1"), exist_ok=True)
    
    output_path = os.path.join("data", "corpus_v1", "payment_anxiety.csv")
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['phrase', 'source', 'category'])
        writer.writerows(phrases)
        
    print(f"Generated {len(phrases)} phrases at {output_path}")
