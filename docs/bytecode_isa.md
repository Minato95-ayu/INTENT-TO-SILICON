# AAYU Bytecode ISA (Instruction Set Architecture)

AAYU compiles source code down to a custom Low-Level Intermediate Representation (LIR) and Bytecode. This bytecode is executed by the AAYU Virtual Machine.

## Instruction Format

Each instruction consists of an OpCode and a variable number of operands.
Format: `OpCode [Operand1] [Operand2] ...`

## OpCodes

### Stack Operations
- `LOAD_CONST <index>`: Pushes a constant from the constant pool onto the stack.
- `LOAD_NAME <name>`: Pushes the value of a local variable or global state onto the stack.
- `STORE_NAME <name>`: Pops the stack and stores the value in a local variable or global state.
- `POP`: Pops the top of the stack and discards it.
- `DUP`: Duplicates the top of the stack.

### Arithmetic & Logic
- `ADD`: Pops two values, adds them, pushes the result.
- `SUB`: Pops two values, subtracts them, pushes the result.
- `MUL`: Pops two values, multiplies them, pushes the result.
- `DIV`: Pops two values, divides them, pushes the result.
- `EQ`: Pops two values, checks equality, pushes `True` or `False`.
- `NOT_EQ`: Pops two values, checks inequality, pushes boolean.
- `GT` / `LT`: Greater than / Less than.
- `AND` / `OR` / `NOT`: Boolean logic operations.

### Control Flow
- `JUMP <target>`: Unconditionally jumps to the target instruction index.
- `JUMP_IF_FALSE <target>`: Pops the stack; if `False`, jumps to the target.
- `JUMP_IF_TRUE <target>`: Pops the stack; if `True`, jumps to the target.
- `CALL_FUNCTION <argc>`: Pops `argc` arguments, pops a callable, executes it, and pushes the return value.
- `RETURN`: Pops the stack and returns from the current function frame.

### OS / Native Integration
- `SYSCALL <action>`: Triggers a kernel interaction or stdlib call directly from bytecode, bypassing high-level wrappers.
- `UI_BUILD <type> <props_count>`: Instructs the UI Runtime to build a logical widget node.

## Execution Model
The AAYU VM is a stack-based machine. All operations consume arguments from the operand stack and push their results back to the stack. Function calls allocate a new Call Frame, which has its own local variable table. Global state is routed through the Kernel to the State Runtime.
