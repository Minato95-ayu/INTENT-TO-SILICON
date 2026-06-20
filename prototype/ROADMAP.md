# AAYU Roadmap & Release Milestones

This document tracks the high-level roadmap, release milestones, and completed features of the AAYU application runtime platform.

---

## 🚀 Milestone: AAYU v0.4.0 (Runtime MVP ACHIEVED)
We have officially achieved full **Virtual Machine Runtime MVP parity** with the AST Interpreter! Complex, real-world AAYU applications can now compile to bytecode (`.ayc`) and run completely on the VM runtime.

### Verified Applications on VM:
1. **Todo App VM**: Direct routing, list operations, HTML templates, and SQLite storage.
2. **Library Management System VM**: Complex relational entities, nested collections loops (`for each`), dynamic route dispatching, database updates, and metrics rendering.

---

## Completed Phases

### Phase 1: Core Language & AST Interpreter (100% Complete)
- [x] Human-first syntax parser and lexer.
- [x] Abstract Syntax Tree (AST) evaluator.
- [x] Basic Control Flow (`if`, `while`, comparisons).
- [x] Database CRUD mappings (SQLite).
- [x] Session & Authentication primitives.

### Phase 2: Developer Ecosystem (90% Complete)
- [x] AAYU CLI (`cli.py`) for compiling and running files.
- [x] VS Code Extension (Syntax highlighting & snippets).
- [x] Language Server Protocol (LSP) skeleton.
- [ ] Standard Library Expansion.

### Phase 3: Stack-based Virtual Machine Runtime (100% Complete)
- [x] **AAYU Intermediate Representation (IR)**: Compact Instruction Set Architecture (ISA).
- [x] **Bytecode Compiler**: AST compiler emitting `.ayc` JSON-serialized bytecode.
- [x] **Virtual Machine**: Execution engine with call frames, variable scoping, and execution stack.
- [x] **VM Standard Library Bridge**: Native Python/SQLite bindings (`db_create`, `db_find`, `render_template`, etc.) triggered via `CALL_TASK`.
- [x] **HTTP Routing & Dispatch**: Dynamic request normalization, form parsing, nested VM request isolation, and mock request execution dispatch.
- [x] **HTTP Socket Server**: Integrated HTTP listener running AAYU bytecode handlers.

---

## Next Phase: Phase 4 — Runtime Hardening (Completed)

With the hardening sprint successfully executed, AAYU has transitioned to a **Stable Runtime Candidate**:

### 1. VM Error Handling & Diagnostics (Phase 4A)
- [x] Propagated line numbers and filenames through the bytecode compiler.
- [x] Added VM call-stack inspection to print descriptive stack traces on runtime crashes.

### 2. Explicit HTTP Methods in Grammar (Phase 4B)
- [x] Replaced temporary route method heuristics with explicit verbs (`get`, `post`, `delete`) in grammar.
- [x] Implemented lookahead parsing for `delete` route registration vs database delete disambiguation.

### 3. Stress Testing & Hardening (Phase 4C)
- [x] Upgraded to `ThreadingHTTPServer` to process requests concurrently on multiple threads.
- [x] Isolated database cursors per request to prevent cross-request contamination.
- [x] Configured SQLite in WAL mode and synchronous `NORMAL` with shared connection `RLock` synchronization.
- [x] Verified zero database locks and stable memory growth under 1000 requests and 100 concurrent writes.

---

## Next Milestone: Phase 4D — Auth, Sessions, Cookies & Native Runtime

With the core runtime hardened, we will begin the next phase:
1. **Auth & Sessions**: Implementing secure cookies, session expiration, and stateful session storage.
2. **Native Runtime Design**: Architectural mapping from Python VM to a native Rust runtime using the same serialization format.

