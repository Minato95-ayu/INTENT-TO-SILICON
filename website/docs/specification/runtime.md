# Runtime Environment

The AAYU Runtime is the execution environment for AAYU Bytecode (`.ayc` files). While AAYU is primarily designed as a generation platform (compiling down to target languages like Rust, Python, or React), it also includes a high-performance native runtime for immediate execution, testing, and edge deployments.

## The AAYU Virtual Machine

The current iteration of the AAYU Runtime is a stack-based Virtual Machine.

When a developer runs `aayu run file.aayu`:
1. The compiler generates bytecode instructions (e.g., `LOAD_CONST`, `STORE_FAST`, `CALL_FUNCTION`).
2. The VM executes these instructions sequentially, manipulating an evaluation stack and an environment (scope) map.

## Core Runtime Components

### Native Memory Management
The AAYU runtime handles variable scoping, garbage collection, and memory allocation automatically. Variables are strictly scoped to the blocks (like `task` or `if`) in which they are defined.

### Database Engine Integration
AAYU is unique in that its runtime natively embeds a database engine (currently SQLite in the prototype). The runtime intercepts bytecode instructions related to database operations (`create`, `find`, `update`, `delete`) and automatically translates them into optimal SQL queries against the local data store.

There is no need to set up ORMs, connection pools, or database drivers.

### Built-in HTTP Server
Similarly, the runtime embeds an HTTP server. When the `serve on` instruction is reached, the VM binds to the specified port and begins listening for requests, routing them automatically to the appropriate AAYU `task` blocks in memory.

## Future: The Rust Runtime (Sprint 24)

To maximize performance, security, and portability, the production version of the AAYU Native Runtime will be written entirely in Rust (`aayu-rs`). This will provide a lightweight, incredibly fast execution environment for `.ayc` binaries, suitable for cloud deployments and embedded systems.
