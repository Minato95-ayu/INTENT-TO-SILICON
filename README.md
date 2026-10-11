<div align="center">
  <h1>AAYU Programming Language</h1>
  <p><strong>Intent-to-Silicon: The Zero-Dependency, Full-Stack Language built for AI Agents and Vibe Coders.</strong></p>
  <p>
    <a href="https://intent-to-silicon.vercel.app">Website & Docs</a> | 
    <a href="https://intent-to-silicon.vercel.app/tutorial">Masterclass Tutorial</a> |
    <a href="https://intent-to-silicon.vercel.app/playground">Interactive Playground</a>
  </p>
</div>

---

## 🤖 Why AI Agents (Cursor, Gemini, Claude) Love AAYU
Modern AI coding agents face three major hurdles with traditional languages: **Dependency Hallucination** (installing packages that don't exist or conflict), **Token Waste** (reading thousands of lines of boilerplate), and **Context Loss** (forgetting the architecture). 
AAYU solves this natively at the compiler level:
1. **Zero External Dependencies:** AAYU has its own built-in SQLite, Web Server, UI Engine, and Math core. An AI Agent will *never* hallucinate a `pip install` or `npm i` command because AAYU handles everything natively.
2. **Context-Map Auto Generation:** AAYU's compiler automatically shrinks your entire full-stack project into a tiny 200-token `.aayu-context.md` file. AI reads this instead of your source code, saving up to 80% on context tokens!
3. **Strict Bounds:** Syntax errors are caught by strict `end` blocks, avoiding pythonic indentation confusion for LLMs.

## ⚡ Why Vibe Coders Love AAYU
If you are a student, a solo dev, or just want to build fast without infrastructure headaches, AAYU feels like plain English.
- No `virtualenv`. No `requirements.txt`. No `package.json`.
- Need a database? Just write `model User end`.
- Need a backend? Just write `route "/api" get respond() end`.
- Native static binary (runs on Tails OS, Linux, Mac, Windows without installing any runtime).

## 🚀 The AAYU Ecosystem (Official Packages)
AAYU ships with native standard libraries out of the box:
- `aayu-gemini`: Native Google Gemini AI integration
- `aayu-ml`: Built-in machine learning models & clustering
- `aayu-auth`: JWT, Session, and OAuth ready
- `aayu-crypto`: Blazing fast cryptography & hashing
- `aayu-http`: High-performance async HTTP client
- `aayu-vision`: Computer vision and image processing
- `aayu-rag`: Retrieval-Augmented Generation toolkit
- `aayu-dataframe`: Pandas-like data manipulation
- `aayu-math`: Advanced mathematical computing

## 🛠️ Hello World

```aayu
app Hello
action main
    print("Hello, AAYU!")
end
run main
```

## 🏗️ Full-Stack Example (AAYUGram)

```aayu
app AAYUGram

model Post
    id Int
    content String
    likes Int = 0
end

route "/api/feed"
    get
        let posts = Post.all()
        respond(posts)
    end
end

Page Home
    Column
        Text("Welcome to AAYUGram")
        Button("Create Post", onClick: createPost)
    end
end

run Home
```

## 🏛️ Pure Self-Hosted Architecture (AAYU Protocol)

AAYU follows the industry standard for production programming languages:

```
┌─────────────────────────────────────────────────────────────┐
│             AAYU SELF-HOSTED COMPILER (compiler/*.aayu)      │
│  5,661 Lines of Pure AAYU — Lexer, Parser, AST, Analyzer,   │
│  Bytecode Emitter, and UI Transpiler                        │
└──────────────────────────────┬──────────────────────────────┘
                               │ Compiles to .ayc Bytecode
                               ▼
┌─────────────────────────────────────────────────────────────┐
│             AAYU SILICON VM & JIT (runtime_rs/)             │
│  Written in Rust for C-level speed, NanBoxed value stack,   │
│  zero-copy memory management, and Native TCP Sockets        │
└─────────────────────────────────────────────────────────────┘
```

1. **Compiler (100% Pure AAYU):** All compiler stages (`lexer.aayu`, `parser.aayu`, `analyzer.aayu`, `compiler.aayu`, `aayuc.aayu`) are written in native AAYU code.
2. **Virtual Machine (Rust Only):** The execution engine (`runtime_rs`) is written in Rust solely for bare-metal speed, JIT compilation, and hardware execution.
3. **Zero Python:** Python is 0% and strictly banned. No runtime overhead, no `pip`, no `npm`.

## 📊 Project Status
**Current Version**: v1.1.0 (Production Core)

| Component | Language | Status |
|-----------|----------|--------|
| **Compiler Pipeline** | Pure AAYU (`.aayu`) | ✅ Self-Hosted (5,661 lines) |
| **Lexer (LZR)** | Pure AAYU (`.aayu`) | ✅ Self-Hosted |
| **Parser & AST** | Pure AAYU (`.aayu`) | ✅ Self-Hosted |
| **Semantic Analyzer** | Pure AAYU (`.aayu`) | ✅ Self-Hosted |
| **Silicon VM Engine** | Rust (`runtime_rs`) | ✅ Working (<40ms cold start) |
| **JIT Compiler** | Rust (`runtime_rs`) | ✅ Working |
| **Built-in Database Engine** | SQLite + Native WAL | ✅ Working |
| **Native HTTP Server** | TCP Socket Engine | ✅ Working |
| **Declarative UI Engine** | Native Widget Tree | ✅ Working |

## 📄 License
MIT License — see [LICENSE](LICENSE)
