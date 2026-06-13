import os
import json
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set

from .concept_graph_engine import ConceptGraphEngine


@dataclass
class ClarificationResult:
    """Structured output of the clarification analysis phase."""
    questions: List[dict] = field(default_factory=list)
    # e.g. [{"concept": "authentication", "question": "...", "options": ["OTP", "Email", "SSO"]}]

    detected_domains: List[str] = field(default_factory=list)
    detected_concepts: List[str] = field(default_factory=list)
    inferred_concepts: List[str] = field(default_factory=list)
    missing_concepts: List[str] = field(default_factory=list)
    
    confidence: Dict[str, float] = field(default_factory=dict)
    is_complete: bool = False


@dataclass
class ResolvedIntent:
    """The output of resolve(). A structured, unambiguous representation of user intent."""
    domain: str = ""
    
    # 3-State Concept Model
    detected: List[str] = field(default_factory=list)
    inferred: List[str] = field(default_factory=list)
    confirmed: List[str] = field(default_factory=list)
    
    # Kept for backward compatibility with BlueprintGenerator
    entities: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    
    original_intent: str = ""
    answers: Dict[str, str] = field(default_factory=dict)


class ClarificationEngine:
    def __init__(self):
        self.clarification_library = {}
        self.concept_modules = {}
        self.graph_engine = ConceptGraphEngine()
        
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

    def _extract_domains(self, raw_intent_text: str) -> List[str]:
        """Deterministically extract the primary domains from intent text."""
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
            "pharmacy": ["pharmacy", "medicine", "prescription"]
        }
        
        # Split intent into distinct words for precise matching
        words_in_intent = set(re.findall(r'\b\w+\b', raw_lower))
        
        detected_domains = []
        for domain, keywords in domain_keywords.items():
            if any(kw in words_in_intent for kw in keywords):
                detected_domains.append(domain)
                
        return detected_domains

    def analyze(self, extracted_concepts: List[str], raw_intent_text: str) -> ClarificationResult:
        """
        Analyzes the extracted concepts and raw intent using ConceptGraphEngine.
        """
        result = ClarificationResult()
        
        # 1. Detect Explicit Concepts & Domains
        result.detected_concepts.extend(extracted_concepts)
        domains = self._extract_domains(raw_intent_text)
        result.detected_domains = domains
        
        # Rule: No domains detected -> Ask domain
        if not domains:
            available_domains = [d for d in self.clarification_library.keys() if not d.startswith("_")]
            result.missing_concepts.append("domain")
            result.questions.append({
                "concept": "domain",
                "question": f"Kaunsa domain hai? Options: {', '.join(available_domains)}",
                "confidence": 0.0,
            })
            result.is_complete = False
            return result
            
        # Rule: Multi-domain detected -> Ask integration question
        if len(domains) > 1:
            result.missing_concepts.append("integration")
            result.questions.append({
                "concept": "integration",
                "question": f"Multi-domain detected: {', '.join(domains)}. How should these interact? Options: 1. Separate systems, 2. Shared records, 3. Integrated workflow",
                "confidence": 0.0
            })
        
        # 2. Expand Graph to get Inferred and Optional Concepts
        explicit_nodes = domains + result.detected_concepts
        inferred_requires, optionals = self.graph_engine.expand(explicit_nodes)
        
        # 'Requires' -> Infer (do not ask, unless confidence is handled later)
        for concept in inferred_requires:
            if concept not in result.detected_concepts and concept not in domains:
                result.inferred_concepts.append(concept)
                
        # 3. Generate Questions for Optional and Implementation Details
        for domain in domains:
            domain_rules = self.clarification_library.get(domain, {})
            questions_map = domain_rules.get("questions", {})
            
            # Optional Concepts -> Always Ask
            for opt in optionals:
                if opt in questions_map:
                    if not any(q['concept'] == opt for q in result.questions):
                        result.missing_concepts.append(opt)
                        result.questions.append({
                            "concept": opt,
                            "question": questions_map[opt],
                            "confidence": 0.0
                        })
            
            # Implementation Details (Requires concepts that have specific questions) -> Always Ask
            for inf in inferred_requires:
                if inf in questions_map:
                    if not any(q['concept'] == inf for q in result.questions):
                        result.missing_concepts.append(inf)
                        result.questions.append({
                            "concept": inf,
                            "question": questions_map[inf],
                            "confidence": 0.0
                        })

        result.is_complete = len(result.questions) == 0
        return result

    def resolve(self, original_intent: str, answers: Dict[str, str], detected_concepts: List[str] = None) -> ResolvedIntent:
        """
        Takes the original intent and user answers to clarification questions.
        Produces a structured ResolvedIntent using 3-State Model.
        """
        if detected_concepts is None:
            detected_concepts = []
            
        resolved = ResolvedIntent()
        resolved.original_intent = original_intent
        resolved.answers = answers
        
        domains = self._extract_domains(original_intent)
        if not domains and "domain" in answers:
            ans_domain = answers["domain"].lower().strip()
            domains = [ans_domain]
            
        resolved.domain = domains[0] if domains else "unknown"
        
        explicit_nodes = domains.copy() + detected_concepts
        
        # Re-run graph expansion
        inferred_requires, optionals = self.graph_engine.expand(explicit_nodes)
        
        # 3-State Population
        resolved.detected = explicit_nodes
        
        for concept in inferred_requires:
            if concept not in explicit_nodes:
                resolved.inferred.append(concept)
        
        # Process answers
        for concept, answer in answers.items():
            if concept in ("domain", "integration"):
                continue
            answer_lower = answer.lower().strip()
            # If yes or a specific detail like 'otp'
            if answer_lower in ("yes", "y", "haan", "ha", "true", "1") or answer_lower not in ("no", "n", "nahi", "nah", "false", "0"):
                resolved.confirmed.append(concept)
                
        # Populate entities and features for BlueprintGenerator backward compatibility
        all_concepts = set(resolved.detected + resolved.inferred + resolved.confirmed)
        
        # For data entities, we can use the domain ontology concepts if they are present
        # To avoid breaking the existing BlueprintGenerator completely, we'll try to include all concepts
        resolved.features = list(all_concepts)
        resolved.entities = [c for c in all_concepts if c not in domains] # Assume everything not a domain is an entity
        
        # If the domain's concept module is explicitly requested, we can optionally merge it
        # But we'll rely on our inferred graph for exact matches!
        
        return resolved

    def lock_intent(self, resolved: ResolvedIntent) -> str:
        """
        Converts a ResolvedIntent into a locked, enriched intent string
        that the BlueprintGenerator can consume directly.
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
            "pharmacy": "Pharmacy Management System"
        }
        
        title = domain_titles.get(resolved.domain, "Custom Application")
        
        # Get components (inferred + confirmed + detected) excluding domain names
        components = set()
        for c in resolved.detected + resolved.inferred + resolved.confirmed:
            if c not in domain_titles:
                components.add(c.replace('_', ' ').title())
                
        # Clean up duplicates
        component_list = sorted(list(components))
        
        if component_list:
            return f"{title} with: {', '.join(component_list)}"
        else:
            return title
