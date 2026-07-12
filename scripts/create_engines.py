"""
=============================================================================
FILE: create_engines.py
PURPOSE: Generates Decision Engine for rule processing
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles generates decision engine for rule processing.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿"""
=============================================================================
FILE: create_engines.py
PURPOSE: Generate Decision Engine and Rule Processing System
=============================================================================
This script creates a "Decision Engine" - a system that makes intelligent
decisions based on rules and conditions. It's used to:
- Define business rules (IF condition THEN action)
- Evaluate conditions against current context
- Recommend actions based on rules
- Track reasoning (why a decision was made)

Example: If a customer orders > $1000, recommend priority shipping.
The Decision Engine evaluates if this rule applies and recommends the action.
=============================================================================
"""

import os
import json

# =========================================================================
# STEP 1: Set up directory for the Decision Engine code
# =========================================================================
base_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\intent_engine\brainos'
os.makedirs(base_dir, exist_ok=True)

decision_engine_code = '''
from typing import List, Dict, Any

class Rule:
    def __init__(self, id: str, priority: int, when: Dict, recommend: Dict, reason: List[str], cost: str, complexity: str, scale: str, confidence: int, unless: Dict = None, avoid: List[str] = None):
        self.id = id
        self.priority = priority
        self.when = when
        self.unless = unless or {}
        self.recommend = recommend
        self.avoid = avoid or []
        self.reason = reason
        self.cost = cost
        self.complexity = complexity
        self.scale = scale
        self.confidence = confidence

class DecisionEngine:
    def __init__(self):
        self.rules = []

    def load_rules(self, rules_data: List[Dict]):
        for r in rules_data:
            self.rules.append(Rule(**r))
        self.rules.sort(key=lambda x: x.priority, reverse=True)

    def evaluate(self, context: Dict[str, Any]) -> List[Rule]:
        triggered_rules = []
        for rule in self.rules:
            # Check 'when' condition
            match = True
            for k, v in rule.when.items():
                if k not in context or context[k] != v:
                    # simplistic evaluation for prototype
                    if isinstance(v, str) and ('>' in v or '<' in v):
                        pass # handle operators in a real engine
                    else:
                        match = False
                        break
            
            # Check 'unless' condition
            if match and rule.unless:
                for k, v in rule.unless.items():
                    if k in context and context[k] == v:
                        match = False
                        break
            
            if match:
                triggered_rules.append(rule)
        
        return triggered_rules

class RecommendationEngine:
    def generate_recommendation(self, rules: List[Rule]) -> Dict:
        recommendation = {
            "technologies": [],
            "avoid": [],
            "reasons": [],
            "confidence_avg": 0,
            "cost_profile": "Medium",
            "complexity_profile": "Medium",
            "scale_profile": "Standard"
        }
        if not rules:
            return recommendation
            
        conf_sum = 0
        for r in rules:
            for cat, techs in r.recommend.items():
                recommendation["technologies"].extend(techs)
            recommendation["avoid"].extend(r.avoid)
            recommendation["reasons"].extend(r.reason)
            conf_sum += r.confidence
            
        recommendation["confidence_avg"] = conf_sum // len(rules)
        # simplistic cost/scale aggregation
        recommendation["cost_profile"] = rules[0].cost
        recommendation["complexity_profile"] = rules[0].complexity
        recommendation["scale_profile"] = rules[0].scale
        
        # Deduplicate
        recommendation["technologies"] = list(set(recommendation["technologies"]))
        recommendation["avoid"] = list(set(recommendation["avoid"]))
        recommendation["reasons"] = list(set(recommendation["reasons"]))
        
        return recommendation

class ArchitectureReviewEngine:
    def review(self, architecture: Dict) -> List[str]:
        problems = []
        techs = architecture.get("technologies", [])
        
        has_auth = any(t in ["JWT", "OAuth2", "Session"] for t in techs)
        has_cache = any(t in ["Redis", "Memcached"] for t in techs)
        has_logs = any(t in ["ELK", "Audit Logs"] for t in techs)
        
        if not has_auth:
            problems.append("Authentication Missing")
        if not has_cache:
            problems.append("Cache Missing (Performance Risk)")
        if not has_logs:
            problems.append("Audit Logs Missing")
            
        return problems

class ProductionReadinessScorer:
    def score(self, problems: List[str], rules: List[Rule]) -> Dict:
        base_security = 100
        base_perf = 100
        base_scale = 100
        base_maint = 100
        base_cost = 100
        
        for p in problems:
            if "Authentication" in p or "Log" in p:
                base_security -= 20
            if "Cache" in p:
                base_perf -= 15
                base_scale -= 10
                
        # Adjust based on scale rules
        if any(r.scale == "1M+ Users" for r in rules):
            base_scale += 5
            base_cost -= 15 # More scale = higher cost/lower cost efficiency
            base_maint -= 5
            
        overall = int((base_security + base_perf + base_scale + base_maint + base_cost) / 5)
        
        return {
            "Security": f"{max(0, min(100, base_security))}%",
            "Performance": f"{max(0, min(100, base_perf))}%",
            "Scalability": f"{max(0, min(100, base_scale))}%",
            "Maintainability": f"{max(0, min(100, base_maint))}%",
            "Cost Efficiency": f"{max(0, min(100, base_cost))}%",
            "Overall": f"{max(0, min(100, overall))}%"
        }
'''

with open(os.path.join(base_dir, 'engines.py'), 'w', encoding='utf-8') as f:
    f.write(decision_engine_code)


test_sim_code = '''
import yaml
from engines import DecisionEngine, RecommendationEngine, ArchitectureReviewEngine, ProductionReadinessScorer

# Dummy rules for Instagram clone
rules_data = [
    {
        "id": "ARCH_001",
        "priority": 100,
        "when": {"domain": "social_media", "realtime": True},
        "recommend": {"cache": ["Redis"], "messaging": ["Kafka"], "realtime": ["WebSocket"]},
        "avoid": ["Polling"],
        "reason": ["Polling wastes bandwidth. Social media needs realtime push."],
        "cost": "High",
        "complexity": "High",
        "scale": "1M+ Users",
        "confidence": 98
    },
    {
        "id": "DB_001",
        "priority": 90,
        "when": {"domain": "social_media", "image_upload": True},
        "recommend": {"database": ["PostgreSQL"], "storage": ["Object Storage", "CDN"]},
        "reason": ["Images require CDN for fast global delivery and scalable Object Storage."],
        "cost": "Medium",
        "complexity": "Medium",
        "scale": "1M+ Users",
        "confidence": 95
    }
]

# Simulate Context extracted from NLP
context = {
    "intent": "Build Instagram",
    "domain": "social_media",
    "realtime": True,
    "image_upload": True
}

print(f"\\n--- BRAINOS ARCHITECTURE GENERATION ---\\n")
print(f"User Request: {context['intent']}\\n")

decision_engine = DecisionEngine()
decision_engine.load_rules(rules_data)

# 1. Evaluate Tradeoffs and Decide
triggered_rules = decision_engine.evaluate(context)

# 2. Recommendation
rec_engine = RecommendationEngine()
recommendation = rec_engine.generate_recommendation(triggered_rules)

print("RECOMMENDATION:")
for cat, techs in recommendation.items():
    print(f"  {cat}: {techs}")
    
# 3. Architecture Review
reviewer = ArchitectureReviewEngine()
problems = reviewer.review(recommendation)

print("\\nPROBLEMS FOUND:")
for p in problems:
    print(f"  × {p}")

# 4. Production Readiness
scorer = ProductionReadinessScorer()
scores = scorer.score(problems, triggered_rules)

print("\\nPRODUCTION READINESS SCORE:")
for k, v in scores.items():
    print(f"  {k}: {v}")

print("\\n--- GENERATION COMPLETE ---")
'''

with open(os.path.join(base_dir, 'simulate.py'), 'w', encoding='utf-8') as f:
    f.write(test_sim_code)

print("Engines created. Running simulation...")
