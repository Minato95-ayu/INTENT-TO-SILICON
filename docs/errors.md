# AAYU Error Reference

This document lists the various errors that can occur during the compilation and execution of AAYU programs, along with their causes and examples.

## Compile-Time Errors

### 1. `LexerError`
Occurs when the lexer encounters an unrecognized character or malformed token.
- **Example**: `LexerError: Unrecognized character '$' at line 12`
- **Fix**: Remove the invalid character. AAYU only uses standard characters for syntax.

### 2. `ParserError`
Occurs when the syntax violates the AAYU grammar rules.
- **Example**: `ParserError: Expect '=' after variable name at line 5`
- **Fix**: Ensure proper grammar. Example: `state count = 0` instead of `state count 0`.

### 3. `SemanticError`
Occurs when the code is syntactically valid but logically flawed (e.g., type mismatch, undefined variable).
- **Example**: `SemanticError: Undefined variable 'user_id' at line 20`
- **Fix**: Ensure all variables and states are declared before use.

## Run-Time Errors

### 1. `VMExecutionError`
A general error occurring during bytecode execution.
- **Example**: `VMExecutionError: Stack underflow`
- **Fix**: Usually indicates a compiler bug where bytecode generated unbalanced stack operations.

### 2. `KernelDispatchError`
Occurs when the VM tries to talk to a runtime plugin that is not registered or throws an error.
- **Example**: `KernelDispatchError: Target runtime 'ui' not found.`
- **Fix**: Ensure the required plugin is booted and registered with the kernel.

### 3. `StateRuntimeError`
Occurs during reactive state updates.
- **Example**: `StateRuntimeError: Maximum update depth exceeded`
- **Fix**: You have created an infinite reactive loop (e.g., a widget updates a state, which forces the widget to rebuild and update the state again).

### 4. `StorageRuntimeError`
Occurs during database operations.
- **Example**: `Database error: no such table: Log`
- **Fix**: Ensure you have dispatched a `migrate` or `db_register_entity` action before inserting data into a model.

### 5. `NetworkRuntimeError`
Occurs during HTTP requests.
- **Example**: `Network Error: Connection Refused`
- **Fix**: The remote server is down, or the timeout was too short.
