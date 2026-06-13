import os
import json
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ClarificationResult:
    """Structured output of the clarification analysis phase."""
    questions: List[dict] = field(default_factory=list)
    # e.g. [{"concept": "authentication", "question": "...", "options": ["OTP", "Email", "SSO"]}]

    detected_concepts: List[str] = field(default_factory=list)
    # Concepts the engine confidently extracted from raw intent

    missing_concepts: List[str] = field(default_factory=list)
    # Concepts that are required but not mentioned

    confidence: Dict[str, float] = field(default_factory=dict)
    # Confidence score per concept (0.0 = absent, 1.0 = explicitly stated)

    is_complete: bool = False
    # True if no clarifications are needed


@dataclass
class ResolvedIntent:
    """The output of resolve(). A structured, unambiguous representation of user intent."""
    domain: str = ""
    entities: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    original_intent: str = ""
    answers: Dict[str, str] = field(default_factory=dict)


class ClarificationEngine:
    def __init__(self):
        self.clarification_library = {}
        self.concept_modules = {}
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        try:
            with open(os.path.join(base_dir, 'dictionary', 'clarification_library.json'), 'r') as f:
                self.clarification_library = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load clarification_library.json: {e}")

        try:
            with open(os.path.join(base_dir, 'dictionary', 'concept_modules.json'), 'r') as f:
                self.concept_modules = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load concept_modules.json: {e}")

    def _extract_domain(self, raw_intent_text: str) -> Optional[str]:
        """Deterministically extract the primary domain from intent text."""
        raw_lower = raw_intent_text.lower()
        
        # Domain keyword mappings (internal identifiers are always English)
        domain_keywords = {
            "healthcare": ["hospital", "clinic", "doctor", "patient", "medical", "health"],
            "education": ["student", "school", "university", "college", "education", "ecosystem", "library", "hostel"],
            "agriculture": ["agriculture", "farm", "crop", "farmer", "agri"],
            "logistics": ["logistics", "fleet", "shipment", "delivery", "warehouse", "tracking"],
            "finance": ["finance", "bank", "payment", "transaction", "portfolio"],
            "ecommerce": ["ecommerce", "shop", "cart", "product catalog", "checkout"],
            "marketplace": ["marketplace", "seller", "buyer", "vendor", "b2b"],
            "government": ["government", "citizen", "civic", "municipal"],
            "social": ["social", "chat", "feed", "profile", "community"],
            "ai": ["ai", "ml", "machine learning", "inference", "llm"],
            "cybersecurity": ["security", "threat", "vulnerability", "siem", "incident"],
        }
        
        best_domain = None
        best_score = 0
        
        # Split intent into distinct words for precise matching
        # This prevents "ai" matching inside "banana" or "hai"
        import re
        words_in_intent = set(re.findall(r'\b\w+\b', raw_lower))
        
        for domain, keywords in domain_keywords.items():
            score = sum(1 for kw in keywords if kw in words_in_intent)
            if score > best_score:
                best_score = score
                best_domain = domain
        
        # If no domain-specific keywords were found at all, return None
        # This triggers domain clarification instead of a false guess
        if best_score == 0:
            return None
                
        return best_domain

    def _compute_confidence(self, raw_intent_lower: str, concept: str) -> float:
        """
        Compute a confidence score (0.0 to 1.0) for whether a concept
        is present in the raw intent text.
        
        - 1.0 = explicitly stated keyword match
        - 0.5 = partial/indirect mention
        - 0.0 = no mention at all
        """
        concept_keywords = self.clarification_library.get("_concept_keywords", {})
        keywords = concept_keywords.get(concept, [concept])
        
        # Count how many keywords match
        matches = sum(1 for kw in keywords if kw in raw_intent_lower)
        
        if matches == 0:
            return 0.0
        elif matches == 1:
            return 0.6
        else:
            return min(1.0, 0.6 + (matches - 1) * 0.2)

    def analyze(self, extracted_concepts: List[str], raw_intent_text: str) -> ClarificationResult:
        """
        Analyzes the extracted concepts and raw intent to detect missing information.
        
        Returns a structured ClarificationResult with questions, confidence scores,
        and a completeness flag.
        """
        result = ClarificationResult()
        
        if not self.clarification_library:
            result.is_complete = True
            return result
            
        raw_intent_lower = raw_intent_text.lower()
        
        # Detect domain
        domain = self._extract_domain(raw_intent_text)
        
        # Find all concepts that were explicitly matched
        for concept in extracted_concepts:
            if concept in self.concept_modules:
                result.detected_concepts.append(concept)
                result.confidence[concept] = 1.0  # Explicitly extracted = full confidence
        
        # If domain is unknown, ask a domain clarification question FIRST
        if domain is None:
            available_domains = [d for d in self.clarification_library.keys() if not d.startswith("_")]
            result.missing_concepts.append("domain")
            result.confidence["domain"] = 0.0
            result.questions.append({
                "concept": "domain",
                "question": f"Kaunsa domain hai? Options: {', '.join(available_domains)}",
                "confidence": 0.0,
            })
            result.is_complete = False
            return result
        
        # Now check domain-specific required concepts
        if domain in self.clarification_library:
            domain_rules = self.clarification_library[domain]
            required_concepts = domain_rules.get("required_concepts", [])
            questions_map = domain_rules.get("questions", {})
            
            for req_concept in required_concepts:
                confidence = self._compute_confidence(raw_intent_lower, req_concept)
                result.confidence[req_concept] = confidence
                
                # Threshold: below 0.5 means we should ask
                if confidence < 0.5:
                    result.missing_concepts.append(req_concept)
                    question_text = questions_map.get(req_concept)
                    if question_text:
                        result.questions.append({
                            "concept": req_concept,
                            "question": question_text,
                            "confidence": confidence,
                        })
        
        result.is_complete = len(result.questions) == 0
        return result

    def resolve(self, original_intent: str, answers: Dict[str, str]) -> ResolvedIntent:
        """
        Takes the original intent and user answers to clarification questions.
        Produces a structured ResolvedIntent that unambiguously describes
        what the user wants.
        
        Args:
            original_intent: The raw, possibly vague, user intent string.
            answers: Dict mapping concept names to user answers.
                     e.g. {"authentication": "otp", "payments": "upi"}
        
        Returns:
            A ResolvedIntent with domain, entities, and features.
        """
        resolved = ResolvedIntent()
        resolved.original_intent = original_intent
        resolved.answers = answers
        
        # Detect primary domain
        # If auto-detection fails, use the domain answer from clarification
        domain = self._extract_domain(original_intent)
        if domain is None and "domain" in answers:
            # User answered the domain clarification question directly
            domain = answers["domain"].lower().strip()
        resolved.domain = domain or "unknown"
        
        # Get base entities from the domain's concept module
        if domain and domain in self.concept_modules:
            concept_data = self.concept_modules[domain]
            resolved.entities = list(concept_data.get("data_entities", []))
        
        # Add features from answers (concepts the user confirmed)
        for concept, answer in answers.items():
            # Skip the meta 'domain' concept — it's not an application feature
            if concept == "domain":
                continue
            answer_lower = answer.lower().strip()
            if answer_lower in ("yes", "y", "haan", "ha", "true", "1"):
                resolved.features.append(concept)
            elif answer_lower not in ("no", "n", "nahi", "nah", "false", "0"):
                # If the answer is a specific choice (e.g., "otp", "upi"), treat as yes + store detail
                resolved.features.append(concept)
        
        return resolved

    def lock_intent(self, resolved: ResolvedIntent) -> str:
        """
        Converts a ResolvedIntent into a locked, enriched intent string
        that the BlueprintGenerator can consume directly.
        
        This is the final output of the Clarification Engine —
        an unambiguous specification of what should be built.
        
        Args:
            resolved: A fully resolved ResolvedIntent.
            
        Returns:
            A deterministic intent string, e.g.:
            "Hospital Management System with: Patients, Doctors, Appointments, Authentication, Payments, Insurance"
        """
        # Domain name in title case
        domain_titles = {
            "healthcare": "Hospital Management System",
            "education": "Student Ecosystem App",
            "agriculture": "Agriculture Management System",
            "logistics": "Logistics Management Platform",
            "finance": "Finance Management System",
            "ecommerce": "E-Commerce Platform",
            "marketplace": "B2B Marketplace",
            "government": "Government Services Portal",
            "social": "Social Platform",
            "ai": "AI Platform",
            "cybersecurity": "Cybersecurity Dashboard",
        }
        
        title = domain_titles.get(resolved.domain, resolved.domain.title() + " Application")
        
        # Build the "with" clause from entities
        entity_names = [e.replace('_', ' ').title() for e in resolved.entities]
        
        # Add confirmed features
        feature_names = [f.replace('_', ' ').title() for f in resolved.features]
        
        all_parts = entity_names + feature_names
        
        if all_parts:
            return f"{title} with: {', '.join(all_parts)}"
        else:
            return title


if __name__ == "__main__":
    engine = ClarificationEngine()
    
    print("=== Clarification Engine Test ===\n")
    
    # Test 1: Vague intent
    print("--- Test 1: Vague Intent ---")
    result = engine.analyze(["healthcare"], "Mujhe hospital app banana hai")
    print(f"Detected: {result.detected_concepts}")
    print(f"Missing: {result.missing_concepts}")
    print(f"Confidence: {result.confidence}")
    print(f"Complete: {result.is_complete}")
    print(f"Questions: {len(result.questions)}")
    for q in result.questions:
        print(f"  [{q['concept']}] {q['question']}")
    
    # Test 2: Explicit intent (should have no questions)
    print("\n--- Test 2: Explicit Intent ---")
    result2 = engine.analyze(
        ["healthcare"],
        "Hospital management system with login OTP, payment gateway, video consultation, insurance"
    )
    print(f"Detected: {result2.detected_concepts}")
    print(f"Missing: {result2.missing_concepts}")
    print(f"Confidence: {result2.confidence}")
    print(f"Complete: {result2.is_complete}")
    print(f"Questions: {len(result2.questions)}")
