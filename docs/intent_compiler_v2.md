# Intent-to-Silicon: Version 2 Architecture (Intent Compiler)

## Overview
Version 2 transforms the Intent-to-Silicon project from a simple NLP pipeline into a true **Natural Language Compiler**. Just as LLVM IR serves as a universal intermediary between high-level programming languages (C++, Rust) and machine code, our **Intent Intermediate Representation (Intent IR)** acts as the universal bridge between ambiguous human natural language and deterministic code-generation models.

## The 12-Stage Compilation Pipeline

The pipeline is divided into three distinct phases: Front-End, Middle-End, and Back-End.

### Phase 1: Front-End (Lexical & Syntax Analysis)
The front-end is responsible for taking raw, unstructured, and messy human language (e.g., Hinglish, typos, slangs) and normalizing it into standard tokens, extracting the functional intent and emotional pain point.

1. **Language Normalization:** Converts slang, typos, and mixed languages into a normalized standard.
   - *Input:* "otp nhi aya bhai"
   - *Output:* `otp_not_received`
2. **Semantic Tokenization:** Parses the normalized string to detect core objects/entities (nouns, verbs).
   - *Input:* "paise kat gaye par order nahi bana"
   - *Output:* `{"payment": "detected", "order": "missing"}`
3. **Intent Extraction:** Identifies the core functional requirement (what feature does the user want?).
   - *Output:* `["login", "search", "payment"]`
4. **Pain Point Extraction:** Maps the user's emotional state or problem to the 20+ category Pain-Point Taxonomy.
   - *Output:* `{"pain_point": "payment_anxiety"}`

### Phase 2: Middle-End (Semantic Analysis & Optimization)
The middle-end is responsible for resolving ambiguities, analyzing logic, and ensuring the intent is solid enough to compile.

5. **Negation Engine:** Scans for multi-word negation within a dependency radius to flip intent logic.
   - *Input:* "OTP login nahi chahiye"
   - *Output:* `{"negated": "otp_login"}`
6. **Conflict Resolver:** Detects and resolves contradictions in the user's input.
   - *Input:* "OTP chahiye. OTP nahi chahiye." -> Triggers resolution logic.
7. **Confidence Engine:** Calculates an overall confidence score for the extracted intent.
   - If `confidence < threshold` (e.g., < 85%), execution halts and moves to Clarification.
8. **Clarification Engine (Cross-Question Engine):** Prompts the user with specific, targeted questions to resolve low-confidence intents.
   - *Input:* "Paise kat gaye" (Confidence: 60%)
   - *Action:* Asks "Bank se deduct hua?" -> "Haan" -> Confidence updated to 95%.

### Phase 3: Back-End (Code Generation & IR)
The back-end maps the locked, high-confidence intent into a deterministic engineering specification.

9. **Intent Graph:** Builds a relationship map between detected functional intents.
   - *Example:* `Refund -> depends_on -> Payment`
10. **Intent IR (Intermediate Representation):** The core moat of the system. This is a JSON-based schema that represents the absolute, unambiguous engineering requirement, stripped of all human emotion.
    - *Example:*
      ```json
      {
        "module": "payment",
        "problem": "orphaned_transaction",
        "solution": "refund_tracker",
        "dependencies": ["auth"]
      }
      ```
11. **YAML Blueprint Serialization:** Translates the JSON Intent IR into a strictly formatted YAML blueprint designed specifically for prompting LLM coding agents.
12. **Agent Execution:** The final blueprint is fed into downstream execution systems (Claude, GPT-4, Cursor) to generate the final application code.

## The Moat: Intent IR
The true value of this architecture lies in **Intent IR**. By standardizing human intent into an intermediate representation, we decouple the *understanding* of human problems from the *generation* of code. This means Intent-to-Silicon can act as the universal "front-end compiler" for any future code-generation AI.
