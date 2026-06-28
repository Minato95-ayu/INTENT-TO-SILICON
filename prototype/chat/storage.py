from typing import Dict
from .session import ChatSession

class SessionStorage:
    def __init__(self):
        self._store: Dict[str, ChatSession] = {}
        
    def save(self, session: ChatSession):
        self._store[session.session_id] = session
        
    def get(self, session_id: str) -> ChatSession:
        return self._store.get(session_id)
