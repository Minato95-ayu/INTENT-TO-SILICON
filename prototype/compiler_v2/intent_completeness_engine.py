from enum import Enum
from dataclasses import dataclass
from typing import List, Dict

from .clarification_engine import ClarificationResult, ResolvedIntent

class IntentState(Enum):
    DRAFT = "DRAFT"
    PARTIAL = "PARTIAL"
    LOCKED = "LOCKED"
    GENERATION_READY = "GENERATION_READY"

@dataclass
class CompletenessResult:
    state: IntentState
    blocking_items: List[str]

class IntentCompletenessEngine:
    def evaluate(self, resolved_intent: ResolvedIntent, clarification_result: ClarificationResult) -> CompletenessResult:
        """
        Evaluates the completeness of an intent and assigns a state.
        """
        if not resolved_intent.domain or resolved_intent.domain == "unknown":
            return CompletenessResult(
                state=IntentState.DRAFT,
                blocking_items=["domain"]
            )
            
        unanswered_questions = []
        for q in clarification_result.questions:
            concept = q["concept"]
            if concept not in resolved_intent.answers:
                unanswered_questions.append(q)
                
        # If no unanswered questions, we are GENERATION_READY
        if not unanswered_questions:
            # Wait, are we missing required concepts? 
            # If a required concept was missing, it would have generated an unanswered question.
            # But what if there are no questions generated because they aren't in clarification_library?
            # Aayu assumes if it's not in clarification_library, it doesn't need clarification.
            return CompletenessResult(
                state=IntentState.GENERATION_READY,
                blocking_items=[]
            )
            
        # Check if there are any missing required concepts (that don't have questions)
        # Actually, missing required concepts are flagged by ClarificationEngine if they have questions.
        # If they don't have questions, they are just inferred.
        
        # Analyze unanswered questions
        blocking_items = [q["concept"] for q in unanswered_questions]
        
        has_feature_or_integration_gap = False
        has_critical_implementation_gap = False
        
        for q in unanswered_questions:
            q_type = q.get("type", "feature")
            q_priority = q.get("priority", "optional")
            
            if q_type in ("feature", "integration"):
                has_feature_or_integration_gap = True
            elif q_type == "implementation" and q_priority == "critical":
                has_critical_implementation_gap = True
                
        if has_feature_or_integration_gap:
            return CompletenessResult(
                state=IntentState.PARTIAL,
                blocking_items=blocking_items
            )
            
        if has_critical_implementation_gap:
            return CompletenessResult(
                state=IntentState.LOCKED,
                blocking_items=blocking_items
            )
            
        # If the only unanswered questions are optional implementation details
        # We can default them and consider it GENERATION_READY
        # The defaulting logic will happen during resolution or generation.
        return CompletenessResult(
            state=IntentState.GENERATION_READY,
            blocking_items=[]
        )
