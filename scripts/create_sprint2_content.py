import os

docs_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\content\docs'

# Clear existing docs to restructure properly
import shutil
if os.path.exists(docs_dir):
    shutil.rmtree(docs_dir)

os.makedirs(docs_dir)

files_to_create = {
    "1-getting-started/1-installation.mdx": {
        "title": "Installation",
        "desc": "Install AAYU from source and set up your environment.",
        "content": '''# Installation

## Overview
AAYU is a blazingly fast, statically typed systems language compiled via LLVM. Currently in alpha, AAYU must be built from source.

## Why it exists
To provide a memory-safe environment without a Garbage Collector (via Deterministic ARC) while maintaining C-like performance, we require a custom LLVM backend toolchain.

## Syntax & Usage
<CodeBlock lang="bash" code="git clone https://github.com/Minato95-ayu/AAYU.git\\ncd AAYU\\nmake build" />

## Output
<CodeBlock lang="bash" code="$ aayu --version\\naayu 0.1.0-alpha (2026-07-05)" />

## Common Errors
<ErrorBlock 
    wrong="make install"
    correct="make build"
    errorMsg="Makefile error: target 'install' not found. Use 'make build'."
/>

## Best Practices
Always ensure you have LLVM 16+ and a compatible C++ compiler (clang or gcc) installed before building AAYU.

## Related Topics
- [Getting Started](/docs/1-getting-started/2-getting-started)
- [CLI Reference](/docs/5-cli/1-cli-reference)
'''
    },
    "1-getting-started/2-getting-started.mdx": {
        "title": "Getting Started",
        "desc": "A quick introduction to the AAYU ecosystem.",
        "content": '''# Getting Started

## Overview
AAYU is more than a language; it's an ecosystem comprising the AAYU Compiler, BrainOS (Autonomous Architect), and the Intent Engine.

## Why it exists
Modern software engineering requires jumping between diagrams, Jira, and IDEs. AAYU unites Intent (what you want) and Code (how it runs).

## Example
<CodeBlock lang="aayu" code='// A simple AAYU file\\nentity Config has\\n    debug: Boolean\\nend.' playgroundUrl="/playground" />

## Best Practices
Treat the AAYU CLI as your central hub. Use ayu init to scaffold new projects instead of manually creating files.

## Related Topics
- [BrainOS Basics](/docs/4-brainos/1-brainos-basics)
'''
    },
    "1-getting-started/3-hello-world.mdx": {
        "title": "Hello World",
        "desc": "Write your first AAYU program.",
        "content": '''# Hello World

## Overview
The classic introductory program.

## Syntax
<CodeBlock lang="aayu" code='fn main()\\ndo\\n    print("Hello, World!").\\nend.' playgroundUrl="/playground" />

## Output
<CodeBlock lang="bash" code="> aayu run main.aayu\\nHello, World!" />

## Common Errors
<ErrorBlock 
    wrong="fn main() {\\n    print(\\"Hello, World!\\");\\n}"
    correct='fn main()\\ndo\\n    print("Hello, World!").\\nend.'
    errorMsg="SyntaxError: Expected 'do' to start block, found '{'."
/>

## Best Practices
Always end your statements with a period (.).
'''
    },
    "2-language/1-syntax.mdx": {
        "title": "Syntax",
        "desc": "AAYU's keyword-driven syntax rules.",
        "content": '''# Syntax

## Overview
AAYU abandons C-style curly braces {} and semicolons ; in favor of keyword blocks (do/end) and periods (.).

## Why it exists
To make the codebase read like an English sentence or specification document, which natively aligns with the Intent Engine NLP parser.

## Example
<CodeBlock lang="aayu" code="entity App\\nhas\\n    port: Number\\nend." playgroundUrl="/playground" />

## Common Errors
<ErrorBlock 
    wrong="entity App has port: Number end"
    correct="entity App\\nhas\\n    port: Number\\nend."
    errorMsg="SyntaxError: Missing terminating period."
/>

## Best Practices
Keep your entities flat. Use extensions (extend) to add behavior rather than nesting functions inside the entity declaration.
'''
    },
    "2-language/2-variables.mdx": {
        "title": "Variables",
        "desc": "Declaring and mutating state.",
        "content": '''# Variables

## Overview
Variables in AAYU are declared using the let keyword. They are strictly typed and immutable by default.

## Syntax
<CodeBlock lang="aayu" code='let name: Text = "Developer".\\nmut age: Number = 25.' playgroundUrl="/playground" />

## Common Errors
<ErrorBlock 
    wrong='let age = 25.\\nage = 26.'
    correct='mut age: Number = 25.\\nage = 26.'
    errorMsg="TypeError: Cannot reassign immutable variable 'age'."
/>

## Best Practices
Prefer let over mut. AAYU's LLVM optimizer can aggressively fold constants and inline immutable state.
'''
    },
    "2-language/3-functions.mdx": {
        "title": "Functions",
        "desc": "Defining logic and behavior.",
        "content": '''# Functions

## Overview
Functions are declared using the n keyword, parameters in parentheses, and a return type via ->.

## Syntax
<CodeBlock lang="aayu" code="fn add(a: Number, b: Number) -> Number\\ndo\\n    return a + b.\\nend." playgroundUrl="/playground" />

## Common Errors
<ErrorBlock 
    wrong="fn add(a, b)\\ndo return a + b. end."
    correct="fn add(a: Number, b: Number) -> Number\\ndo return a + b. end."
    errorMsg="TypeError: Missing type annotations for parameters 'a' and 'b'."
/>

## Best Practices
Keep functions pure where possible. The Semantic Analyzer checks for pure execution paths to allow concurrent invocation.
'''
    },
    "2-language/4-modules.mdx": {
        "title": "Modules",
        "desc": "Organizing AAYU code.",
        "content": '''# Modules

## Overview
Modules allow you to split your AAYU codebase across multiple files.

## Syntax
<CodeBlock lang="aayu" code='import "math".\\n\\nlet pi = math.PI.' />

## Best Practices
AAYU modules are resolved based on the directory structure. Keep your folder structure flat and semantic.
'''
    },
    "2-language/5-packages.mdx": {
        "title": "Packages",
        "desc": "Using the apm package manager.",
        "content": '''# Packages

## Overview
pm (AAYU Package Manager) handles dependencies.

## Syntax
<CodeBlock lang="bash" code="aayu pkg add http" />

## Output
<CodeBlock lang="bash" code="Resolving http@latest...\\n[PASS] Downloaded http v1.2.0.\\nUpdated aayu.toml." />

## Best Practices
Always check in your ayu.lock file to version control to ensure deterministic builds.
'''
    },
    "3-architecture/1-compiler-pipeline.mdx": {
        "title": "Compiler Pipeline",
        "desc": "How AAYU source becomes native machine code.",
        "content": '''# Compiler Pipeline

## Overview
The AAYU compiler is a multi-pass system written in Python (prototype) that ultimately targets LLVM IR.

<PipelineDiagram stages={["Lexer", "Parser", "AST", "Semantic", "Optimizer", "LLVM", "Binary"]} />

## Why it exists
A direct-to-LLVM pipeline ensures that AAYU runs as fast as C or Rust without the overhead of an interpreter or JIT.

## Best Practices
Use the CLI flag ayu build --emit-llvm to inspect the generated IR if you are optimizing a hot-path in your application.

## Related Topics
- [Playground](/playground) (Interactive Pipeline View)
'''
    },
    "3-architecture/2-runtime.mdx": {
        "title": "Runtime (DARC)",
        "desc": "Deterministic ARC memory management.",
        "content": '''# Runtime & Memory

## Overview
AAYU does not use a Garbage Collector. It uses **Deterministic Automatic Reference Counting (DARC)**.

## Why it exists
GC pauses (stop-the-world) are unacceptable in high-performance systems. DARC statically analyzes lifetimes during the Semantic pass and inserts 
etain/
elease instructions directly into the LLVM IR.

## Common Errors
<ErrorBlock 
    wrong="let ptr = get_dangling_reference()."
    correct="let ptr = acquire_safe_reference()."
    errorMsg="MemoryError: Lifetime validation failed. Reference outlives owner."
/>

## Best Practices
Avoid deep cyclic data structures. If you must use cycles, use the weak keyword to break reference loops.
'''
    },
    "4-brainos/1-brainos-basics.mdx": {
        "title": "BrainOS Basics",
        "desc": "Autonomous Architectural Scaffolding.",
        "content": '''# BrainOS Basics

## Overview
BrainOS is the AI orchestrator within the AAYU ecosystem. It acts as a senior software architect.

<PipelineDiagram stages={["Intent", "Knowledge Graph", "Decision Engine", "Planner", "Scaffold AAYU"]} />

## Why it exists
Writing boilerplate entities and plumbing APIs takes time. BrainOS understands your Intent (e.g., "Build an ERP") and generates the foundational AST instantly.

## Example
<CodeBlock lang="bash" code='aayu brain generate "Build a scalable hospital management system"' />

## Output
<CodeBlock lang="bash" code="[BrainOS] Analyzing Domain: Healthcare\\n[BrainOS] Applying Tradeoffs: High Security, ACID Compliance.\\n[BrainOS] Generated 45 AAYU Entities.\\n[PASS] Project scaffolded in /hospital_erp." />

## Best Practices
Use BrainOS to bootstrap projects, but always review the generated AAYU code before pushing to production.
'''
    },
    "5-cli/1-cli-reference.mdx": {
        "title": "CLI Reference",
        "desc": "The official AAYU CLI tool.",
        "content": '''# CLI Reference

## Overview
The ayu command line tool handles building, running, and managing packages.

## Core Commands
- ayu run <file>: Compile and execute immediately.
- ayu build: Compile to native binary.
- ayu pkg: Interact with the package manager.
- ayu brain: Invoke the BrainOS orchestrator.

## Example
<CodeBlock lang="bash" code="aayu build main.aayu -O3 --target x86_64" />

## Best Practices
For production, always use the -O3 optimization flag.
'''
    }
}

for filepath, data in files_to_create.items():
    full_path = os.path.join(docs_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Add cross-linking footer automatically
    content = data["content"] + "\\n\\n[Edit on GitHub (Available in v1.0)](#)\\n"
    
    file_str = f"""---
title: "{data['title']}"
description: "{data['desc']}"
---

{content}"""

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(file_str)

print("Created 12 Real Documentation MDX pages.")
