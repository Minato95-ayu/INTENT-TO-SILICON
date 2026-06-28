import os

class IntentRouter:
    @staticmethod
    def resolve_domain(user_input: str) -> str:
        """Simple keyword matching for now."""
        user_input = user_input.lower()
        if "hospital" in user_input or "clinic" in user_input:
            return "hospital"
        
        # Check if we have that domain JSON
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if os.path.exists(os.path.join(base_dir, "data", "domains", f"{user_input}.json")):
            return user_input
            
        return "unknown"
