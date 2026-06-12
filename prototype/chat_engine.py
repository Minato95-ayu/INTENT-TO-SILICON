import csv
import os

# Yeh function hamari dictionary CSV load karega
def load_dictionary(filepath):
    dictionary_map = {}
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # remove spaces and make lowercase for easy matching
                word = row['hindi_word'].lower().strip()
                dictionary_map[word] = {
                    'english': row['english_meaning'],
                    'tech_spec': row['technical_spec']
                }
    except FileNotFoundError:
        print("Error: Dictionary file nahi mili!")
    return dictionary_map

# Layer 3: Cross Questioning Engine
# Agar user ambiguous word use karta hai, toh hum pehle use cross-question karenge
cross_questions = {
    "fast": "Kitna fast chahiye bhai? (1) Normal speed ya (2) Ekdum ultra-low latency (< 200ms)?",
    "secure": "Security kis level ki? (1) Sirf login password ya (2) Proper AES-256 encryption?",
    "log": "Kitne log use karenge lagbhag? (1) Sirf main aur mere dost ya (2) Bahut saari public?",
    "payment": "Payment kaise loge? (1) Sirf UPI ya (2) Credit Card/International bhi?",
    "private": "Kaun dekh sakta hai? (1) Sab log ya (2) Sirf main dekhun?"
}

def start_chatbot():
    print("==================================================")
    print(" INTENT-TO-SILICON : Prototype Engine v0.1")
    print("==================================================")
    print("System: Batao bhai, kaisa software banana hai?")
    print("(Type 'exit' to stop)\n")
    
    # Locate dictionary path automatically
    base_dir = os.path.dirname(os.path.dirname(__file__))
    dict_path = os.path.join(base_dir, 'dictionary', 'hinglish_technical_map.csv')
    tech_dictionary = load_dictionary(dict_path)
    
    # Store finalized specs
    final_specs = []
    
    while True:
        user_input = input("\nTu (User): ").lower()
        
        if user_input in ['exit', 'quit', 'bas', 'band karo']:
            print("System: Bye! Tera architecture ready hai.")
            break
            
        # ---------------------------------------------------------
        # Step 1: Detect ambiguity and ask cross questions (Layer 3)
        # ---------------------------------------------------------
        clarified_intent = user_input
        
        for vague_word, question in cross_questions.items():
            if vague_word in user_input:
                print(f"\nSystem (Layer 3 - Disambiguation): {question}")
                reply = input("Tu (User): ").lower()
                
                # Simple human-like logic: agar option 2 ya strong words select kiye
                if '2' in reply or 'ekdum' in reply or 'bahut' in reply or 'proper' in reply or 'sirf' in reply:
                    # Update intent behind the scenes
                    if vague_word == "fast": clarified_intent += " ekdum fast chahiye"
                    elif vague_word == "secure": clarified_intent += " secure chahiye"
                    elif vague_word == "log": clarified_intent += " bahut log aayenge"
                    elif vague_word == "payment": clarified_intent += " payment chahiye"
                    elif vague_word == "private": clarified_intent += " sirf main dekhun"
                else:
                    print("System: Theek hai, standard/normal rakhenge.")
        
        # ---------------------------------------------------------
        # Step 2: Dictionary Match (Layer 4)
        # ---------------------------------------------------------
        print("\n--- Layer 4: Dictionary Mapping ---")
        matched_something = False
        
        for hindi_phrase, mapping in tech_dictionary.items():
            if hindi_phrase in clarified_intent:
                print(f"Matched Intent: '{hindi_phrase}' -> {mapping['tech_spec']}")
                if mapping['tech_spec'] not in final_specs:
                    final_specs.append(mapping['tech_spec'])
                matched_something = True
                
        if not matched_something:
            print("System: Samajh nahi aaya, thoda clear words mein batao.")
        else:
            # ---------------------------------------------------------
            # Step 3: Structure Generate (Layer 5)
            # ---------------------------------------------------------
            print("\nSystem (Layer 5 - Structured Architecture):")
            print("Abhi tak ka finalized technical format:")
            for spec in final_specs:
                print(f" ✅ {spec}")

if __name__ == "__main__":
    start_chatbot()
