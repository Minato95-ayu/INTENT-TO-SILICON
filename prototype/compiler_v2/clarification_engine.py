import os
import json
import re

class ClarificationEngine:
    def __init__(self):
        self.clarification_library = {}
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        try:
            with open(os.path.join(base_dir, 'dictionary', 'clarification_library.json'), 'r') as f:
                self.clarification_library = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load clarification_library.json: {e}")

    def analyze(self, extracted_concepts, raw_intent_text):
        """
        Analyzes the extracted concepts and the raw intent to detect missing information.
        Returns a list of clarification questions.
        """
        if not self.clarification_library:
            return []
            
        raw_intent_lower = raw_intent_text.lower()
        concept_keywords = self.clarification_library.get("_concept_keywords", {})
        
        clarifications_needed = []
        
        for concept in extracted_concepts:
            domain_rules = self.clarification_library.get(concept)
            if not domain_rules:
                continue
                
            required_concepts = domain_rules.get("required_concepts", [])
            questions_map = domain_rules.get("questions", {})
            
            for req_concept in required_concepts:
                # Check if the raw text contains keywords for this required concept
                keywords = concept_keywords.get(req_concept, [req_concept])
                
                is_mentioned = any(kw in raw_intent_lower for kw in keywords)
                
                if not is_mentioned:
                    question = questions_map.get(req_concept)
                    if question and question not in clarifications_needed:
                        clarifications_needed.append(question)
                        
        return clarifications_needed

if __name__ == "__main__":
    engine = ClarificationEngine()
    print("Testing Clarification Engine:")
    q = engine.analyze(["education"], "Mujhe student ecosystem app banana hai")
    print(q)
