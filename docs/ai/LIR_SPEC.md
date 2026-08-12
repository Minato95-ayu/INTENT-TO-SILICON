# AAYU Linear IR (LIR) Specification

**Status:** Draft
**Version:** 1.0

## Overview
The AAYU Linear Intermediate Representation (LIR) is a low-level, machine-independent, linear instruction sequence that sits between the Optimizer (SSA MIR) and the Target Backends (Bytecode, LLVM, Native). 

Unlike MIR, which relies on SSA form and `PHI` nodes, LIR has no `PHI` nodes and maps closely to a traditional register-based or stack-based machine.

## Characteristics of LIR

1. **No PHI Nodes**: All `PHI` nodes are eliminated by inserting explicit `LIR_MOVE` instructions along incoming edges (with critical edge splitting as necessary).
2. **Canonical Opcode Set**: `LIR_` prefixed instructions prevent accidental sharing or conflation with MIR nodes.
3. **Physical Registers**: While MIR operates on infinite virtual registers, LIR operates on `PhysicalRegister`s mapped by the Linear Scan allocator, and spills are explicit via `LIR_LOAD_SPILL` and `LIR_STORE_SPILL`.
4. **Machine Independent**: LIR instructions don't care if the target is x86, ARM, or Bytecode. It provides a common ground for the backend to lower from.

## Instruction Set Architecture (ISA)

### Memory Operations
* `LIR_LOAD_CONST dest, val`: Load a literal.
* `LIR_LOAD_LOCAL dest, slot`: Load a local variable (usually bypassed by register allocation, reserved for unpromotable locals).
* `LIR_STORE_LOCAL slot, src`: Store to a local variable.
* `LIR_LOAD_GLOBAL dest, name`: Load from a global state variable.
* `LIR_STORE_GLOBAL name, src`: Store to a global state variable.
* `LIR_LOAD_SPILL dest, slot`: Reload a spilled register from a stack slot.
* `LIR_STORE_SPILL slot, src`: Spill a register to a stack slot.

### Arithmetic & Logic
* `LIR_ADD dest, src1, src2`
* `LIR_SUB dest, src1, src2`
* `LIR_MUL dest, src1, src2`
* `LIR_DIV dest, src1, src2`
* `LIR_CMP_EQ dest, src1, src2`
* `LIR_CMP_GT dest, src1, src2`
* `LIR_CMP_LT dest, src1, src2`

### Control Flow
* `LIR_JUMP target_block`
* `LIR_BRANCH cond, true_block, false_block`
* `LIR_CALL dest, target, [args...]`
* `LIR_RET val`

### Data Movement
* `LIR_MOVE dest, src`: Represents a copy of data between two physical registers. Often coalesced.

## PHI Elimination
During LIR generation, `PHI` nodes in MIR are dissolved:
```
# MIR
B3:
  r3 = PHI (B1: r1), (B2: r2)
```
becomes:
```
# LIR
B1:
  ...
  LIR_MOVE p3, p1
  LIR_JUMP B3
B2:
  ...
  LIR_MOVE p3, p2
  LIR_JUMP B3
```
If an edge between `B1` and `B3` is critical, it is split via a new block `B1_split`.
