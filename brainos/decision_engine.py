class DecisionEngine:
    """
    Analyzes the raw human intent to determine strict constraints.
    """
    def __init__(self):
        self.rules = {
            "hospital": ["High Security", "ACID Compliance", "Audit Logging"],
            "banking": ["High Security", "ACID Compliance", "Zero Data Loss", "High Throughput"],
            "blog": ["High Read Throughput", "Eventual Consistency", "SEO Optimized"],
            "erp": ["Complex Relational Data", "Role Based Access", "Reporting"],
            "crm": ["Complex Relational Data", "Role Based Access", "Multi-Tenant Isolation"],
            "high read": ["High Read Throughput", "Edge Caching"],
            "realtime": ["WebSockets", "Low Latency"]
        }

    def analyze(self, intent: str) -> list[str]:
        intent_lower = intent.lower()
        constraints = []
        for keyword, rules in self.rules.items():
            if keyword in intent_lower:
                constraints.extend(rules)
        if not constraints:
            constraints.append("Standard Web Constraints")
        return list(set(constraints))
