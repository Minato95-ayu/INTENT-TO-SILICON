# AAYU Decision Log

This log records major architectural decisions, ensuring that rationale is preserved as the repository evolves.

## Milestone 8: High-Level Intermediate Representation (HIR-3)

### Phase 8.1: HIR-3 Semantic Boundary Enforcement
- **Decision:** Establish strict boundary: HIR nodes must rely purely on deterministic IDs (TypeID, SymbolID, FieldID, VariantID) assigned by the SemanticContext. Fallbacks to `core::Null` or raw types are strictly prohibited.
- **Rationale:** Separating semantics from machine representation is critical. However, because the legacy MIR and lowering pipeline previously relied on AST-like type inference directly, enforcing this boundary breaks existing compilation downstream. 
- **Status:** Approved. MIR/Lowering regression failures are explicitly documented and accepted as expected migration contract breaks. The downstream pipeline will be rewritten to consume HIR-3 in subsequent phases.


## Milestone 7: Production Readiness (Ecosystem & DX)

### Phase 7.2: AAYU Linter
- **Decision:** Do not fail builds on warnings by default. Introduce `--strict` mode to promote warnings to errors.
- **Rationale:** Ensures that CI pipelines aren't blocked by minor stylistic suggestions or empty blocks while still providing teams the option to enforce strict quality controls, aligning with modern production tooling (e.g. Go, Rust).
- **Status:** Approved & Implemented.

### Phase 7.1: AAYU Formatter
- **Decision:** Implement Formatter outside the semantic pass pipeline directly relying on parser AST.
- **Rationale:** Formatter strictly deals with AST stringification without semantic resolution. Running it outside the semantic pipeline prevents mutating the AST or evaluating types, ensuring a zero-side-effect format run. `aayu fmt` ensures an opinionated canonical layout for the community.
- **Status:** Approved & Implemented.

## Milestone 5: Type System & Optimization

### Phase 5.8: Static Optimization
- **Decision:** Implement Constant Folding, Dead Code Elimination, and Branch Pruning strictly as AST transformations via an `ASTTransformerPass`.
- **Rationale:** To adhere to the Architecture Freeze, optimization happens purely at the AST semantic layer. The compiler and VM are untouched, ensuring behavior is preserved exactly while performance improves.
- **Status:** Approved & Implemented.

### Phase 5.7: Generics
- **Decision:** Implement type erasure generics entirely within the semantic layer.
- **Rationale:** To adhere to the Architecture Freeze, generics (<T>) are resolved into GenericPlaceholderType and GenericInstance purely during type checking. The Compiler and VM remain completely oblivious to generics, meaning zero regressions in execution logic.
- **Status:** Approved & Implemented.

### Phase 5.6: Traits & Extensions
- **Decision:** Implement purely semantic extensions and zero-cost abstraction compiler pass.
- **Rationale:** To strictly adhere to the compiler/VM freeze, Phase 5.6 is limited to AST parsing, semantic scope isolation, and type checking interface contracts. Method dispatch lowering is deferred.
- **Status:** Approved & Implemented.

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
