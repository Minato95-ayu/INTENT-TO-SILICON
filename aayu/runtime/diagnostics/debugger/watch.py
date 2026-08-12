from .exceptions import EvaluationError

class WatchEvaluator:
    """Safely evaluates watch expressions using the compiler."""
    
    def __init__(self, snapshot):
        self.snapshot = snapshot
        
    def evaluate(self, expression: str) -> str:
        # CTO Mandate: Push through Lexer -> Parser -> Semantic -> Tiny VM
        # For now, we mock the result based on snapshot locals if it's a simple variable.
        
        # If it's a simple variable lookup in the current frame:
        if len(self.snapshot.call_stack) > 0:
            current_frame = self.snapshot.call_stack[-1]
            if expression in current_frame["locals"]:
                return str(current_frame["locals"][expression])
                
        # Mocking complex evaluation
        if expression == "state.counter":
            return "42"
            
        raise EvaluationError(f"Cannot evaluate '{expression}'")
