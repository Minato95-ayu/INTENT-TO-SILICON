import json
import os

unseen_examples = [
  # 1. Payment
  {
    "input": "paise account se nikal gaye par ticket book nahi hui",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "orphaned_transaction",
      "secondary_problem": None,
      "evidence": ["paise", "nikal gaye", "ticket book nahi"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.90
    }
  },
  {
    "input": "upi pin galat dikha raha hai baar baar",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "friction_in_payment",
      "secondary_problem": None,
      "evidence": ["upi pin galat"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.85
    }
  },
  {
    "input": "EMI bounce hone ka msg aaya jabki balance tha",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "false_failure_message",
      "secondary_problem": None,
      "evidence": ["EMI bounce", "msg aaya", "balance tha"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.92
    }
  },
  {
    "input": "cashback abhi tak nahi mila",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "promo_code_failure",
      "secondary_problem": None,
      "evidence": ["cashback", "nahi mila"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.88
    }
  },
  {
    "input": "do baar payment cut gayi ek hi order ki",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "duplicate_transaction",
      "secondary_problem": None,
      "evidence": ["do baar payment", "cut gayi"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.95
    }
  },
  {
    "input": "gateway load hi nahi ho raha",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "gateway_timeout",
      "secondary_problem": None,
      "evidence": ["gateway", "load hi nahi"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.90
    }
  },
  {
    "input": "credit card link nahi ho raha",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "friction_in_payment",
      "secondary_problem": None,
      "evidence": ["credit card", "link nahi"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.85
    }
  },
  {
    "input": "refund 7 din se process me atka hai",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "delayed_refund",
      "secondary_problem": None,
      "evidence": ["refund", "atka hai"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.93
    }
  },
  {
    "input": "without otp 5000 ka transaction ho gaya",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "unauthorized_transaction_suspicion",
      "secondary_problem": None,
      "evidence": ["without otp", "transaction ho gaya"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.96
    }
  },
  {
    "input": "promo code lagane par error aa raha hai",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "promo_code_failure",
      "secondary_problem": None,
      "evidence": ["promo code", "error"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.89
    }
  },
  
  # 2. Auth
  {
    "input": "verification message hi nahi mila",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "otp_delivery_failure",
      "secondary_problem": None,
      "evidence": ["verification message", "nahi mila"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.95
    }
  },
  {
    "input": "bar bar captcha galat bata raha hai",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "captcha_validation_error",
      "secondary_problem": None,
      "evidence": ["captcha galat"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.90
    }
  },
  {
    "input": "face id kaam nahi kar rahi",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "biometric_failure",
      "secondary_problem": None,
      "evidence": ["face id", "kaam nahi"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.88
    }
  },
  {
    "input": "logout nahi kar pa raha",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "friction_in_auth",
      "secondary_problem": None,
      "evidence": ["logout nahi"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.85
    }
  },
  {
    "input": "link se password change nahi ho raha",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "email_delivery_failure",
      "secondary_problem": None,
      "evidence": ["password change nahi"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.89
    }
  },
  {
    "input": "account block dikha raha hai bina kisi reason ke",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "account_locked",
      "secondary_problem": None,
      "evidence": ["account block"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.95
    }
  },
  {
    "input": "login pe tap karte hi screen safed ho jati hai",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "friction_in_auth",
      "secondary_problem": "ui_freeze",
      "evidence": ["login", "screen safed"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.92
    }
  },
  {
    "input": "authenticator app ka code invalid aa raha hai",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "friction_in_auth",
      "secondary_problem": None,
      "evidence": ["authenticator code invalid"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.88
    }
  },
  {
    "input": "purana number band hai, naya kaise add karu",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "friction_in_auth",
      "secondary_problem": None,
      "evidence": ["purana number band", "naya kaise"],
      "requires_diagnosis": False,
      "requires_clarification": True,
      "confidence_score": 0.85
    }
  },
  {
    "input": "email pe koi reset link nahi aaya",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "email_delivery_failure",
      "secondary_problem": None,
      "evidence": ["reset link nahi aaya"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.94
    }
  },

  # 3. Navigation
  {
    "input": "past orders dekhne ka button kahan gaya",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "hidden_feature",
      "secondary_problem": None,
      "evidence": ["past orders", "button kahan"],
      "requires_diagnosis": False,
      "requires_clarification": True,
      "confidence_score": 0.88
    }
  },
  {
    "input": "customer care ka number kidhar milega",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "feature_discoverability",
      "secondary_problem": None,
      "evidence": ["customer care", "kidhar milega"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.92
    }
  },
  {
    "input": "dark mode on kaise karu",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "feature_discoverability",
      "secondary_problem": None,
      "evidence": ["dark mode", "kaise karu"],
      "requires_diagnosis": False,
      "requires_clarification": True,
      "confidence_score": 0.90
    }
  },
  {
    "input": "bhasha hindi karni hai par setting nahi mil rahi",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "hidden_feature",
      "secondary_problem": None,
      "evidence": ["bhasha hindi", "setting nahi mil"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.89
    }
  },
  {
    "input": "homepage pe wapas aane ka koi rasta nahi hai",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "navigation_trap",
      "secondary_problem": None,
      "evidence": ["homepage", "wapas aane ka rasta nahi"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.93
    }
  },
  {
    "input": "search box me kuch bhi likho results nahi aate",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "feature_failure",
      "secondary_problem": None,
      "evidence": ["search box", "results nahi aate"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.91
    }
  },
  {
    "input": "profile pic change karne ka option hide ho gaya",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "hidden_feature",
      "secondary_problem": None,
      "evidence": ["profile pic option", "hide"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.87
    }
  },
  {
    "input": "address edit karne pe save nahi hota",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "feature_failure",
      "secondary_problem": None,
      "evidence": ["address edit", "save nahi"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.90
    }
  },
  {
    "input": "ek page se dusre page jane me menu gayab ho jata hai",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "ui_rendering_issue",
      "secondary_problem": None,
      "evidence": ["menu gayab"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.88
    }
  },
  {
    "input": "saved items wala folder kahan hai",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "feature_discoverability",
      "secondary_problem": None,
      "evidence": ["saved items", "kahan hai"],
      "requires_diagnosis": False,
      "requires_clarification": True,
      "confidence_score": 0.92
    }
  },

  # 4. Performance
  {
    "input": "app bahut ruk ruk ke chal rahi hai",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "performance_degradation",
      "secondary_problem": None,
      "evidence": ["ruk ruk ke"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.94
    }
  },
  {
    "input": "kholte hi band ho jati hai screen",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "application_crash",
      "secondary_problem": None,
      "evidence": ["kholte hi", "band"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.96
    }
  },
  {
    "input": "video play karne pe buffering hi hoti rehti hai",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "high_latency",
      "secondary_problem": None,
      "evidence": ["video", "buffering"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.90
    }
  },
  {
    "input": "phone ki battery bahut jaldi khatam ho rahi hai is app se",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "high_resource_usage",
      "secondary_problem": None,
      "evidence": ["battery", "khatam"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.92
    }
  },
  {
    "input": "images load hone me 2 minute lag rahe hain",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "resource_loading_failure",
      "secondary_problem": None,
      "evidence": ["images", "load hone me 2 minute"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.89
    }
  },
  {
    "input": "scroll karne pe lag hota hai",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "ui_lag",
      "secondary_problem": None,
      "evidence": ["scroll", "lag"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.95
    }
  },
  {
    "input": "network full hai par app offline dikha raha hai",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "high_latency",
      "secondary_problem": None,
      "evidence": ["network full", "offline dikha raha"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.88
    }
  },
  {
    "input": "background me app battery drain kar rahi hai",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "high_resource_usage",
      "secondary_problem": None,
      "evidence": ["background", "battery drain"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.93
    }
  },
  {
    "input": "open karne me 30 seconds lagte hain",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "performance_degradation",
      "secondary_problem": None,
      "evidence": ["open", "30 seconds"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.91
    }
  },
  {
    "input": "har do second me freeze ho jata hai",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "ui_freeze",
      "secondary_problem": None,
      "evidence": ["freeze"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.96
    }
  },

  # 5. Trust / Support
  {
    "input": "mera data chori to nahi ho jayega",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "privacy_anxiety",
      "secondary_problem": None,
      "evidence": ["data", "chori to nahi"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.92
    }
  },
  {
    "input": "card details save karna safe hai kya",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "security_anxiety",
      "secondary_problem": None,
      "evidence": ["card details", "safe hai kya"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.89
    }
  },
  {
    "input": "koi insan se baat karni hai, machine se nahi",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "bot_frustration",
      "secondary_problem": None,
      "evidence": ["insan", "machine se nahi"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.94
    }
  },
  {
    "input": "ticket raise kiye hue 2 din ho gaye koi reply nahi",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "support_unresponsive",
      "secondary_problem": None,
      "evidence": ["ticket", "koi reply nahi"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.96
    }
  },
  {
    "input": "privacy policy itni complicated kyu hai",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "policy_confusion",
      "secondary_problem": None,
      "evidence": ["privacy policy", "complicated"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.91
    }
  },
  {
    "input": "lagta hai mere account me fraud hua hai",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "trust_deficit",
      "secondary_problem": None,
      "evidence": ["fraud"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.95
    }
  },
  {
    "input": "mujhe apke platform pe bharosa nahi hai",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "trust_deficit",
      "secondary_problem": None,
      "evidence": ["bharosa nahi"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.93
    }
  },
  {
    "input": "spam mails aana shuru ho gaye aapke app se",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "data_leak_suspicion",
      "secondary_problem": None,
      "evidence": ["spam mails"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.90
    }
  },
  {
    "input": "live chat ka option kyun hata diya",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "support_channel_missing",
      "secondary_problem": None,
      "evidence": ["live chat", "hata diya"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.88
    }
  },
  {
    "input": "customer care ka number humesha busy aata hai",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "support_unreachable",
      "secondary_problem": None,
      "evidence": ["customer care", "busy"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.92
    }
  }
]

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
    
    out_path = '../data/unseen_examples_50.json'
    with open(out_path, 'w') as f:
        json.dump(unseen_examples, f, indent=2)
    print(f"Generated {out_path} with {len(unseen_examples)} cases.")
