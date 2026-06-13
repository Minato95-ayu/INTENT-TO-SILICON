import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from prototype.nlp_engine import process_single_input, load_libraries, load_json

def save_user_profile(profiles):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base_dir, 'data', 'user_profiles.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=2)

def continuous_learning_loop(user_input, user_id):
    func_lib, emotion_lib = load_libraries()
    
    # Load profile to inject custom learned slangs into the libraries dynamically
    profiles = load_json('user_profiles.json', folder='data')
    user_profile = profiles.get(user_id, {})
    
    learned_slang = user_profile.get("learned_slang", {})
    
    # Temporarily inject learned slang into runtime library
    for slang, category in learned_slang.items():
        if category in func_lib:
            func_lib[category]['root_lemmas'].append(slang)
        elif category in emotion_lib:
            if 'examples' in emotion_lib[category]:
                emotion_lib[category]['examples'].append(slang)
            else:
                emotion_lib[category].setdefault('root_lemmas', []).append(slang)
    print(f"\nUser [{user_id}]: {user_input}")
    
    # Run the standard engine
    # Headless reply "1" to bypass standard cross questions for this test script
    metrics = process_single_input(user_input, func_lib, emotion_lib, user_id=user_id, headless_reply="1")
    
    if metrics["status"] == "fail_hard":
        print("\n[System (v0.7 Continuous Learning)]: Safe Halt Triggered (Out of Vocabulary).")
        print("System: Mujhe aapka word samajh nahi aaya. Ye word kis category ka hai?")
        
        # Display categories for the user to map to
        categories = list(func_lib.keys()) + list(emotion_lib.keys())
        for i, cat in enumerate(categories):
            print(f"  {i+1}. {cat}")
            
        # Simulated user response (in production, this would be real user input)
        target_category = "performance"
        target_word = "jhakkaas"
        print(f"\nTu: Word '{target_word}' ka matlab '{target_category}' hai.")
        
        # Input Validation: Only allow safe alphabetic words (no code injection)
        import re
        if not re.match(r'^[a-zA-Z\u0900-\u097F ]+$', target_word):
            print(f"\n[Security] Invalid input rejected: '{target_word}' contains unsafe characters.")
            return
        if target_category not in categories:
            print(f"\n[Security] Invalid category rejected: '{target_category}' is not a known category.")
            return
        
        print(f"\n[System]: Learning mapped! '{target_word}' -> '{target_category}'")

        # Save to user profile
        if "learned_slang" not in user_profile:
            user_profile["learned_slang"] = {}
        user_profile["learned_slang"][target_word] = target_category
        
        profiles[user_id] = user_profile
        save_user_profile(profiles)
        
        print("[System]: Re-running with updated localized vocabulary...")
        
        # Re-run loop
        continuous_learning_loop(user_input, user_id)
        
    elif metrics["blueprint_path"]:
        print(f"[System]: Success! Intent locked. Blueprint generated at {metrics['blueprint_path']}")
        
if __name__ == "__main__":
    print("==================================================")
    print(" INTENT-TO-SILICON : Continuous Learning v0.7")
    print("==================================================")
    
    # We pass a slang "fatafat" which is currently mapped to urgency.
    # Wait, "fatafat" is already in urgency! 
    # Let's use a completely fake slang word "jhakkaas"
    continuous_learning_loop("mujhe ek jhakkaas system chahiye", "user_tech_lead_anjali")
