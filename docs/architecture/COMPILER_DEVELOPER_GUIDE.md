# AAYU Compiler Developer Guide

Welcome to the AAYU Compiler codebase. This guide serves as the roadmap for future contributors. The AAYU compiler is structured as a strict, unidirectional pipeline. Each stage has a single, immutable responsibility.

## Pipeline Architecture

```
Lexer
  ↓
Parser
  ↓
AST Validator
  ↓
Semantic (Context & Passes)
  ↓
HIR (High-Level Intermediate Representation)
  ↓
MIR (Mid-Level Intermediate Representation)
  ↓
LIR (Low-Level Intermediate Representation)
  ↓
LLVM Lowering
  ↓
Binary
```

### 1. Lexer
- **Responsibility:** Converts raw UTF-8 source code into a stream of Tokens.
- **Rules:** Strips whitespace and comments. Fails immediately on invalid characters.

### 2. Parser
- **Responsibility:** Consumes the Token stream to build the Abstract Syntax Tree (AST).
- **Rules:** The AST represents the raw grammatical structure of the program. It performs zero type checking or symbol resolution.

### 3. AST Validator
- **Responsibility:** Ensures the AST strictly conforms to syntactic bounds before semantics begin.
- **Rules:** Once validated, the AST becomes 100% immutable. No pass may alter an AST node.

### 4. Semantic (Pass Manager)
- **Responsibility:** Type checking, symbol resolution, and scope management.
- **Rules:** Composed of sequential passes (`ScopePass` -> `SymbolPass` -> `TypePass`). Passes do not mutate the AST. They map deterministic `node_id`s to metadata in the `SemanticContext` (`SymbolRegistry`, `TypeRegistry`).

### 5. HIR (High-Level Intermediate Representation)
- **Responsibility:** Represents **Language Semantics**.
- **Rules:** Desugars complex AST structures into simpler language constructs. Does not attempt optimization. It is the purest structural representation of the source intent.

### 6. MIR (Mid-Level Intermediate Representation)
- **Responsibility:** Represents **Execution Semantics**.
- **Rules:** Converts language constructs into a control-flow graph (CFG). This is where high-level optimizations (like dead code elimination or loop unrolling) occur. Independent of the target machine.

### 7. LIR (Low-Level Intermediate Representation)
- **Responsibility:** Represents **Machine Semantics**.
- **Rules:** Abstracts the target architecture. Handles register allocation strategies, stack layouts, and ABI calling conventions (as defined in `ABI_V1.md`).

### 8. LLVM Lowering
- **Responsibility:** Translates LIR into LLVM IR.
- **Rules:** Hands over execution to the LLVM framework for deep target-specific optimizations (O1, O2, O3) and object file generation.

### 9. Binary
- **Responsibility:** The final linked executable.

## Golden Rules for Contributors
1. **Never Guess:** If a user makes a mistake, emit an error. Do not try to "fix" it for them implicitly.
2. **One Way:** Implement features exactly as specified in the Language Specification. No multiple syntaxes for the same semantic feature.
3. **Internal PANIC:** If the compiler encounters an invalid state downstream (e.g., LIR receives untyped MIR), it must `PANIC`. A bad binary is unacceptable.
4. **Specification First:** Never write compiler code for a feature that hasn't been formally specified and frozen via an RFC.

---

### Metadata
- **Version:** 1.0
- **Status:** Frozen
- **Owner:** AAYU Core Team
- **Frozen Date:** 2026-08-07
- **Last Modified:** 2026-08-07
- **Compatibility:** Guaranteed for 1.x
- **Breaking Changes:** Not Allowed
