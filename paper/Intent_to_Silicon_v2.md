# Intent-to-Silicon: Ambiguity Reduction in Natural Language to Software Specification Translation

**Author:** Ayush Kumar Mishra (Ayush Kaushik)  
**Date:** June 2026  

## Abstract
The transition from human thought to machine-executable code is hindered not primarily by the reasoning limitations of artificial intelligence, but by the inherent ambiguity of natural language. While modern Large Language Models (LLMs) possess significant code-generation capabilities, their reliance on underspecified, vague human input frequently leads to hallucinated specifications and erroneous software architectures. This paper introduces **Intent-to-Silicon**, an active ambiguity-reduction framework designed to intercept and process raw human intent—specifically in multilingual contexts (Hindi/Hinglish/English)—before code generation occurs. Through a 7-layer processing pipeline featuring an Active Disambiguation Engine, a Hinglish-to-Technical Semantic Dictionary, and Clause Boundary Negation heuristics, the framework translates ambiguous user statements into strictly typed, machine-readable YAML blueprints. Empirical benchmarking on a synthetic dataset of 121 diverse inputs demonstrates that the system achieves a 66.1% direct specification success rate and an 85.0% negation parsing accuracy. Crucially, by preferring safe halting over unsupported inference, the framework completely eliminates architectural hallucination (0% rate) on out-of-vocabulary inputs.

---

## 1. Introduction

### 1.1 The Problem of Ambiguity in Code Generation
The fundamental interface between humans and computers has historically relied on intermediate programming languages (e.g., C++, Java, Python). These languages were engineered specifically to enforce mathematical precision and eliminate the ambiguity inherent in human communication. Recent advancements in artificial intelligence have attempted to bypass this intermediate layer, enabling Natural Language to Code (NL2Code) generation. However, natural language is inherently subjective, context-dependent, and frequently underspecified. When a user requests a "good, fast system," the requirement lacks the technical boundaries necessary for deterministic software construction.

### 1.2 The Research Gap
Existing code-generation agents (such as GitHub Copilot or Devin) often treat ambiguous prompts as complete instructions. When faced with missing technical specifications, these systems tend to employ predictive modeling to "guess" the user's intent. This behavior frequently results in architectural hallucination—the generation of complex software structures (e.g., specific database paradigms or authentication protocols) that the user neither requested nor required. The gap in current research lies not in generating better code, but in generating better *specifications* prior to the coding phase.

### 1.3 Hypothesis
This research hypothesizes that introducing an active ambiguity-reduction framework—one that maps raw, multilingual human intent to rigid functional parameters and explicitly asks for clarification on ambiguous nodes—will significantly improve the deterministic quality of software specifications and eliminate architectural hallucination. 

### 1.4 Contributions
The primary contributions of the Intent-to-Silicon framework are:
1. **The Semantic Dictionary:** A domain-specific mapping of Hindi/Hinglish root lemmas to exact technical requirements and hard dependencies.
2. **Active Disambiguation Engine:** A conversational mechanism that halts execution and queries the user when intent is detected but underspecified.
3. **YAML Blueprint Generation:** The serialization of verified intent into a machine-readable format to act as a flawless scaffold for downstream LLM code generators.
4. **Reproducible Benchmarking Framework:** An empirical evaluation suite measuring specification success, negation accuracy, and safe-halting behavior.

---

## 2. Methodology

The Intent-to-Silicon architecture is built upon a 7-layer processing pipeline, decoupling intent extraction from code execution. The current implementation (v0.4) focuses on the core Natural Language Processing (NLP) engine responsible for intent mapping and negation handling.

### 2.1 The Semantic Library Mapping
Instead of relying on deep learning vector embeddings which can introduce unpredictable fuzziness, the framework utilizes a deterministic root-lemma dictionary. Inputs are tokenized and matched against categorical root lemmas. For example, the presence of the root `jaldi` or `fast` maps to the `performance` category. Once matched, the system assigns an exact, non-negotiable technical value (e.g., `REQUIREMENT: P99 Latency < 200ms`) and enforces hard dependencies (e.g., `CDN_CACHE_REQUIRED`). 

### 2.2 Directional Proximity Heuristics for Negation (v0.4)
A significant challenge in intent parsing is handling explicit feature exclusion without accidentally discarding valid surrounding requirements (e.g., "I want a fast app but no chat"). The NLP engine implements clause-boundary splitting and directional proximity heuristics to manage this:
- **Clause Splitting:** Inputs are segmented into isolated clauses using conjunctions and delimiters (e.g., `lekin`, `but`, `,`).
- **Backward Negators (Hindi):** Terms like `nahi` or `mat` typically follow the target feature. The system checks if a detected feature appears within a 3-word window *before* the negator.
- **Forward Negators (English):** Terms like `without` or `no` typically precede the target feature. The system checks if the feature appears within a 3-word window *after* the negator.

Features matching these heuristics are stripped from the active requirements pool and explicitly serialized into an `excluded_requirements` section of the YAML blueprint, proving successful exclusion to the downstream generator.

### 2.3 Safe Halting (Hallucination Avoidance)
If an input is entirely out-of-vocabulary (OOV) and matches no functional or emotional root lemmas, the system is hardcoded to halt execution and return a `fail_hard` status. This deliberate limitation ensures that the framework prefers to ask for clarification rather than utilizing unsupported inference to generate hallucinated specifications.
