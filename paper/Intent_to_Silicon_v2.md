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
