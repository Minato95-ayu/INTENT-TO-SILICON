from typing import Dict, Any

class ChatSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.domain = None
        self.answers: Dict[str, Any] = {}
        
    def set_domain(self, domain: str):
        self.domain = domain
        
    def add_answer(self, q_id: str, answer: Any):
        self.answers[q_id] = answer
