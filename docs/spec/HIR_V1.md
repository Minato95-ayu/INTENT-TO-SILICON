# High-Level Intermediate Representation (HIR) v1.0

## 1. Purpose
The HIR is the first intermediate representation in the AAYU compiler pipeline. It represents a fully validated, semantically correct program. In HIR:
- There is absolutely no ambiguity.
- There are no unresolved symbols.
- There are no unresolved types.
- The representation is 100% machine-independent.

## 2. Responsibilities
HIR is strictly responsible for representing:
- Qualified symbol references.
- Resolved types.
- Struct layouts (attached directly to nodes).
- Enum layouts (attached directly to nodes).
- Resolved module references.
- Constant folding (if permitted by language specification).
- Scope information.

It is explicitly **NOT** responsible for Ownership rules, LLVM lowering, or Register allocation.

## 3. What it CAN do (and MUST NEVER contain)
HIR is an abstraction over the semantics, not the syntax. Therefore, it **MUST NEVER** contain:
- Parser Tokens.
- Raw Syntax.
- Comments or Whitespace.
- String source text (unless as a evaluated literal value).
- File parsing logic.
- LLVM instructions or MIR opcodes.
- Stack offsets or CPU Registers.

## 4. Input
The input to the HIR generator is an immutable `AST` and a fully populated `SemanticContext` containing `SymbolRegistry` and `TypeRegistry`.

## 5. Output
A complete `HIRModule` graph representing the language semantics of the original program.

## 6. HIR Node List
The frozen set of allowed nodes in HIR v1.0:
- `HIRModule`
- `HIRAction`
- `HIRBlock`
- `HIRVariable`
- `HIRAssignment`
- `HIRIf`
- `HIRLoop`
- `HIRReturn`
- `HIRCall`
- `HIRStructInit`
- `HIRStructFieldAccess`
- `HIREnumValue`
- `HIRBinary`
- `HIRUnary`
- `HIRLiteral`
- `HIRCast`

*(No other nodes may be introduced without an RFC changing this specification.)*

## 7. HIR Validation Rules
Before any MIR generation can begin, the HIR Validator must ensure:
- [x] Every node has a resolved `Type`.
- [x] Every node has a mapped `SourceMap` reference.
- [x] Every symbol is resolved.
- [x] Every struct and enum layout is resolved.
- [x] Every module and import is resolved.
- [x] No duplicate node IDs exist.
- [x] The Control Flow Graph (CFG) at the high level is valid.

## 8. HIR Invariants
- HIR cannot contain unresolved identifiers.
- HIR cannot contain parser errors.
- HIR cannot contain unknown types.
- HIR cannot contain duplicate symbols.
- HIR cannot contain cyclic scopes.
- HIR cannot contain invalid struct layouts.

## 9. Lowering Contract
The contract between HIR and MIR is strictly:
`Input -> Validated Program -> Typed -> Resolved -> Lower Ready`
HIR **does not** perform machine-level optimizations.

## 10. Errors
If the HIR Validator detects a violation of any Invariant (e.g., an `UnknownType` slips through), it must immediately trigger a compiler `PANIC`. Semantic errors must be caught in the Semantic Phase, not in the HIR Phase.

## 11. Examples
An AST `ActionCallNode(core.print)` is desugared and mapped directly to a `HIRCall` where the target is a fully qualified `SymbolID` pointing to the `core.print` definition, completely bypassing string-based lookups.

## 12. Future Reserved Space
These features are reserved for future versions and must not be implemented in v1.0:
- Generic Types
- Traits
- Ownership
- Lifetimes
- Pattern Matching
- Reflection
- Async
- Macros

---

### Metadata
- **Version:** 1.0
- **Status:** Frozen
- **Owner:** AAYU Core Team
- **Frozen Date:** 2026-08-07
- **Last Modified:** 2026-08-07
- **Compatibility:** Guaranteed for 1.x
- **Breaking Changes:** Not Allowed
