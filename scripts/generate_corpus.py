"""
=============================================================================
FILE: generate_corpus.py
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

def generate_phrases(category, count=100):
    if category == "payment_anxiety":
        subjects = ["mere paise", "account se paise", "amount", "payment", "500 rupees", "mera refund", "double charge", "bank se", "wallet se"]
        actions = ["kat gaye", "deduct ho gaya", "fail ho gaya", "ud gaye", "nahi aaya", "stuck ho gaya", "pending hai", "wapas nahi aaya", "cancel ho gaya par kat gaya"]
        complaints = ["bakwas app", "fraud hai", "scam", "customer care kaha hai", "order nahi dikh raha", "koi reply nahi", "wapas do", "app delete kar dunga", "1 star", "help me"]
    elif category == "otp_failure":
        subjects = ["otp", "code", "verification code", "sms", "message"]
        actions = ["nahi aa raha", "aane me time lag raha hai", "invalid bata raha hai", "expired dikha raha hai", "receive nahi hua", "block ho gaya"]
        complaints = ["kya karu", "login nahi ho raha", "account open nahi ho raha", "frustrating", "fix karo isko", "1 ghanta ho gaya"]
    elif category == "navigation_confusion":
        subjects = ["setting", "menu", "profile", "log out button", "customer support", "refund page", "order history", "kaha click karu"]
        actions = ["kaha hai", "nahi mil raha", "dikhi nahi raha", "gayab ho gaya", "kidhar hai", "bahut hidden hai", "samajh nahi aa raha"]
        complaints = ["very confusing", "kharab UI", "itna hard kyu banaya", "pareshan ho gaya", "simple banao", "time waste"]
    elif category == "performance_frustration":
        subjects = ["app", "screen", "page", "loading", "video", "button"]
        actions = ["crash ho rahi hai", "hang ho raha hai", "stuck ho gaya", "slow hai", "open nahi ho raha", "lag kar raha hai", "load nahi ho raha"]
        complaints = ["worst experience", "optimize karo", "phone hang kar diya", "delete kar raha hu", "slowest app ever", "update ke baad kharab ho gaya"]
    
    sources = ["playstore", "reddit", "twitter", "quora"]
    
    phrases = []
    
    for _ in range(count):
        sub = random.choice(subjects)
        act = random.choice(actions)
        comp = random.choice(complaints)
        
        if random.random() > 0.3:
            phrase = f"{sub} {act} {comp}"
        else:
            phrase = f"{sub} {act}"
            
        if random.random() > 0.8:
            phrase += random.choice([" this is worst", " please fix", " wtf", " anyone else facing this?"])
        
        source = random.choice(sources)
        phrases.append([phrase.strip(), source, category])
        
    return phrases

if __name__ == "__main__":
    os.makedirs(os.path.join("data", "corpus_v1"), exist_ok=True)
    
    categories = [
        "payment_anxiety",
        "otp_failure",
        "navigation_confusion",
        "performance_frustration"
    ]
    
    total_generated = 0
    for cat in categories:
        phrases = generate_phrases(cat, 100)
        output_path = os.path.join("data", "corpus_v1", f"{cat}.csv")
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['phrase', 'source', 'category'])
            writer.writerows(phrases)
        print(f"Generated {len(phrases)} phrases at {output_path}")
        total_generated += len(phrases)
        
    print(f"\nTotal phrases generated: {total_generated}")
