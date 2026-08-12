# AAYU Register Allocation Specification

## 1. Overview
The Register Allocation engine in AAYU uses the **Linear Scan** algorithm (Poletto & Sarkar), operating on an optimized Static Single Assignment (SSA) Low-Level IR (LIR). The allocator is target-agnostic but designed primarily for Native JIT and LLVM backends. The existing Bytecode VM does not perform allocation, instead operating on the infinite virtual register pool.

## 2. Invariants
- **Infinite Virtual Registers (Pre-Allocation):** LIR initially contains unbounded virtual registers.
- **Finite Physical Registers (Post-Allocation):** Based on the backend target, the virtual registers are mapped to a bounded set of $K$ physical registers.
- **VM Bypass:** The Bytecode backend completely bypasses Register Allocation and Target Lowering logic.

## 3. Register Classes
Physical registers belong to specific classes, supporting multi-architectural conventions (e.g., x86_64, ARM64):
- **GENERAL:** General purpose integer operations (`r0-r15`, `rax`, `x0`).
- **FLOAT:** Floating point/scalar ops.
- **VECTOR:** SIMD ops.
- **SPECIAL:** Dedicated hardware flags, frame pointers (`rbp`, `rsp`, `fp`), or reserved convention registers.

## 4. Live Intervals
A live interval tracks the precise lifetime of a virtual register. 
- **Start / End:** The global instruction index (assigned via Reverse Post Order traversal).
- **Uses:** A list of all indices where the register is referenced (Def or Use).
- **Spill Cost:** Determines which interval to spill when physical registers are exhausted.
  ```math
  \text{Spill Cost} = \frac{\text{Use Count}}{\text{End} - \text{Start}}
  ```

## 5. Linear Scan Algorithm
1. **Instruction Numbering:** Traverse CFG in Reverse Post Order. Number all instructions by increments of 2 (leaving gaps for spill rewrites).
2. **Liveness Analysis:** Dataflow analysis computes `LiveIn` and `LiveOut` sets per basic block.
3. **Interval Construction:** Using liveness sets and local block traversal, map each virtual register to its `LiveInterval`.
4. **Linear Scan:**
   - Sort intervals by `Start` index.
   - Maintain a list of `Active` intervals sorted by `End` index.
   - For each interval:
     - Free physical registers from any `Active` intervals that have ended.
     - If physical registers are available, allocate one.
     - If not, compute the `Spill Cost` among all `Active` intervals (including the current one) and spill the one with the lowest cost.
5. **Spill Rewrite:** Replace virtual references of spilled registers with `LOAD_SPILL` and `STORE_SPILL` pseudos. Repeat Allocation if necessary.

## 6. AnalysisManager Invalidation
- Structural CFG changes (e.g., from Spill Rewrite) **must** invoke `AnalysisManager.invalidate_all()`.
- Liveness and Interval data are cached securely in `AnalysisManager` and tied strictly to the current CFG state.
