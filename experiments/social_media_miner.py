import json
import os
import sys

# Simulated Extraction Rules (In production, this would be an LLM call)
EXTRACTION_RULES = [
    {
        "keywords": ["gol gol ghoomne", "slow", "time lagata"],
        "pain_point": "performance_frustration",
        "extracted_phrase": "gol gol ghoomne"
    },
    {
        "keywords": ["udd gaye", "kat gaye", "lootere"],
        "pain_point": "payment_anxiety",
        "extracted_phrase": "rupay udd gaye"
    },
    {
        "keywords": ["itne saare button", "samajh nahi aata", "chidiya ud jaye"],
        "pain_point": "navigation_confusion",
        "extracted_phrase": "chidiya ud jaye"
    },
    {
        "keywords": ["data leak", "dar lagta", "delete"],
        "pain_point": "trust_deficit",
        "extracted_phrase": "data leak ho jayega"
    },
    {
        "keywords": ["tatkal book", "fast", "session expire"],
        "pain_point": "urgency",
        "extracted_phrase": "session expire"
    },
    {
        "keywords": ["bot system", "insaan se baat", "phone nahi uthate"],
        "pain_point": "support_frustration",
        "extracted_phrase": "phone nahi uthate"
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
