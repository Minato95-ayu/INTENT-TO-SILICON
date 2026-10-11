# 🚀 THE AAYU BOOTSTRAP GUIDE (Killing Python Forever)

Welcome to the final phase of AAYU's architecture. This document explains how you will permanently transition AAYU from a Python-dependent interpreter to a **100% Native, Zero-Dependency, Rust-Powered Virtual Machine**.

By the end of this process, the Python codebase will be deleted forever, and AAYU will be fully **Self-Hosted** (Compiler written in AAYU, Engine written in Rust).

---

## 🛠️ Prerequisites
You need the Rust compiler installed on your PC to build the engine.
1. Download and install Rust from [rustup.rs](https://rustup.rs/)
2. Open a new terminal and verify: `cargo --version`

---

## ⚔️ Phase 1: Build the Native Engine (Rust VM)
We need to forge the C-level performance engine that will run AAYU bytecode.

1. Open your terminal in the root of the `INTENT-TO-SILICON` project.
2. Navigate to the Rust VM folder:
   ```bash
   cd runtime_rs
   ```
3. Build the highly-optimized native executable:
   ```bash
   cargo build --release
   ```
4. Copy the newly forged engine to your root folder:
   ```bash
   copy target\release\aayu-vm.exe ..\
   cd ..
   ```
*You now hold the `aayu-vm.exe` — the 0.01s Execution Engine.*

---

## 🧬 Phase 2: Compile the AAYU Compiler
We must use the old Python compiler *one last time* to translate the new AAYU Compiler (`aayuc.aayu`) into binary bytecode.

1. Run the legacy Python compiler to generate the bytecode:
   ```bash
   python -m tools.cli compile src/self_hosted/aayuc.aayu
   ```
2. You will now see a file named `aayuc.aybc`. 
*This file is your entire Compiler Logic (Lexer + Parser + Emitter) converted to raw, machine-readable binary.*

---

## 🔥 Phase 3: The Great Python Purge (Zero Dependency Achieved)
The native engine is ready. The native bytecode compiler is ready. Python is now obsolete.

Run these commands to permanently destroy the old architecture:
```bash
# Delete the old Python Runtime and Compiler
rmdir /s /q compiler
rmdir /s /q runtime
rmdir /s /q tools

# Delete old executable and configs
rmdir /s /q dist
rmdir /s /q build
del aayu.spec
del pyproject.toml
```
**Congratulations! AAYU is now 100% Python-Free and Zero-Dependency.**

---

## ⚡ Phase 4: Running AAYU Code Natively
How do you run code now that Python is gone? You use the Engine to run the Compiler, which compiles your code!

To run any AAYU file (e.g., `hello.aayu`), the architecture flows like this:
```bash
# 1. The Rust VM runs the AAYU Compiler to generate bytecode for hello.aayu
aayu-vm.exe aayuc.aybc hello.aayu

# 2. The Rust VM runs the newly generated hello.aybc
aayu-vm.exe hello.aybc
```

*Welcome to God-Level Speed. Welcome to True Self-Hosting.*
