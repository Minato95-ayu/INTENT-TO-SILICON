import json
import os
from datetime import datetime

# =====================================================================
# INTENT-TO-SILICON: NLP Engine v0.3 (YAML Blueprint Compiler)
# Final step: Closes the loop from Human Intent to deployable YAML Blueprint.
# Includes Confidence Scores & Requirement Sources.
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

def dict_to_yaml(data, indent=0):
    """Simple YAML serializer to avoid pyyaml dependency"""
    yaml_str = ""
    prefix = "  " * indent
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict):
                if not v:
                    yaml_str += f"{prefix}{k}: {{}}\n"
                else:
                    yaml_str += f"{prefix}{k}:\n{dict_to_yaml(v, indent + 1)}"
            elif isinstance(v, list):
                if not v:
                    yaml_str += f"{prefix}{k}: []\n"
                else:
                    yaml_str += f"{prefix}{k}:\n"
                    for item in v:
                        if isinstance(item, dict):
                            first = True
                            for sub_k, sub_v in item.items():
                                if first:
                                    yaml_str += f"{prefix}  - {sub_k}: {sub_v}\n"
                                    first = False
                                else:
                                    if isinstance(sub_v, list):
                                        yaml_str += f"{prefix}    {sub_k}:\n{dict_to_yaml(sub_v, indent + 3)}"
                                    else:
                                        yaml_str += f"{prefix}    {sub_k}: {sub_v}\n"
                        else:
                            yaml_str += f"{prefix}  - \"{item}\"\n"
            else:
                yaml_str += f"{prefix}{k}: \"{v}\"\n"
    elif isinstance(data, list):
        for item in data:
            yaml_str += f"{prefix}- \"{item}\"\n"
    return yaml_str

def generate_blueprint_yaml(func_specs, hard_dependencies, emotion_candidates):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_dir = os.path.join(base_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    blueprint_filename = f"intent_blueprint_{timestamp}.yaml"
    blueprint_path = os.path.join(output_dir, blueprint_filename)
    
    # Structure the YAML data with clean separation
    blueprint_data = {
        "project": {
            "name": "Intent-to-Silicon Generated Project",
            "version": "0.3.0",
            "generated_at": timestamp
        },
        "functional_architecture": {
            "requirements": func_specs,
            "hard_dependencies": list(hard_dependencies)
        },
        "emotional_ux_architecture": {
            "detected_emotions": emotion_candidates
        }
    }
    
    yaml_content = dict_to_yaml(blueprint_data)
    
    with open(blueprint_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
        
    return blueprint_path

def start_nlp_engine():
    print("==================================================")
    print(" INTENT-TO-SILICON : Translator v0.3 (YAML Blueprint)")
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
                    final_func_specs.append({
                        "category": category,
                        "value": data['exact_value'],
                        "confidence": 1.0,
                        "source": "user clarified"
                    })
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
                    "source": "inferred from text",
                    "ux_patterns": data['candidate_ux_patterns']
                })
        
        # ---------------------------------------------------------
        # YAML Blueprint Generation Output
        # ---------------------------------------------------------
        print("\n==================================================")
        print(" TRANSLATION RESULT (Human Intent -> YAML Blueprint) ")
        print("==================================================")
        
        if final_func_specs or emotion_candidates:
            blueprint_path = generate_blueprint_yaml(final_func_specs, hard_dependencies, emotion_candidates)
            print(f"✅ SUCCESS: Machine-Readable YAML Blueprint Generated!")
            print(f"📁 Path: {blueprint_path}")
            print("\nIs Blueprint YAML ko sidha kisi auto-deployment pipeline (K8s/Docker) mein feed kiya ja sakta hai.")
        else:
            print("System: Standard defaults applied. No explicit specs triggered.")
            
        print("==================================================")

if __name__ == "__main__":
    start_nlp_engine()
