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

## 🏛️ Architecture

```
┌─────────────────────────────────────────┐
│              AAYU Source (.aayu)         │
├──────┬──────┬──────┬──────┬─────────────┤
│Lexer │Parser│ AST  │Seman-│   IR        │
│      │      │      │tic   │Pipeline     │
├──────┴──────┴──────┴──────┼─────────────┤
│         HIR → MIR → LIR  │  Bytecode   │
├───────────────────────────┼─────────────┤
│     Stack-based VM        │   GC Heap   │
├───────────────────────────┴─────────────┤
│  stdlib: math | ai | ml | db | http     │
└─────────────────────────────────────────┘
```

## 📊 Project Status
**Current Version**: v1.1.0 (Development)

| Feature | Status |
|---------|--------|
| Compiler Pipeline | ✅ Working |
| Self-Hosted Bootstrapping | ✅ Done (Phase 3) |
| Rust JIT VM | ✅ Working (50ms Benchmark) |
| Database/Storage | ✅ Working |
| Web Server/Routes | ✅ Working |
| CLI Tools | ✅ Working |
| Frontend UI | ✅ Working |
| AI/ML stdlib | ✅ Working |

## 📄 License
MIT License — see [LICENSE](LICENSE)
