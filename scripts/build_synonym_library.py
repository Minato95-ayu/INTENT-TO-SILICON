import json
import os

synonym_library = {
  "payment": {
    "duplicate_transaction": [
      ["do baar"], ["double"]
    ],
    "delayed_transaction": [
      ["pending"]
    ],
    "orphaned_transaction": [
      ["paise", "nikal"], ["paise", "ud"], ["kat gaye"], ["paise", "cut"], 
      ["debited"], ["payment failed"], ["transaction fail"]
    ],
    "false_failure_message": [
      ["bounce", "msg"], ["msg aaya", "ud gaye"]
    ],
    "unauthorized_transaction_suspicion": [
      ["without otp"], ["paise nahi kate"]
    ],
    "friction_in_payment": [
      ["upi pin", "galat"], ["credit card", "link nahi"], ["bina upi"]
    ],
    "promo_code_failure": [
      ["cashback"], ["promo code"]
    ],
    "gateway_timeout": [
      ["gateway"], ["bank server"]
    ],
    "delayed_refund": [
      ["refund", "atka"], ["refund", "nahi aaya"], ["refund", "process"]
    ],
    "missing_payment_method": [
      ["emi"]
    ]
  },
  "auth": {
    "email_delivery_failure": [
      ["password change nahi"], ["reset link"], ["email verification"], ["password reset"]
    ],
    "biometric_failure": [
      ["face id"], ["fingerprint"]
    ],
    "friction_in_auth": [
      ["logout"], ["purana number"], ["bina otp"], ["password", "mangta"], ["dusre number"], ["authenticator"], ["delay", "issue nahi"], ["login", "kaam nahi"], ["call aa sakta hai kya"]
    ],
    "otp_delivery_failure": [
      ["verification message"], ["otp"], ["code"], ["sms"], ["receive nahi"]
    ],
    "captcha_validation_error": [
      ["captcha"]
    ],
    "account_locked": [
      ["account block"], ["locked"]
    ],
    "frequent_session_expiry": [
      ["session expired"]
    ]
  },
  "navigation": {
    "hidden_feature": [
      ["past orders"], ["bhasha hindi", "setting nahi"], ["profile pic"], ["wallet balance"], ["refund", "status"], ["profile edit"]
    ],
    "feature_discoverability": [
      ["customer care", "milega"], ["dark mode"], ["saved items"], ["font size"], ["settings kidhar"], ["language change kaise"], ["setting kidhar"], ["order history nahi mil"]
    ],
    "navigation_trap": [
      ["homepage", "wapas"], ["home page"]
    ],
    "feature_failure": [
      ["search box"], ["address edit"], ["search bar"], ["address change"]
    ],
    "ui_rendering_issue": [
      ["menu gayab"], ["menu option"]
    ],
    "navigation_flow_break": [
      ["back button"]
    ]
  },
  "performance": {
    "performance_degradation": [
      ["ruk ruk"], ["open", "seconds"], ["slow"]
    ],
    "ui_freeze": [
      ["freeze"], ["atakti"], ["loading"]
    ],
    "application_crash": [
      ["band ho"], ["crash"], ["close ho"]
    ],
    "high_latency": [
      ["buffering"], ["offline"], ["video play"]
    ],
    "high_resource_usage": [
      ["battery"], ["heat"], ["garam"]
    ],
    "resource_loading_failure": [
      ["images load"], ["image load"]
    ],
    "ui_lag": [
      ["scroll"]
    ]
  },
  "trust_support": {
    "privacy_anxiety": [
      ["chori"], ["data", "safe"], ["safe nahi"]
    ],
    "security_anxiety": [
      ["card details", "safe"], ["hack"], ["secure"]
    ],
    "bot_frustration": [
      ["insan"], ["machine"], ["bot"]
    ],
    "support_unresponsive": [
      ["ticket raise", "reply"], ["support ticket"], ["customer support", "bekar"]
    ],
    "policy_confusion": [
      ["privacy policy"], ["terms and conditions"]
    ],
    "trust_deficit": [
      ["fraud"], ["bharosa"], ["fake"]
    ],
    "data_leak_suspicion": [
      ["spam mails"], ["spam calls"]
    ],
    "support_channel_missing": [
      ["live chat"]
    ],
    "support_unreachable": [
      ["customer care", "busy"], ["customer care", "kaha"], ["customer care", "kidhar"]
    ],
    "privacy_control_anxiety": [
      ["card details delete"]
    ]
  }
}

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
    
    out_path = '../dictionary/synonym_library.json'
    with open(out_path, 'w') as f:
        json.dump(synonym_library, f, indent=2)
    print(f"Generated {out_path}")
