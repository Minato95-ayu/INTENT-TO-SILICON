class ClarificationEngine:
    """
    Flags missing architectural pieces that a human would typically ask about.
    """
    def __init__(self):
        self.required_properties = {
            "ecommerce": ["Payment Gateway", "Inventory System"],
            "crm": ["Email Integration"]
        }
        
    def check_missing_requirements(self, domain: str, intent: str) -> list[str]:
        missing = []
        intent_lower = intent.lower()
        
        if domain in self.required_properties:
            for req in self.required_properties[domain]:
                if req.lower() not in intent_lower:
                    missing.append(req)
                    
        return missing