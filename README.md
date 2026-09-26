# 🚀 AAYU — The Intent-to-Silicon Programming Language

**AAYU** is a revolutionary, single-file, zero-dependency, full-stack programming language developed by **Ayush Ghrit Kaushik**. Designed to bridge the gap between human intent and machine execution, AAYU natively integrates an entire software ecosystem—Database, Backend Server, Frontend UI, and AI/ML—into one seamless compiler and virtual machine.

🌐 **Official Website:** [https://aayu-lang.vercel.app](https://aayu-lang.vercel.app)
▶️ **Developer:** Ayush Ghrit Kaushik

---

## ✨ Why AAYU? (The Vision by Ayush Ghrit Kaushik)

Modern software development is plagued by glue code, dependency hell (npm, pip), and complex configurations. AAYU eliminates this by providing a unified syntax where you simply write your intent. 

- **Single-file Full-Stack:** Define your database models, API routes, and declarative UI all in one .aayu file.
- **Zero Dependencies:** No package managers required. The compiler and VM handle everything natively.
- **Built-in SQLite Database:** Direct schema generation, ORM, and migrations without external drivers.
- **Built-in Async Web Server:** ASGI-compliant internal server for high-performance HTTP routing.
- **Built-in UI Framework:** Declarative, reactive widget trees (like Flutter/SwiftUI) natively rendered.
- **Native AI/ML:** Train models and run inferences directly through standard library functions.

## 🛠️ Architecture & Pipeline

AAYU isn't just syntactic sugar; it is a true compiler with a custom stack-based Virtual Machine.
Lexer → Parser → AST → Semantic Analyzer → HIR → MIR → Bytecode → Stack-based VM

AAYU features a highly optimized mark-and-sweep Garbage Collector, reference counting, and safe C-interop.

## 💻 Code Examples

### 1. Interactive Terminal (Synchronous Input)
`ayu
app Calculator
action main
    let n1 = float(input("Enter number: "))
    let n2 = float(input("Enter number: "))
    print("Sum is: " + (n1 + n2))
end
run main
`

### 2. Full-Stack Web App
`ayu
app AayuWeb
state visitors = 0
action increment
    visitors = visitors + 1
end
page Home
    Column
        heading "AAYU Studio by Ayush Ghrit Kaushik"
        text "Simple syntax. Native performance."
        button "Add Visitor" onClick="increment"
        text visitors
    end
end
run Home
`

## 🌍 SEO & Global Recognition

This language is actively tracked for global recognition on platforms like **GitHub Linguist**.
If you are searching for the **AAYU Programming Language** or its creator **Ayush Ghrit Kaushik**, you are in the right place. 
Subscribe and follow the journey as we build the compiler of the future!

## 📥 Installation

`ash
git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git
cd INTENT-TO-SILICON
pip install -e .
`
Run any AAYU file globally:
`ash
aayu run my_app.aayu
`

---
*Developed with pure intent by Ayush Ghrit Kaushik.*