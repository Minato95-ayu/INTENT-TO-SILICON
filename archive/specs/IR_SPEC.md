# AAYU Intermediate Representation (IR) Specification

This document serves as the canonical specification for the AAYU Compiler's Intermediate Representation architecture. It outlines the design, semantics, and transformations required to bridge the gap between high-level Semantic AST and low-level Stack Bytecode, providing the necessary foundations for optimization passes and future LLVM/JIT backends.

## 1. Architectural Pipeline

The AAYU compiler pipeline strictly follows this multi-stage lowering process:

```text
Lexer 
  ↓
Parser
  ↓
AST
  ↓
Phase 12.0 Semantic Pipeline (Scope → Symbol → Type → Constant Evaluation)
  ↓
HIR (High-Level IR)
  ↓
MIR (Mid-Level IR / Three-Address Code)
  ↓
CFG (Control Flow Graph) + Basic Blocks
  ↓
SSA (Static Single Assignment)
  ↓
Pass Manager (Optimizations)
  ↓
LIR (Low-Level IR / Stack Machine)
  ↓
Bytecode Generation
```

## 2. HIR (High-Level IR)
**Goal:** Abstract away syntactic sugar and represent the purely semantic meaning of the source code.
- Strongly typed nodes based on the Semantic AST.
- Preserves high-level control flow (`if`, `while`, `for`).
- Retains closure and higher-order function boundaries.

## 3. MIR (Mid-Level IR) & Three-Address Code (TAC)
**Goal:** Flatten control flow and simplify operations for rigorous optimization.
- **Register-Based:** MIR uses virtual registers (`r1`, `r2`) instead of an implicit stack.
- **Three-Address Code:** Instructions take the form `dest = opcode src1 src2`.

### MIR Opcodes
| Category | Opcodes |
| :--- | :--- |
| **Data Flow** | `MOVE`, `LOAD_CONST`, `LOAD_GLOBAL`, `STORE_GLOBAL`, `PHI` |
| **Arithmetic** | `ADD`, `SUB`, `MUL`, `DIV`, `MOD` |
| **Logic/Relational** | `COMPARE`, `AND`, `OR`, `NOT` |
| **Control Flow** | `JUMP`, `BRANCH`, `CALL`, `RETURN` |

## 4. CFG (Control Flow Graph)
**Goal:** Map the execution flow of MIR instructions.

### BasicBlock Format
Every BasicBlock maintains explicit flow and analysis metadata:
- `id`: Unique identifier (e.g., `bb0`, `bb1`).
- `instructions`: Linear list of MIR instructions terminating in a jump/branch/return.
- `predecessors`: List of incoming blocks.
- `successors`: List of outgoing blocks.
- **Analysis Data:**
  - `dominators`: Blocks that must execute before this block.
  - `post_dominators`: Blocks that must execute after this block.
  - `live_in` / `live_out`: Variable liveness sets for register allocation.
  - `loop_depth`: Nesting level for loop optimizations.
  - `frequency`: Estimated execution frequency for profile-guided optimization.

## 5. SSA (Static Single Assignment)
**Goal:** Ensure every variable is assigned exactly once, simplifying data-flow analysis.

### Rules & Semantics
1. **Scope:** SSA is strictly applied to local variables, temporaries, and parameters. Global state and object fields remain in memory (`LOAD_GLOBAL` / `STORE_GLOBAL`).
2. **Algorithm:** Constructed using the **Cytron Algorithm**.
   - Compute Dominance Frontiers.
   - Insert `PHI` nodes at frontier merge points.
   - Rename variables sequentially (e.g., `x_0`, `x_1`).

## 6. Pass Manager & Optimizations
**Goal:** An extensible, decoupled engine for transforming SSA-form MIR.

Passes are dynamically registered and run sequentially. Required initial passes:
- **Constant Folding & Propagation:** Precompute constants and propagate values.
- **Copy Propagation:** Eliminate redundant register-to-register moves.
- **Common Subexpression Elimination (CSE):** Reuse identical computations.
- **Algebraic & Branch Simplification:** Remove redundant ops (`x+0`) and dead branches.
- **Dead Code / Dead Store Elimination (DCE/DSE):** Strip unread assignments.
- **Strength Reduction & LICM:** Future optimizations for arithmetic and loops.

## 7. LIR (Low-Level IR)
**Goal:** Map optimized virtual registers back to physical/virtual stack slots.
- Performs SSA Deconstruction (Phi elimination).
- Maps register lifespans to Stack Slots.
- Prepares for direct 1:1 emission to AAYU Bytecode.

## 8. Register Allocation (Future)
**Goal:** Map unbounded SSA virtual registers to a finite set of physical registers (or strictly bounded stack slots).
- Linear Scan / Graph Coloring algorithms.
- Spill code generation.

## 9. Calling Convention (Future)
**Goal:** Standardize how functions/actions receive parameters and return values.
- Argument passing (Registers vs Stack).
- Caller-saved vs Callee-saved registers.

## 10. Metadata & Diagnostics
**Goal:** Maintain rich source mapping for debugging and robust error reporting.
- Source line/column mapping for every IR instruction.
- Type annotations and symbol table references.

## 11. Debug Info (Future)
**Goal:** Support external debuggers (DWARF format equivalent).
- Variable lifetime tracking.
- Call frame unwind data.
