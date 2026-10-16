<p align="center">
  <img src="website/public/aayu-logo.png" alt="AAYU Logo" width="180" />
</p>

<h1 align="center">AAYU — Intent to Silicon</h1>

<p align="center">
  <strong>The programming language where your intent becomes silicon-ready bytecode.</strong><br/>
  Single-file full-stack · Built-in Database · Built-in Server · Built-in UI · AI/ML Native
</p>

<p align="center">
  <a href="https://github.com/Minato95-ayu/INTENT-TO-SILICON/releases"><img src="https://img.shields.io/badge/version-v1.1.0-purple?style=flat-square" alt="Version"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Proprietary-blue?style=flat-square" alt="License"/></a>
  <a href="https://aayulang.com"><img src="https://img.shields.io/badge/website-aayulang.com-emerald?style=flat-square" alt="Website"/></a>
</p>

---

## What is AAYU?

AAYU is a **single-file full-stack programming language** built for the AI-agent era. One `.aayu` file contains your database models, API routes, frontend UI, and business logic — zero external dependencies, zero config files.

```aayu
app TodoApp

model Task { title: String, done: Bool }

route "/api/tasks"
  get
    respond Task.all()
  end
end

Page Home
  Column
    Text("My Tasks")
    Button("Add Task", onClick: addTask)
  end
end

run Home
```

> **Python** needs Flask + SQLAlchemy + React + npm = 15 files, 500 lines.
> **AAYU** does the same in **1 file, 20 lines.**

---

## 🌐 Flagship Showcase: AAYU Silicon Enterprise Portal

Experience the world's first single-file full-stack enterprise platform written in 100% pure AAYU:

- 🚀 **Live Interactive Demo:** [https://trailers-keeping-column-diagnosis.trycloudflare.com/](https://trailers-keeping-column-diagnosis.trycloudflare.com/) *(Zero install needed — run it in your browser!)*
- 📄 **Direct Source Code:** [examples/enterprise_auth_portal.aayu](https://github.com/Minato95-ayu/INTENT-TO-SILICON/blob/main/examples/enterprise_auth_portal.aayu) *(Direct link to the exact single-file source code)*
- 💻 **Run Locally in 1 Command:**
  ```powershell
  aayu run examples/enterprise_auth_portal.aayu --web --port 8080
  ```

### What's Inside:
1. **🌊 7-Layer Liquid Data (`std/liquid.aayu`):** Molecular sharding with SHA-256 checkpoints and $O(1)$ prefix-suffix phone cache routing. Bit tampering causes instant tamper-freeze.
2. **🐜 Ant-Man Vector Media (`std/media.aayu`):** Converts 5 MB photos to 2.4 KB SVG vector math coordinates, saving **99.85%** storage with infinite 100x zoom clarity.
3. **⚡ In-Memory WAL Database (`aayudb_wal.json`):** Microsecond RAM operations crash-persisted to disk.
4. **🛡️ 2FA + OTP Zero-Knowledge Auth:** Real two-step verification and biometrics without third-party services.

---

## Quick Start

```powershell
# Clone & build
git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git
cd INTENT-TO-SILICON
cargo build --release --manifest-path runtime_rs/Cargo.toml
cargo build --release --manifest-path compiler_bootstrap/Cargo.toml

# Run
bin/aayu-vm run hello.aayu
```

---

## Architecture

```
 .aayu Source
    │
    ▼
┌─────────┐   ┌────────┐   ┌─────┐   ┌─────┐   ┌─────┐   ┌──────────┐   ┌───────────┐
│  Lexer   │──▸│ Parser │──▸│ AST │──▸│ HIR │──▸│ MIR │──▸│ Bytecode │──▸│  Rust VM  │
└─────────┘   └────────┘   └─────┘   └─────┘   └─────┘   └──────────┘   └───────────┘
  Pure AAYU     Pure AAYU   Pure AAYU                        .ayc file     Stack-based
```

- **Compiler pipeline** → 100% pure AAYU (self-hosted)
- **VM & JIT** → Rust (for C-level execution speed)
- **Memory** → Union-Style NaN-Boxing + Mark-and-Sweep GC

---

## Project Status

| Component | Status | Language |
|-----------|--------|----------|
| Compiler (Lexer/Parser/AST) | ✅ Working | Pure AAYU |
| Bytecode VM | ✅ Working | Rust |
| Database/Storage | ✅ Working | AAYU + Rust |
| HTTP Server/Routes | ✅ Working | AAYU + Rust |
| CLI Tools | ✅ Working | AAYU |
| Frontend UI | 🔨 In Progress | AAYU |
| AI/ML stdlib | 🔨 In Progress | AAYU |
| Mobile IDE (Android) | ✅ Released | TypeScript |
| VS Code Extension | ✅ Released | TypeScript |

---

## Downloads

| Platform | Link |
|----------|------|
| 🖥️ Windows Installer | [Download .exe](https://aayulang.com/download) |
| 📱 Android Mobile IDE | [Download .zip](https://aayulang.com/downloads/aayu-mobile-ide.zip) |
| 🧩 VS Code Extension | [Download .vsix](https://aayulang.com/downloads/aayu-1.2.0.vsix) |
| 📖 Master Handbook (21 Ch) | [Download PDF](https://aayulang.com/aayu-handbook.pdf) |
| 🐧 Linux/macOS | [Install Script](https://aayulang.com/downloads/aayu-linux.sh) |

---

## Created By

**Ayush Ghrit Kaushik** · [@Minato95-ayu](https://github.com/Minato95-ayu)

> *"Modern programming is bloated. AAYU is the reset button — the first language designed for AI Agents to build silicon-ready empires."*

---

## Links

- [Website](https://aayulang.com) · [Tutorial](https://aayulang.com/tutorial) · [Roadmap](ROADMAP.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md)
