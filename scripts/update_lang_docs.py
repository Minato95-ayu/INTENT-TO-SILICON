"""
=============================================================================
FILE: update_lang_docs.py
PURPOSE: Updates language documentation
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles updates language documentation.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os
import json

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\data\language-content.tsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# I will add deep documentation for 'type-system', 'optimizer', 'package-manager', 'standard-library'
if '"type-system"' not in content:
    new_docs = """
  "type-system": {
    title: "Type System",
    description: "AAYU features a strong, static, and inference-first type system designed for enterprise scale.",
    body: (
      <>
        <h2 className="text-2xl font-bold mt-8 mb-4">Core Principles</h2>
        <p className="mb-4">The type system in AAYU is strict. There is no implicit coercion between mismatched types. This guarantees that your Intent Graph maps exactly to runtime safety.</p>
        <h3 className="text-xl font-bold mt-6 mb-3">Algebraic Data Types</h3>
        <p className="mb-4">AAYU supports ADTs out of the box, allowing you to model complex states securely.</p>
        <pre className="bg-[#0d0d0d] p-4 rounded-lg border border-white/10 overflow-x-auto mb-6">
          <code className="text-sm font-mono text-zinc-300">
{enum Result<T, E>
has
    Ok(T)
    Err(E)
end.}
          </code>
        </pre>
      </>
    )
  },
  "optimizer": {
    title: "Optimizer",
    description: "The AAYU Optimizer works at both the Intent level and the Bytecode level.",
    body: (
      <>
        <h2 className="text-2xl font-bold mt-8 mb-4">Intent-Level Optimization</h2>
        <p className="mb-4">Before lowering to LLVM IR, AAYU analyzes the Intent Graph. If it sees you are repeatedly querying a database entity without caching, the Tradeoff Engine injects a Redis cache layer automatically.</p>
        <h2 className="text-2xl font-bold mt-8 mb-4">LLVM Lowering</h2>
        <p className="mb-4">Once lowered, AAYU applies aggressive Dead Code Elimination (DCE), Loop Unrolling, and Monomorphization for generic types.</p>
      </>
    )
  },
  "package-manager": {
    title: "Package Manager (apm)",
    description: "Dependency management built natively into the AAYU toolchain.",
    body: (
      <>
        <h2 className="text-2xl font-bold mt-8 mb-4">Zero Configuration</h2>
        <p className="mb-4">AAYU eschews complex package.json or Cargo.toml files for a simple \ayu.mod\ file. Dependencies are fetched securely via the AAYU Registry.</p>
        <pre className="bg-[#0d0d0d] p-4 rounded-lg border border-white/10 overflow-x-auto mb-6">
          <code className="text-sm font-mono text-zinc-300">
{// aayu.mod
module my_app 1.0.0
require http_server >= 2.1.0}
          </code>
        </pre>
      </>
    )
  },
"""
    content = content.replace("const DOCS_DB: Record<string, Partial<ContentItem>> = {", "const DOCS_DB: Record<string, Partial<ContentItem>> = {\n" + new_docs)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated language-content.tsx")
