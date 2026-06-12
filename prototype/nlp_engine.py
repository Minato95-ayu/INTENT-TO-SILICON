import json
import os

# =====================================================================
# INTENT-TO-SILICON: NLP Engine v2.0 (with Emotional Layer)
# Solves 6 AI failures + Maps Emotion -> UX Patterns
# =====================================================================

def load_json(filename):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base_dir, 'dictionary', filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_libraries():
    return load_json('nlp_semantic_library.json'), load_json('emotion_semantic_library.json')

def is_word_matching_root(input_word, root_lemmas):
    for root in root_lemmas:
        if root in input_word:
            return True
    return False

def start_nlp_engine():
    print("==================================================")
    print(" INTENT-TO-SILICON : Translator v2.0 (Functional + Emotion)")
    print("==================================================")
    print("System: Batao bhai, kaisa software banana hai?")
    
    func_library, emotion_library = load_libraries()
    
    while True:
        try:
            user_input = input("\nTu (User): ").lower().strip()
        except EOFError:
            break
            
        if user_input in ['exit', 'quit', 'bas']:
            break
            
        words = user_input.split()
        
        matched_func_categories = []
        matched_emotions = []
        
        final_func_specs = []
        hard_dependencies = set()
        emotion_candidates = []
        
        # ---------------------------------------------------------
        # Step 1: Intent Extraction (Primary: Functional, Secondary: Emotional)
        # ---------------------------------------------------------
        for word in words:
            # 1. Functional Extraction
            for category, data in func_library.items():
                if is_word_matching_root(word, data['root_lemmas']):
                    if category not in matched_func_categories:
                        matched_func_categories.append(category)
            
            # 2. Emotion Extraction
            for category, data in emotion_library.items():
                if is_word_matching_root(word, data['root_lemmas']):
                    if category not in matched_emotions:
                        matched_emotions.append(category)
        
        # ---------------------------------------------------------
        # OOV Detection
        # ---------------------------------------------------------
        if not matched_func_categories and not matched_emotions:
            print("System (OOV Error): Bhai, is sentence mein koi technical ya emotional intent nahi mila.")
            continue
            
        # ---------------------------------------------------------
        # Step 2: Active Disambiguation (Only for Functional)
        # ---------------------------------------------------------
        if matched_func_categories:
            for category in matched_func_categories:
                data = func_library[category]
                print(f"\nSystem (Disambiguation): {data['cross_question']}")
                reply = input("Tu (Reply): ").lower()
                
                if '2' in reply or 'ekdum' in reply or 'proper' in reply or 'haan' in reply:
                    final_func_specs.append(data['exact_value'])
                    for dep in data['hard_dependencies']:
                        hard_dependencies.add(dep)
        
        # ---------------------------------------------------------
        # Step 3: Emotion Mapping (Ranked UX Patterns)
        # ---------------------------------------------------------
        if matched_emotions:
            for category in matched_emotions:
                data = emotion_library[category]
                emotion_candidates.append({
                    "emotion": data['emotion_type'],
                    "confidence": data['base_confidence'],
                    "ux_patterns": data['candidate_ux_patterns']
                })
        
        # ---------------------------------------------------------
        # Step 4: Structured Output
        # ---------------------------------------------------------
        print("\n==================================================")
        print(" TRANSLATION RESULT (Human Intent -> Architecture) ")
        print("==================================================")
        
        # PRIMARY: Functional Architecture
        print("\n[PRIMARY: FUNCTIONAL ARCHITECTURE]")
        if final_func_specs:
            for spec in final_func_specs:
                print(f" ✅ {spec}")
            if hard_dependencies:
                for dep in hard_dependencies:
                    print(f" ⚙️  HARD DEPENDENCY: {dep}")
        else:
            print(" ℹ️  Standard defaults applied.")
            
        # SECONDARY: Emotional UX Design
        if emotion_candidates:
            print("\n[SECONDARY: EMOTIONAL UX MODIFIERS]")
            for ec in emotion_candidates:
                print(f" 🎭 Emotion Detected: {ec['emotion']} (Confidence: {ec['confidence']})")
                print(" 💡 Candidate UX Patterns:")
                for pattern in ec['ux_patterns']:
                    print(f"    - {pattern}")
                    
        print("==================================================")

if __name__ == "__main__":
    start_nlp_engine()
