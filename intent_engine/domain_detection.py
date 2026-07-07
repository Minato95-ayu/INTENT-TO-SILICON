class DomainDetection:
    def detect(self, text: str) -> str:
        text = text.lower()
        if "user" in text or "login" in text:
            return "auth"
        if "pay" in text or "cart" in text:
            return "ecommerce"
        return "general"
