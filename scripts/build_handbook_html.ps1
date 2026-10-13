# ==============================================================================
# Script to compile the Official AAYU Handbook HTML
# ==============================================================================

$logoB64 = Get-Content -Raw "$PSScriptRoot\..\assets\icons\aayu_dark_base64.txt"

$html = @"
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>The Official AAYU Handbook - Ayush Ghrit Kaushik</title>
<style>
  @page {
    size: A4;
    margin: 16mm 14mm 16mm 14mm;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.6;
    font-size: 13.5px;
  }

  .page-break {
    page-break-after: always;
    break-after: page;
  }

  /* COVER PAGE */
  .cover-page {
    height: 100vh;
    min-height: 960px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: linear-gradient(135deg, #090d16 0%, #111827 50%, #1e1b4b 100%);
    color: #ffffff;
    padding: 60px 48px;
    border-radius: 12px;
    page-break-after: always;
  }

  .cover-header {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .cover-logo {
    width: 64px;
    height: 64px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.35);
  }

  .cover-badge {
    display: inline-block;
    background: rgba(99, 102, 241, 0.2);
    border: 1px solid #6366f1;
    color: #c7d2fe;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
  }

  .cover-title {
    font-size: 44px;
    font-weight: 800;
    line-height: 1.15;
    margin-top: 30px;
    background: linear-gradient(to right, #ffffff, #c7d2fe, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .cover-subtitle {
    font-size: 17px;
    color: #94a3b8;
    margin-top: 16px;
    font-weight: 400;
    line-height: 1.5;
    max-width: 95%;
  }

  .cover-features {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 40px;
  }

  .feat-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 16px 20px;
    border-radius: 10px;
  }

  .feat-card h4 {
    color: #a5b4fc;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 5px;
  }

  .feat-card p {
    color: #cbd5e1;
    font-size: 12px;
    line-height: 1.5;
  }

  .cover-footer {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
    padding-top: 24px;
  }

  .author-box h3 {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
  }

  .author-box p {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 2px;
  }

  .edition-tag {
    text-align: right;
    color: #c7d2fe;
    font-size: 12px;
    line-height: 1.4;
  }

  /* HEADINGS */
  h1 {
    font-size: 24px;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2.5px solid #6366f1;
    padding-bottom: 8px;
    margin-top: 28px;
    margin-bottom: 14px;
  }

  h2 {
    font-size: 17px;
    font-weight: 700;
    color: #1e293b;
    margin-top: 20px;
    margin-bottom: 10px;
  }

  h3 {
    font-size: 14.5px;
    font-weight: 600;
    color: #334155;
    margin-top: 14px;
    margin-bottom: 6px;
  }

  p {
    margin-bottom: 10px;
  }

  /* CODE BLOCKS */
  pre {
    background: #0f172a;
    color: #e2e8f0;
    padding: 12px 16px;
    border-radius: 8px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    line-height: 1.55;
    margin: 10px 0 14px 0;
    border-left: 4px solid #6366f1;
    overflow-x: auto;
  }

  code {
    font-family: 'Consolas', 'Courier New', monospace;
    background: #f1f5f9;
    color: #4338ca;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
  }

  pre code {
    background: transparent;
    color: inherit;
    padding: 0;
    font-size: 12px;
    font-weight: normal;
  }

  /* TABLES */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px 0;
    font-size: 12.5px;
  }

  th, td {
    padding: 8px 12px;
    border: 1px solid #e2e8f0;
    text-align: left;
  }

  th {
    background: #f8fafc;
    color: #0f172a;
    font-weight: 700;
  }

  tr:nth-child(even) td {
    background: #fbfcfe;
  }

  /* CALLOUT BOXES */
  .box {
    padding: 12px 16px;
    border-radius: 8px;
    margin: 14px 0;
    font-size: 12.5px;
    line-height: 1.5;
  }

  .box-title {
    font-weight: 700;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .box-tip {
    background: #eef2ff;
    border-left: 4px solid #6366f1;
    color: #312e81;
  }

  .box-note {
    background: #f0fdf4;
    border-left: 4px solid #22c55e;
    color: #14532d;
  }

  .box-caution {
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    color: #78350f;
  }

  .box-deepdive {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #0f172a;
    color: #334155;
  }

  .hinglish {
    background: #faf5ff;
    border-left: 4px solid #a855f7;
    padding: 10px 14px;
    border-radius: 6px;
    margin: 10px 0;
    font-size: 12.5px;
    color: #581c87;
  }

  /* PRACTICE SETS */
  .practice-set {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 16px 0;
  }

  .practice-title {
    font-size: 14px;
    font-weight: 700;
    color: #4338ca;
    margin-bottom: 10px;
    border-bottom: 1px dashed #cbd5e1;
    padding-bottom: 6px;
  }

  .q-block {
    margin-bottom: 12px;
  }

  .q-text {
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 4px;
  }

  .q-sol-title {
    font-weight: 600;
    color: #16a34a;
    font-size: 11.5px;
    margin-top: 4px;
    margin-bottom: 2px;
  }
</style>
</head>
<body>

<!-- ============================================================================== -->
<!-- COVER PAGE -->
<!-- ============================================================================== -->
<div class="cover-page">
  <div>
    <div class="cover-header">
      <img class="cover-logo" src="data:image/png;base64,$logoB64" alt="AAYU Logo">
      <div class="cover-badge">★ OFFICIAL INTENT-TO-SILICON ARCHITECTURE ★</div>
    </div>
    
    <div class="cover-title">The Official AAYU<br>Handbook</div>
    <div class="cover-subtitle">The Complete Guide to Intent-to-Silicon Computing: Language Fundamentals, Architecture & Production Full-Stack Mastery. Written from the ground up for developers and autonomous AI coding agents.</div>

    <div class="cover-features">
      <div class="feat-card">
        <h4>⚡ Single-File Full-Stack</h4>
        <p>Database models, API routes, and reactive UI pages declared cleanly in a single .ay file with zero glue code.</p>
      </div>
      <div class="feat-card">
        <h4>🚀 10ms Boot & 2.4 MB RAM</h4>
        <p>Ultra-compact toolchain (735 KB compiler, 890 KB VM) with near-instant cold start and 36,000+ static req/sec.</p>
      </div>
      <div class="feat-card">
        <h4>🛡️ 48-Bit Nan-Boxed Register VM</h4>
        <p>Hardware-level register optimization. C-level execution speed with deterministic compile-time memory bounds.</p>
      </div>
      <div class="feat-card">
        <h4>📦 Zero External Dependencies</h4>
        <p>No npm, no pip, no fragmentation. Standard library includes native crypto, math, record store, and JSON/AYON.</p>
      </div>
    </div>
  </div>

  <div class="cover-footer">
    <div class="author-box">
      <h3>Ayush Ghrit Kaushik</h3>
      <p>Creator & Lead Systems Architect of AAYU</p>
      <p style="color: #64748b; font-size: 11px; margin-top: 4px;">Project: github.com/Minato95-ayu/INTENT-TO-SILICON</p>
    </div>
    <div class="edition-tag">
      <strong>First Edition — 2026 Reference</strong><br>
      Complete Pedagogical Guide<br>
      English + Conceptual Intuition
    </div>
  </div>
</div>

<!-- ============================================================================== -->
<!-- TABLE OF CONTENTS -->
<!-- ============================================================================== -->
<h1>📑 Table of Contents</h1>
<p>This handbook covers the core computer science fundamentals through the lens of the modern AAYU programming language:</p>

<table>
  <thead>
    <tr>
      <th style="width: 18%;">Chapter</th>
      <th style="width: 52%;">Topic & Core Concepts</th>
      <th style="width: 30%;">Key Takeaways</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Chapter 0</strong></td>
      <td>Introduction to AAYU & Intent Computing</td>
      <td>The Intent-to-Silicon philosophy, Modern 2026 perspective, Toolchain architecture</td>
    </tr>
    <tr>
      <td><strong>Chapter 0.5</strong></td>
      <td>Terminal, PowerShell & Tooling Mastery</td>
      <td>Extensions (.ay, .aa, .aayu), CLI commands, Silent compilation, GitHub Linguist</td>
    </tr>
    <tr>
      <td><strong>Chapter 1</strong></td>
      <td>Variables, Constants & Data Types</td>
      <td>let vs state, 48-bit Nan-Boxing, 256-slot frame limit</td>
    </tr>
    <tr>
      <td><strong>Chapter 2</strong></td>
      <td>Operators & Expressions</td>
      <td>Arithmetic, Comparisons, Polymorphic + overloading</td>
    </tr>
    <tr>
      <td><strong>Chapter 3</strong></td>
      <td>Conditional Instructions (Decision Making)</td>
      <td>if, elif, else, explicit end blocks, Guard clauses</td>
    </tr>
    <tr>
      <td><strong>Chapter 4</strong></td>
      <td>Loop Control & Invariant Iteration</td>
      <td>while loops, Collection traversal with len(), Infinite-loop avoidance</td>
    </tr>
    <tr>
      <td><strong>Chapter 5</strong></td>
      <td>Functions & Actions (Modular Code)</td>
      <td>action declarations, Scope isolation, 256-parameter limit, Recursion</td>
    </tr>
    <tr>
      <td><strong>Chapter 6</strong></td>
      <td>Data Structures: Arrays & Dictionaries</td>
      <td>Dynamic arrays, Key-value dictionaries, In-place access</td>
    </tr>
    <tr>
      <td><strong>Chapter 7</strong></td>
      <td>The AYON Data Format & Web Standards</td>
      <td>Human-friendly superset, Comment preservation, Browser JSON compatibility</td>
    </tr>
    <tr>
      <td><strong>Chapter 8</strong></td>
      <td>Full-Stack Architecture & Native Database</td>
      <td>AayuDb RAM-first storage with WAL, HTTP response helpers, Single-file web pages</td>
    </tr>
    <tr>
      <td><strong>Chapter 9</strong></td>
      <td>The Standard Library (std/) Reference</td>
      <td>math, crypto, db, server, http, fs, ai, ledger, json, ayon</td>
    </tr>
    <tr>
      <td><strong>Chapter 10</strong></td>
      <td>The Ultimate Cheat Sheet & 10 Master Problems</td>
      <td>Syntax summary, Common pitfalls, 10 fully verified algorithmic solutions</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- ============================================================================== -->
<!-- CHAPTER 0: PHILOSOPHY -->
<!-- ============================================================================== -->
<h1>Chapter 0: Introduction to AAYU & Intent Computing</h1>

<h2>1. What is AAYU?</h2>
<p><strong>AAYU</strong> is an <em>Intent-to-Silicon</em> programming language designed and built by <strong>Ayush Ghrit Kaushik</strong>. The fundamental goal of AAYU is to eliminate the friction that slows down developers and autonomous AI coding agents:</p>
<ul style="margin-left: 20px; margin-bottom: 12px;">
  <li><strong>Eliminating Fragile Toolchains:</strong> Traditional stacks require complex build configs, package registries (npm/pip), and multi-directory boilerplate just to build a microservice.</li>
  <li><strong>Deterministic Execution:</strong> By using explicit <code>end</code> blocks instead of whitespace indentation, AAYU guarantees 100% syntactic clarity across all platforms, editors, and AI agents.</li>
  <li><strong>Zero Memory Corruption:</strong> Hardware-level 48-bit Nan-Boxing prevents pointer bugs, segmentation faults, and out-of-bounds memory corruption.</li>
</ul>

<div class="hinglish">
  <strong>Aasan Bhasha Me:</strong> AAYU me aap jo intent sochte hain, wahi seedha code banta hai. Na kisi package manager ka jhanjhat, na semicolon, na whitespace crash hone ka darr. Iska execution Rust ke ultra-fast virtual machine par silicon speed par hota hai.
</div>

<h2>2. Modern 2026 Architectural Positioning</h2>
<p>In modern software engineering (2026), different languages excel in specific domains. Here is where AAYU fits uniquely alongside industry standards:</p>
<table>
  <thead>
    <tr>
      <th>Dimension</th>
      <th>Python 3.14+</th>
      <th>Go / Rust</th>
      <th>AAYU</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Primary Strength</strong></td>
      <td>Data science, rich package ecosystem</td>
      <td>Systems programming, large distributed backends</td>
      <td>Single-file microservices, edge tools, AI agents</td>
    </tr>
    <tr>
      <td><strong>Toolchain Footprint</strong></td>
      <td>Heavy (100+ MB runtime, virtual environments)</td>
      <td>Moderate compiler footprint</td>
      <td>Ultra-light (735 KB compiler, 890 KB VM)</td>
    </tr>
    <tr>
      <td><strong>Cold Boot Time</strong></td>
      <td>~80-150 ms</td>
      <td>~15-30 ms</td>
      <td><strong>~10 ms</strong> (Instant VM startup)</td>
    </tr>
    <tr>
      <td><strong>Runtime Memory</strong></td>
      <td>~30-50 MB base RAM</td>
      <td>~10-20 MB base RAM</td>
      <td><strong>~2.4 MB</strong> base RAM</td>
    </tr>
    <tr>
      <td><strong>Scope Delimitation</strong></td>
      <td>Significant whitespace indentation</td>
      <td>Curly braces <code>{}</code></td>
      <td>Explicit <code>end</code> keywords</td>
    </tr>
  </tbody>
</table>

<h2>3. Hello World Program in AAYU</h2>
<pre><code># The Purest Hello World
print("Hello, World!")</code></pre>

<div class="box box-deepdive">
  <div class="box-title">🔍 Silicon Deep Dive: How Hello World Executes</div>
  When you execute <code>print("Hello, World!")</code>:
  <ol style="margin-left: 18px; margin-top: 4px;">
    <li><strong>Lexer:</strong> Tokenizes the source into <code>[Token::Print, Token::LeftParen, Token::StringLiteral("Hello, World!"), Token::RightParen]</code>.</li>
    <li><strong>Parser:</strong> Emits an AST node: <code>Statement::Print(Expr::StringLiteral)</code>.</li>
    <li><strong>Emitter:</strong> Allocates string constant index 0 in the string table and generates native bytecode: <code>PUSH_CONST 0</code> followed by opcode 81 (<code>PRINT</code>).</li>
    <li><strong>Virtual Machine:</strong> Evaluates the Nan-Boxed pointer and outputs cleanly to stdout with zero class overhead.</li>
  </ol>
</div>

<div class="practice-set">
  <div class="practice-title">📝 Practice Set 0 (Basics of AAYU)</div>
  <div class="q-block">
    <div class="q-text">Q1. Write the code to output your name and current project to the console.</div>
    <div class="q-sol-title">Solution:</div>
    <pre><code>print("Name: Ayush Kaushik, Project: AAYU")</code></pre>
  </div>
  <div class="q-block">
    <div class="q-text">Q2. Why does AAYU use the explicit 'end' keyword instead of Python indentation or C braces?</div>
    <div class="q-sol-title">Solution:</div>
    <p>Whitespace indentation can easily break during copy-pasting, Git merges, or automated AI code generation. Braces require shift-key combos and extra punctuation. Explicit <code>end</code> keywords are unambiguous, visually clean, and read like natural English.</p>
  </div>
</div>

<div class="page-break"></div>

<!-- ============================================================================== -->
<!-- CHAPTER 0.5: TOOLING & TERMINAL -->
<!-- ============================================================================== -->
<h1>Chapter 0.5: Terminal, PowerShell & Tooling Mastery</h1>

<h2>1. Official File Extensions (.ay, .aa, .aayu)</h2>
<p>AAYU supports three official extensions across the compiler, runtime, and editor toolchains:</p>
<ul>
  <li><code>.ay</code> — <strong>Recommended 2-Letter Short Extension!</strong> Fastest and cleanest to type (e.g. <code>main.ay</code>), similar to Python's <code>.py</code> and Rust's <code>.rs</code>.</li>
  <li><code>.aa</code> — Alternative 2-letter double-A extension (e.g. <code>app.aa</code>).</li>
  <li><code>.aayu</code> — Standard full-length extension (e.g. <code>program.aayu</code>).</li>
</ul>

<h2>2. Running Code from PowerShell / CMD / Terminal</h2>
<p>You can create an AAYU file using any text editor (VS Code, Notepad, or Vim) and run it directly:</p>
<pre><code># Step 1: Create a file in Notepad or VS Code
notepad hello.ay

# Step 2: Add code and save:
print("AAYU running cleanly from terminal!")

# Step 3: Run directly via PowerShell or CMD:
aayu hello.ay</code></pre>

<div class="box box-tip">
  <div class="box-title">💡 Production Clean Output (Zero Debug Noise!)</div>
  The modern AAYU compiler runs <strong>100% silently by default</strong>. Just like running <code>python script.py</code>, running <code>aayu script.ay</code> prints only your program output with zero AST dumps or internal compiler noise.
</div>

<h2>3. Complete AAYU CLI Reference</h2>
<table>
  <thead>
    <tr>
      <th style="width: 35%;">Command</th>
      <th style="width: 35%;">What It Does</th>
      <th style="width: 30%;">When to Use</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>aayu &lt;file.ay&gt;</code></td>
      <td>Compiles and runs the file directly</td>
      <td>Daily development and quick testing</td>
    </tr>
    <tr>
      <td><code>aayu run &lt;file.ay&gt; --jit</code></td>
      <td>Executes using the native JIT engine</td>
      <td>Heavy math and tensor operations</td>
    </tr>
    <tr>
      <td><code>aayu build &lt;file.ay&gt; -o app.ayc</code></td>
      <td>Compiles source to pre-built bytecode</td>
      <td>Distributing compiled binaries</td>
    </tr>
    <tr>
      <td><code>aayu app.ayc</code></td>
      <td>Executes pre-compiled bytecode at silicon speed</td>
      <td>Production deployment & containers</td>
    </tr>
    <tr>
      <td><code>aayu --version</code></td>
      <td>Prints the engine version and architecture</td>
      <td>Verifying toolchain updates</td>
    </tr>
  </tbody>
</table>

<h2>4. GitHub Linguist Integration</h2>
<p>To ensure GitHub identifies your repository as 100% AAYU, include a <code>.gitattributes</code> file at the root of your project:</p>
<pre><code>*.aayu linguist-language=AAYU
*.ay linguist-language=AAYU
*.aa linguist-language=AAYU
*.py linguist-vendored</code></pre>

<div class="page-break"></div>

<!-- ============================================================================== -->
<!-- CHAPTER 1: VARIABLES & TYPES -->
<!-- ============================================================================== -->
<h1>Chapter 1: Variables, Constants & Data Types</h1>

<h2>1. Variables: let vs state</h2>
<p>AAYU provides two distinct variable mechanisms tailored for specific programming patterns:</p>
<pre><code># 1. Local Mutable Variable (Standard scoped variable)
let name = "AAYU"
let version = 1.2
let counter = 0
counter = counter + 1

# 2. State Variable (Reactive component & application state)
state active_users = 100
active_users = active_users + 1

# 3. Top-Level Global Declaration
global ENGINE_MODE = "Silicon"</code></pre>

<div class="hinglish">
  <strong>Samjho Aasan Bhasha Me:</strong> <code>let</code> se aap standard variables banate hain jinhe function ya block me update kiya ja sakta hai (e.g. <code>counter = counter + 1</code>). <code>state</code> ko tab use kiya jata hai jab variable UI widgets ya reactive state se bind hota hai.
</div>

<h2>2. Primitive Data Types</h2>
<table>
  <thead>
    <tr>
      <th>Type</th>
      <th>Description</th>
      <th>Example in AAYU</th>
      <th>Internal Representation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Integer</strong></td>
      <td>Signed whole numbers</td>
      <td><code>let count = 42</code></td>
      <td>48-bit Signed Int (Nan-Boxed)</td>
    </tr>
    <tr>
      <td><strong>Float</strong></td>
      <td>Floating-point numbers</td>
      <td><code>let pi = 3.14159</code></td>
      <td>IEEE 754 64-bit Double</td>
    </tr>
    <tr>
      <td><strong>Boolean</strong></td>
      <td>True or False states</td>
      <td><code>let is_running = true</code></td>
      <td>Nan-Boxed Tagged Bool</td>
    </tr>
    <tr>
      <td><strong>String</strong></td>
      <td>UTF-8 text characters</td>
      <td><code>let title = "AAYU"</code></td>
      <td>Heap String Arena</td>
    </tr>
    <tr>
      <td><strong>Array</strong></td>
      <td>Ordered sequence of values</td>
      <td><code>let items = [1, 2, 3]</code></td>
      <td>Heap Array Object</td>
    </tr>
    <tr>
      <td><strong>Dictionary</strong></td>
      <td>Key-value associative map</td>
      <td><code>let d = {"k": "v"}</code></td>
      <td>Heap Dict Object</td>
    </tr>
  </tbody>
</table>

<div class="box box-deepdive">
  <div class="box-title">🔍 The 256 Slot Limit: Why 256 Local Variables Per Function?</div>
  In AAYU, every function frame allocates exactly 256 indexed local slots addressed by a single byte (0..255). This design guarantees that local variable lookup is an instant array index with zero hashing overhead, providing maximum CPU L1-cache locality.
</div>

<div class="box box-caution">
  <div class="box-title">⚠️ Common Mistakes to Avoid</div>
  <ul style="margin-left: 18px;">
    <li><strong>Semicolons:</strong> Do not write <code>let x = 10;</code>. Statements in AAYU are newline-delimited.</li>
    <li><strong>Unquoted Strings:</strong> Always wrap text in double quotes: <code>let name = "Ayush"</code>.</li>
    <li><strong>48-Bit Integer Range:</strong> Standard integer arithmetic operates within the signed 48-bit range (-140 trillion to +140 trillion). For scientific scales, use Floats.</li>
  </ul>
</div>

<div class="practice-set">
  <div class="practice-title">📝 Practice Set 1 (Variables & Calculations)</div>
  <div class="q-block">
    <div class="q-text">Q1. Calculate the Area of a Rectangle (Length = 15, Width = 8) and print the result.</div>
    <div class="q-sol-title">Solution:</div>
    <pre><code>let length = 15
let width = 8
let area = length * width
print("Length:", length)
print("Width:", width)
print("Area of Rectangle:", area)</code></pre>
  </div>
  <div class="q-block">
    <div class="q-text">Q2. Convert Celsius temperature (37.0 C) to Fahrenheit using the formula F = (C * 1.8) + 32.</div>
    <div class="q-sol-title">Solution:</div>
    <pre><code>let celsius = 37.0
let fahrenheit = (celsius * 1.8) + 32.0
print("Celsius:", celsius)
print("Fahrenheit:", fahrenheit)</code></pre>
  </div>
</div>

<div class="page-break"></div>

<!-- ============================================================================== -->
<!-- CHAPTER 2: OPERATORS -->
<!-- ============================================================================== -->
<h1>Chapter 2: Operators & Expressions</h1>

<h2>1. Arithmetic & Comparison Operators</h2>
<table>
  <thead>
    <tr>
      <th>Operator</th>
      <th>Operation</th>
      <th>Example</th>
      <th>Evaluated Output</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><code>+</code></td><td>Addition / Polymorphic Concatenation</td><td><code>10 + 5</code></td><td><code>15</code></td></tr>
    <tr><td><code>-</code></td><td>Subtraction</td><td><code>20 - 7</code></td><td><code>13</code></td></tr>
    <tr><td><code>*</code></td><td>Multiplication</td><td><code>6 * 7</code></td><td><code>42</code></td></tr>
    <tr><td><code>/</code></td><td>Division</td><td><code>100 / 4</code></td><td><code>25</code></td></tr>
    <tr><td><code>%</code></td><td>Modulo (Remainder)</td><td><code>17 % 5</code></td><td><code>2</code></td></tr>
    <tr><td><code>==</code></td><td>Equality Comparison</td><td><code>10 == 10</code></td><td><code>true</code></td></tr>
    <tr><td><code>!=</code></td><td>Inequality Comparison</td><td><code>10 != 5</code></td><td><code>true</code></td></tr>
    <tr><td><code>&lt;</code>, <code>&gt;</code></td><td>Relational Ordering</td><td><code>15 &gt; 8</code></td><td><code>true</code></td></tr>
    <tr><td><code>&lt;=</code>, <code>&gt;=</code></td><td>Relational Inclusion</td><td><code>10 &gt;= 10</code></td><td><code>true</code></td></tr>
  </tbody>
</table>

<h2>2. Polymorphic Overloading</h2>
<p>The <code>+</code> operator automatically adapts to the types of its operands:</p>
<pre><code># 1. Number Addition:
print(10 + 20)           # 30

# 2. String Concatenation:
print("Hello " + "AAYU") # Hello AAYU

# 3. String + Number Concatenation:
print("Area: " + 42)     # Area: 42

# 4. Array Concatenation:
print([1, 2] + [3, 4])   # [1, 2, 3, 4]</code></pre>

<h2>3. Clean Guard Clauses for Logic</h2>
<p>To avoid operator precedence confusion and ensure deterministic execution for AI agents, multi-condition logic is expressed using clean nested blocks (Guard Clauses):</p>
<pre><code>let age = 20
let has_id = true

if age >= 18
    if has_id == true
        print("Access granted!")
    end
end</code></pre>

<div class="practice-set">
  <div class="practice-title">📝 Practice Set 2 (Operators & Logic)</div>
  <div class="q-block">
    <div class="q-text">Q1. Determine whether a given number is Even or Odd using the Modulo operator.</div>
    <div class="q-sol-title">Solution:</div>
    <pre><code>let num = 28
if num % 2 == 0
    print(num, "is EVEN")
else
    print(num, "is ODD")
end</code></pre>
  </div>
</div>

<div class="page-break"></div>

<!-- ============================================================================== -->
<!-- CHAPTER 3: CONDITIONALS -->
<!-- ============================================================================== -->
<h1>Chapter 3: Conditional Branching</h1>

<h2>1. The if / elif / else Structure</h2>
<p>Conditional branches in AAYU evaluate conditions top-to-bottom and execute the first matching block. Every block is closed with an explicit <code>end</code> keyword:</p>
<pre><code>let score = 84

if score >= 90
    print("Grade: A+ (Honors)")
elif score >= 75
    print("Grade: A (Distinction)")
elif score >= 50
    print("Grade: B (First Division)")
else
    print("Grade: Retake required")
end</code></pre>

<div class="practice-set">
  <div class="practice-title">📝 Practice Set 3 (Decision Making)</div>
  <div class="q-block">
    <div class="q-text">Q1. Find the largest among three numbers (a = 45, b = 78, c = 32).</div>
    <div class="q-sol-title">Solution:</div>
    <pre><code>let a = 45
let b = 78
let c = 32

let largest = a
if b > largest
    largest = b
end
if c > largest
    largest = c
end
print("Largest number is:", largest)</code></pre>
  </div>
</div>

<div class="page-break"></div>

<!-- ============================================================================== -->
<!-- CHAPTER 4: LOOPS -->
<!-- ============================================================================== -->
<h1>Chapter 4: Loop Control & Invariant Iteration</h1>

<h2>1. The while Loop</h2>
<p>AAYU uses <code>while</code> loops for repetition. The loop condition is checked before each iteration:</p>
<pre><code># Basic counting loop:
let i = 1
while i <= 5
    print("Step:", i)
    i = i + 1
end</code></pre>

<h2>2. Traversing Collections</h2>
<p>Arrays and strings are traversed cleanly using the built-in <code>len()</code> function:</p>
<pre><code>let languages = ["AAYU", "Rust", "Go", "C"]
let idx = 0
let total = len(languages)

while idx < total
    print("Index", idx, ":", languages[idx])
    idx = idx + 1
end</code></pre>

<div class="practice-set">
  <div class="practice-title">📝 Practice Set 4 (Loops & Math)</div>
  <div class="q-block">
    <div class="q-text">Q1. Print the Multiplication Table for N = 7 from 1 to 10.</div>
    <div class="q-sol-title">Solution:</div>
    <pre><code>let n = 7
let i = 1
while i <= 10
    print(n, "x", i, "=", n * i)
    i = i + 1
end</code></pre>
  </div>
  <div class="q-block">
    <div class="q-text">Q2. Check whether a number (e.g. 29) is Prime.</div>
    <div class="q-sol-title">Solution:</div>
    <pre><code>let num = 29
let is_prime = 1
let d = 2
while d < num
    if num % d == 0
        is_prime = 0
    end
    d = d + 1
end
if is_prime == 1
    print(num, "is PRIME")
else
    print(num, "is NOT prime")
end</code></pre>
  </div>
</div>

<div class="page-break"></div>

<!-- ============================================================================== -->
<!-- CHAPTER 5: FUNCTIONS -->
<!-- ============================================================================== -->
<h1>Chapter 5: Functions & Actions</h1>

<h2>1. Function Declarations (action)</h2>
<p>Functions in AAYU are declared with the <code>action</code> keyword. They can accept parameters and return values:</p>
<pre><code>action compute_rectangle_area(w, h)
    let area = w * h
    return area
end

let result = compute_rectangle_area(12, 5)
print("Computed Area:", result) # 60</code></pre>

<h2>2. Recursive Functions</h2>
<p>Actions fully support recursion with frame safety up to the virtual machine stack depth limit:</p>
<pre><code>action fibonacci(n)
    if n <= 1
        return n
    end
    return fibonacci(n - 1) + fibonacci(n - 2)
end

print("Fibonacci(7):", fibonacci(7)) # 13</code></pre>

<div class="practice-set">
  <div class="practice-title">📝 Practice Set 5 (Modular Actions)</div>
  <div class="q-block">
    <div class="q-text">Q1. Write an action that computes the average of three scores.</div>
    <div class="q-sol-title">Solution:</div>
    <pre><code>action average3(s1, s2, s3)
    let total = s1 + s2 + s3
    return total / 3.0
end
print("Average:", average3(85, 90, 95))</code></pre>
  </div>
</div>

<div class="page-break"></div>

<!-- ============================================================================== -->
<!-- CHAPTER 6: ARRAYS & DICTIONARIES -->
<!-- ============================================================================== -->
<h1>Chapter 6: Data Structures: Arrays & Dictionaries</h1>

<h2>1. Dynamic Arrays</h2>
<p>Arrays hold an ordered list of elements indexed from 0:</p>
<pre><code>let numbers = [10, 20, 30, 40]
print("First item:", numbers[0])
print("Total items:", len(numbers))

# Append an element via array concatenation:
numbers = numbers + [50]
print("Updated items:", numbers) # [10, 20, 30, 40, 50]</code></pre>

<h2>2. Key-Value Dictionaries</h2>
<p>Dictionaries map string keys to values:</p>
<pre><code>let user = {
    "username": "ayush_kaushik",
    "role": "Lead Architect",
    "score": 100
}
print("Username:", user["username"])
print("Role:", user["role"])</code></pre>

<div class="page-break"></div>

<!-- ============================================================================== -->
<!-- CHAPTER 7: AYON & STANDARDS -->
<!-- ============================================================================== -->
<h1>Chapter 7: The AYON Data Format & Web Standards</h1>

<h2>1. What is AYON?</h2>
<p><strong>AYON</strong> (<em>AAYU Object Notation</em>) is a human-friendly data format that supports comments and clean key-value structures. Through the standard library module <code>std/ayon</code>, AAYU converts seamlessly between AYON and strict RFC-compliant JSON for browser and API compatibility:</p>
<pre><code>import "std/ayon"

let payload = { "service": "auth", "status": "active" }
let json_str = ayon_stringify(payload)
print("Serialized JSON:", json_str)</code></pre>

<div class="page-break"></div>

<!-- ============================================================================== -->
<!-- CHAPTER 8: FULL-STACK & DB -->
<!-- ============================================================================== -->
<h1>Chapter 8: Full-Stack Architecture & Native Database</h1>

<h2>1. AAYU Native Database (AayuDb)</h2>
<p>AAYU features a zero-dependency, in-memory Key-Value and Document record store backed by an atomic Write-Ahead Log (WAL) and SSD persistence. Records are managed with pure AAYU helpers:</p>
<pre><code>import "std/db"

# Create typed records
let r1 = db_create_record(1, "Task1", "Pending")
let r2 = db_create_record(2, "Task2", "Completed")
let store = [r1, r2]

# Query and filter records
let active = db_filter_records(store, "value", "Pending")
print("Pending tasks count:", db_count_records(active))</code></pre>

<h2>2. Declarative Web Pages</h2>
<p>AAYU programs can define self-contained UI pages directly in the source file without external web frameworks:</p>
<pre><code>Page Dashboard
    Column
        Heading "AAYU Systems Console"
        Text "Zero-dependency single-file deployment active."
    end
end</code></pre>

<div class="page-break"></div>

<!-- ============================================================================== -->
<!-- CHAPTER 9: STANDARD LIBRARY -->
<!-- ============================================================================== -->
<h1>Chapter 9: The Standard Library Reference (std/)</h1>
<p>All official modules reside in the <code>std/</code> directory and can be imported from any location on the system:</p>

<table>
  <thead>
    <tr>
      <th style="width: 20%;">Module</th>
      <th style="width: 35%;">Purpose</th>
      <th style="width: 45%;">Verified Native Functions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>std/math</code></td>
      <td>Mathematical operations</td>
      <td><code>sqrt(x)</code>, <code>pow(base, exp)</code>, <code>abs(x)</code>, <code>min(a, b)</code>, <code>max(a, b)</code>, <code>clamp(v, l, h)</code></td>
    </tr>
    <tr>
      <td><code>std/crypto</code></td>
      <td>Cryptographic hashing & verification</td>
      <td><code>hash_string(data)</code>, <code>hash_combine(h1, h2)</code>, <code>compute_merkle_root(list)</code>, <code>verify_pow_difficulty(h, z)</code></td>
    </tr>
    <tr>
      <td><code>std/db</code></td>
      <td>In-memory & persistent records</td>
      <td><code>db_create_record(id, name, val)</code>, <code>db_filter_records(recs, fld, val)</code>, <code>db_find_by_id(recs, id)</code>, <code>db_count_records(recs)</code></td>
    </tr>
    <tr>
      <td><code>std/server</code></td>
      <td>HTTP response generators</td>
      <td><code>format_response(status, type, body)</code>, <code>json_response(status, data)</code>, <code>html_response(status, html)</code></td>
    </tr>
    <tr>
      <td><code>std/http</code></td>
      <td>HTTP client request formatting</td>
      <td><code>parse_url_protocol(url)</code>, <code>format_request(method, path, host, body)</code>, <code>status_is_ok(code)</code></td>
    </tr>
    <tr>
      <td><code>std/fs</code></td>
      <td>Path & extension utilities</td>
      <td><code>file_exists(path)</code>, <code>format_path(dir, file)</code>, <code>get_extension(path)</code></td>
    </tr>
    <tr>
      <td><code>std/ai</code></td>
      <td>Tensor & neural forward passes</td>
      <td><code>mat_vec_mul(mat, vec)</code>, <code>vec_add(v1, v2)</code>, <code>mlp_forward_pass(features)</code></td>
    </tr>
    <tr>
      <td><code>std/ledger</code></td>
      <td>State transitions & blockchain verification</td>
      <td><code>verify_balance(bal, amt, fee)</code>, <code>apply_transfer(s, r, amt)</code>, <code>verify_chain_link(prev, curr)</code></td>
    </tr>
    <tr>
      <td><code>std/json</code></td>
      <td>RFC 8259 JSON serialization</td>
      <td><code>json_quote(s)</code>, <code>json_format_object(pairs)</code>, <code>json_format_array(items)</code></td>
    </tr>
    <tr>
      <td><code>std/ayon</code></td>
      <td>AYON data parsing and conversion</td>
      <td><code>ayon_parse_value(src)</code>, <code>ayon_stringify(val)</code></td>
    </tr>
  </tbody>
</table>

<pre><code># Example: Using std/math and std/crypto
import "std/math"
import "std/crypto"

print("Square root of 144:", sqrt(144.0))
print("SHA-style hash of 'AAYU':", hash_string("AAYU"))</code></pre>

<div class="page-break"></div>

<!-- ============================================================================== -->
<!-- CHAPTER 10: CHEAT SHEET & 10 MASTER PROBLEMS -->
<!-- ============================================================================== -->
<h1>Chapter 10: Cheat Sheet & 10 Master Practice Problems</h1>

<h2>1. AAYU Syntax Cheat Sheet</h2>
<table>
  <thead>
    <tr>
      <th>Task</th>
      <th>AAYU Syntax</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Console Output</td><td><code>print("Value:", x)</code></td></tr>
    <tr><td>Variable Declaration</td><td><code>let x = 10</code></td></tr>
    <tr><td>Reactive State Variable</td><td><code>state counter = 0</code></td></tr>
    <tr><td>Top-Level Global</td><td><code>global SYSTEM_ID = "Engine1"</code></td></tr>
    <tr><td>Function Definition</td><td><code>action my_fn(a, b) ... return a + b ... end</code></td></tr>
    <tr><td>Conditional Branching</td><td><code>if x &gt; 5 ... elif x == 5 ... else ... end</code></td></tr>
    <tr><td>Loop Iteration</td><td><code>while i &lt; total ... i = i + 1 ... end</code></td></tr>
    <tr><td>Array Creation & Append</td><td><code>let arr = [1, 2, 3]</code> &nbsp;|&nbsp; <code>arr = arr + [4]</code></td></tr>
    <tr><td>Dictionary Creation</td><td><code>let user = {"name": "Ayush", "role": "Architect"}</code></td></tr>
    <tr><td>Standard Library Import</td><td><code>import "std/math"</code></td></tr>
  </tbody>
</table>

<h2>2. 10 Master Algorithmic Problems & Verified Solutions</h2>

<div class="practice-set">
  <div class="practice-title">🏆 Problem 1: Reverse an Array</div>
  <p>Reverse an array <code>[10, 20, 30, 40, 50]</code> in place and print the reversed collection.</p>
  <div class="q-sol-title">Verified Solution:</div>
  <pre><code>let arr = [10, 20, 30, 40, 50]
let reversed = []
let idx = len(arr) - 1

while idx >= 0
    reversed = reversed + [arr[idx]]
    idx = idx - 1
end

print("Reversed Array:", reversed)</code></pre>
</div>

<div class="practice-set">
  <div class="practice-title">🏆 Problem 2: Fibonacci Sequence (First 10 Numbers)</div>
  <p>Generate and print the first 10 numbers in the Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34.</p>
  <div class="q-sol-title">Verified Solution:</div>
  <pre><code>let count = 10
let a = 0
let b = 1
let i = 0

print("Fibonacci Sequence:")
while i < count
    print(a)
    let nxt = a + b
    a = b
    b = nxt
    i = i + 1
end</code></pre>
</div>

<div class="practice-set">
  <div class="practice-title">🏆 Problem 3: Palindrome String Checker</div>
  <p>Verify whether a string (e.g. <code>"madam"</code>) is a palindrome.</p>
  <div class="q-sol-title">Verified Solution:</div>
  <pre><code>let word = "madam"
let l = len(word)
let is_pal = 1
let i = 0

while i < l / 2
    if word[i] != word[l - 1 - i]
        is_pal = 0
    end
    i = i + 1
end

if is_pal == 1
    print(word, "is a PALINDROME!")
else
    print(word, "is NOT a palindrome.")
end</code></pre>
</div>

<div class="practice-set">
  <div class="practice-title">🏆 Problem 4: Find Maximum & Minimum in an Array</div>
  <p>Locate both the maximum and minimum numbers in an unsorted array.</p>
  <div class="q-sol-title">Verified Solution:</div>
  <pre><code>let nums = [45, 12, 89, 3, 67, 99, 23]
let max_val = nums[0]
let min_val = nums[0]
let i = 1
let total = len(nums)

while i < total
    if nums[i] > max_val
        max_val = nums[i]
    end
    if nums[i] < min_val
        min_val = nums[i]
    end
    i = i + 1
end

print("Maximum:", max_val)
print("Minimum:", min_val)</code></pre>
</div>

<div class="practice-set">
  <div class="practice-title">🏆 Problem 5: Linear Search Algorithm</div>
  <p>Search for target 308 in an array and return its 0-based index, or -1 if not found.</p>
  <div class="q-sol-title">Verified Solution:</div>
  <pre><code>action search(arr, target)
    let i = 0
    let total = len(arr)
    while i < total
        if arr[i] == target
            return i
        end
        i = i + 1
    end
    return 0 - 1
end

let items = [101, 204, 308, 412, 550]
let found_idx = search(items, 308)
print("Found target 308 at index:", found_idx)</code></pre>
</div>

<div class="practice-set">
  <div class="practice-title">🏆 Problem 6: Character Frequency Counter</div>
  <p>Count the occurrences of character <code>'a'</code> in the string <code>"aayulanguage"</code>.</p>
  <div class="q-sol-title">Verified Solution:</div>
  <pre><code>let text = "aayulanguage"
let target_char = "a"
let count = 0
let i = 0
let l = len(text)

while i < l
    if text[i] == target_char
        count = count + 1
    end
    i = i + 1
end

print("Frequency of 'a':", count) # 4</code></pre>
</div>

<div class="practice-set">
  <div class="practice-title">🏆 Problem 7: Factorial Calculation (Iterative)</div>
  <p>Compute N! for N = 5 using iterative multiplication.</p>
  <div class="q-sol-title">Verified Solution:</div>
  <pre><code>action factorial(n)
    let result = 1
    let curr = 1
    while curr <= n
        result = result * curr
        curr = curr + 1
    end
    return result
end

print("Factorial of 5 is:", factorial(5)) # 120</code></pre>
</div>

<div class="practice-set">
  <div class="practice-title">🏆 Problem 8: Sum & Average Calculation</div>
  <p>Calculate the sum and average of an array of student scores.</p>
  <div class="q-sol-title">Verified Solution:</div>
  <pre><code>let scores = [80, 90, 70, 85, 95]
let sum = 0
let i = 0
let total = len(scores)

while i < total
    sum = sum + scores[i]
    i = i + 1
end

let avg = sum / total
print("Total Sum:", sum)
print("Average Score:", avg)</code></pre>
</div>

<div class="practice-set">
  <div class="practice-title">🏆 Problem 9: Filter Even and Odd Numbers</div>
  <p>Separate an array of integers into distinct lists of even and odd values.</p>
  <div class="q-sol-title">Verified Solution:</div>
  <pre><code>let numbers = [12, 7, 19, 24, 31, 40, 55]
let evens = []
let odds = []
let i = 0
let total = len(numbers)

while i < total
    let n = numbers[i]
    if n % 2 == 0
        evens = evens + [n]
    else
        odds = odds + [n]
    end
    i = i + 1
end

print("Evens:", evens)
print("Odds:", odds)</code></pre>
</div>

<div class="practice-set">
  <div class="practice-title">🏆 Problem 10: Two-Sum Target Matcher</div>
  <p>Given an array <code>[2, 7, 11, 15]</code>, find two numbers that sum up to target <code>9</code>.</p>
  <div class="q-sol-title">Verified Solution:</div>
  <pre><code>action find_two_sum(arr, target)
    let i = 0
    let total = len(arr)
    while i < total
        let j = i + 1
        while j < total
            if arr[i] + arr[j] == target
                return [arr[i], arr[j]]
            end
            j = j + 1
        end
        i = i + 1
    end
    return []
end

let pair = find_two_sum([2, 7, 11, 15], 9)
print("Two numbers that sum to 9:", pair) # [2, 7]</code></pre>
</div>

</body>
</html>
"@

Set-Content -Path "$PSScriptRoot\..\docs\AAYU_OFFICIAL_HANDBOOK.html" -Value $html -Encoding utf8
Set-Content -Path "$PSScriptRoot\..\docs\AAYU_HANDBOOK_CWH_STYLE.html" -Value $html -Encoding utf8

Write-Host "Successfully compiled docs/AAYU_OFFICIAL_HANDBOOK.html and docs/AAYU_HANDBOOK_CWH_STYLE.html!" -ForegroundColor Green
