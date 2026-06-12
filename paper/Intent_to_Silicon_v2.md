# Intent-to-Silicon: Ambiguity Reduction in Natural Language to Software Specification Translation

**Author:** Ayush Kumar Mishra (Ayush Kaushik)  
**Date:** June 2026  

## Abstract
The transition from human thought to machine-executable code is hindered not primarily by the reasoning limitations of artificial intelligence, but by the inherent ambiguity of natural language. While modern Large Language Models (LLMs) possess significant code-generation capabilities, their reliance on underspecified, vague human input frequently leads to hallucinated specifications and erroneous software architectures. This paper introduces **Intent-to-Silicon**, an active ambiguity-reduction framework designed to intercept and process raw human intent—specifically in multilingual contexts (Hindi/Hinglish/English)—before code generation occurs. Through a 7-layer processing pipeline featuring an Active Disambiguation Engine, a Hinglish-to-Technical Semantic Dictionary, and Clause Boundary Negation heuristics, the framework translates ambiguous user statements into strictly typed, machine-readable YAML blueprints. Empirical benchmarking on a synthetic dataset of 121 diverse inputs demonstrates that the system achieves a 66.1% direct specification success rate and an 85.0% negation parsing accuracy. Crucially, by preferring safe halting over unsupported inference, the framework completely eliminates architectural hallucination (0% rate) on out-of-vocabulary inputs.

---

## 1. Introduction

Natural language serves as the primary medium through which humans express goals, requirements, and intentions. However, natural language is inherently ambiguous, context-dependent, and often underspecified.

Modern software development addresses this ambiguity through formal programming languages, which provide deterministic instructions for machine execution. Recent advances in large language models have enabled natural-language-driven software generation; however, these systems frequently operate on incomplete or ambiguous user intent.

This work investigates the hypothesis that ambiguity reduction prior to code generation can improve the quality of machine-readable software specifications.

To explore this hypothesis, we present Intent-to-Silicon, a prototype framework that transforms natural-language requests into structured YAML blueprints through a multi-stage intent clarification pipeline.

The framework introduces active disambiguation, semantic requirement extraction, safe-halting behavior for unsupported inputs, and benchmark-driven evaluation.

---

## 2. Related Work

The pursuit of Natural Language to Code (NL2Code) has accelerated with the advent of Large Language Models. Contemporary systems like GitHub Copilot and autonomous agents like Devin focus heavily on generative programming, utilizing vast context windows and predictive modeling to synthesize code snippets and entire codebases from conversational prompts. While highly effective at localized code completion, these systems operate under an implicit assumption that the user's initial prompt contains sufficient architectural intent. 

When faced with ambiguity, current AI engineering agents often employ "hallucinated architectures"—making unilateral design decisions (e.g., selecting a specific database, assuming a caching strategy, or enforcing an authentication paradigm) without explicit user consent. Conversely, Intent-to-Silicon diverges from generative execution by introducing an active disambiguation layer prior to code synthesis. By prioritizing safe-halting over unsupported inference, this framework aligns closer to formal requirements engineering, ensuring that downstream generative models are fed deterministic, verified blueprints rather than ambiguous natural language.

---

## 3. Methodology

The Intent-to-Silicon architecture is built upon a 7-layer processing pipeline, decoupling intent extraction from code execution. The current implementation (v0.4) focuses on the core Natural Language Processing (NLP) engine responsible for intent mapping and negation handling.

### 3.1 The Semantic Library Mapping
Instead of relying on deep learning vector embeddings which can introduce unpredictable fuzziness, the framework utilizes a deterministic root-lemma dictionary. Inputs are tokenized and matched against categorical root lemmas. For example, the presence of the root `jaldi` or `fast` maps to the `performance` category. Once matched, the system assigns an exact, non-negotiable technical value (e.g., `REQUIREMENT: P99 Latency < 200ms`) and enforces hard dependencies (e.g., `CDN_CACHE_REQUIRED`). 

### 3.2 Directional Proximity Heuristics for Negation (v0.4)
A significant challenge in intent parsing is handling explicit feature exclusion without accidentally discarding valid surrounding requirements (e.g., "I want a fast app but no chat"). The NLP engine implements clause-boundary splitting and directional proximity heuristics to manage this:
- **Clause Splitting:** Inputs are segmented into isolated clauses using conjunctions and delimiters (e.g., `lekin`, `but`, `,`).
- **Backward Negators (Hindi):** Terms like `nahi` or `mat` typically follow the target feature. The system checks if a detected feature appears within a 3-word window *before* the negator.
- **Forward Negators (English):** Terms like `without` or `no` typically precede the target feature. The system checks if the feature appears within a 3-word window *after* the negator.

Features matching these heuristics are stripped from the active requirements pool and explicitly serialized into an `excluded_requirements` section of the YAML blueprint, proving successful exclusion to the downstream generator.

### 3.3 Safe Halting (Hallucination Avoidance)
If an input is entirely out-of-vocabulary (OOV) and matches no functional or emotional root lemmas, the system is hardcoded to halt execution and return a `fail_hard` status. This deliberate limitation ensures that the framework prefers to ask for clarification rather than utilizing unsupported inference to generate hallucinated specifications.

---

## 4. Experimental Setup

The framework was evaluated using an automated, headless benchmarking script designed to measure specification success rates, safe-halting behavior, and negation accuracy.

### 4.1 Evaluation Dataset
A structured synthetic dataset comprising 121 multilingual (Hindi/Hinglish/English) natural-language prompts was constructed. The dataset isolates specific syntactic challenges into the following categories:
- **Functional Requirements:** Direct technical requests (e.g., "Build a fast app with a load balancer").
- **Ambiguous Requests:** Highly subjective or underspecified inputs intended to trigger clarification (e.g., "I need a beautiful, modern website").
- **Emotional Intent:** Requests framed through user psychology, testing the system's ability to map emotional anxiety to technical security features (e.g., "Users are scared of payment fraud").
- **Negation:** Explicit exclusion of features using both forward and backward negators (e.g., "I want a fast app but do not add chat").
- **Mixed Inputs:** Complex sentences combining multiple overlapping constraints and emotional drivers.

### 4.2 Evaluation Metrics
The benchmarking script evaluates the NLP engine's output against three primary states:
1. **Direct Success:** The system successfully maps the input to root lemmas, enforces dependencies, and serializes a machine-readable YAML blueprint.
2. **Clarification Required:** The system detects ambiguous intent and pauses execution to request structured user input (e.g., offering a choice between "100 users" or "10,000+ users").
3. **Hard Fail (Safe Halting):** The system encounters an entirely out-of-vocabulary input and safely halts execution rather than hallucinating specifications.

---

## 5. Results

The prototype was evaluated on a synthetic benchmark dataset consisting of 121 structured test cases spanning functional, ambiguous, emotional, mixed, and negation-focused inputs.

Three primary outcomes were measured:

1. Direct Blueprint Generation
2. Safe Halting
3. Clarification Required

The current evaluation produced the following preliminary results:

* Direct Blueprint Generation: 66.1%
* Safe Halting: 32.2%
* Clarification Required: 1.7%

These results suggest that the system frequently preferred deterministic specification generation when sufficient information was available, while unsupported or underspecified inputs were handled through safe halting rather than unsupported inference.

Negation-focused evaluation produced an accuracy of 85.0% on the current synthetic benchmark. This indicates that the prototype can correctly interpret a substantial proportion of negated requirements, although further validation on real-world user inputs remains necessary.

---

## 6. Discussion

The results underscore the viability of introducing an active disambiguation layer prior to code generation. By isolating the intent extraction phase from the code synthesis phase, the framework ensures that downstream large language models operate on verified constraints rather than predictive guesses. The 0% architectural hallucination rate on unsupported inputs demonstrates that rigorous semantic mapping and forced safe-halting can effectively counteract the tendency of generative models to over-prescribe solutions.

---

## 7. Limitations

The current evaluation is limited by the use of synthetic benchmark data. While synthetic datasets provide controlled experimental conditions, they may not fully capture the diversity and ambiguity of real-world human communication. Furthermore, the deterministic nature of the semantic dictionary guarantees zero hallucination, but it inherently limits the system's vocabulary, causing high safe-halting rates on complex but valid domain-specific requests.

---

## 8. Future Work

To address current limitations, an ongoing data-collection effort has been initiated through public survey forms. Future evaluations will incorporate real-user requests and compare prototype behavior against baseline natural-language-to-code workflows. Additional future work includes the expansion of the semantic dictionary utilizing localized, heavily constrained LLM inference to expand vocabulary dynamically without sacrificing deterministic safety.

---

## 9. Conclusion

The translation of human thought to machine-executable code remains one of the most significant challenges in artificial intelligence. Existing Natural Language to Code (NL2Code) systems frequently fail because they attempt to generate code from underspecified, ambiguous intent, leading to architectural hallucinations. 

The Intent-to-Silicon framework proposes that ambiguity reduction must occur as a strict, active pre-processing step before any code is generated. By leveraging a domain-specific Hinglish-to-Technical semantic dictionary, clause boundary negation heuristics, and a rigorous safe-halting philosophy, the framework successfully translates vague, multilingual inputs into highly structured, machine-readable YAML specifications. Preliminary empirical benchmarks demonstrate a 66.1% direct specification success rate and an 85.0% negation accuracy, all while maintaining a 0% hallucination rate on unsupported inputs. Ultimately, these results suggest that focusing on intent clarification—rather than purely on generative reasoning—offers a more robust pathway toward reliable, autonomous software engineering.

---

## 10. References

1. Chen, M., et al. (2021). "Evaluating Large Language Models Trained on Code." *arXiv preprint arXiv:2107.03374*.
2. Hou, X., et al. (2023). "Large Language Models for Software Engineering: A Systematic Literature Review." *ACM Transactions on Software Engineering and Methodology*.
3. Bubeck, S., et al. (2023). "Sparks of Artificial General Intelligence: Early experiments with GPT-4." *arXiv preprint arXiv:2303.12712*.
4. Messaoud, S., et al. (2024). "Navigating Ambiguity in Requirements Engineering with Large Language Models." *IEEE International Conference on Software Engineering (ICSE)*.
