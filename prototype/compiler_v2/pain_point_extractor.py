class PainPointExtractor:
    def extract(self, normalized_data):
        tokens = normalized_data['tokens']
        raw = normalized_data['raw']
        
        neg_indices = [t['index'] for t in tokens if t['tag'] == '[NEG]']
        
        ir = {
            "module": "unknown",
            "primary_problem": None,
            "secondary_problem": None,
            "evidence": [],
            "requires_diagnosis": False,
            "requires_clarification": False,
            "confidence_score": 0.0
        }
        
        def has_neg_after(word_idx, window=4):
            for n in neg_indices:
                if 0 < (n - word_idx) <= window:
                    return True
            return False

        def get_idx(word):
            for t in tokens:
                if t['word'] == word:
                    return t['index']
            return -1

        # Emotion / Trust Root Matching with NEG Proximity
        dar_idx = get_idx("dar")
        if dar_idx != -1:
            ir["module"] = "trust_support"
            if has_neg_after(dar_idx, window=3):
                ir["primary_problem"] = None
                ir["evidence"] = ["dar", "nahi"]
                ir["confidence_score"] = 0.95
            else:
                ir["primary_problem"] = "security_anxiety"
                ir["evidence"] = ["dar"]
                ir["confidence_score"] = 0.85
            return ir
            
        bot_idx = get_idx("bot")
        if bot_idx != -1:
            ir["module"] = "trust_support"
            problem_idx = max(get_idx("problem"), get_idx("issue"))
            if problem_idx != -1 and has_neg_after(problem_idx, window=2):
                ir["primary_problem"] = None
                ir["evidence"] = ["bot", "nahi"]
                ir["confidence_score"] = 0.90
            else:
                ir["primary_problem"] = "bot_frustration"
                ir["evidence"] = ["bot"]
                ir["confidence_score"] = 0.94
            return ir

        # Fallback to simulated mapping logic
        text = raw
        
        if any(w in text for w in ["kat gaye", "debited", "double payment", "payment failed", "transaction pending", "paise nahi kate", "paise ud gaye"]):
            ir["module"] = "payment"
            if "double" in text:
                ir["primary_problem"] = "duplicate_transaction"
            elif "pending" in text:
                ir["primary_problem"] = "delayed_transaction"
            elif "paise nahi kate" in text:
                ir["primary_problem"] = "unauthorized_transaction_suspicion"
                ir["requires_diagnosis"] = True
            else:
                ir["primary_problem"] = "orphaned_transaction"
                if "msg aaya par paise ud gaye" in text or "paise ud gaye" in text:
                    ir["secondary_problem"] = "false_failure_message"
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
            
        elif any(w in text for w in ["otp", "code", "sms"]) and any(w in text for w in ["nahi aaya", "receive nahi", "nahi mila", "delay"]):
            ir["module"] = "auth"
            if "delay ka koi issue nahi" in text:
                ir["primary_problem"] = "friction_in_auth"
                ir["requires_clarification"] = True
            else:
                ir["primary_problem"] = "otp_delivery_failure"
        elif "call aa sakta hai kya" in text or "dusre number pe" in text:
            ir["module"] = "auth"
            ir["primary_problem"] = "friction_in_auth"
            ir["requires_clarification"] = True
        elif "password reset" in text or "email verification" in text:
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
            
        elif "refund ka status kaha" in text:
            ir["module"] = "navigation"
            ir["primary_problem"] = "hidden_feature"
            ir["requires_clarification"] = True
        elif "settings kidhar" in text or "order history nahi mil" in text or "language change kaise" in text or "dark mode" in text or "font size" in text:
            ir["module"] = "navigation"
            ir["primary_problem"] = "feature_discoverability"
            if "settings" in text or "language" in text:
                ir["requires_clarification"] = True
        elif "profile edit" in text:
            ir["module"] = "navigation"
            ir["primary_problem"] = "hidden_feature"
        elif "wallet balance" in text:
            ir["module"] = "navigation"
            ir["primary_problem"] = "hidden_feature"
            ir["requires_clarification"] = True
        elif "address change" in text:
            ir["module"] = "navigation"
            ir["primary_problem"] = "feature_failure"
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
            
        elif "slow" in text:
            ir["module"] = "performance"
            ir["primary_problem"] = "performance_degradation"
            ir["requires_diagnosis"] = True
            if "crash" in text:
                ir["secondary_problem"] = "application_crash"
        elif "loading" in text or "screen freeze" in text or "khulte hi freeze" in text or "atakti hai" in text:
            ir["module"] = "performance"
            ir["primary_problem"] = "ui_freeze"
            ir["requires_diagnosis"] = True
            if "band ho jata" in text:
                ir["secondary_problem"] = "application_crash"
        elif "crash" in text or "band ho jata" in text:
            ir["module"] = "performance"
            ir["primary_problem"] = "application_crash"
            ir["requires_diagnosis"] = True
        elif "video play" in text:
            ir["module"] = "performance"
            ir["primary_problem"] = "high_latency"
            ir["requires_diagnosis"] = True
        elif "garam" in text or "battery" in text or "heat" in text:
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
            
        elif "customer care" in text or "customer support" in text:
            ir["module"] = "trust_support"
            ir["primary_problem"] = "support_unreachable" if "kidhar hai" in text else "support_unresponsive"
        elif "secure" in text:
            ir["module"] = "trust_support"
            ir["primary_problem"] = "security_anxiety"
        elif "data safe" in text or "safe nahi" in text:
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
        elif "terms and conditions" in text or "privacy policy" in text:
            ir["module"] = "trust_support"
            ir["primary_problem"] = "policy_confusion"
        elif "hack" in text:
            ir["module"] = "trust_support"
            ir["primary_problem"] = "security_anxiety"
        elif "spam calls" in text:
            ir["module"] = "trust_support"
            ir["primary_problem"] = "data_leak_suspicion"

        return ir
