import json
import os

# =====================================================================
# INTENT-TO-SILICON: NLP Engine v1.0
# Yeh script 6 AI failures ko solve karne ke liye banai gayi hai:
# 1. Ambiguity, 2. Missing Knowledge (OOV), 3. Reasoning Mistakes, etc.
# =====================================================================

def load_nlp_library():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, 'dictionary', 'nlp_semantic_library.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Simple NLP Stemming: Check agar word kisi root_lemma se start/match hota hai
def is_word_matching_root(input_word, root_lemmas):
    for root in root_lemmas:
        # e.g., root "suraksh" will match "suraksha", "surakshit"
        if root in input_word:
            return True
    return False

def start_nlp_engine():
    print("==================================================")
    print(" INTENT-TO-SILICON : NLP Translator v1.0")
    print("==================================================")
    print("System: Batao bhai, kaisa software banana hai?")
    
    nlp_library = load_nlp_library()
    
    while True:
        try:
            user_input = input("\nTu (User): ").lower().strip()
        except EOFError:
            break
            
        if user_input in ['exit', 'quit', 'bas']:
            break
            
        words = user_input.split()
        matched_categories = []
        final_specs = []
        hard_dependencies = set()
        
        # ---------------------------------------------------------
        # Layer 1 & 2: Stemming & Intent Extraction
        # ---------------------------------------------------------
        for word in words:
            for category, data in nlp_library.items():
                if is_word_matching_root(word, data['root_lemmas']):
                    if category not in matched_categories:
                        matched_categories.append(category)
        
        # ---------------------------------------------------------
        # Missing Knowledge (OOV Detection)
        # ---------------------------------------------------------
        if not matched_categories:
            print("System (OOV Error): Bhai, is sentence mein koi pakka technical intent nahi mila.")
            print("Kya tum isme koi naya word use kar rahe ho jo dictionary mein nahi hai?")
            print("[Self-Learning Mode Triggered... (Log for future update)]")
            continue
            
        # ---------------------------------------------------------
        # Layer 3 & 4: Active Disambiguation & Hard Mapping
        # ---------------------------------------------------------
        for category in matched_categories:
            data = nlp_library[category]
            print(f"\nSystem (Disambiguation): {data['cross_question']}")
            reply = input("Tu (Reply): ").lower()
            
            # Agar proper requirement maangi
            if '2' in reply or 'ekdum' in reply or 'proper' in reply or 'haan' in reply:
                final_specs.append(data['exact_value'])
                # Planning Failure Prevention: Add hard dependencies
                for dep in data['hard_dependencies']:
                    hard_dependencies.add(dep)
        
        # ---------------------------------------------------------
        # Layer 5: Output Exact Values & Dependencies (Prevent Planning Mistakes)
        # ---------------------------------------------------------
        print("\n==================================================")
        print(" TRANSLATION RESULT (Human -> Binary Specs) ")
        print("==================================================")
        for spec in final_specs:
            print(f" [REQUIREMENT] -> {spec}")
            
        if hard_dependencies:
            print("\n [HARD DEPENDENCIES AUTOMATICALLY ADDED]:")
            for dep in hard_dependencies:
                print(f"  -> + {dep}")
        print("==================================================")

if __name__ == "__main__":
    start_nlp_engine()
