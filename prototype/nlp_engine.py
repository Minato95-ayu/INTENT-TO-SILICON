import json
import os
from datetime import datetime

# =====================================================================
# INTENT-TO-SILICON: NLP Engine v3.0 (Blueprint Compiler)
# Final step: Closes the loop from Human Intent to deployable JSON Blueprint.
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

def generate_blueprint(func_specs, hard_dependencies, emotion_candidates):
    """
    Generates a machine-readable JSON blueprint from the parsed intents.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_dir = os.path.join(base_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    blueprint_filename = f"intent_blueprint_{timestamp}.json"
    blueprint_path = os.path.join(output_dir, blueprint_filename)
    
    blueprint_data = {
        "project": {
            "name": "Intent-to-Silicon Generated Project",
            "generated_at": timestamp,
            "version": "1.0.0"
        },
        "architecture": {
            "functional_requirements": func_specs,
            "hard_dependencies": list(hard_dependencies)
        },
        "ux_psychology": {
            "emotion_modifiers": emotion_candidates
        }
    }
    
    with open(blueprint_path, 'w', encoding='utf-8') as f:
        json.dump(blueprint_data, f, indent=4)
        
    return blueprint_path

def start_nlp_engine():
    print("==================================================")
    print(" INTENT-TO-SILICON : Translator v3.0 (Blueprint Compiler)")
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
        # Intent Extraction
        # ---------------------------------------------------------
        for word in words:
            for category, data in func_library.items():
                if is_word_matching_root(word, data['root_lemmas']):
                    if category not in matched_func_categories:
                        matched_func_categories.append(category)
            
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
        # Active Disambiguation (Functional)
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
        # Emotion Mapping
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
        # Blueprint Compiler Output
        # ---------------------------------------------------------
        print("\n==================================================")
        print(" TRANSLATION RESULT (Human Intent -> Silicon) ")
        print("==================================================")
        
        if final_func_specs or emotion_candidates:
            blueprint_path = generate_blueprint(final_func_specs, hard_dependencies, emotion_candidates)
            print(f"✅ SUCCESS: Machine-Readable Blueprint Generated!")
            print(f"📁 Path: {blueprint_path}")
            print("\nIs Blueprint JSON ko seedha kisi auto-deployment pipeline mein feed kiya ja sakta hai.")
        else:
            print("System: Standard defaults applied. No explicit specs triggered.")
            
        print("==================================================")

if __name__ == "__main__":
    start_nlp_engine()
