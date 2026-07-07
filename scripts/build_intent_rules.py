"""
=============================================================================
FILE: build_intent_rules.py
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

intent_rules = {
  "payment": {
    "gateway_timeout": {
      "roots": ["gateway", "bank server", "server", "down"],
      "required_tags": []
    },
    "duplicate_transaction": {
      "roots": ["do baar", "double", "do bar charge"],
      "required_tags": []
    },
    "delayed_transaction": {
      "roots": ["pending", "stuck"],
      "required_tags": []
    },
    "false_failure_message": {
      "roots": ["bounce", "msg", "message", "msg aaya"],
      "required_tags": []
    },
    "unauthorized_transaction_suspicion": {
      "roots": ["without otp", "apne aap", "paise nahi kate"],
      "required_tags": []
    },
    "orphaned_transaction": {
      "roots": ["[MONEY_DEDUCTED]", "[TRANSACTION_FAILED]", "paise nikal", "paise ud", "paise cut", "paise kate", "debited"],
      "required_tags": []
    },
    "friction_in_payment": {
      "roots": ["upi pin", "credit card", "bina upi", "upi error", "upi"],
      "required_tags": []
    },
    "promo_code_failure": {
      "roots": ["cashback", "promo code", "coupon", "promo"],
      "required_tags": []
    },
    "delayed_refund": {
      "roots": ["refund"],
      "required_tags": ["nahi", "[NEGATIVE_MATCH]", "[DELIVERY_FAILURE]"]
    },
    "missing_payment_method": {
      "roots": ["emi"],
      "required_tags": []
    }
  },
  "auth": {
    "email_delivery_failure": {
      "roots": ["password reset", "reset link", "email verification", "recovery mail", "password change"],
      "required_tags": []
    },
    "biometric_failure": {
      "roots": ["face id", "fingerprint"],
      "required_tags": []
    },
    "friction_in_auth": {
      "roots": ["logout", "purana number", "bina otp", "password", "dusre number", "authenticator", "login", "call aa sakta"],
      "required_tags": []
    },
    "otp_delivery_failure": {
      "roots": ["verification", "otp", "code", "sms"],
      "required_tags": []
    },
    "captcha_validation_error": {
      "roots": ["captcha"],
      "required_tags": []
    },
    "account_locked": {
      "roots": ["account block", "locked", "block"],
      "required_tags": []
    },
    "frequent_session_expiry": {
      "roots": ["session expired"],
      "required_tags": []
    }
  },
  "navigation": {
    "hidden_feature": {
      "roots": ["past orders", "profile pic", "wallet balance", "profile edit", "refund ka status", "refund"],
      "required_tags": ["status", "kaha"]
    },
    "feature_discoverability": {
      "roots": ["dark mode", "saved items", "font size", "settings", "language", "setting", "order history", "bhasha"],
      "required_tags": []
    },
    "navigation_trap": {
      "roots": ["homepage", "home page"],
      "required_tags": []
    },
    "feature_failure": {
      "roots": ["search box", "address", "search bar", "profile details", "gayab"],
      "required_tags": []
    },
    "ui_rendering_issue": {
      "roots": ["menu", "aadhe cut"],
      "required_tags": []
    },
    "navigation_flow_break": {
      "roots": ["back button", "back karne"],
      "required_tags": []
    }
  },
  "performance": {
    "high_latency": {
      "roots": ["video", "offline", "buffering"],
      "required_tags": []
    },
    "performance_degradation": {
      "roots": ["[SLOW_PERFORMANCE]", "open", "time", "slow", "ruk ruk"],
      "required_tags": []
    },
    "application_crash": {
      "roots": ["[APPLICATION_EXIT]"],
      "required_tags": []
    },
    "ui_freeze": {
      "roots": ["[UI_FREEZE]", "atak gaya", "atakti", "atak"],
      "required_tags": []
    },
    "high_resource_usage": {
      "roots": ["battery", "heat", "garam", "phone"],
      "required_tags": []
    },
    "resource_loading_failure": {
      "roots": ["images", "image"],
      "required_tags": []
    },
    "ui_lag": {
      "roots": ["scroll", "scroll lag"],
      "required_tags": []
    }
  },
  "trust_support": {
    "trust_deficit": {
      "roots": ["fraud", "bharosa", "fake"],
      "required_tags": []
    },
    "support_unresponsive": {
      "roots": ["ticket", "sunta nahi"],
      "required_tags": []
    },
    "support_unreachable": {
      "roots": ["customer care", "customer support"],
      "required_tags": []
    },
    "policy_confusion": {
      "roots": ["privacy policy", "terms and conditions", "samajh nahi"],
      "required_tags": []
    },
    "privacy_anxiety": {
      "roots": ["data", "safe", "privacy", "safe nahi"],
      "required_tags": ["nahi", "chori"]
    },
    "security_anxiety": {
      "roots": ["card details safe", "secure", "hack"],
      "required_tags": []
    },
    "bot_frustration": {
      "roots": ["insan", "machine", "bot", "agent"],
      "required_tags": []
    },
    "data_leak_suspicion": {
      "roots": ["spam"],
      "required_tags": []
    },
    "support_channel_missing": {
      "roots": ["live chat"],
      "required_tags": []
    },
    "privacy_control_anxiety": {
      "roots": ["card details delete"],
      "required_tags": []
    }
  }
}

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
    
    out_path = '../dictionary/intent_rules.json'
    with open(out_path, 'w') as f:
        json.dump(intent_rules, f, indent=2)
    print(f"Generated {out_path}")
