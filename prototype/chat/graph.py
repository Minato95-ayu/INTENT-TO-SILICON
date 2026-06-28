import json
import os
from typing import List, Optional
from .question import Question

class QuestionGraph:
    def __init__(self, domain: str):
        self.domain = domain
        self.questions = []
        self._load()
        
    def _load(self):
        # Path to data/domains/{domain}.json
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, "data", "domains", f"{self.domain}.json")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Domain '{self.domain}' not found at {file_path}")
            
        with open(file_path, "r") as f:
            data = json.load(f)
            
        for q_data in data.get("questions", []):
            self.questions.append(Question(q_data))
            
    def get_questions(self) -> List[Question]:
        """Return questions in sequential order for now (can be a true graph later)."""
        return self.questions
