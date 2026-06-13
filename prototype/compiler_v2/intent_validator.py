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


class IntentValidationError(Exception):
    """Raised when the intent fails validation and cannot proceed to compilation."""
    pass


@dataclass
class ValidationResult:
    """The result of intent validation."""
    is_valid: bool = False
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class IntentValidator:
    """
    Validates a locked intent before it enters the BlueprintGenerator.
    
    Checks:
    1. No unresolved questions remain
    2. No missing required concepts (all must be resolved or explicitly declined)
    3. Domain is identified
    4. At least one entity is present
    """

    def validate(self, clarification_result, resolved_intent) -> ValidationResult:
        """
        Validates the locked intent.
        
        Args:
            clarification_result: The ClarificationResult from analyze()
            resolved_intent: The ResolvedIntent from resolve()
            
        Returns:
            ValidationResult with is_valid flag and any errors/warnings.
        """
        result = ValidationResult()
        errors = []
        warnings = []
        
        # Check 1: No unresolved questions
        if not clarification_result.is_complete:
            unanswered = [q["concept"] for q in clarification_result.questions]
            # Check if these were answered in the resolved intent
            for concept in unanswered:
                if concept not in resolved_intent.answers:
                    errors.append(
                        f"Unresolved question for concept: '{concept}'. "
                        f"User must answer before compilation can proceed."
                    )
        
        # Check 2: Domain is identified
        if not resolved_intent.domain or resolved_intent.domain == "unknown":
            errors.append(
                "Could not identify the application domain. "
                "Please specify the type of application (e.g., hospital, education, logistics)."
            )
        
        # Check 3: At least one entity exists
        if not resolved_intent.entities:
            errors.append(
                "No data entities found for this domain. "
                "The ontology may be missing entries for this domain."
            )
        
        # Check 4: Missing concepts with no answer
        for concept in clarification_result.missing_concepts:
            if concept not in resolved_intent.answers:
                warnings.append(
                    f"Concept '{concept}' was not mentioned and not answered. "
                    f"Defaulting to: excluded."
                )
        
        result.errors = errors
        result.warnings = warnings
        result.is_valid = len(errors) == 0
        
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
            if result.warnings:
                error_msg += "\n\nWarnings:\n" + "\n".join(
                    [f"  • {w}" for w in result.warnings]
                )
            raise IntentValidationError(error_msg)
        
        # Print warnings even on success
        if result.warnings:
            print("\n[Intent Validator] Warnings:")
            for w in result.warnings:
                print(f"  ⚠ {w}")
        
        return result


if __name__ == "__main__":
    # Quick self-test
    from clarification_engine import ClarificationResult, ResolvedIntent
    
    validator = IntentValidator()
    
    # Test: valid intent
    cr = ClarificationResult(is_complete=True)
    ri = ResolvedIntent(domain="healthcare", entities=["patient", "doctor"])
    result = validator.validate(cr, ri)
    print(f"Valid intent: is_valid={result.is_valid}, errors={result.errors}")
    
    # Test: invalid intent (no domain)
    cr2 = ClarificationResult(is_complete=True)
    ri2 = ResolvedIntent(domain="unknown", entities=[])
    result2 = validator.validate(cr2, ri2)
    print(f"Invalid intent: is_valid={result2.is_valid}, errors={result2.errors}")
