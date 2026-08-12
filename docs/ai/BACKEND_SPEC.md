# AAYU Backend Lowering Specification

**Status:** Draft
**Version:** 1.0

## Overview
AAYU utilizes a tripartite backend architecture to achieve maximum flexibility for development, execution, and extreme performance. The architecture officially branches immediately after **Phase 13.7 (LIR Generation)**.

## Architecture

```text
                     [ SSA MIR ]
                          │
                          ▼
            [ Optimization & Allocation ]
                          │
                          ▼
             [ LIR (Linear IR) Pipeline ]
                          │
      ┌───────────────────┼────────────────────┐
      ▼                   ▼                    ▼
[ Bytecode ]          [ LLVM ]             [ Native ]
```

### 1. Bytecode Backend (`.aybc`)
**Purpose:** Rapid execution, cross-platform portability, fast startup for local development and edge functions.
**Input:** LIR
**Lowering Strategy:**
* The Bytecode backend operates on an infinite stack. 
* LIR physical registers are mapped to stack slots/variables. 
* Linear Scan allocation overhead (like `LOAD_SPILL` and `STORE_SPILL`) is technically ignored or mapped to standard local variable access, as the VM manages memory virtually.
* LIR Instructions are directly translated into the `Opcode` set defined in the AAYU VM execution loop.

### 2. LLVM Backend
**Purpose:** Maximum optimization, research-grade performance, complex pipeline integrations (Clang/LLC).
**Input:** LIR
**Lowering Strategy:**
* The LLVM Backend translates LIR directly into `LLVM IR`. 
* We leverage `llvmlite` (or similar LLVM bindings).
* LIR `PhysicalRegister`s and Spills dictate precise machine state if needed, though LLVM's internal `regalloc` can be deferred to if we pass virtual registers directly.
* LLVM handles instruction scheduling, advanced loop vectorization, and JIT compilation to native machine code.

### 3. Native Backend
**Purpose:** Direct control over execution without LLVM dependency (e.g. AOT standalone binaries for specific targets like x86_64, ARM64, or RISC-V).
**Input:** LIR + Register Allocation Mapping
**Lowering Strategy:**
* Directly translate LIR into Target Assembly (e.g., AT&T syntax for x86_64).
* The register assignments, stack frames, and spills created in Phase 13.3-13.6 are strictly adhered to.
* `SpillSlotManager` computes precise stack frame sizes in bytes.

## Phase 13.8 Roadmap
The backend splitting happens in Phase 13.8. 
A standard `Backend` interface is introduced:

```python
class Backend:
    def lower(self, func: FunctionLIR) -> Any:
        pass
        
class BytecodeBackend(Backend):
    def lower(self, func: FunctionLIR) -> BytecodeModule:
        ...

class LLVMBackend(Backend):
    def lower(self, func: FunctionLIR) -> llvmlite.ir.Module:
        ...
```
