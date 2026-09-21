<div align="center">
  <img src="website/public/aayu-logo.png" alt="AAYU Logo" width="200" />
  <h1>AAYU Programming Language</h1>
  <p><strong>Intent-to-Silicon: Write your intent. AAYU compiles it to native machine code.</strong></p>
  <p>
    <a href="https://intent-to-silicon.vercel.app/">Website</a> • 
    <a href="https://www.linkedin.com/in/ayushh-kaushiq-1a950825a/">LinkedIn</a> • 
    <a href="https://www.instagram.com/aa.yu_s/">Instagram</a>
  </p>
</div>

---

## What is AAYU? 
Are you a student learning to code? Or a developer tired of setting up environments, dealing with huge dependencies, and slow execution? 

**AAYU** is built for you. AAYU is a **Native AOT (Ahead-of-Time) Compiled Systems Language** designed to be incredibly simple to learn, yet as fast as C++ or Rust. 

Imagine writing code that looks as easy as Python, but when you hit run, it compiles directly into a standalone .exe native binary. **No Python VM. No Node.js. No pip packages required to run your apps.** It's just you, your code, and the silicon.

AAYU is a **fully bootstrapped (self-hosted)** language. This means the AAYU compiler itself is written in AAYU!

## 🚀 Why AAYU? (The Features)
- **Zero Python/Node Overhead**: AAYU generates its own pure C code behind the scenes and natively compiles it. 0% Python dependency at runtime.
- **Python Simplicity, C++ Speed**: We designed the syntax (ction, let, while) to be readable for absolute beginners, while outputting machine code that runs in nanoseconds.
- **Single-File Full Stack**: (Coming soon) Build your UI, API, and Database in a single .aayu file without juggling 5 different frameworks.
- **Stand-Alone Binaries**: Share your apps as a single .exe file. Your friends don't need to install anything to run your code!

## 💻 Code Example
Look how simple it is. No classes or boilerplate required to get started.

`ayu
// A simple AAYU program
let limit = 1000
let i = 0
let sum = 0

// Native Loop Execution (runs at silicon speed!)
while i < limit
  sum = sum + i
  i = i + 1
end

print("The total sum is:")
print(sum)
`

## 🛠️ How to Get Started

Right now, AAYU is in active development. If you are a developer or student who wants to compile AAYU code:

### Option 1: Native Executable (For Users)
Soon, you will be able to simply download ayuc.exe from our releases and run:
`ash
# Simply pass your file to the AAYU compiler
aayuc my_program.aayu
`

### Option 2: Build from Source (For Compiler Contributors)
If you want to help develop the AAYU compiler itself, you can use our Python bootstrap script:
`ash
git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git
cd INTENT-TO-SILICON
pip install -e .

# Use the bootstrap CLI to build your .aayu files
aayu build my_program.aayu
`
*(Note: pip install is ONLY used right now if you are developing the compiler itself. Regular AAYU users will never need Python!)*

## 🧠 About the Creator
**Ayush Ghrit Kaushik** (GitHub: [@Minato95-ayu](https://github.com/Minato95-ayu))  
I built AAYU because I believe programming should be accessible, fast, and completely free of the bloated ecosystems we see today. The goal was to create a tool that respects the developer's time and computer's resources. Everything from the parser to the native C-backend was engineered to bring the joy of programming back.

Connect with me and follow AAYU's journey:
- [LinkedIn](https://www.linkedin.com/in/ayushh-kaushiq-1a950825a/)
- [Instagram](https://www.instagram.com/aa.yu_s/)

---
**Copyright © 2026 Ayush Ghrit Kaushik. All Rights Reserved.**  
Unauthorized copying, reproduction, or distribution is strictly prohibited.
