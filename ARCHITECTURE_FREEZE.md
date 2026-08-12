# AAYU Architecture v1.0 Frozen

This document officially declares that the **AAYU Architecture v1.0** is frozen as of Sprint 32.

The foundational design of the AAYU platform is now stabilized and verified across multiple example domains (Hospital, CRM, E-Commerce, School, Blog, and AI-Agent).

## Verified Pipeline (Track A: Software Factory)

The AAYU pipeline successfully transforms declarative intent into functional, deployable full-stack software via the following deterministic flow:

1. **Intent / AAYU Code** (`.aayu` definition)
2. **Parser** (Validates syntax and structural integrity)
3. **AST** (Abstract Syntax Tree)
4. **IR** (AAYU Intermediate Representation v1)
5. **Target Engine** (Scoring heuristics and Stack Selection)
6. **Code Generators**:
   - `React Generator` (Frontend)
   - `FastAPI Generator` (Backend)
   - `PostgreSQL Generator` (Database)
7. **Orchestrator** (Docker Compose, Env, README)

## Verified Pipeline (Track B: Native Runtime)

The initial groundwork for the Native Runtime environment is complete:

1. **AAYU Code**
2. **Compiler** (Outputs AYC format)
3. **AYC Bytecode** (`.ayc` standard defined)
4. **Rust Runtime** (AAYU VM skeleton constructed)
5. **Execution** (Mini VM tested on subset opcodes)

## Reflection Contract (Phase 4.6)

Reflection is implemented as a Standard Library module (`reflect`), not as core language keywords. The following contract strictly governs reflection behavior to preserve the Milestone 3 architectural freeze:

1. **Read-Only Access**: Reflection may inspect runtime objects and metadata.
2. **Immutability**: Reflection must **never** mutate runtime metadata or compiler metadata (e.g., changing visibility, modifying exported status).
3. **VM Integrity**: The core VM and Compiler remain generic and agnostic to reflection. All reflection logic is encapsulated in the `reflect_lib` standard library.

## Phase 8: HIR-3 Freeze (Types & Expressions)

The HIR-3 Semantic Boundary is officially **FROZEN** as of August 2026.
1. **Semantic Separation**: HIR is strictly separated from machine code output and relies purely on deterministic IDs (TypeID, SymbolID, FieldID, VariantID).
2. **Strict Validation**: Missing identifiers correctly trigger structured `InternalCompilerError`s instead of relying on legacy fallbacks.
3. **Immutable Status**: HIR-3 is immutable unless a future RFC explicitly changes the specification or a formally identified correctness defect is discovered. Downstream MIR/Lowering stages must adapt to this stable semantic-ID contract.

## Phase 9: MIR Architecture Specification (v1.0) Freeze

The MIR v1.0 Specification (`MIR_V1.md`) is officially **FROZEN**.
1. **Machine-Oriented Lowering**: MIR strictly lowers HIR semantics into logical machine operations without inventing missing semantics or implicit conversions.
2. **Target Layout Separation**: MIR remains target-agnostic. All dynamic sizing, alignment, padding, and physical bit-widths (for enums) are deferred to a new `TargetLayout` subsystem.
3. **Exact Layout Boundaries**: Strict definitions enforce string representations (`Ptr<Byte>`, `USize`) and explicit `Optional<T>` structures over ambiguous null-pointers.
4. **SSA Deferred**: MIR-1 explicitly defers SSA construction and mid-level optimizations to a future MIR-2 phase, prioritizing correctness and layout first.

## Moving Forward

With the architecture frozen for both HIR and the MIR specification, the next sequential sprint is **MIR-1 Implementation**. This implementation will follow the strict verification discipline: Unit → Integration → Stress → Fuzz → Benchmark → Regression → Audit → Confidence Report → Implementation Freeze.
