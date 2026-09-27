<div align="center">
  <img src="https://raw.githubusercontent.com/Minato95-ayu/INTENT-TO-SILICON/main/website/public/aayu-logo.png" width="120" alt="AAYU Logo" />
  <h1>AAYU Programming Language</h1>
  <p><strong>Intent-to-Silicon: The Zero-Dependency, Full-Stack Programming Language.</strong></p>
  <p>
    <a href="https://intent-to-silicon.vercel.app">Website & Docs</a> • 
    <a href="https://intent-to-silicon.vercel.app/tutorial">Masterclass Tutorial</a>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Version-1.1.0-blue?style=flat-square" alt="Version" />
    <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License" />
    <img src="https://img.shields.io/badge/Build-Passing-brightgreen?style=flat-square" alt="Build" />
    <img src="https://img.shields.io/badge/Creator-Ayush_Ghrit_Kaushik-purple?style=flat-square" alt="Creator" />
  </p>
</div>

---

## ⚡ What is AAYU?

**AAYU** (created by Ayush Ghrit Kaushik) is a revolutionary programming language designed to eliminate modern development bloat. Instead of managing complex stacks (React + Node + SQL + PyTorch), AAYU gives you a complete, high-performance ecosystem in a **single `.aayu` file**.

AAYU compiles your intent directly into optimized bytecode executed by its custom Stack-based Virtual Machine.

### 🔥 Core Capabilities (Built-in)
- 🗄️ **Zero-Config Database:** Native SQLite engine with auto-migrations.
- 🌐 **ASGI Web Server:** High-speed HTTP server built directly into the runtime (`--web`).
- 🎨 **Declarative UI:** Native widget tree (Page, Column, Button) rendering to HTML/CSS.
- 🧠 **Native AI/ML Engine:** Train K-Means and Neural Nets *without* external dependencies.
- 🎮 **Game Engine:** Render 2D canvas, sprites, and physics natively.
- 📊 **Data Visualization:** Built-in charting and graphing widgets.

---

## 🏗️ Architecture & Compiler Pipeline

AAYU is not a wrapper; it features a genuine **7-stage compiler pipeline**:

```mermaid
graph LR
  A[Source .aayu] --> B(Lexer)
  B --> C(Parser/AST)
  C --> D(Semantic)
  D --> E(HIR)
  E --> F(MIR)
  F --> G(LIR)
  G --> H(Bytecode)
  H --> I[(AAYU Stack VM)]
```

*The AAYU Stack VM features a Mark-and-Sweep Garbage Collector (GC), strict type enforcement, and optimized execution loops.*

---

## 🚀 Quick Start

### 1. Install AAYU
*Requires Python 3.12+ (Reference VM implementation prior to Native Rust port).*
```bash
git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git
cd INTENT-TO-SILICON
pip install -e .
```

### 2. Run a Program
Create `hello.aayu`:
```aayu
app HelloWorld

action main
    print("Welcome to AAYU!")
end

run main
```
Execute it:
```bash
aayu run hello.aayu
```

### 3. Launch a Full-Stack Web App
```bash
aayu run myapp.aayu --web
```
*Your app is now live at `http://localhost:3000` with the built-in ASGI server.*

---

## 🛡️ Reliability & Benchmarks

AAYU operates on a **Zero-Error Tolerance** law. 
- **100% Test Coverage:** Every compiler stage, IR transformation, and VM opcode is rigorously tested.
- **Proofs:** You can find verifiable test proofs and benchmarks on our [Official Website](https://intent-to-silicon.vercel.app).
- **Production-Ready Core:** Strict error handling, deterministic execution, and memory safety.

---

## ⚖️ License & Intellectual Property

Copyright (c) 2024-2026 **Ayush Ghrit Kaushik**. All rights reserved.

The AAYU compiler, bytecode architecture, and standard library concepts are original works by Ayush Ghrit Kaushik. Deep metadata watermarks are embedded within the compiler core to protect against unauthorized cloning or IP theft.

*For enterprise usage or core contributions, please refer to `CONTRIBUTING.md`.*