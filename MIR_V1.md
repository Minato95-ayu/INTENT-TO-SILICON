# MIR Architecture Specification (v1.0)

> **Status:** `FROZEN`
> **Architecture:** AAYU MIR v1.0

## 1. Purpose
The Middle Intermediate Representation (MIR) serves as the bridge between declarative semantic representation (HIR) and machine-specific backend generation (LLVM IR). MIR translates the semantic "WHAT" from HIR into the machine-oriented "HOW". 

## 2. Position in Compiler Pipeline
```
LANGUAGE SPEC -> Semantic Analysis -> HIR -> [ MIR Lowering ] -> MIR -> [ Target Layout ] -> Native Backend
```
MIR operates explicitly after HIR validation. MIR lowering produces logical machine-level operations, which are later resolved against a target-specific `TargetLayout` / `ABIDescription` before LLVM emission.

## 3. MIR Responsibilities
- **Machine-Oriented Lowering:** Converting semantic intent into explicit machine operations.
- **Explicit Memory Management:** Representing allocations, loads, stores, and copies.
- **Explicit Control Flow:** Flattening structured loops and conditionals into basic blocks and branches.
- **Target-Agnostic Layout Prep:** MIR prepares the logical layout of structs and enums, but relies on a separate `TargetLayout` subsystem for concrete byte sizing and alignment.
- **Deterministic Representation:** Preserving strict deterministic IDs and tracking the exact compiler state.

## 4. Non-Responsibilities
- **NO Semantic Invention:** MIR must never infer, guess, or create missing semantic rules.
- **NO High-Level Optimization:** Constant folding, dead code elimination, and inlining are explicitly forbidden in MIR-1.
- **NO Target ABI Hardcoding:** MIR does not invent target-specific rules (e.g., x86 register classes, calling conventions). It queries a `TargetLayout` subsystem.
- **NO SSA Construction:** MIR-1 does not enforce Static Single Assignment (SSA). SSA is deferred to a future `MIR-2` phase.

## 5. HIR → MIR Contract
- Every valid HIR node MUST map deterministically to a MIR construct.
- Missing semantic information in HIR (e.g., missing TypeID) MUST yield an `InternalCompilerError` (ICE) during lowering.
- MIR never falls back to arbitrary types or null semantics.

## 6. MIR Node/Instruction Model
MIR instructions are flat and strictly ordered within Basic Blocks. Complex nested expressions from HIR are flattened into sequential instructions utilizing temporary intermediate values.

## 7. MIR Type System
MIR translates `TypeID`s from the Semantic Type Registry into explicit machine types (`mir::Int`, `mir::Float`, `mir::Bool`, `mir::Ptr`, `mir::Aggregate`). 

## 8. Memory Model
MIR utilizes explicit, ownership-agnostic memory operations based on the language's defined semantics:
- `alloca`: Stack allocation for local variables.
- `load`: Reading a value from a memory address.
- `store`: Writing a value to a memory address.
- `memcpy`: Bulk copying for aggregates.

## 9. Aggregate Layout
Structs are lowered to explicit `mir::Aggregate` layouts. MIR resolves `FieldID` accesses into logical base-pointer index offsets. The exact byte offsets and padding are calculated dynamically by consuming the `TargetLayout` subsystem, rather than being hardcoded into MIR.

## 10. Enum Representation
Enums are strictly lowered to a tagged union format:
```
mir::Enum {
    tag: mir::Int32,   // Logical Base discriminant
    payload: mir::Aggregate // (Optional) Payload
}
```
`mir::Int32` is the logical MIR discriminant representation; physical storage width/layout is determined by `TargetLayout`.
*Note: Advanced pattern matching will only be implemented in MIR when officially defined by `LANGUAGE_V1`.*

## 11. Optional Representation
`Optional<T>` is strictly lowered as a concrete struct containing a boolean flag and the payload:
```
mir::Aggregate {
    has_value: mir::Bool,
    payload: T
}
```
There is no "null pointer" magic for `Optional<T>` in MIR unless specifically dictated by a future optimization phase. The layout is concrete and explicitly sized.

## 12. String Representation
Strings are lowered into exactly one concrete layout:
```
mir::String {
    data: mir::Ptr<mir::Byte>,
    length: mir::USize
}
```
`capacity` is explicitly excluded from MIR-1 unless the language specification mandates dynamic string growth.

## 13. References & Pointers
MIR explicitly distinguishes between values and pointers. HIR references are lowered to MIR pointer types (`mir::Ptr<T>`), and automatic dereferencing is made explicit via `load` instructions.

## 14. Basic Blocks & Terminators
Control flow is represented as a directed graph of Basic Blocks. Every block MUST end with a Terminator instruction (e.g., `Branch`, `CondBranch`, `Return`, `Unreachable`).

## 15. Function/Action Lowering
MIR provides explicit storage locations for variables whose storage semantics require them. As an implementation policy for MIR-1, lowering may allocate all local variables via `alloca` in the function's entry block, but this is not an immutable architectural law.

## 16. Calls & ABI Metadata
Function calls include explicit logical arguments. The translation into physical passing conventions (registers vs stack) is delegated to the `TargetLayout` and the native backend.

## 17. Casts & Conversions
MIR contains explicit conversion instructions **only** for conversion operations already authorized by the Language Specification and represented explicitly by HIR.
- No implicit conversion may be invented by MIR.
- Since HIR-3 has no cast syntax, MIR-1 implements **zero** general cast lowering requirements.

## 18. Deterministic IDs
Since one HIR node may lower into multiple MIR instructions, MIR Node IDs are derived deterministically:
```
MIRNodeID = Hash(ModuleID, HIRNodeID, LoweringPhase, LocalOrdinal)
```
Random UUIDs, memory addresses, or Python `id()` calls are strictly forbidden.

## 19. Validation Invariants
The MIR Validator enforces:
- All used variables are backed by an allocation.
- Block terminators are valid.
- Type layouts match instruction requirements.

## 20. Error/ICE Rules
Any invariant violation within MIR throws a structured `InternalCompilerError`, citing the exact phase and violated MIR invariant.

## 21. Serialization & Snapshots
MIR must be fully serializable to a human-readable text format and JSON to ensure deterministic compiler snapshots for testing and debugging.

## 22. Optimization Boundary
MIR-1 is purely for correctness and machine-oriented lowering; concrete target layout is supplied by `TargetLayout`. No optimization passes run during this phase.

## 23. LLVM Boundary
MIR maintains logical machine-level detail so that the subsequent MIR-to-LLVM pass is a direct, mechanical translation guided by `TargetLayout`, devoid of semantic decision-making.

## 24. Reserved Future Features
- `MIR-2`: Static Single Assignment (SSA) construction (`phi` nodes, dominance).
- Mid-level optimizations (CSE, DCE, constant propagation).

## 25. Forbidden Responsibilities
- Parsing and Semantic Analysis.
- Guessing implicit conversions.
- Target ABI hardcoding.

## 26. Verification Requirements
- MIR must be verified via strict ID determinism tests.
- Lowering must pass fuzzing tests to ensure missing HIR data yields an ICE.

## 27. Freeze Criteria
MIR-1 will be frozen when the lowering of the standard syntax works flawlessly end-to-end against the specification, passing Unit, Integration, Stress, Fuzz, and Benchmark tests, with zero semantic assumptions.
