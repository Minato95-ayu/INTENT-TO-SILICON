# AAYU Compiler Constitution v1.0

This Constitution defines the immutable architectural rules and philosophy for the AAYU Language and Compiler. These rules were officially frozen in v1.0 and must not be violated by any future feature addition or architectural change.

## Rule 1: Language Specification First
The Language Specification drives the Compiler, never the other way around. 
The pipeline order is strictly:
`Language Spec -> Parser -> Semantic -> HIR -> MIR -> LLVM`
The compiler implementation must never decide the language design.

## Rule 2: Compiler Never Guesses
If the program is ambiguous or invalid, compilation fails with a precise diagnostic and a suggested fix. 
The compiler must never make assumptions or automatically coerce types (e.g., silently adding String and Int).

## Rule 3: No Hidden Magic
AAYU is explicit. There are no hidden runtime coercions (like JavaScript's `5 + "6" = "56"`) or runtime type errors (like Python). The compiler must explain everything statically.

## Rule 4: One Way
Each feature has exactly one syntax. For example, struct initialization uses one clear syntax. This keeps the language simple for both the user to write and the compiler to parse. 

## Rule 5: Zero Runtime Cost
AAYU code must look simple but execute optimally. High-level abstractions (like struct field access) must be heavily optimized by the compiler (lowered to `getelementptr`, `load`) without adding runtime overhead. 

## Rule 6: Compiler Trusts Nothing
Every stage of the compilation pipeline must independently verify its inputs. 
`Lexer -> Parser -> AST Validator -> Semantic -> HIR Validator -> MIR Validator -> LLVM Validator -> Binary Validator -> Tests`

## Rule 7: Internal Assertions
If there is an internal bug, the compiler must PANIC rather than generate a wrong binary. A bad binary is unacceptable.

## Rule 8: Immutable Everything
From the moment an AST is parsed, it is completely immutable. HIR and MIR are immutable. Passes are pure functions that do not mutate nodes but instead write metadata to the Semantic Context.

## Rule 9: Reproducible Build
Given the same source code, the compiler must deterministically generate the identical AST, HIR, MIR, LLVM IR, and Binary on any machine.

## Rule 10: Compiler Confidence
The compiler must report a 100% confidence metric after every build, ensuring that all phases (Lexer, Parser, AST, Semantic, HIR, MIR, LLVM, Optimizer, Binary, Tests) passed their verifications.

## Rule 11: 3-Level Testing (Permanent)
Features are only merged if they pass all three levels:
- **Level 1**: Unit Tests
- **Level 2**: Integration Tests
- **Level 3**: Stress, Regression, Fuzz, Performance, Architecture Tests
If Level 3 fails, the feature is rejected.

## Rule 12: Architecture Freeze
Features follow a strict lifecycle:
`Specification -> Architecture -> Freeze -> Implementation -> Testing -> Confidence -> Freeze Again`
Direct coding without specification and architecture freeze is prohibited.

## Rule 13: One Feature = One Responsibility
Features should not be overloaded. A Struct is strictly for data, not for methods, serialization, reflection, or AI metadata. If those features are needed, they will be distinct features. Keep orthogonal concepts orthogonal.

## Rule 14: Compiler Core Never Depends on AI
The compiler must be deterministic and fully standalone. It will never depend on an LLM (Gemini, GPT, Claude, etc.) for core decision making. AI is strictly a developer assistant, never a dependency of the compiler executable.

## Rule 15: Language Must Outlive the Compiler
The AAYU language design is independent of its backend. If we switch from LLVM to WebAssembly, ARM, or JVM, the language must not change by a single line. The language is an abstraction, the compiler is an implementation.

## Rule 16: RFC Process is Mandatory
Whenever a new language feature is proposed (Generics, Traits, Ownership, Async, Pattern Matching, Reflection, etc.), it MUST undergo the RFC (Request for Comments) process. The lifecycle is strictly: `RFC Document -> Formal Specification -> Freeze -> Implementation`. Under no circumstances should compiler code for a new language feature be written before its RFC and Specification are finalized and frozen.

## Rule 17: One IR, One Responsibility
- `AST`: Syntax only.
- `Semantic`: Meaning only.
- `HIR`: High-level validated program semantics (Ambiguity is zero).
- `MIR`: Machine-independent operations, control flow, and optimization boundaries.
- `LIR`: Machine-level lowering.
- `LLVM`: Native code generation.
No IR layer is allowed to perform the duties of another IR layer.

## Rule 18: Strict "No Hidden Magic" for Compiler Actions
The AAYU compiler will NEVER silently:
- Type convert.
- Create variables.
- Inject imports.
- Allocate memory (unless explicitly mandated by the specification).
- Perform optimizations that change observable behavior.
Every compiler transformation MUST be explicitly documented in the specification.

## Rule 19: Mandatory Specification Structure
Every specification document must strictly adhere to this format:
`Purpose`, `Responsibilities`, `What it CAN do`, `What it CANNOT do`, `Input`, `Output`, `Invariants`, `Validation Rules`, `Errors`, `Examples`, `Future Reserved Space`, `Version`, `Frozen`.

## Rule 20: One Document = One Truth
Every feature or compiler layer has exactly ONE specification document (e.g., `HIR_V1.md`). A concept is defined fully and exclusively in its respective specification document. It must never be redundantly described or contradicted elsewhere.

## Rule 21: Implementation Never Leads Specification
Code is never written before the specification. The absolute order of feature development is:
`Idea -> RFC -> Specification -> Architecture Review -> Freeze -> Implementation -> Testing -> Confidence Report -> Merge`
## Rule 22: Every IR Must Be Independently Testable
Every intermediate representation layer (AST, HIR, MIR, LIR) must be fully testable in isolation. Validation must pass without requiring compilation down to LLVM.

## Rule 23: Canonical IR Rule
A specific AST must deterministically produce the exact same HIR, MIR, and LIR every time. There is no randomness, no arbitrary ordering, and no hidden variations. The mapping must be canonical.

## Rule 24: Performance & Memory Regression Rule
Compiler execution performance (Compile Time) and Memory footprint must stay strictly within defined budgets (e.g., 10,000 nodes < 200ms and < 40MB). Any optimization or feature that breaches these bounds without an explicit specification update is a regression and must trigger a pipeline failure.

## Rule 25: Snapshot Protection Rule
Every IR layer (HIR, MIR, LIR, LLVM) is protected by Golden Snapshot tests. Any output variation that does not match the frozen snapshot will immediately fail the build to detect architectural regressions.

---

### AAYU Master Roadmap
To ensure maximum stability, the roadmap strictly separates specification from implementation, prioritizing stable specifications above all else.

**Phase 1-3 (Completed & Frozen):**
- Compiler Constitution
- Language Specification v1.0
- Memory Model v1.0
- ABI v1.0
- Standard Library Specification
- Compiler Architecture & Developer Guide
- Module System Foundation

**Phase 4+ (Next Order):**
1. **HIR Specification** (Freeze) - HIR nodes, invariants, validation rules, v1.0.
2. **MIR Specification** (Freeze) - Opcodes, CFG, Optimization boundaries.
3. **LIR Specification** (Freeze)
4. **LLVM Lowering Specification**
5. **Bytecode Specification** (`AYBC v1`)
6. **VM Specification**
*(Implementation begins ONLY after the specification for that stage is frozen.)*

---

### Warning on Over-Engineering
While planning for the future (Ownership, Lifetimes, Traits, Generics) is essential, interfaces should be frozen but implementations must remain lazy. Implement features **only when the current language requires them** to maintain a lean, robust, and maintainable codebase.
