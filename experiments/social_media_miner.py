"""
=============================================================================
FILE: social_media_miner.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import json
import os
import sys

# Simulated Extraction Rules (In production, this would be an LLM call)
EXTRACTION_RULES = [
    {
        "keywords": ["dimaag ki dahi", "slow", "time lagata", "faaltu speed", "hang ho gaya"],
        "pain_point": "performance_frustration",
        "extracted_phrase": "dimaag ki dahi"
    },
    {
        "keywords": ["waat lag gayi", "session expire"],
        "pain_point": "urgency",
        "extracted_phrase": "waat lag gayi"
    },
    {
        "keywords": ["faaltu", "bakwaas", "hang ho gaya"],
        "pain_point": "performance_frustration",
        "extracted_phrase": "faaltu speed"
    },
    {
        "keywords": ["arre yaar", "data leak", "dar lagta"],
        "pain_point": "trust_deficit",
        "extracted_phrase": "arre yaar"
    },
    {
        "keywords": ["bot system", "insaan se baat", "dimaag kharab"],
        "pain_point": "support_frustration",
        "extracted_phrase": "insaan se baat"
    },
    {
        "keywords": ["kahan click karu", "sir ke upar"],
        "pain_point": "navigation_confusion",
        "extracted_phrase": "sir ke upar"
    }
]

def mine_social_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, 'data', 'raw_social_media_dump.json')
    output_file = os.path.join(base_dir, 'data', 'proposed_new_patterns.json')
    
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        
    print("Initiating Social Media Data Ingestion Pipeline...")
    proposed_updates = {}
    
    for item in raw_data:
        text = item['text']
        source = item['source']
        
        # Simulate LLM Extraction
        for rule in EXTRACTION_RULES:
            if any(kw in text.lower() for kw in rule['keywords']):
                cat = rule['pain_point']
                phrase = rule['extracted_phrase']
                
                if cat not in proposed_updates:
                    proposed_updates[cat] = []
                    
                if phrase not in [p['phrase'] for p in proposed_updates[cat]]:
                    proposed_updates[cat].append({
                        "phrase": phrase,
                        "source": source,
                        "raw_context": text
                    })
                    print(f"[Miner] Extracted '{phrase}' for category '{cat}' from {source}.")
                    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(proposed_updates, f, indent=2)
        
    print(f"\n[SUCCESS] Mining complete! Proposed patterns saved to {output_file}")
    print("[WARNING] Action Required: A human researcher must review and approve these before they are merged into pain_point_taxonomy.json.")

if __name__ == "__main__":
    mine_social_data()
