# AAYU — Intent-to-Silicon Programming Language

> Write your intent. AAYU compiles it to silicon-ready bytecode.

AAYU is a **single-file full-stack programming language** with built-in Database, Backend Server, Frontend UI, and AI/ML — all zero-dependency, zero-config.

## ✨ What Makes AAYU Different

- **Single-file full-stack**: Database models, API routes, UI pages, and AI/ML — all in one `.aayu` file
- **Zero dependencies**: No npm, no pip, no package managers needed for core features
- **Real compiler pipeline**: Lexer → Parser → AST → HIR → MIR → LIR → Bytecode → Stack-based VM
- **Memory safe**: Mark-and-sweep garbage collector with reference counting
- **Built-in database**: SQLite with schema engine, query planner, transaction manager, migration engine
- **Built-in web server**: REST API routes with middleware, auth, and session management
- **Built-in UI**: Declarative widget-tree (Flutter-like) with reactive state
- **AI/ML stdlib**: Native model training, inference, clustering — no external libraries

## 🚀 Quick Start

```bash
# Clone and install
git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git
cd INTENT-TO-SILICON
pip install -e .

# Run your first program
aayu run hello.aayu

# Run with web server
aayu run aayugram.aayu --web
```

## 📝 Hello World

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

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run compiler tests
python -m pytest tests/compiler/ -v
```

## 📊 Project Status

**Current Version**: v1.1.0

| Feature | Status |
|---------|--------|
| Compiler Pipeline (Lexer → LIR) | ✅ Working |
| Stack-based VM + Bytecode | ✅ Working |
| Garbage Collector (Mark & Sweep) | ✅ Working |
| Database / Storage Engine | ✅ Working |
| Web Server / REST Routes | ✅ Working |
| CLI Tools (`aayu run`, `aayu doctor`) | ✅ Working |
| Frontend UI (Declarative Widgets) | 🔨 In Progress |
| AI/ML Standard Library | 🔨 In Progress |
| Package Manager (APM) | 📋 Planned |

## 📄 License

MIT License — see [LICENSE](LICENSE)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
