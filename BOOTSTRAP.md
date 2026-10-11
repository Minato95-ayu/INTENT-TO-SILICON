# 🚀 THE AAYU BOOTSTRAP GUIDE

Welcome to the self-hosted architecture of AAYU. The AAYU ecosystem operates with **Zero Python Dependencies**:
- **Self-Hosted Compiler**: Written in pure AAYU (`compiler/*.aayu`).
- **High-Performance VM**: Written in Rust (`runtime_rs/`) for C-level execution speed, Nan-tagging, and deterministic memory management.
- **Prebuilt Seed Toolchain**: Available out-of-the-box in `bin/` (`aayuc.exe`, `aayu-vm.exe`, `bin/aayuc.ayc`).

---

## 🛠️ Toolchain Layout

```
INTENT-TO-SILICON/
├── bin/
│   ├── aayuc.exe        # Native seed compiler
│   ├── aayu-vm.exe      # Native Rust VM runtime
│   └── aayuc.ayc        # Compiled self-hosted compiler bytecode
├── compiler/            # 100% Pure AAYU self-hosted compiler source
│   ├── aayuc.aayu       # Main compiler driver
│   ├── lexer.aayu       # Lexer & tokenizer
│   ├── parser.aayu      # Recursive descent parser
│   ├── analyzer.aayu    # Semantic analyzer & type checker
│   ├── compiler.aayu    # Bytecode generator
│   └── c_backend.aayu   # Native C codegen backend
└── runtime_rs/          # Pure Rust Virtual Machine & JIT
    └── src/
        ├── vm.rs        # Stack-based Nan-tagged VM engine
        ├── opcodes.rs   # Type-safe opcode contracts
        ├── memory.rs    # GC & dynamic memory manager
        ├── net.rs       # Multi-threaded server with panic isolation
        └── db.rs        # RAM-first SSD-backed WAL engine
```

---

## ⚡ Quick Start: Running AAYU Code Natively

You do not need Python or any external package manager to run AAYU code:

### 1. Compile an AAYU file to bytecode (`.ayc`):
```powershell
.\bin\aayuc.exe hello.aayu -o hello.ayc
```

### 2. Execute bytecode on the AAYU VM:
```powershell
.\bin\aayu-vm.exe hello.ayc
```

---

## 🧬 Rebuilding the Self-Hosted Toolchain

### Step 1: Rebuild the Rust VM from source
If you have modified `runtime_rs/`:
```powershell
cd runtime_rs
cargo build --release
copy target\release\aayu-vm.exe ..\bin\aayu-vm.exe -Force
cd ..
```

### Step 2: Recompile the Self-Hosted Compiler Bytecode
Compile the self-hosted compiler (`compiler/aayuc.aayu`) into binary bytecode using the seed compiler:
```powershell
.\bin\aayuc.exe compiler\aayuc.aayu -o bin\aayuc.ayc
```

### Step 3: Verify the Self-Hosted Compiler on the VM
Execute the compiler bytecode directly on the VM:
```powershell
.\bin\aayu-vm.exe bin\aayuc.ayc
```

---

## 🛡️ Security & Concurrency Guarantees

1. **Memory Safety**:
   - `runtime_rs/src/opcodes.rs` enforces safe pattern matching with safe fallbacks and zero undefined behavior.
2. **Panic Isolation**:
   - `runtime_rs/src/net.rs` and the VM server engine execute connection workers with `std::panic::catch_unwind`, isolating panics from taking down the server.
3. **Deterministic Performance**:
   - Tested under ApacheBench at **36,784 req/sec** with 1.36 ms latency and 2.4 MB RSS RAM.
