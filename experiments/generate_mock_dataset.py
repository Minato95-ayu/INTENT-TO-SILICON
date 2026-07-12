"""
=============================================================================
FILE: generate_mock_dataset.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import json
import os

mock_data = [
    # Payment Anxiety
    {"phrase": "paise kat gaye par order nahi hua", "expected_intent": "Payment Anxiety", "category": "payment_anxiety"},
    {"phrase": "refund kab aayega bhai", "expected_intent": "Payment Anxiety", "category": "payment_anxiety"},
    {"phrase": "account khali kar dega ye app", "expected_intent": "Payment Anxiety", "category": "payment_anxiety"},
    {"phrase": "scam lag raha hai mereko", "expected_intent": "Payment Anxiety", "category": "payment_anxiety"},
    {"phrase": "gareeb bana dega mehenga hai", "expected_intent": "Payment Anxiety", "category": "payment_anxiety"},
    
    # Performance Frustration
    {"phrase": "kholte kholte subah ho jayegi", "expected_intent": "Performance Frustration", "category": "performance_frustration"},
    {"phrase": "app hang ho gaya beech mein", "expected_intent": "Performance Frustration", "category": "performance_frustration"},
    {"phrase": "safed screen aa gayi aur atak gaya", "expected_intent": "Performance Frustration", "category": "performance_frustration"},
    {"phrase": "slow hai bekar app", "expected_intent": "Performance Frustration", "category": "performance_frustration"},
    {"phrase": "load nahi ho raha hai ghoom raha hai", "expected_intent": "Performance Frustration", "category": "performance_frustration"},
    
    # Navigation Confusion
    {"phrase": "kaha click karu kuch samajh nahi aa raha", "expected_intent": "Navigation / UI Confusion", "category": "navigation_confusion"},
    {"phrase": "pata nahi aage kya karna hai confuse hu", "expected_intent": "Navigation / UI Confusion", "category": "navigation_confusion"},
    {"phrase": "sir ke upar se gaya ye interface", "expected_intent": "Navigation / UI Confusion", "category": "navigation_confusion"},
    {"phrase": "bohot bawasir UI hai", "expected_intent": "Navigation / UI Confusion", "category": "navigation_confusion"},
    {"phrase": "uljhan ho rahi hai hard hai", "expected_intent": "Navigation / UI Confusion", "category": "navigation_confusion"},
    
    # Urgency
    {"phrase": "jaldi kar bhai time nahi hai", "expected_intent": "Urgency", "category": "urgency"},
    {"phrase": "fatafat checkout karna hai", "expected_intent": "Urgency", "category": "urgency"},
    {"phrase": "emergency mein turant kaam aana chahiye", "expected_intent": "Urgency", "category": "urgency"},
    
    # Trust Deficit
    {"phrase": "data leak hone ka dar hai", "expected_intent": "Trust Deficit", "category": "trust_deficit"},
    {"phrase": "safe nahi lag raha fraud hoga", "expected_intent": "Trust Deficit", "category": "trust_deficit"},
    {"phrase": "mera data chori ho gaya toh?", "expected_intent": "Trust Deficit", "category": "trust_deficit"},
    
    # Support Frustration
    {"phrase": "customer care se baat karni hai koi nahi sunta", "expected_intent": "Support Frustration", "category": "support_frustration"},
    {"phrase": "bot bakwas hai insaan se connect karo", "expected_intent": "Support Frustration", "category": "support_frustration"},
    
    # OOV / Safe Halt
    {"phrase": "mujhe pizza khana hai", "expected_intent": "safe_halt", "category": "safe_halt"},
    {"phrase": "xyz123 random words hdjskd", "expected_intent": "safe_halt", "category": "safe_halt"},
    {"phrase": "aaj mausam kaisa hai", "expected_intent": "safe_halt", "category": "safe_halt"},
    {"phrase": "sachin tendulkar ne match jeeta", "expected_intent": "safe_halt", "category": "safe_halt"},
    {"phrase": "I want to watch a movie on netflix", "expected_intent": "safe_halt", "category": "safe_halt"}
]

def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    os.makedirs(os.path.join(base_dir, 'data'), exist_ok=True)
    out_path = os.path.join(base_dir, 'data', 'mock_pain_points_dataset.json')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(mock_data, f, indent=2)
        
    print(f"Generated mock dataset with {len(mock_data)} phrases at {out_path}")

if __name__ == "__main__":
    main()
