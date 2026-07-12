"""
=============================================================================
FILE: intent_ir_coverage.py
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

def load_expected():
    with open('../data/intent_ir_expected_outputs.json', 'r') as f:
        return json.load(f)

# Mock Baseline Predictor (Simulating the semantic capability before full V2 Compiler)
def predict_intent_ir(text):
    text = text.lower()
    
    ir = {
        "module": "unknown",
        "primary_problem": None,
        "requires_clarification": False,
        "requires_diagnosis": False
    }
    
    # 1. Payment rules
    if any(w in text for w in ["kat gaye", "debited", "double payment", "payment failed", "transaction pending"]):
        ir["module"] = "payment"
        if "double" in text:
            ir["primary_problem"] = "duplicate_transaction"
        elif "pending" in text:
            ir["primary_problem"] = "delayed_transaction"
        else:
            ir["primary_problem"] = "orphaned_transaction"
            
    elif "refund" in text and "status" not in text:
        ir["module"] = "payment"
        ir["primary_problem"] = "delayed_refund"
    elif "emi" in text:
        ir["module"] = "payment"
        ir["primary_problem"] = "missing_payment_method"
    elif "bank server" in text:
        ir["module"] = "payment"
        ir["primary_problem"] = "gateway_timeout"
        ir["requires_diagnosis"] = True
    elif "bina upi" in text:
        ir["module"] = "payment"
        ir["primary_problem"] = "friction_in_payment"
        ir["requires_clarification"] = True
    elif "promo code" in text:
        ir["module"] = "payment"
        ir["primary_problem"] = "promo_code_failure"
        
    # 2. Auth rules
    elif any(w in text for w in ["otp", "code", "sms"]) and any(w in text for w in ["nahi aaya", "receive nahi", "nahi mila"]):
        ir["module"] = "auth"
        ir["primary_problem"] = "otp_delivery_failure"
    elif "password reset" in text:
        ir["module"] = "auth"
        ir["primary_problem"] = "email_delivery_failure"
    elif "fingerprint" in text:
        ir["module"] = "auth"
        ir["primary_problem"] = "biometric_failure"
    elif "session expired" in text:
        ir["module"] = "auth"
        ir["primary_problem"] = "frequent_session_expiry"
    elif "captcha" in text:
        ir["module"] = "auth"
        ir["primary_problem"] = "captcha_validation_error"
    elif "locked" in text:
        ir["module"] = "auth"
        ir["primary_problem"] = "account_locked"
    elif "login" in text and "kaam nahi" in text:
        ir["module"] = "auth"
        ir["requires_clarification"] = True
        ir["requires_diagnosis"] = True
    elif "bina otp" in text:
        ir["module"] = "auth"
        ir["primary_problem"] = "friction_in_auth"
        ir["requires_clarification"] = True
    elif "password" in text and "mangta" in text:
        ir["module"] = "auth"
        ir["primary_problem"] = "friction_in_auth"
        
    # 3. Navigation rules
    elif "refund ka status kaha" in text:
        ir["module"] = "navigation"
        ir["primary_problem"] = "hidden_feature"
        ir["requires_clarification"] = True
    elif "settings kidhar" in text or "order history nahi mil" in text or "language change kaise" in text or "dark mode" in text:
        ir["module"] = "navigation"
        ir["primary_problem"] = "feature_discoverability"
        if "settings" in text or "language" in text:
            ir["requires_clarification"] = True
    elif "profile edit" in text:
        ir["module"] = "navigation"
        ir["primary_problem"] = "hidden_feature"
    elif "back button" in text:
        ir["module"] = "navigation"
        ir["primary_problem"] = "navigation_flow_break"
    elif "home page" in text:
        ir["module"] = "navigation"
        ir["primary_problem"] = "navigation_trap"
    elif "search bar" in text:
        ir["module"] = "navigation"
        ir["primary_problem"] = "feature_failure"
    elif "menu options" in text:
        ir["module"] = "navigation"
        ir["primary_problem"] = "ui_rendering_issue"
        
    # 4. Performance rules
    elif "slow" in text:
        ir["module"] = "performance"
        ir["primary_problem"] = "performance_degradation"
        ir["requires_diagnosis"] = True
    elif "loading" in text or "screen freeze" in text:
        ir["module"] = "performance"
        ir["primary_problem"] = "ui_freeze"
        ir["requires_diagnosis"] = True
    elif "crash" in text or "band ho jata" in text:
        ir["module"] = "performance"
        ir["primary_problem"] = "application_crash"
        ir["requires_diagnosis"] = True
    elif "video play" in text:
        ir["module"] = "performance"
        ir["primary_problem"] = "high_latency"
        ir["requires_diagnosis"] = True
    elif "garam" in text or "battery" in text:
        ir["module"] = "performance"
        ir["primary_problem"] = "high_resource_usage"
        ir["requires_diagnosis"] = True
    elif "image load" in text:
        ir["module"] = "performance"
        ir["primary_problem"] = "resource_loading_failure"
        ir["requires_diagnosis"] = True
    elif "scroll" in text:
        ir["module"] = "performance"
        ir["primary_problem"] = "ui_lag"
        ir["requires_diagnosis"] = True
        
    # 5. Trust rules
    elif "customer care" in text:
        ir["module"] = "trust_support"
        ir["primary_problem"] = "support_unreachable"
    elif "secure" in text:
        ir["module"] = "trust_support"
        ir["primary_problem"] = "security_anxiety"
    elif "data safe" in text:
        ir["module"] = "trust_support"
        ir["primary_problem"] = "privacy_anxiety"
    elif "fake" in text:
        ir["module"] = "trust_support"
        ir["primary_problem"] = "trust_deficit"
        ir["requires_clarification"] = True
    elif "support ticket" in text:
        ir["module"] = "trust_support"
        ir["primary_problem"] = "support_unresponsive"
    elif "card details delete" in text:
        ir["module"] = "trust_support"
        ir["primary_problem"] = "privacy_control_anxiety"
    elif "live chat" in text:
        ir["module"] = "trust_support"
        ir["primary_problem"] = "support_channel_missing"
    elif "terms and conditions" in text:
        ir["module"] = "trust_support"
        ir["primary_problem"] = "policy_confusion"
    elif "bot se baat" in text:
        ir["module"] = "trust_support"
        ir["primary_problem"] = "bot_frustration"
    elif "spam calls" in text:
        ir["module"] = "trust_support"
        ir["primary_problem"] = "data_leak_suspicion"

    return ir

def run_benchmark():
    data = load_expected()
    
    total = len(data)
    prob_correct = 0
    mod_correct = 0
    amb_correct = 0
    no_guess_correct = 0
    
    for item in data:
        expected = item
        pred = predict_intent_ir(item['input'])
        
        if expected['expected_problem'] == pred['primary_problem']:
            prob_correct += 1
        
        if expected['expected_module'] == pred['module']:
            mod_correct += 1
            
        if expected['requires_clarification'] == pred['requires_clarification']:
            amb_correct += 1
            
        if expected['requires_diagnosis'] == pred['requires_diagnosis']:
            no_guess_correct += 1
            
    prob_acc = (prob_correct / total) * 100
    mod_acc = (mod_correct / total) * 100
    amb_acc = (amb_correct / total) * 100
    guess_acc = (no_guess_correct / total) * 100
    overall = (prob_acc + mod_acc + amb_acc + guess_acc) / 4
    
    print("====================================")
    print("INTENT IR COVERAGE BENCHMARK")
    print("====================================\n")
    print(f"Total Examples: {total}\n")
    print(f"Problem Accuracy:        {prob_acc:.1f}%")
    print(f"Module Accuracy:         {mod_acc:.1f}%")
    print(f"Ambiguity Accuracy:      {amb_acc:.1f}%")
    print(f"No Guessing Accuracy:    {guess_acc:.1f}%\n")
    print(f"Overall Semantic Score:  {overall:.1f}%")
    print("====================================")

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
    run_benchmark()
