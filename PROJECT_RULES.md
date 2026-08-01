# AAYU Engineering Rules and Standards

This document establishes the strict engineering, release, and quality assurance rules for the AAYU programming language and compiler project.

## 1. The "Definition of Done"

A feature is NOT considered "Done" until it has successfully traversed all stages of the compiler architecture and meets these strict criteria:

✓ Specification implemented
✓ Parser implemented
✓ Semantic analyzer implemented
✓ IR implemented
✓ Bytecode implemented
✓ Native VM implemented
✓ Unit tests pass
✓ Conformance tests pass
✓ No regression
✓ Documentation updated
✓ Benchmarks collected (if applicable)

## 2. Conformance Suite Structure

The AAYU Conformance Suite must remain granular and independent. Each language feature must have its own dedicated test file in `tests/conformance/`.

Example structure:
```
tests/conformance/
├── 001_print.aayu
├── 002_variables.aayu
...
└── test_runner.py
```

## 3. Release Rules

Releases must follow an absolute zero-tolerance policy for failures:

* **0 FAIL**
* **0 CRASH**
* **0 NOT IMPLEMENTED**

Only when the Conformance Suite outputs `✅ Phase XX VERIFIED` is a release authorized.
If there is a single exception, the status remains `❌ DO NOT RELEASE`.

## 4. The Engineering Rule (Zero Degradation)

> **Never implement a new language feature while any existing conformance test is failing.**

This ensures the compiler maintains the stability characteristics found in mature projects like Go, Rust, and Python. Features must be built incrementally upon a foundation of passing tests.

## 5. Project Roadmap (Phase 11A to 16)

### Phase 11A
* Language Spec Freeze
* Parser Complete
* Semantic Analyzer
* IR
* Bytecode
* Native VM
* Opcode Coverage
* Conformance Suite
* Linux
* macOS
* Windows
* Benchmarks
* Documentation
* Release Candidate
* Stable Release

**Exit condition**: `0 FAIL`, `0 CRASH`, `100% Conformance`

### Phase 11A Priorities (Frozen)
1. Print
2. Variables
3. Arithmetic
4. Boolean
5. Comparison
6. If / Else
7. While
8. Functions
9. Recursion
10. Strings
11. Arrays
12. Dictionaries
13. Error Handling
14. File I/O
15. HTTP
16. Database

### Phase 11B (Memory System)
* Arena allocator
* Heap allocator
* Object model
* Mark
* Sweep
* Incremental GC
* Thread safe GC

### Phase 11C (Performance)
* Peephole Optimizer
* Constant Folding
* Dead Code Elimination
* Inline Cache
* JIT

### Phase 11D (LLVM Backend)
* LLVM IR
* Native Binary
* Cross Compilation
* Linker

### Phase 12 (Self Hosting)
* Compiler written in AAYU

### Phase 13 (Developer Ecosystem)
* VS Code
* LSP
* Formatter
* Debugger
* Registry
* Documentation

### Phase 14 (Intent Engine)
* Natural Language → AAYU

### Phase 15 (Brain OS)
* Operating system architecture using AAYU and AI

### Phase 16 (Intent-to-Silicon)
* Hardware compilation target

## 6. Versioning & Release Policy

AAYU follows a strict semantic structure aligned with maturity milestones:

| Version | Meaning            |
| ------- | ------------------ |
| v0.2.x  | Runtime fixes only |
| v0.3.x  | Memory System      |
| v0.4.x  | JIT                |
| v0.5.x  | LLVM               |
| v0.6.x  | Self Hosting       |
| v1.0    | Stable Language    |

## 7. Long-term Canonical Architecture

The AAYU pipeline is isolated through strict, versioned, independent canonical specification contracts:

```text
Human Intent
      ↓
Intent Engine
      ↓
LANGUAGE_SPEC
      ↓
Compiler
      ↓
BYTECODE_SPEC
      ↓
VM_SPEC
      ↓
MEMORY_MODEL
      ↓
Runtime
      ↓
CPU
```

The Language, Bytecode, VM, Memory, and Standard Library (`STDLIB_SPEC`) teams may operate independently as long as their artifacts comply with the exact specification contracts.
