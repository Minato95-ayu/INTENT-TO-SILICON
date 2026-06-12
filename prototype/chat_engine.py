import json
import os

# =====================================================================
# INTENT-TO-SILICON: Semantic Engine
# Yeh script demonstrate karti hai ki Human Language ko directly 
# EXACT Binary/Technical requirements mein kaise badla jayega.
# =====================================================================

def load_semantic_library():
    """ JSON Dictionary load karta hai jisme Human Word = Exact Value mapped hai """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, 'dictionary', 'semantic_library.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: semantic_library.json nahi mili!")
        return {}

def start_translation_engine():
    print("==================================================")
    print(" INTENT-TO-SILICON : Direct Translator v0.2")
    print("==================================================")
    print("System: Batao bhai, kaisa software banana hai?")
    print("(Type 'exit' to stop)\n")
    
    # Load Library
    semantic_library = load_semantic_library()
    
    while True:
        try:
            user_input = input("\nTu (Human Intent): ").lower()
        except EOFError:
            break
            
        if user_input in ['exit', 'quit', 'bas', 'band karo']:
            print("System: Translation complete. Bye!")
            break
            
        final_binary_specs = []
        
        # ---------------------------------------------------------
        # Layer 1 to 4: Detect Ambiguity -> Cross Question -> Exact Value
        # ---------------------------------------------------------
        for category, data in semantic_library.items():
            # Check agar is category ka koi keyword user input mein hai
            keyword_found = any(kw in user_input for kw in data['keywords'])
            
            if keyword_found:
                # Ambiguity mil gayi! Ab cross-question poocho
                print(f"\nSystem (Disambiguation - {category.upper()}): {data['cross_question']}")
                try:
                    reply = input("Tu (Reply): ").lower()
                except EOFError:
                    reply = "2"
                
                # Agar user ne proper requirement maangi (Option 2 ya strong words)
                if '2' in reply or 'ekdum' in reply or 'proper' in reply or 'haan' in reply:
                    final_binary_specs.append(data['exact_value'])
                    
        # ---------------------------------------------------------
        # Layer 5: Output Exact Values
        # ---------------------------------------------------------
        if not final_binary_specs:
            print("System: Koi exact requirement nahi mili. Thoda aur clear batao.")
        else:
            print("\n==================================================")
            print(" TRANSLATION RESULT (Human -> Binary Specs) ")
            print("==================================================")
            for spec in final_binary_specs:
                print(f" [EXECUTING] -> {spec}")
            print("==================================================")

if __name__ == "__main__":
    start_translation_engine()
