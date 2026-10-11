# AAYU Bytecode ISA (v1)

Date: 2026-06-28
Status: Frozen

The AAYU Virtual Machine uses a stack-based Instruction Set Architecture (ISA). This document defines the frozen base instructions. All future compilers targeting `.ayc` must emit these instructions, and all future VMs must support them to guarantee backward compatibility.

## Memory Model
- **Operand Stack**: Used for intermediate values.
- **Environment**: A mapping of variable names to values, supporting lexical scoping (closures).
- **Program Counter (PC)**: Points to the next instruction in the bytecode array.

## Instructions

### Stack Manipulation & Variables
- `LOAD_CONST <value>`: Pushes a constant value onto the stack.
- `LOAD_VAR <name>`: Looks up the variable `<name>` in the environment and pushes its value.
- `STORE_VAR <name>`: Pops a value from the stack and stores it in the environment as `<name>`.

### Control Flow
- `JUMP <offset>`: Unconditionally shifts the PC by `<offset>` instructions.
- `JUMP_IF_FALSE <offset>`: Pops a value from the stack. If it evaluates to `false` (or 0), shifts the PC by `<offset>`.

### Functions & Tasks
- `CALL <name> <arg_count>`: Pops `<arg_count>` arguments from the stack, looks up `<name>`, and executes the function/task in a new scope.
- `RETURN`: Returns from the current function call, pushing the return value (or None) onto the caller's stack.

### Arithmetic
*(Pops right operand, pops left operand, computes, pushes result)*
- `ADD`
- `SUB`
- `MUL`
- `DIV`
- `MOD`

### Logic & Comparison
*(Pops right operand, pops left operand, computes, pushes result)*
- `EQ`: Equal
- `NOT_EQ`: Not equal
- `LT`: Less than
- `GT`: Greater than
- `LTE`: Less than or equal
- `GTE`: Greater than or equal
- `AND`: Logical AND
- `OR`: Logical OR
- `NOT`: Logical NOT (pops one operand)

### Data Structures
- `MAKE_LIST <size>`: Pops `<size>` elements, creates a list, and pushes it.
- `MAKE_MAP <size>`: Pops `<size>` key-value pairs, creates a map, and pushes it.
- `LIST_APPEND`: Pops value, pops list, appends value, pushes list.
- `MAP_SET`: Pops value, pops key, pops map, sets key=value, pushes map.
- `MAP_GET`: Pops key, pops map, retrieves value, pushes value.
