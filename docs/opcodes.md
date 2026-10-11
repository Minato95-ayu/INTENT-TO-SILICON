# AAYU Opcode Reference (FROZEN v1.0)

This document provides a comprehensive list of all opcodes used by the AAYU Virtual Machine. 
Each opcode specifies its input operands, output behavior, and stack effect.

## Memory & Variable Operations

### `LOAD_CONST`
- **Operands**: 1 (Value)
- **Description**: Loads a constant value onto the top of the stack.
- **Stack Effect**: `[] → [value]`

### `LOAD_VAR`
- **Operands**: 1 (Variable Name)
- **Description**: Resolves a variable name in the current environment and pushes its value onto the stack.
- **Stack Effect**: `[] → [value]`

### `STORE_VAR`
- **Operands**: 1 (Variable Name)
- **Description**: Pops a value from the stack and stores it in the specified variable.
- **Stack Effect**: `[value] → []`

### `POP`
- **Operands**: 0
- **Description**: Removes the top value from the stack.
- **Stack Effect**: `[value] → []`

---

## Math & Logic Operations

### `ADD`, `SUB`, `MUL`, `DIV`, `MOD`
- **Operands**: 0
- **Description**: Pops two values, performs the mathematical operation, and pushes the result.
- **Stack Effect**: `[val1, val2] → [result]`

### `NEG`
- **Operands**: 0
- **Description**: Negates the top value on the stack.
- **Stack Effect**: `[val] → [-val]`

### `EQ`, `NE`, `LT`, `LE`, `GT`, `GE`
- **Operands**: 0
- **Description**: Pops two values, compares them, and pushes a boolean result.
- **Stack Effect**: `[val1, val2] → [boolean]`

### `NOT`
- **Operands**: 0
- **Description**: Performs a logical NOT on the top value.
- **Stack Effect**: `[boolean] → [boolean]`

---

## Control Flow

### `JUMP`
- **Operands**: 1 (Offset)
- **Description**: Unconditionally jumps by the specified instruction offset.
- **Stack Effect**: `[] → []`

### `JUMP_IF_FALSE`
- **Operands**: 1 (Offset)
- **Description**: Pops the top value. If falsy, jumps by the specified offset.
- **Stack Effect**: `[condition] → []`

### `JUMP_IF_TRUE`
- **Operands**: 1 (Offset)
- **Description**: Pops the top value. If truthy, jumps by the specified offset.
- **Stack Effect**: `[condition] → []`

### `JUMP_BACKWARD`
- **Operands**: 1 (Offset)
- **Description**: Unconditionally jumps backward by the specified offset (used in loops).
- **Stack Effect**: `[] → []`

---

## Functions & Calls

### `CALL`
- **Operands**: 1 (Number of Arguments)
- **Description**: Calls a built-in function or creates a new frame for a user-defined task. Pops arguments from the stack.
- **Stack Effect**: `[arg1, ..., argN] → [result]` (after return)

### `CALL_TASK`
- **Operands**: 1 (Task Name)
- **Description**: Specifically invokes an AAYU task (used primarily in the execution start process).
- **Stack Effect**: `[] → [result]`

### `RETURN`
- **Operands**: 0
- **Description**: Pops the return value from the current frame and pushes it to the caller's frame, then destroys the current frame.
- **Stack Effect**: `[value] → []` (in current frame), `[] → [value]` (in caller frame)

---

## Collections

### `MAKE_LIST`
- **Operands**: 1 (Number of Elements)
- **Description**: Pops N elements from the stack and creates a ListValue containing those elements.
- **Stack Effect**: `[elem1, ..., elemN] → [ListValue]`

### `MAKE_MAP`
- **Operands**: 1 (Number of Key-Value Pairs)
- **Description**: Pops 2N elements (Key, Value, Key, Value...) from the stack and creates a MapValue.
- **Stack Effect**: `[key1, val1, ..., keyN, valN] → [MapValue]`

---

## Database Operations

### `DB_INSERT`
- **Operands**: 0
- **Description**: Pops the model name and a map of fields, then delegates execution to the Storage Runtime. Pushes a NullValue.
- **Stack Effect**: `[model_name, fields_map] → [NullValue]`

### `DB_FIND`
- **Operands**: 0
- **Description**: Pops the model name, executes a query, and pushes a ListValue of the returned records as MapValues.
- **Stack Effect**: `[model_name] → [ListValue(MapValues)]`

### `DB_UPDATE`
- **Operands**: 0
- **Description**: Pops the model name and fields, updates matching records, and pushes a NullValue.
- **Stack Effect**: `[model_name, fields_map] → [NullValue]`

### `DB_DELETE`
- **Operands**: 0
- **Description**: Pops the model name, deletes the records, and pushes a NullValue.
- **Stack Effect**: `[model_name] → [NullValue]`

---

## Exception Handling

### `TRY_BEGIN`
- **Operands**: 1 (Catch Offset)
- **Description**: Pushes an exception handling block onto the VM state. If an exception occurs, jumps to Catch Offset.
- **Stack Effect**: `[] → []`

### `TRY_END`
- **Operands**: 0
- **Description**: Pops the active exception handling block.
- **Stack Effect**: `[] → []`

### `THROW`
- **Operands**: 0
- **Description**: Pops a string value from the stack and raises it as an exception.
- **Stack Effect**: `[error_message] → []`

### `PANIC`
- **Operands**: 0
- **Description**: Similar to THROW but used for fatal VM errors.
- **Stack Effect**: `[error_message] → []`

### `FINALLY_BEGIN`, `FINALLY_END`
- **Operands**: 0
- **Description**: Used to mark the boundaries of a finally block that must execute regardless of exceptions.
- **Stack Effect**: `[] → []`
