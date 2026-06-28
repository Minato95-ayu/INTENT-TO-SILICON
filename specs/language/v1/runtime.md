# AAYU Runtime (v1)

Date: 2026-06-28
Status: In Progress

The AAYU Runtime executes the generated AAYU Bytecode (`.ayc`). It is designed to be highly portable and secure, isolating project code from system resources.

## Core Concepts
- **Environment Context**: A mapping of variable scopes. 
- **Call Stack**: For managing function invocations.
- **Built-ins**: A native interface bridging `.aayu` logic to the underlying OS (e.g. `show`, HTTP routing, SQLite calls).

## Runtime Types
1. **Numbers**: 64-bit floating point.
2. **Text**: UTF-8 Strings.
3. **Booleans**: True/False representations.
4. **Lists**: Dynamically sized arrays.
5. **Maps**: Key-value pairs (dictionaries).
6. **Records**: Strongly typed struct instances.

## Execution Model
The Runtime must implement an infinite loop that reads the bytecode array and executes instructions linearly, manipulating the Operand Stack, until `RETURN` is encountered on the main block or EOF is reached.
