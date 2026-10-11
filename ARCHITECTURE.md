# AAYU Intent-to-Silicon System Architecture & Design Specification

> **"Write your intent. AAYU compiles it directly to silicon-ready bytecode."**  
> Complete technical blueprint, directory layout, execution pipeline, and bytecode specification.

---

## 🏛️ 1. Architectural Philosophy

Traditional full-stack software development is fragmented across incompatible ecosystems: Python for ML, Node.js/Express for backend, React/Next.js for frontend, SQL for database, and Docker/Kubernetes for orchestration. This introduces massive dependency trees (1,200+ `node_modules`), token waste for AI coding agents, and complex glue code.

**AAYU solves this with Intent-to-Silicon Architecture:**
1. **Single-File Full-Stack:** Database models, API routes, UI widget trees, and neural AI logic co-exist in one `.aayu` source file.
2. **Zero External Dependencies:** No `npm`, no `pip`, no runtime interpreter. Built-in SQLite, built-in non-blocking TCP web server, built-in UI DOM engine, and built-in tensor math.
3. **Pure Self-Hosted Compiler:** The compiler pipeline (Lexer, Parser, AST, Semantic Analyzer, Bytecode Emitter) is written in 5,661+ lines of pure `.aayu`.
4. **Silicon Virtual Machine (Rust):** The VM and JIT engine are implemented in Rust solely for C-level bare-metal execution speed, NaN-boxed 64-bit values, and sub-millisecond cold starts.

---

## 🗺️ 2. Repository Directory Map

The AAYU repository is structured with clean, modular separation of concerns:

```
INTENT-TO-SILICON/
├── bin/                     # Official Binaries & Seed Bytecode
│   ├── aayu.exe             # Unified AAYU CLI tool (compile & run)
│   ├── aayu-vm.exe          # Standalone Silicon Virtual Machine
│   ├── aayuc.exe            # Standalone Bytecode Compiler
│   └── aayuc.ayc            # Self-hosted seed compiler bytecode (32 KB)
│
├── compiler/                # Pure Self-Hosted AAYU Compiler (.aayu)
│   ├── aayuc.aayu           # Compiler entrypoint & orchestration pipeline
│   ├── lexer.aayu           # LZR Tokenizer & Lexical Scanner
│   ├── parser.aayu          # Recursive descent AST parser
│   ├── analyzer.aayu        # Semantic type-checker & symbol resolver
│   ├── compiler.aayu        # Bytecode generation & jump patcher
│   └── ui_renderer.aayu     # Declarative UI-to-DOM transpiler
│
├── compiler_bootstrap/      # Minimal Rust Bootstrap Seed Compiler
│   ├── Cargo.toml           # Standalone Rust manifest
│   ├── build.rs             # Windows icon & resource embedding
│   └── src/                 # Bootstrap lexer, parser, and emitter
│
├── runtime_rs/              # AAYU Silicon VM & JIT Runtime (Rust)
│   ├── Cargo.toml           # Engine manifest
│   └── src/
│       ├── main.rs          # CLI entrypoint & bytecode file loader
│       ├── vm.rs            # Stack machine, NaN-boxing, opcode dispatch
│       ├── jit.rs           # Just-In-Time native machine code compilation
│       ├── memory.rs        # Zero-copy Heap Manager (Arrays, Dicts, Strings)
│       ├── net.rs           # Multi-threaded TCP HTTP socket engine
│       ├── db.rs            # SQLite & Write-Ahead Log (WAL) storage
│       ├── math.rs          # Tensor math, MatMul, neural activations
│       └── ui.rs            # Declarative Widget-Tree DOM builder
│
├── std/                     # AAYU Standard Libraries
│   ├── http/                # HTTP request & response utilities
│   ├── json/                # Serialization & parsing
│   ├── math/                # Statistical & algebraic routines
│   └── db/                  # ORM & query builder helpers
│
├── examples/                # Production Full-Stack Showcase Projects
│   ├── todo_api.aayu        # Complete TodoMVC CRUD REST API (19 lines)
│   ├── chat_server.aayu     # Real-time WebSocket chat backend
│   ├── url_shortener.aayu   # In-memory Bit.ly clone with SSD persistence
│   ├── auth_system.aayu     # Cryptographic JWT authentication engine
│   ├── neuro_ledger.aayu    # AI-verified PoUW blockchain state machine
│   └── portfolio.aayu       # Interactive Developer Portfolio Web Application
│
├── tests/                   # Automated Verification Test Suite
│   ├── run_tests.ps1        # Automated test harness & timing runner
│   ├── test_01_vars.aayu    # Variables & string operations test
│   ├── test_02_floats.aayu  # IEEE-754 floating point arithmetic test
│   ├── test_03_loops.aayu   # While loops, break, and conditionals test
│   ├── test_04_fibonacci.aayu # 20-iteration Fibonacci loop test (6765)
│   └── test_suite_proof.aayu# Full regression verification proof
│
├── website/                 # Official Next.js Interactive Documentation Portal
│   ├── app/                 # App Router (Docs, Tutorial, Playground, Architecture)
│   └── public/              # Releases, binaries, assets
│
├── vscode-aayu/             # Official VS Code Extension (LSP, Syntax Highlighting)
│
├── ARCHITECTURE.md          # This System Design Specification
├── README.md                # Public GitHub Front-Door & Quick Start
└── LICENSE                  # MIT License
```

---

## ⚡ 3. The Three-Layer Execution Engine

```
┌────────────────────────────────────────────────────────────────────────┐
│                        1. COMPILER LAYER (.aayu)                       │
│  Source Code (.aayu) ➔ Lexer ➔ Parser ➔ AST ➔ Analyzer ➔ Emitter       │
│  Output: Pure Standalone Binary Bytecode (.ayc)                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Executed by
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     2. SILICON VM LAYER (runtime_rs)                   │
│  NanBox 64-bit Stack | Multi-Thread Worker Pool | JIT Machine Code     │
│  Memory Heap Manager | Embedded SQLite WAL     | Non-Blocking TCP      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Rebuilt reproducibly by
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   3. BOOTSTRAP LAYER (compiler_bootstrap)              │
│  Zero-dependency Rust seed compiler for cold reproducible builds       │
└────────────────────────────────────────────────────────────────────────┘
```

### Layer 1: Self-Hosted Compiler Pipeline (`compiler/`)
1. **Lexer (`lexer.aayu`):** Converts `.aayu` source characters into a stream of typed tokens (`KEYWORD`, `IDENTIFIER`, `NUMBER`, `STRING`, `PUNCTUATION`). Skips comments (`#` and `//`) and tracks precise line/column numbers.
2. **Parser (`parser.aayu`):** Implements recursive-descent parsing with operator precedence climbing for expressions. Builds an Abstract Syntax Tree (AST) supporting declarations (`app`, `model`, `route`, `action`, `state`, `page`, `widget`), statements (`let`, `while`, `if/else`, `return`, `assignment`), and expressions (`binary`, `call`, `subscript`, `dict`, `array`).
3. **Semantic Analyzer (`analyzer.aayu`):** Resolves identifiers, tracks lexical scopes, validates type consistency, and flags undeclared symbols before bytecode emission.
4. **Bytecode Emitter (`compiler.aayu`):** Emits variable-length bytecode matching the Silicon VM. Stack operations are emitted as compact 1-byte opcodes; constants and jump targets use 16-bit operands with two-pass jump patching.

### Layer 2: Silicon Virtual Machine (`runtime_rs/`)
1. **NaN-Boxed Value Representation (`NanVal`):**
   Values are represented in a single 64-bit word (`u64`) via IEEE-754 NaN boxing:
   - `Float`: Standard IEEE 754 float (`val < 0x7FF8_0000_0000_0000`)
   - `Integer`: `0x7FF8 | 48-bit signed integer`
   - `Boolean`: `0x7FFA | (0 or 1)`
   - `Null`: `0x7FFB | 0`
   - `String`: `0x7FFC | 48-bit string heap index`
   - `Array`: `0x7FFD | 48-bit heap array reference`
   - `Dictionary`: `0x7FFE | 48-bit heap dictionary reference`
2. **Crash-Resistant Multi-Threaded TCP Server:**
   - Client connections are accepted asynchronously and dispatched to thread worker pools.
   - Each socket sets 5-second `read_timeout` and `write_timeout` to guard against Slowloris attacks.
   - Connections execute within `std::panic::catch_unwind(AssertUnwindSafe(...))` so client panics cannot crash the main server daemon.
3. **Storage & State Machine:**
   - Key-value state is stored in in-memory RAM cache with Write-Ahead Logging (WAL) to disk.
   - Database operations execute via direct compiled AST queries without SQL string concatenation vulnerabilities.

### Layer 3: Reproducibility & Bootstrap Loop (`compiler_bootstrap/`)
A common issue in self-hosted languages is the "chicken-and-egg" bootstrap problem. AAYU solves this with:
1. `compiler_bootstrap/` provides a minimal Rust seed compiler that compiles `compiler/aayuc.aayu` into `bin/aayuc.ayc`.
2. `aayu-vm.exe` runs `bin/aayuc.ayc`, which can then compile `compiler/*.aayu` to produce new compiler bytecode.
3. Anyone cloning the repository can build the seed compiler locally via:
   ```bash
   cargo build --release --manifest-path compiler_bootstrap/Cargo.toml
   ```

---

## 📋 4. Bytecode Instruction Set Architecture (ISA)

AAYU bytecode uses variable-length instructions optimized for rapid dispatch:

| Opcode | Hex | Mnemonic | Operands | Stack Effect | Description |
|---|---|---|---|---|---|
| `0` | `0x00` | `OP_HALT` | None (1B) | `[] -> []` | Terminates VM execution cleanly |
| `1` | `0x01` | `OP_PUSH_CONST` | 2 bytes (3B) | `[] -> [val]` | Pushes constant at 16-bit pool index |
| `2` | `0x02` | `OP_POP` | None (1B) | `[val] -> []` | Discards top stack value |
| `5` | `0x05` | `OP_LOAD_VAR` | 1 byte (2B) | `[] -> [val]` | Pushes local variable from slot index (0..255) |
| `6` | `0x06` | `OP_STORE_VAR` | 1 byte (2B) | `[val] -> []` | Stores top value to local variable slot |
| `16` | `0x10` | `OP_ADD` | None (1B) | `[a, b] -> [a + b]` | Polymorphic addition (Int, Float, String concat, Array merge) |
| `17` | `0x11` | `OP_SUB` | None (1B) | `[a, b] -> [a - b]` | Numeric subtraction (Int, Float) |
| `18` | `0x12` | `OP_MUL` | None (1B) | `[a, b] -> [a * b]` | Numeric multiplication (Int, Float) |
| `19` | `0x13` | `OP_DIV` | None (1B) | `[a, b] -> [a / b]` | Numeric division with zero-check (Int, Float) |
| `32` | `0x20` | `OP_JMP` | 2 bytes (3B) | `[] -> []` | Unconditional jump to 16-bit offset |
| `33` | `0x21` | `OP_JMP_IF_FALSE` | 2 bytes (3B) | `[cond] -> []` | Jumps to 16-bit offset if condition is false |
| `34` | `0x22` | `OP_CALL` | 2 bytes (3B) | `[func, args...] -> [ret]` | Invokes native or user action with argument count |
| `35` | `0x23` | `OP_RET` | None (1B) | `[ret] -> [ret]` | Returns from current action frame |
| `38` | `0x26` | `OP_CMP_EQ` | None (1B) | `[a, b] -> [bool]` | Pushes true if `a == b` |
| `39` | `0x27` | `OP_CMP_NEQ` | None (1B) | `[a, b] -> [bool]` | Pushes true if `a != b` |
| `41` | `0x29` | `OP_CMP_LT` | None (1B) | `[a, b] -> [bool]` | Pushes true if `a < b` |
| `42` | `0x2A` | `OP_CMP_GT` | None (1B) | `[a, b] -> [bool]` | Pushes true if `a > b` |
| `43` | `0x2B` | `OP_CMP_LTE` | None (1B) | `[a, b] -> [bool]` | Pushes true if `a <= b` |
| `44` | `0x2C` | `OP_CMP_GTE` | None (1B) | `[a, b] -> [bool]` | Pushes true if `a >= b` |
| `48` | `0x30` | `OP_STORE_STATE` | 2 bytes (3B) | `[val] -> []` | Persists key-value state to RAM & WAL |
| `49` | `0x31` | `OP_LOAD_STATE` | 2 bytes (3B) | `[] -> [val]` | Retrieves key-value state from RAM |
| `81` | `0x51` | `OP_PRINT` | None (1B) | `[val] -> []` | Prints value with newline |
| `128`| `0x80` | `OP_BUILD_DICT` | 2 bytes (3B) | `[k1, v1...] -> [dict]` | Allocates heap dictionary with N pairs |
| `134`| `0x86` | `OP_CREATE_ARRAY`| 2 bytes (3B) | `[e1, e2...] -> [arr]` | Allocates heap array with N elements |
| `136`| `0x88` | `OP_LOAD_SUBSCR` | None (1B) | `[obj, key] -> [val]` | Array index or Dict key lookup |
| `137`| `0x89` | `OP_STORE_SUBSCR`| None (1B) | `[obj, key, val] -> []`| Array or Dict subscript mutation |
| `200`| `0xC8` | `OP_RENDER_PAGE` | 2 bytes (3B) | `[] -> []` | Emits compiled HTML component to DOM |

---

## 🔒 5. Security & Invariant Proofs

1. **Zero Supply-Chain Vulnerabilities:**
   By eliminating `node_modules` and Python packages, AAYU eliminates package-squatting, transitive dependency hijacking, and poisoned post-install scripts.
2. **No Raw Pointer Dereferencing:**
   All heap allocations occur in indexed vectors inside `MemoryManager`. No raw pointers are exposed to user bytecode.
3. **Structured Query Integrity:**
   Database models are compiled to AST validation structures. Injection via string concatenation is structurally impossible.
4. **Resilient HTTP Engine:**
   Socket timeouts + worker thread panic isolation guarantee that single-client malformed requests never disrupt overall server availability.

---

## 🚀 6. Verification & Test Suite

To run the automated regression suite:
```powershell
powershell -ExecutionPolicy Bypass -File tests\run_tests.ps1
```
Results verify compiler correctness, NaN-box decoding, arithmetic loops, and control flow in **< 40ms**.
