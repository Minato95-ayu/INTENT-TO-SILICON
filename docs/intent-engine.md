# Intent Engine

The Intent Engine translates raw human language into structured JSON IR.

## Pipeline
1. **Offline NLP**: Performs tokenization, stop-word removal, POS tagging, and entity extraction without external API dependencies.
2. **Knowledge Graph**: Resolves domain synonyms and injects structural requirements.
3. **Clarification Engine**: Detects missing business logic (e.g., requesting an Ecommerce app without specifying a Payment Gateway) and flags it for the developer.

## Output JSON IR
The output is consumed by BrainOS.\n