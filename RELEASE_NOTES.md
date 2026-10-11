# AAYU v1.0.0 Stable 🚀

We are incredibly proud to announce the **first stable release of AAYU**!

AAYU is an AI-native application language that allows developers to build native HTTP servers, UI renderers, and state management systems using pure declarative intent, with zero external dependencies. 

## What's in 1.0.0 Stable?

### 1. The Application Language
AAYU completely redesigns the syntax to focus on what matters. Say goodbye to boilerplate, HTML, CSS, and wiring code.
```
app hello_world

page Home
    text "Welcome to AAYU 1.0!"
end

run
```

### 2. Built-in Runtime & Virtual Machine
The AAYU compiler produces a highly optimized custom bytecode that runs on our native Stack-Based Virtual Machine. The VM handles layout rendering, state reactivity, memory management (mark-and-sweep GC), and routing automatically.

### 3. Developer Experience (DX) First
- **`aayu new <project>`**: Scaffolds a new project instantly.
- **`aayu run`**: Compiles and executes the project seamlessly.
- **`aayu build`**: Generates a lean release binary.
- **`aayu doctor`**: Instant environment diagnostics.

### 4. 15-Minute Learning Curve
We’ve rewritten the entire [documentation suite](https://aayu.dev/docs) with an interactive "Learn in 15 Minutes" curriculum that takes you from Hello World to a fully functional application.

### 5. 10 Production Examples
To prove the capability of the language, we've bundled 10 examples in the `examples/` directory, including a Todo list, Chat UI, Dashboard, and even a WhatsApp clone—all written in pure AAYU.

## Installation
```bash
pip install aayu-lang
```
Or download the standalone `.exe` from the assets below.

## Quick Start
```bash
aayu new my_app
cd my_app
aayu run
```

---
*Thank you to everyone who tested the RC candidates. This is just the beginning of Intent-Driven Development.*