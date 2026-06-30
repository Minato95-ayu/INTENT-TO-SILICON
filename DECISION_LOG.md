# AAYU Decision Log

This log records major architectural decisions, ensuring that rationale is preserved as the repository evolves.

## Milestone 5: Type System

### Phase 5.5: Interfaces
- **Decision:** Introduce the "Language Evolution Policy" (Additive Only).
- **Rationale:** To implement Interfaces without violating the Architecture Freeze, we refine the freeze to mean "Core architecture is frozen, but grammar, keywords, and AST nodes can be extended additively". Existing syntax, semantics, and bytecode remain completely unchanged.
- **Status:** Approved & Implementing.

### Phase 5.4: Type Inference
- **Decision:** Implement purely local type inference.
- **Rationale:** We want to preserve deterministic compilation and keep passes simple. Variables infer their type from their initialization expression. Functions without return type annotations infer their return type from return statements. If a function has ambiguous/differing returns, it defaults to `AnyType` for MVP rather than doing advanced unification.
- **Status:** Approved & Implemented.

### Phase 5.3: Type Checker
- **Decision:** MVP Type Checker enforces assignments, basic arithmetic and function return types.
- **Rationale:** Strict typing enforces safety, but legacy dynamically-typed code is permitted using `AnyType` to ensure backwards compatibility. `UnknownType` and `ErrorType` are reserved to prevent cascading errors on typos.
- **Status:** Approved & Implemented.

### Phase 5.2: Symbol Types
- **Decision:** Introduce `declared_type` and `resolved_type` properties on all `Symbol` instances.
- **Rationale:** The `SymbolTable` acts as the source of truth for semantic passes. Binding types here prevents polluting the AST unnecessarily during early passes.
- **Status:** Approved & Implemented.

### Phase 5.1: Type AST
- **Decision:** Restrict parser updates purely to parsing Type Annotations.
- **Rationale:** We must keep the AST frozen in functionality while expanding its capacity. Adding `TypeNode` instances allows the semantic pipeline to evaluate types without compiler changes.
- **Status:** Approved & Implemented.
