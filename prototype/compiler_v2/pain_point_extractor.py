import json
import os

class PainPointExtractor:
    def __init__(self):
        # Load intent rules (Semantic Proximity Library)
        self.intent_rules = {}
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        try:
            with open(os.path.join(base_dir, 'dictionary', 'intent_rules.json'), 'r') as f:
                self.intent_rules = json.load(f)
        except Exception:
            pass

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

        if not self.intent_rules:
            return ir

        matched_problems = []
        evidence_found = []
        found_module = None
        
        # Token proximity and semantic matching
        # Convert tokens to a single list of strings for easy searching of tags and words
        token_strings = [t["word"] if t["tag"] == "[WORD]" else t["tag"] for t in tokens]
        
        for module, problems in self.intent_rules.items():
            for problem, rule in problems.items():
                roots = rule.get("roots", [])
                req_tags = rule.get("required_tags", [])
                
                # Check roots
                has_root = False
                matched_root = None
                for r in roots:
                    if r in raw:
                        has_root = True
                        matched_root = r
                        break
                        
                if has_root:
                    # Check tags
                    has_tags = True
                    if req_tags:
                        has_tags = any(tag in raw or tag in token_strings for tag in req_tags)
                        
                    if has_tags:
                        if problem not in matched_problems:
                            matched_problems.append(problem)
                        if found_module is None:
                            found_module = module
                        evidence_found.append(matched_root)

    def extract_all(self, normalized_data):
        """
        Extracts multiple intents from the normalized data.
        Returns a list of Intent IR objects.
        """
        intents = []
        raw = normalized_data.get("raw", "").lower()
        tokens = normalized_data.get("tokens", [])
        
        def get_idx(word):
            for t in tokens:
                if t["word"] == word:
                    return t["index"]
            return -1

        def has_neg_after(idx, window=2):
            for t in tokens:
                if t["index"] > idx and t["index"] <= idx + window and t["tag"] == "[NEG]":
                    return True
            return False

        # Token strings for easy searching
        token_strings = [t["word"] if t["tag"] == "[WORD]" else t["tag"] for t in tokens]
        
        # Base bot logic
        bot_idx = get_idx("bot")
        if bot_idx != -1:
            ir = {
                "module": "trust_support",
                "primary_problem": None,
                "secondary_problem": None,
                "evidence": [],
                "requires_diagnosis": False,
                "requires_clarification": False,
                "confidence_score": 0.0
            }
            problem_idx = max(get_idx("problem"), get_idx("issue"))
            if problem_idx != -1 and has_neg_after(problem_idx, window=2):
                ir["primary_problem"] = None
                ir["evidence"] = ["bot", "nahi"]
                ir["confidence_score"] = 0.90
            else:
                ir["primary_problem"] = "bot_frustration"
                ir["evidence"] = ["bot"]
                ir["confidence_score"] = 0.94
            
            if ir["primary_problem"]:
                intents.append(ir)

        if not self.intent_rules:
            # Fallback if no rules loaded
            if not intents:
                return [{
                    "module": "unknown",
                    "primary_problem": None,
                    "secondary_problem": None,
                    "evidence": [],
                    "requires_diagnosis": False,
                    "requires_clarification": False,
                    "confidence_score": 0.0
                }]
            return intents
            
        for module, problems in self.intent_rules.items():
            for problem, rule in problems.items():
                roots = rule.get("roots", [])
                req_tags = rule.get("required_tags", [])
                
                has_root = False
                matched_root = None
                for r in roots:
                    if r.lower() in raw:
                        has_root = True
                        matched_root = r
                        break
                        
                if has_root:
                    has_tags = True
                    if req_tags:
                        has_tags = any(tag in raw or tag in token_strings for tag in req_tags)
                        
                    if has_tags:
                        # Create a distinct Intent IR for this match
                        ir = {
                            "module": module,
                            "primary_problem": problem,
                            "secondary_problem": None,
                            "evidence": [matched_root],
                            "requires_diagnosis": problem in ["unauthorized_transaction_suspicion", "gateway_timeout", "friction_in_payment", "captcha_validation_error", "biometric_failure", "email_delivery_failure", "account_locked", "friction_in_auth", "feature_failure", "ui_rendering_issue", "performance_degradation", "application_crash", "high_latency", "high_resource_usage", "resource_loading_failure", "ui_freeze", "ui_lag", "trust_deficit", "data_leak_suspicion"],
                            "requires_clarification": problem in ["friction_in_payment", "friction_in_auth", "hidden_feature", "feature_discoverability", "trust_deficit", "missing_payment_method"],
                            "confidence_score": 0.92
                        }
                        # Avoid duplicates
                        if not any(i.get("primary_problem") == problem for i in intents):
                            intents.append(ir)

        if not intents:
            intents.append({
                "module": "unknown",
                "primary_problem": None,
                "secondary_problem": None,
                "evidence": [],
                "requires_diagnosis": False,
                "requires_clarification": False,
                "confidence_score": 0.0
            })

        return intents

    def extract(self, normalized_data):
        # Legacy extract still returns the first match for backward compatibility
        intents = self.extract_all(normalized_data)
        if intents and intents[0]["primary_problem"] is not None:
            return intents[0]
        
        # If unknown, just return the blank struct
        return intents[0]
