# 0002. Bytecode Instruction Set Architecture (ISA) Freeze

Date: 2026-06-28

## Status
Accepted

## Context
The AAYU Virtual Machine uses a custom bytecode ISA to execute `.aayu` source code. In the early stages, instructions were added, modified, or removed frequently. As AAYU matures and we plan for long-term backwards compatibility (e.g. running compiled `.ayc` files on future versions of the engine), we need a stable ISA.

## Decision
We freeze the core AAYU Bytecode ISA. Any additions or modifications to the instruction set must now undergo formal review and be documented in the `specs/language/v1/bytecode.md` specification.
The frozen base instruction set includes standard stack VM operations:
- `LOAD_CONST`
- `LOAD_VAR`
- `STORE_VAR`
- `CALL`
- `RETURN`
- `JUMP`
- `JUMP_IF_FALSE`
- Arithmetic: `ADD`, `SUB`, `MUL`, `DIV`, `MOD`
- Logic/Comparison: `EQ`, `NOT_EQ`, `LT`, `GT`, `LTE`, `GTE`, `AND`, `OR`, `NOT`
- Collections: `MAKE_LIST`, `MAKE_MAP`, `LIST_APPEND`, `MAP_SET`, `MAP_GET`

## Consequences
- **Positive:** A stable foundation for the VM and Compiler. Ensures future backwards compatibility of `.ayc` files.
- **Negative:** Adding new language features that require new runtime primitives will involve more process and careful design to ensure the ISA remains clean.
