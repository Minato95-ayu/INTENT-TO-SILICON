class ConstraintResolver:
    def resolve(self, constraints_list):
        resolved = {
            "security": "standard",
            "performance": "standard",
            "availability": "99.9",
            "budget": "medium",
            "latency": "medium"
        }
        
        for constraint in constraints_list:
            c = constraint.lower()
            if "fast" in c or "high throughput" in c or "performance" in c:
                resolved["performance"] = "high"
                resolved["latency"] = "low"
            if "secure" in c or "encrypted" in c:
                resolved["security"] = "high"
            if "cheap" in c or "low cost" in c:
                resolved["budget"] = "low"
                
        return resolved
