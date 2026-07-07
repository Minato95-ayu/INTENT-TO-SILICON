"""
=============================================================================
FILE: generate_unseen_examples.py
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

unseen_examples = [
  {
    "test_id": "unseen_1",
    "input": "OTP ki jagah call aa sakta hai kya?",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "friction_in_auth",
      "secondary_problem": None,
      "evidence": ["OTP ki jagah", "call aa sakta hai"],
      "requires_diagnosis": False,
      "requires_clarification": True,
      "confidence_score": 0.85
    }
  },
  {
    "test_id": "unseen_2",
    "input": "paise nahi kate par order dikha raha hai",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "unauthorized_transaction_suspicion",
      "secondary_problem": None,
      "evidence": ["paise nahi kate", "order dikha raha"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.88
    }
  },
  {
    "test_id": "unseen_3",
    "input": "mujhe payment ka koi dar nahi hai",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": None,
      "secondary_problem": None,
      "evidence": ["payment", "dar nahi"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.95
    }
  },
  {
    "test_id": "unseen_4",
    "input": "app khulte hi freeze ho jata hai bina kuch dabaye",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "ui_freeze",
      "secondary_problem": None,
      "evidence": ["freeze ho jata hai", "bina kuch dabaye"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.90
    }
  },
  {
    "test_id": "unseen_5",
    "input": "customer support bilkul bekar hai koi sunta nahi",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "support_unresponsive",
      "secondary_problem": None,
      "evidence": ["customer support", "koi sunta nahi"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.92
    }
  },
  {
    "test_id": "unseen_6",
    "input": "delivery address change karne ka option gayab ho gaya",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "feature_failure",
      "secondary_problem": None,
      "evidence": ["address change", "gayab ho gaya"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.88
    }
  },
  {
    "test_id": "unseen_7",
    "input": "mera account hack ho gaya lagta hai",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "security_anxiety",
      "secondary_problem": None,
      "evidence": ["account hack", "lagta hai"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.94
    }
  },
  {
    "test_id": "unseen_8",
    "input": "bot se mujhe koi problem nahi hai",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": None,
      "secondary_problem": None,
      "evidence": ["bot", "koi problem nahi"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.90
    }
  },
  {
    "test_id": "unseen_9",
    "input": "baar baar loading dikha ke band ho jata hai app",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "ui_freeze",
      "secondary_problem": "application_crash",
      "evidence": ["loading", "band ho jata"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.89
    }
  },
  {
    "test_id": "unseen_10",
    "input": "email verification nahi ho raha, link invalid hai",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "email_delivery_failure",
      "secondary_problem": None,
      "evidence": ["email verification", "link invalid"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.91
    }
  },
  {
    "test_id": "unseen_11",
    "input": "kisi dusre number pe OTP bhej do",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "friction_in_auth",
      "secondary_problem": None,
      "evidence": ["dusre number pe", "OTP bhej do"],
      "requires_diagnosis": False,
      "requires_clarification": True,
      "confidence_score": 0.86
    }
  },
  {
    "test_id": "unseen_12",
    "input": "wallet balance dikhayi nahi de raha",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "hidden_feature",
      "secondary_problem": None,
      "evidence": ["wallet balance", "dikhayi nahi de raha"],
      "requires_diagnosis": False,
      "requires_clarification": True,
      "confidence_score": 0.82
    }
  },
  {
    "test_id": "unseen_13",
    "input": "transaction fail hone ka msg aaya par paise ud gaye",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "orphaned_transaction",
      "secondary_problem": "false_failure_message",
      "evidence": ["transaction fail", "paise ud gaye"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.93
    }
  },
  {
    "test_id": "unseen_14",
    "input": "privacy policy padhne me samajh nahi aa rahi",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "policy_confusion",
      "secondary_problem": None,
      "evidence": ["privacy policy", "samajh nahi aa rahi"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.89
    }
  },
  {
    "test_id": "unseen_15",
    "input": "app ka font size badhane ki setting kidhar hai",
    "intent_ir": {
      "module": "navigation",
      "primary_problem": "feature_discoverability",
      "secondary_problem": None,
      "evidence": ["font size", "setting kidhar hai"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.90
    }
  },
  {
    "test_id": "unseen_16",
    "input": "lagta hai mera data safe nahi hai",
    "intent_ir": {
      "module": "trust_support",
      "primary_problem": "privacy_anxiety",
      "secondary_problem": None,
      "evidence": ["data", "safe nahi"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.92
    }
  },
  {
    "test_id": "unseen_17",
    "input": "EMI ka option tha par abhi missing hai",
    "intent_ir": {
      "module": "payment",
      "primary_problem": "missing_payment_method",
      "secondary_problem": None,
      "evidence": ["EMI", "abhi missing hai"],
      "requires_diagnosis": False,
      "requires_clarification": False,
      "confidence_score": 0.91
    }
  },
  {
    "test_id": "unseen_18",
    "input": "OTP delay ka koi issue nahi hai, problem password mein hai",
    "intent_ir": {
      "module": "auth",
      "primary_problem": "friction_in_auth",
      "secondary_problem": None,
      "evidence": ["OTP delay", "issue nahi", "problem password mein"],
      "requires_diagnosis": False,
      "requires_clarification": True,
      "confidence_score": 0.84
    }
  },
  {
    "test_id": "unseen_19",
    "input": "phone bahut heat ho raha hai app kholne par",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "high_resource_usage",
      "secondary_problem": None,
      "evidence": ["phone bahut heat", "app kholne par"],
      "requires_diagnosis": True,
      "requires_clarification": False,
      "confidence_score": 0.92
    }
  },
  {
    "test_id": "unseen_20",
    "input": "internet sahi chal raha hai fir bhi app atakti hai",
    "intent_ir": {
      "module": "performance",
      "primary_problem": "ui_freeze",
      "secondary_problem": None,
      "evidence": ["internet sahi", "app atakti hai"],
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
    
    out_path = '../data/unseen_examples_20.json'
    with open(out_path, 'w') as f:
        json.dump(unseen_examples, f, indent=2)
    print(f"Generated {out_path} with {len(unseen_examples)} cases.")
