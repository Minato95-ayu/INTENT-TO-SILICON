<div align="center">
  <img src="https://raw.githubusercontent.com/Minato95-ayu/INTENT-TO-SILICON/main/website/public/aayu-logo.png" width="120" alt="AAYU Logo" />
  <h1>AAYU Programming Language</h1>
  <p><strong>Intent-to-Silicon: The Zero-Dependency, Full-Stack Language built for AI Agents and Vibe Coders.</strong></p>
  <p>
    <a href="https://intent-to-silicon.vercel.app">Website & Docs</a> • 
    <a href="https://intent-to-silicon.vercel.app/tutorial">Masterclass Tutorial</a>
  </p>
</div>

---

## 🚀 Why AI Agents (Cursor, Gemini, Claude) Love AAYU
Modern AI coding agents face three major hurdles with traditional languages: **Dependency Hallucination** (installing packages that don't exist or conflict), **Token Waste** (reading thousands of lines of boilerplate), and **Context Loss** (forgetting the architecture). 
AAYU solves this natively at the compiler level:
1. **Zero External Dependencies:** AAYU has its own built-in SQLite, Web Server, UI Engine, and Math core. An AI Agent will *never* hallucinate a pip install or 
pm i command because AAYU handles everything natively.
2. **Context-Map Auto Generation:** AAYU's compiler automatically shrinks your entire full-stack project into a tiny 200-token .aayu-context.md file. AI reads this instead of your source code, saving up to 80% on context tokens!
3. **Strict Bounds:** Syntax errors are caught by strict end blocks, avoiding pythonic indentation confusion for LLMs.

## 🧘‍♂️ Why Vibe Coders Love AAYU
If you are a student, a solo dev, or just want to build fast without infrastructure headaches, AAYU feels like plain English.
- No irtualenv. No equirements.txt. No package.json.
- Need a database? Just write model User end.
- Need a backend? Just write oute "/api" get respond() end.
- Native static binary (runs on Tails OS, Linux, Mac, Windows without installing any runtime).

## 📝 Hello World

`ayu
app AayuDemo
action main
    let prompt = "Build an AI app"
    print("Welcome to AAYU!")
end
run main
`

## 🏗️ Architecture

AAYU is self-hosted (ayuc.aayu compiles AAYU code) and uses a high-performance **Native Rust Virtual Machine** (ayu-vm). 

`
┌─────────────────────────────────────────┐
│              AAYU Source (.aayu)        │
├──────┬──────┬──────┬──────┬─────────────┤
│Lexer │Parser│ AST  │Seman-│   IR        │
├──────┴──────┴──────┴──────┼─────────────┤
│         HIR → MIR         │  Bytecode   │
├───────────────────────────┼─────────────┤
│     Native Rust VM (.exe) │ Arrays/Dict │
└─────────────────────────────────────────┘
`

## 🧪 Quick Start

`ash
# Clone the repository
git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git
cd INTENT-TO-SILICON/runtime_rs

# Build the ultra-fast Rust VM (Static Binary)
cargo build --release

# Run the REPL or any AAYU file (Runs anywhere, even Tails OS!)
./target/release/aayu-vm
`

## 📄 License
MIT License
