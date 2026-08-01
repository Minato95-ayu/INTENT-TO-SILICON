# AAYU Instruction Set Architecture (ISA)

This document freezes the bytecode contract between the AAYU Compiler and the AAYU VM.
Any changes to this ISA require synchronized updates in both `compiler/bytecode/` and `runtime/vm/`.

## 1. Stack Operations
- `LOAD_CONST <index>`: Push a constant from the constant pool onto the stack.
- `LOAD_VAR <name>`: Push a local/global variable onto the stack.
- `STORE_VAR <name>`: Pop top of stack and store it in a variable.
- `POP`: Pop and discard the top of the stack.

## 1.5 Array & Map Operations
- `CREATE_ARRAY <size>`: Pop `<size>` elements, construct an array, and push it.
- `GET_LENGTH`: Pop array/string/map, push its length.
- `LOAD_SUBSCR`: Pop index, pop array/map. Push `array[index]`.
- `STORE_SUBSCR`: Pop index, pop array/map, pop value. Set `array[index] = value`.

## 2. Control Flow
- `JUMP <offset>`: Unconditional jump relative to the current instruction pointer.
- `JUMP_IF_FALSE <offset>`: Pop the top of the stack. If false, jump by offset.
- `JUMP_IF_TRUE <offset>`: Pop the top of the stack. If true, jump by offset.
- `CALL <args_count>`: Call a function. The function and its arguments must be on the stack.
- `RETURN`: Return from the current function with the value on top of the stack.

## 3. UI Construction (Reactive Rendering)
- `BUILD_PAGE <id>`: Create a new Page widget.
- `BUILD_LAYOUT <id> <type>`: Create a Layout widget (Row/Column/Stack).
- `BUILD_TEXT <id>`: Create a Text widget.
- `BUILD_BUTTON <id>`: Create a Button widget.
- `BUILD_INPUT <id>`: Create an Input widget.
- `ADD_CHILD`: Pop a child widget and a parent widget from the stack, add child to parent, push parent back.
- `SET_PROP <key>`: Pop a value and a widget from the stack. Set widget.props[key] = value.

## 4. State Management
- `STATE_INIT <key>`: Initialize a global/scoped reactive state variable.
- `STATE_GET <key>`: Push the value of a reactive state variable onto the stack.
- `STATE_SET <key>`: Pop a value and set it to a reactive state variable. Triggers the reactive dependency graph.

## 5. Storage (Models)
- `MODEL_INSERT <model_name>`: Insert a record into the database.
- `MODEL_QUERY <model_name>`: Query records from the database.
- `MODEL_DELETE <model_name>`: Delete records from the database.

## 6. Networking & Web
- `HTTP_REQUEST <method> <url>`: Perform an async HTTP request.
- `SERVER_START <port>`: Start the web server.
- `ROUTE_BIND <path>`: Bind a function (top of stack) to a web route.

## 7. Execution Infrastructure
- `EVENT_BIND <topic>`: Bind a function (top of stack) to an EventBus topic.
- `EVENT_EMIT <topic>`: Emit an event to the EventBus.
- `TASK_CREATE`: Spawn a background task in the Scheduler.
- `TASK_WAIT`: Yield execution until a task completes.

## Instruction Format

Each instruction is serialized as a tuple or struct:
`(OPCODE, ARG1, ARG2)`

Example:
`(OPCODE.LOAD_CONST, 0, None)`
`(OPCODE.BUILD_TEXT, "text_1", None)`
