"""
Aayu Intent Validator

Sits between ClarificationEngine and BlueprintGenerator.
Ensures that no unresolved questions, no missing required concepts,
and no ambiguity remain before the intent is passed to compilation.

Pipeline position:
    ClarificationEngine → Intent Lock → IntentValidator → BlueprintGenerator
"""

from dataclasses import dataclass, field
from typing import List

from .intent_completeness_engine import IntentCompletenessEngine, IntentState

class IntentValidationError(Exception):
    """Raised when the intent fails validation and cannot proceed to compilation."""
    pass


@dataclass
class ValidationResult:
    """The result of intent validation."""
    is_valid: bool = False
    state: IntentState = IntentState.DRAFT
    blocking_items: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class IntentValidator:
    """
    Validates a locked intent before it enters the BlueprintGenerator.
    
    Checks:
    1. Evaluates completeness using IntentCompletenessEngine.
    2. Intent must be in GENERATION_READY state to be valid.
    """
    
    def __init__(self):
        self.completeness_engine = IntentCompletenessEngine()

    def validate(self, clarification_result, resolved_intent) -> ValidationResult:
        """
        Validates the locked intent using CompletenessEngine.
        
        Args:
            clarification_result: The ClarificationResult from analyze()
            resolved_intent: The ResolvedIntent from resolve()
            
        Returns:
            ValidationResult with is_valid flag and any errors/warnings.
        """
        result = ValidationResult()
        
        completeness = self.completeness_engine.evaluate(resolved_intent, clarification_result)
        result.state = completeness.state
        result.blocking_items = completeness.blocking_items
        
        if completeness.state == IntentState.GENERATION_READY:
            result.is_valid = True
        else:
            result.is_valid = False
            result.errors.append(f"Intent is not ready for generation. State is {completeness.state.name}.")
            if completeness.blocking_items:
                result.errors.append(f"Blocking items: {', '.join(completeness.blocking_items)}")
                
        return result

    def validate_or_raise(self, clarification_result, resolved_intent):
        """
        Validates and raises IntentValidationError if validation fails.
        Convenience method for pipeline use.
        """
        result = self.validate(clarification_result, resolved_intent)
        
        if not result.is_valid:
            error_msg = "\n".join([
                "Aayu Intent Validation Failed",
                "",
                "Errors:",
                *[f"  • {e}" for e in result.errors],
            ])
            raise IntentValidationError(error_msg)
        
        return result
