import json
import os

hidden_examples = [
  {
    "input": "app apne aap auto close ho rahi hai",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "application_crash",
      "secondary_problem": None,
      "evidence": ["auto close"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.90
    }
  },
  {
    "input": "verification sms nahi prapt hua",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "otp_delivery_failure",
      "secondary_problem": None,
      "evidence": ["verification sms", "nahi prapt"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.95
    }
  },
  {
    "input": "customer support kahan chupake rakha hai",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "feature_discoverability",
      "secondary_problem": None,
      "evidence": ["customer support kahan"],
      "requires_diagnosis": False,
      "requires_clarification": True,
      "confidence_score": 0.85
    }
  },
  {
    "input": "coupon lagane ke baad reject ho gaya",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "promo_code_failure",
      "secondary_problem": None,
      "evidence": ["coupon", "reject"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.90
    }
  },
  {
    "input": "UPI error bata raha hai checkout ke time",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "friction_in_payment",
      "secondary_problem": None,
      "evidence": ["UPI error"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.88
    }
  },
  {
    "input": "mere account se balance deduct ho gaya par order nahi aaya",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "orphaned_transaction",
      "secondary_problem": None,
      "evidence": ["balance deduct", "order nahi aaya"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.92
    }
  },
  {
    "input": "dusri bhasha me kaise chalau isko",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "feature_discoverability",
      "secondary_problem": None,
      "evidence": ["dusri bhasha", "kaise chalau"],
      "requires_diagnosis": False,
      "requires_clarification": True,
      "confidence_score": 0.89
    }
  },
  {
    "input": "fingerprint read nahi ho raha",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "biometric_failure",
      "secondary_problem": None,
      "evidence": ["fingerprint read nahi"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.90
    }
  },
  {
    "input": "kisi agent se connect karao",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "bot_frustration",
      "secondary_problem": None,
      "evidence": ["agent", "connect"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.93
    }
  },
  {
    "input": "app kholte hi screen safed pad jati hai",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "ui_freeze",
      "secondary_problem": None,
      "evidence": ["screen safed"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.88
    }
  },
  {
    "input": "mere paise gayab ho gaye",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "unauthorized_transaction_suspicion",
      "secondary_problem": None,
      "evidence": ["paise gayab"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.94
    }
  },
  {
    "input": "email pe recovery mail aahi nahi raha",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "email_delivery_failure",
      "secondary_problem": None,
      "evidence": ["recovery mail", "nahi raha"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.95
    }
  },
  {
    "input": "profile details update nahi ho pa rahi",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "feature_failure",
      "secondary_problem": None,
      "evidence": ["profile details", "update nahi"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.90
    }
  },
  {
    "input": "bar bar captcha match fail ho jata hai",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "captcha_validation_error",
      "secondary_problem": None,
      "evidence": ["captcha match fail"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.91
    }
  },
  {
    "input": "refund ab tak bank me credit nahi hua",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "delayed_refund",
      "secondary_problem": None,
      "evidence": ["refund", "credit nahi hua"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.94
    }
  },
  {
    "input": "transaction fail bol ke do bar charge kar liya",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "duplicate_transaction",
      "secondary_problem": "false_failure_message",
      "evidence": ["transaction fail", "do bar charge"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.96
    }
  },
  {
    "input": "mera account kisine hack kar liya hai",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "security_anxiety",
      "secondary_problem": None,
      "evidence": ["account hack"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.98
    }
  },
  {
    "input": "bahut time laga raha hai open hone me",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "performance_degradation",
      "secondary_problem": None,
      "evidence": ["bahut time laga raha"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.89
    }
  },
  {
    "input": "back karne ka koi nishan hi nahi hai",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "navigation_flow_break",
      "secondary_problem": None,
      "evidence": ["back karne ka nishan nahi"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.92
    }
  },
  {
    "input": "mera address save ka button nahi chal raha",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "feature_failure",
      "secondary_problem": None,
      "evidence": ["address save button nahi chal raha"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.88
    }
  }
]

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
    
    out_path = '../data/hidden_examples_20.json'
    with open(out_path, 'w') as f:
        json.dump(hidden_examples, f, indent=2)
    print(f"Generated {out_path}")
