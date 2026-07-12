"""
=============================================================================
FILE: patch_taxonomy_2.py
PURPOSE: Fixes or patches existing code
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles fixes or patches existing code.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import json
import os

file_path = os.path.join('dictionary', 'pain_point_taxonomy.json')
with open(file_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

# Define root lemmas for each category to catch single emotional words 
root_lemmas = {
    "payment_anxiety": ["payment", "paise", "refund", "fraud", "dhokha", "scam", "chori", "paisa"],
    "navigation_confusion": ["confus", "uljhan", "samajh nahi", "kaha click", "pata nahi", "idea", "pata na chale"],
    "performance_frustration": ["bore", "hang", "slow", "atak", "load nahi", "bekar", "ghoom", "fun", "khushi", "maza"],
    "trust_deficit": ["trust", "safe", "privacy", "secure", "private", "leak", "dar", "nizi", "akele"],
    "support_frustration": ["koi nahi sunta", "bakwas", "insaan se", "customer care"],
    "urgency": ["urgency", "jaldi", "fatafat", "turant", "time nahi", "fast fast", "impatient"]
}

for cat, lemmas in root_lemmas.items():
    if cat in d:
        d[cat]["root_lemmas"] = lemmas

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)

print("Taxonomy patched with MORE root_lemmas!")
