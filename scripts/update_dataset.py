import json
import os
import random

def generate_robust_dataset():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    dataset_path = os.path.join(base_dir, 'data', 'mock_pain_points_dataset.json')
    
    # Let's create exactly 100 structured test cases to test the new aggressive engine
    dataset = []
    
    # 1. Standard Pain Points (Emotion -> Functional mapping test)
    phrases_payment = ["paise kat gaye par order nahi hua", "refund kab aayega bhai", "account khali kar dega ye app", "fraud ho gaya mere sath", "double payment lag gaya"]
    phrases_nav = ["kaha click karu kuch samajh nahi aa raha", "pata nahi aage kya karna hai confuse hu", "sir ke upar se gaya ye interface", "kuch dikh nahi raha"]
    phrases_perf = ["app hang ho gaya beech mein", "safed screen aa gayi aur atak gaya", "slow hai bekar app", "kholte kholte subah ho jayegi", "load nahi ho raha hai ghoom raha hai"]
    phrases_trust = ["data leak hone ka dar hai", "safe nahi lag raha fraud hoga", "mera data chori ho gaya toh?"]
    phrases_support = ["customer care se baat karni hai koi nahi sunta", "bot bakwas hai insaan se connect karo", "koi sunne wala nahi hai"]
    
    for p in phrases_payment: dataset.append({"phrase": p, "expected_category": "payment_anxiety", "type": "emotion"})
    for p in phrases_nav: dataset.append({"phrase": p, "expected_category": "navigation_confusion", "type": "emotion"})
    for p in phrases_perf: dataset.append({"phrase": p, "expected_category": "performance_frustration", "type": "emotion"})
    for p in phrases_trust: dataset.append({"phrase": p, "expected_category": "trust_deficit", "type": "emotion"})
    for p in phrases_support: dataset.append({"phrase": p, "expected_category": "support_frustration", "type": "emotion"})

    # 2. Negation Test Cases (Testing clause boundary)
    negation_cases = [
        {"phrase": "fast chahiye par chat nahi", "expected_category": "performance", "negated": "realtime", "type": "negation"},
        {"phrase": "safe hona chahiye, bina live sync ke", "expected_category": "security", "negated": "realtime", "type": "negation"},
        {"phrase": "database chahiye lekin offline mat dena", "expected_category": "database", "negated": "availability", "type": "negation"},
        {"phrase": "speed chahiye par bina login ke", "expected_category": "performance", "negated": "security", "type": "negation"},
        {"phrase": "scale acha ho, par data save mat karna", "expected_category": "scale", "negated": "database", "type": "negation"}
    ]
    for n in negation_cases: dataset.append(n)
    
    # 3. OOV / Safe Halt Cases
    safe_halt_cases = [
        "mujhe pizza khana hai", "xyz123 random words hdjskd", "aaj mausam kaisa hai", "sachin tendulkar ne match jeeta", "I want to watch a movie on netflix"
    ]
    for s in safe_halt_cases: dataset.append({"phrase": s, "expected_category": "safe_halt", "type": "oov"})
    
    # 4. Low Confidence / Short Phrases (Should trigger forced questions)
    low_confidence_cases = [
        {"phrase": "sirf data theek karo", "expected_category": "database", "type": "low_confidence"},
        {"phrase": "login banao", "expected_category": "security", "type": "low_confidence"},
        {"phrase": "chat chahiye", "expected_category": "realtime", "type": "low_confidence"}
    ]
    for l in low_confidence_cases: dataset.append(l)

    # Fill the rest to 100 with random variations of performance, payment, scale, database, etc.
    functional_phrases = [
        {"phrase": "bohot public aayegi server crash nahi hona chahiye", "expected_category": "scale"},
        {"phrase": "realtime chat chahiye jismein speed achi ho", "expected_category": "realtime"},
        {"phrase": "offline bhi chalna chahiye", "expected_category": "availability"},
        {"phrase": "data database mein save hona chahiye security ke sath", "expected_category": "database"},
        {"phrase": "fast speed loading chahiye", "expected_category": "performance"}
    ]
    
    while len(dataset) < 100:
        c = random.choice(functional_phrases)
        dataset.append({"phrase": c["phrase"] + f" {random.randint(1,1000)}", "expected_category": c["expected_category"], "type": "functional"})
        
    with open(dataset_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2)
        
    print(f"Generated robust dataset with {len(dataset)} items.")

if __name__ == "__main__":
    generate_robust_dataset()
