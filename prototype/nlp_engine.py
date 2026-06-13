import json
import os
from datetime import datetime

# =====================================================================
# INTENT-TO-SILICON: NLP Engine v0.4 (Evaluation Ready)
# Decoupled processing logic for benchmarking and headless evaluation.
# Track Clarification Required instead of Fail_Ambiguous.
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

def generate_blueprint_yaml(func_specs, hard_dependencies, emotion_candidates, excluded_specs=None):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_dir = os.path.join(base_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    if excluded_specs is None:
        excluded_specs = []
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    blueprint_filename = f"intent_blueprint_{timestamp}.yaml"
    blueprint_path = os.path.join(output_dir, blueprint_filename)
    
    blueprint_data = {
        "project": {
            "name": "Intent-to-Silicon Generated Project",
            "version": "0.4.0",
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
    if excluded_specs:
        blueprint_data["functional_architecture"]["excluded_requirements"] = excluded_specs
        
    yaml_content = dict_to_yaml(blueprint_data)
    
    with open(blueprint_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
        
    return blueprint_path

def process_single_input(user_input, func_library, emotion_library, headless_reply=None):
    """Processes a single input and returns metrics and blueprint path."""
    BACKWARD_NEGATORS = ['nahi', 'nahin', 'mat', 'na']
    FORWARD_NEGATORS = ['without', 'exclude', 'remove', 'no', "don't", 'do not']
    CLAUSE_DELIMITERS = [',', '.', 'lekin', 'par', 'but', 'and', 'aur']

    normalized_input = user_input.lower()
    for delim in CLAUSE_DELIMITERS:
        if len(delim) > 1:
            normalized_input = normalized_input.replace(f" {delim} ", "|")
        else:
            normalized_input = normalized_input.replace(delim, "|")
            
    clauses = [c.strip() for c in normalized_input.split("|") if c.strip()]

    matched_func_categories = []
    matched_emotions = []
    negated_func_categories = []
    
    final_func_specs = []
    final_excluded_specs = []
    hard_dependencies = set()
    emotion_candidates = []
    
    # 1. Intent Extraction with Clause Boundaries & Directional Heuristics
    for clause in clauses:
        words = clause.split()
        clause_funcs = []
        clause_emotions = []
        
        for i, word in enumerate(words):
            for category, data in func_library.items():
                if is_word_matching_root(word, data['root_lemmas']):
                    clause_funcs.append((category, i))
            
            for category, data in emotion_library.items():
                if is_word_matching_root(word, data['root_lemmas']):
                    clause_emotions.append((category, i))
                    
        backward_indices = [i for i, w in enumerate(words) if w in BACKWARD_NEGATORS]
        forward_indices = [i for i, w in enumerate(words) if w in FORWARD_NEGATORS]
        
        for cat, idx in clause_funcs:
            is_negated = False
            for b_idx in backward_indices:
                if 0 < b_idx - idx <= 3:
                    is_negated = True
                    break
            for f_idx in forward_indices:
                if 0 < idx - f_idx <= 3:
                    is_negated = True
                    break
                    
            if is_negated:
                if cat not in negated_func_categories:
                    negated_func_categories.append(cat)
            else:
                if cat not in matched_func_categories:
                    matched_func_categories.append(cat)
                    
        for cat, idx in clause_emotions:
            if cat not in matched_emotions:
                matched_emotions.append(cat)
                
    metrics = {
        "initial_ambiguity_count": len(matched_func_categories),
        "emotions_detected": len(matched_emotions),
        "negated_intents_detected": len(negated_func_categories),
        "status": "success",
        "blueprint_path": None,
        "questions_asked": len(matched_func_categories)
    }

    # OOV Detection
    if not matched_func_categories and not matched_emotions and not negated_func_categories:
        metrics["status"] = "fail_hard"
        return metrics
        
    # 2. Active Disambiguation (Functional) - v0.5 Upgrade
    if matched_func_categories:
        for category in matched_func_categories:
            data = func_library[category]
            
            if headless_reply is not None:
                reply = headless_reply
            else:
                print(f"\nSystem (Ambiguity Detected!): {data['cross_question']}")
                reply = input("Tu (Reply: Enter option number): ").strip()
            
            options = data.get('options', {})
            
            # For backward compatibility with negated categories or if options aren't fully migrated
            if 'exact_value' in data and not options:
                # Legacy v0.4 logic fallback
                if reply in ['yes', 'haan', '1', '2']:
                    final_func_specs.append({
                        "category": category,
                        "value": data['exact_value'],
                        "confidence": 1.0,
                        "source": "user clarified (legacy)"
                    })
                    for dep in data.get('hard_dependencies', []):
                        hard_dependencies.add(dep)
            else:
                # v0.5 Strict Disambiguation
                if reply in options:
                    selected_option = options[reply]
                    final_func_specs.append({
                        "category": category,
                        "value": selected_option['exact_value'],
                        "confidence": 1.0,
                        "source": f"user actively disambiguated (selected option {reply})"
                    })
                    for dep in selected_option['hard_dependencies']:
                        hard_dependencies.add(dep)
                else:
                    # User provided invalid input, 'no', or missing headless reply. Ambiguity unresolved.
                    pass
                
    # If functional categories matched but ambiguity was not resolved for all of them
    if matched_func_categories and len(final_func_specs) < len(matched_func_categories):
        metrics["status"] = "clarification_required"
        
    # 3. Emotion Mapping - v0.5 Upgrade (Active Disambiguation for Psychology)
    if matched_emotions:
        for category in matched_emotions:
            data = emotion_library[category]
            
            if headless_reply is not None:
                reply = headless_reply
            else:
                print(f"\nSystem (Emotional Ambiguity Detected!): {data['cross_question']}")
                reply = input("Tu (Reply: Enter option number): ").strip()
            
            options = data.get('options', {})
            
            # Legacy fallback if no options defined
            if 'candidate_ux_patterns' in data and not options:
                emotion_candidates.append({
                    "emotion": data['emotion_type'],
                    "confidence": data['base_confidence'],
                    "source": "inferred from text (legacy)",
                    "ux_patterns": data['candidate_ux_patterns']
                })
            else:
                # Strict v0.5 Disambiguation for Emotions
                if reply in options:
                    selected_option = options[reply]
                    emotion_candidates.append({
                        "emotion": data['emotion_type'],
                        "confidence": 1.0,
                        "source": f"user emotionally disambiguated (selected option {reply})",
                        "ux_patterns": selected_option['ux_patterns'],
                        "technical_spec": selected_option['technical_spec']
                    })
                else:
                    # User provided invalid input. Emotion remains unresolved.
                    pass
                    
    # If emotions matched but ambiguity was not resolved for all of them
    if matched_emotions and len(emotion_candidates) < len(matched_emotions):
        metrics["status"] = "clarification_required"

    # Process Negated Categories
    for category in negated_func_categories:
        data = func_library[category]
        # In v0.5, exact_value is inside options. We will join all option values to show what's excluded.
        if 'options' in data:
            excluded_vals = " OR ".join([opt['exact_value'] for opt in data['options'].values()])
        else:
            excluded_vals = data.get('exact_value', 'Unknown')
            
        final_excluded_specs.append({
            "category": category,
            "value": excluded_vals,
            "confidence": 1.0,
            "source": "explicitly negated"
        })

    # 4. Generate YAML if valid intent locked
    if final_func_specs or emotion_candidates or final_excluded_specs:
        blueprint_path = generate_blueprint_yaml(final_func_specs, hard_dependencies, emotion_candidates, final_excluded_specs)
        metrics["blueprint_path"] = blueprint_path
        
    return metrics

def start_nlp_engine():
    print("==================================================")
    print(" INTENT-TO-SILICON : Translator v0.4 (Eval Ready)")
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
            
        metrics = process_single_input(user_input, func_library, emotion_library)
        
        if metrics["status"] == "fail_hard":
            print("System (Hard Fail): Bhai, is sentence mein koi technical ya emotional intent nahi mila.")
        elif metrics["status"] == "clarification_required":
            print("System (Clarification Required): Bhai, aur clear batao exactly kya chahiye.")
        elif metrics["blueprint_path"]:
            print(f"✅ SUCCESS: Machine-Readable YAML Blueprint Generated!")
            print(f"📁 Path: {metrics['blueprint_path']}")

if __name__ == "__main__":
    start_nlp_engine()
