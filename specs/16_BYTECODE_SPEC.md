Specification: 16_BYTECODE_SPEC.md
Version: 0.1.0
Status:
[x] Draft
[ ] Review
[ ] Frozen
[ ] Deprecated

Owner: Compiler Team
Depends On: 00_ARCHITECTURE
Compiler Version: >=0.5.0
Last Updated: 2026-08-04

---

# AAYU Bytecode Specification (ABS) v1.0

The AAYU Bytecode is a low-level, stack-based instruction set designed to represent AAYU source code. It is designed to be executable by the AAYU Virtual Machine (Native VM).

## Architecture
The AAYU Bytecode architecture relies on:
1. **Header**: Strict metadata ensuring VM backward compatibility.
2. **Instruction Set**: 8-bit opcodes, followed by optional multi-byte operands.
3. **Constant Pool**: A table mapping constant values (Strings, Numbers, etc.) to IDs.
4. **Execution Stack**: A standard LIFO stack used for variable passing, arithmetic, and returns.
5. **Call Stack**: Used for tracking function calls and scope isolation.

## Header Format
Every `.aybc` file begins with a strict header structure:
- `Magic (4 bytes)`: `0x41 0x41 0x59 0x55` (AAYU)
- `Version (2 bytes)`: Overall Bytecode Format Version.
- `Bytecode Version (2 bytes)`: Minor versioning.
- `VM Version (2 bytes)`: Target Virtual Machine version required.
- `Flags (2 bytes)`: Execution and runtime flags.
- `Checksum (4 bytes)`: Data integrity verification hash.
- `Constant Pool Size (4 bytes)`: Length of the embedded constant pool.
- `Instruction Stream Size (4 bytes)`: Length of the executable instructions.

## Instruction Set (Opcodes)

### Stack Operations
- `OP_PUSH_CONST (0x01)`: Pushes a constant from the constant pool onto the stack.
- `OP_POP (0x02)`: Pops the top value off the stack.
- `OP_DUP (0x03)`: Duplicates the top value on the stack.

### Arithmetic Operations
- `OP_ADD (0x10)`: Pops two values, adds them, and pushes the result.
- `OP_SUB (0x11)`: Pops two values, subtracts them, and pushes the result.
- `OP_MUL (0x12)`: Pops two values, multiplies them, and pushes the result.
- `OP_DIV (0x13)`: Pops two values, divides them, and pushes the result.

### Control Flow
- `OP_JMP (0x20)`: Unconditionally jumps to the target offset.
- `OP_JMP_IF_FALSE (0x21)`: Jumps to the target offset if the popped value is false.
- `OP_CALL (0x22)`: Calls a function.
- `OP_RET (0x23)`: Returns from the current function.
- `OP_HALT (0xFF)`: Terminates VM execution cleanly.

### Comparison
- `OP_CMP_EQ (0x26)`: Pushes true if A == B.
- `OP_CMP_NEQ (0x27)`: Pushes true if A != B.
- `OP_CMP_LT (0x29)`: Pushes true if A < B.
- `OP_CMP_GT (0x2A)`: Pushes true if A > B.
- `OP_CMP_LTE (0x2B)`: Pushes true if A <= B.
- `OP_CMP_GTE (0x2C)`: Pushes true if A >= B.

### State and Variables
- `OP_STORE_STATE (0x30)`: Stores top value into state/variable context.
- `OP_LOAD_STATE (0x31)`: Loads state/variable context onto the stack.
- `OP_INIT_STATE (0x32)`: Initializes a new state tracking identifier.

### I/O and Standard Library Calls
- `OP_PRINT (0x51)`: Pops and prints the top value.
- `OP_OP_ASYNC_CALL (0x81)`: Dispatches an asynchronous native function call (e.g. `http`, `fs`).

### Collections and Access
- `OP_CREATE_ARRAY (0x86)`: Initializes a new Array on the stack.
- `OP_GET_LENGTH (0x87)`: Pushes the length of an iterable.
- `OP_LOAD_SUBSCR (0x88)`: Loads the element of a collection by index/key.
- `OP_STORE_SUBSCR (0x89)`: Stores a value into a collection by index/key.
- `OP_BUILD_DICT (0x80)`: Constructs a Dictionary natively.

### Error Handling
- `OP_SETUP_EXCEPT (0x90)`: Registers an exception handler block.
- `OP_POP_EXCEPT (0x91)`: Removes the current exception handler.
- `OP_THROW (0x92)`: Throws the popped value as an exception.
- `OP_RETHROW (0x93)`: Rethrows an uncaught exception.
- `OP_SETUP_FINALLY (0x94)`: Registers a finally block.
- `OP_EXEC_FINALLY (0x95)`: Executes the finally block.

### Component and UI Handling
- `OP_CALL_COMPONENT (0x28)`: Calls a Native UI component builder.
- `OP_BUILD_WIDGET (0x50)`: Constructs a UI Widget node.
- `OP_SET_THEME (0x70)`: Updates the current UI theme state.
