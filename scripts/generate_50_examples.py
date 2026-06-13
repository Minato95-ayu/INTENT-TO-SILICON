import json
import os

examples = []

# 1. Payment (10)
payment_inputs = [
    ("paise kat gaye par order nahi bana", "orphaned_transaction", None, ["paise", "kat gaye", "order nahi bana"], False, False, 0.95),
    ("amount debited but flight not booked", "orphaned_transaction", None, ["amount debited", "flight not booked"], False, False, 0.94),
    ("refund abhi tak account me nahi aaya", "delayed_refund", None, ["refund", "abhi tak", "nahi aaya"], False, False, 0.92),
    ("double payment ho gaya galti se", "duplicate_transaction", None, ["double payment", "galti se"], False, False, 0.96),
    ("payment failed bata raha hai par paise cut gaye", "orphaned_transaction", "false_failure_message", ["payment failed", "paise cut gaye"], False, False, 0.90),
    ("emi ka option kyu nahi dikh raha", "missing_payment_method", None, ["emi", "option", "nahi dikh raha"], False, False, 0.88),
    ("bank server down hai kya payment stuck hai", "gateway_timeout", None, ["bank server down", "payment stuck"], True, False, 0.85),
    ("bina UPI ke payment kaise karu", "friction_in_payment", None, ["bina UPI", "kaise karu"], False, True, 0.82),
    ("promo code invalid bata raha hai", "promo_code_failure", None, ["promo code", "invalid"], False, False, 0.93),
    ("transaction pending me atka hua hai 2 ghante se", "delayed_transaction", None, ["transaction pending", "atka hua"], False, False, 0.91)
]

# 2. OTP/Auth (10)
auth_inputs = [
    ("OTP nahi aaya", "otp_delivery_failure", None, ["OTP", "nahi aaya"], False, False, 0.95),
    ("OTP receive nahi hua", "otp_delivery_failure", None, ["OTP", "receive nahi hua"], False, False, 0.95),
    ("login kaam nahi kar raha", None, None, ["login", "kaam nahi kar raha"], True, True, 0.50),
    ("bar bar password kyu mangta hai", "friction_in_auth", None, ["bar bar password", "mangta hai"], False, False, 0.89),
    ("account locked bata raha hai", "account_locked", None, ["account locked"], False, False, 0.94),
    ("password reset link mail pe nahi aayi", "email_delivery_failure", None, ["password reset link", "nahi aayi"], False, False, 0.93),
    ("fingerprint se login nahi ho raha", "biometric_failure", None, ["fingerprint", "login nahi ho raha"], False, False, 0.91),
    ("session expired bar bar kyu likh raha hai", "frequent_session_expiry", None, ["session expired", "bar bar"], False, False, 0.88),
    ("login bina OTP ke karna hai", "friction_in_auth", None, ["login", "bina OTP"], False, True, 0.87),
    ("captcha galat bata raha hai jabki sahi dala hai", "captcha_validation_error", None, ["captcha", "galat bata raha"], False, False, 0.92)
]

# 3. Navigation (10)
nav_inputs = [
    ("refund ka status kaha dekhu", "hidden_feature", None, ["refund status", "kaha dekhu"], False, True, 0.70),
    ("settings kidhar hai", "feature_discoverability", None, ["settings", "kidhar hai"], False, True, 0.75),
    ("order history nahi mil rahi", "feature_discoverability", None, ["order history", "nahi mil rahi"], False, False, 0.88),
    ("profile edit karne ka option kaha hai", "hidden_feature", None, ["profile edit", "option kaha hai"], False, False, 0.89),
    ("back button dabane pe app band ho gaya", "navigation_flow_break", "application_crash", ["back button", "app band"], False, False, 0.90),
    ("home page pe wapas kaise jau", "navigation_trap", None, ["home page", "wapas kaise jau"], False, False, 0.85),
    ("search bar kaam nahi kar raha", "feature_failure", None, ["search bar", "kaam nahi kar raha"], False, False, 0.91),
    ("menu options aadhe cut rahe hain screen pe", "ui_rendering_issue", None, ["menu options", "cut rahe hain"], False, False, 0.93),
    ("language change kaise karu", "feature_discoverability", None, ["language change", "kaise karu"], False, True, 0.80),
    ("dark mode on karne ka button nahi mil raha", "feature_discoverability", None, ["dark mode", "button nahi mil raha"], False, False, 0.87)
]

# 4. Performance (10)
perf_inputs = [
    ("app slow hai", "performance_degradation", None, ["app", "slow hai"], True, False, 0.60),
    ("loading pe atak gaya", "ui_freeze", None, ["loading", "atak gaya"], True, False, 0.85),
    ("screen freeze ho gayi", "ui_freeze", None, ["screen freeze"], True, False, 0.88),
    ("app crash ho gaya", "application_crash", None, ["app crash"], True, False, 0.90),
    ("app bahut slow hai aur crash bhi hota hai", "performance_degradation", "application_crash", ["slow", "crash"], True, False, 0.62),
    ("video play hone me bahut time le raha hai", "high_latency", None, ["video play", "bahut time"], True, False, 0.85),
    ("phone garam ho jata hai app chalane pe", "high_resource_usage", None, ["phone garam", "app chalane pe"], True, False, 0.88),
    ("battery bahut jaldi drain ho rahi hai", "high_resource_usage", None, ["battery", "drain ho rahi hai"], True, False, 0.89),
    ("image load hi nahi ho rahi", "resource_loading_failure", None, ["image load", "nahi ho rahi"], True, False, 0.84),
    ("scroll karte waqt lag ho raha hai", "ui_lag", None, ["scroll karte", "lag ho raha"], True, False, 0.91)
]

# 5. Trust/Support (10)
trust_inputs = [
    ("customer care ka number kidhar hai bhai", "support_unreachable", None, ["customer care", "number kidhar hai"], False, False, 0.90),
    ("payment secure hai ya nahi dar lag raha hai", "security_anxiety", None, ["payment secure", "dar lag raha hai"], False, False, 0.85),
    ("mera data safe hai ya nahi kaise pata chalega", "privacy_anxiety", None, ["data safe", "kaise pata"], False, False, 0.88),
    ("app fake lag raha hai fraud toh nahi", "trust_deficit", None, ["app fake", "fraud"], False, True, 0.82),
    ("support ticket raise kiya tha koi reply nahi aaya", "support_unresponsive", None, ["support ticket", "koi reply nahi"], False, False, 0.92),
    ("meri card details delete kaise karu", "privacy_control_anxiety", None, ["card details", "delete kaise karu"], False, False, 0.89),
    ("live chat option kyu nahi hai yaha", "support_channel_missing", None, ["live chat", "kyu nahi hai"], False, False, 0.91),
    ("terms and conditions bahut confusing hain", "policy_confusion", None, ["terms and conditions", "confusing"], False, False, 0.86),
    ("bot se baat nahi karni real human chahiye", "bot_frustration", None, ["bot se baat nahi", "real human chahiye"], False, False, 0.94),
    ("spam calls aa rahe hain jabse app install kiya", "data_leak_suspicion", None, ["spam calls", "app install kiya"], False, False, 0.95)
]

def map_to_json(module, inputs):
    for i, (inp, primary, secondary, evidence, req_diag, req_clar, conf) in enumerate(inputs):
        examples.append({
            "test_id": f"{module}_{i+1}",
            "input": inp,
            "intent_ir": {
                "module": module,
                "primary_problem": primary,
                "secondary_problem": secondary,
                "evidence": evidence,
                "requires_diagnosis": req_diag,
                "requires_clarification": req_clar,
                "confidence_score": conf
            }
        })

map_to_json("payment", payment_inputs)
map_to_json("auth", auth_inputs)
map_to_json("navigation", nav_inputs)
map_to_json("performance", perf_inputs)
map_to_json("trust_support", trust_inputs)

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
    
    out_path = '../data/intent_ir_examples_50.json'
    with open(out_path, 'w') as f:
        json.dump(examples, f, indent=2)
    print(f"Generated {out_path} with {len(examples)} cases.")
