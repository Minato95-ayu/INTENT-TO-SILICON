from .graph import IntentGraph
from .suggestion_engine import SuggestionEngine

class CrossQuestionEngine:
    def __init__(self, suggestion_engine: SuggestionEngine):
        self.suggestion_engine = suggestion_engine
        
    def generate_questions(self, graph: IntentGraph) -> list:
        questions = []
        
        # Rule 1: Entity has no fields
        for entity_name, data in graph.entities.items():
            if not data["fields"]:
                suggestions = self.suggestion_engine.get_common_fields(entity_name)
                q = f"The entity '{entity_name}' currently has no fields defined. Would you like to add some of these common fields?\n  Suggestions: {', '.join(suggestions)}"
                questions.append(q)
                
        # Rule 2: Entity is missing common fields
        for entity_name, data in graph.entities.items():
            if data["fields"]:
                common_fields = self.suggestion_engine.get_common_fields(entity_name)
                missing = [f for f in common_fields if f not in data["fields"]]
                if missing:
                    q = f"For '{entity_name}', would you also like to track these fields?\n  Suggestions: {', '.join(missing)}"
                    questions.append(q)
                    
        # Rule 3: Relationship unclear (Future Gold Mine)
        entities_present = list(graph.entities.keys())
        if "Student" in entities_present and "Library" in entities_present:
            q = "I notice both 'Student' and 'Library' exist. Can a Student belong to a Library? How do they relate?"
            if q not in questions:
                questions.append(q)
                
        return questions
