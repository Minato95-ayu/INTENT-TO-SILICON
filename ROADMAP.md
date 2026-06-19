# AAYU Evolution Roadmap

This roadmap outlines the major milestones of AAYU's development as we transition from a deterministic intent compiler into a fully-fledged, compiled bytecode-based language ecosystem.

---

## Current Status Overview
```text
Language Core          100% ✅ [v0.1.0]
Web Framework          100% ✅ [v0.2.0]
Developer Ecosystem    100% ✅ [v0.2.5]
Bytecode & VM          95%  🚧 [v0.3.1]
Native Runtime         0%   🔮 [v0.4.0+]
```

---

## Phase 1: Core Language & Interpreter ✅
- [x] Human-first declarative syntax (Keywords: `number`, `text`, `is`, `show`, `if`, etc.)
- [x] AST-walking recursive interpreter (`interpreter.py`)
- [x] Standard library for math, file I/O, and string operations
- [x] Robust user-friendly compiler error and tracebacks system

## Phase 2: Developer Ecosystem ✅
- [x] **CLI & Package Manager**: `aayu new`, `aayu run`, `aayu install` for dependency management
- [x] **VS Code Extension**: Syntax highlighting, snippet blocks, and configurator
- [x] **LSP Server**: Live diagnostic syntax errors and autocomplete bindings
- [x] **Testing Framework**: Native `test "name" ... end.` discovery and execution runner (`aayu test`)

## Phase 3: Runtime Evolution & VM 🚧
Transitioning from AST-walking to a compiled stack-based Virtual Machine architecture.

- [x] **Phase 3A: IR Design**: Design stack-based AAYU bytecode and AST -> bytecode compiler
- [x] **Phase 3B: Basic VM**: First Stack-VM execution loop (`LOAD_CONST`, `LOAD_NAME`, `STORE_NAME`)
- [x] **Phase 3C: Control Flow**: Comparison opcodes (`EQUAL`, `GREATER`, `LESS`, `NOT`) and relative jumps for `if`/`else` and `while` loops
- [x] **Phase 3D: Call Frames**: Stack frame framing (`CallFrame` contexts) enabling local scope isolation and recursive task execution
- [x] **Phase 3E: Bytecode Serialization**: Recursive JSON serializer/deserializer to output `.ayc` files and execute compiled programs
- [ ] **Phase 3F: Collection VM Support**: VM opcodes/stdlib support for Lists (`BUILD_LIST`, `ADD_TO_LIST`) and Maps (`MAP_GET`, `MAP_SET`)
- [ ] **Phase 3G: Web Runtime Bridge**: Integrate database operations and HTTP servers into the VM

## Phase 4: Native Runtime (Rust/C++) 🔮
Replacing the Python VM engine with a standalone native runtime.
- [ ] AAYU VM Rust Prototype (executing `.ayc` files directly)
- [ ] Native standard library mappings
- [ ] Independent cross-platform binary distribution (fully removing Python dependency)

---

## Key Architectural Decisions

### VM Scope: Language vs. Web Framework Execution
To transition AAYU's full ecosystem (including the Todo App and Library System) to the VM, we must decide how to handle Web/DB constructs:
- **Decision: Standard Library / Built-in Mappings (Option A)**
  - Rather than bloating the VM ISA with monolithic database/HTTP opcodes, the compiler will translate web operations (`serve`, `route`, `find`, `create`) into `CALL_TASK` instructions targeting a built-in standard library.
  - The VM runtime will provide these standard library functions in native code (initially Python, later Rust).
  - This keeps the VM ISA minimal, clean, and highly portable.
