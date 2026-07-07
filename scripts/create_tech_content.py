"""
=============================================================================
FILE: create_tech_content.py
PURPOSE: Creates technical documentation
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles creates technical documentation.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os

base_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\data'
os.makedirs(base_dir, exist_ok=True)

content = '''
import React from 'react';
import { languageNavData } from './language';

type ContentItem = {
  title: string;
  description: string;
  body: React.ReactNode;
  prev?: { title: string; slug: string };
  next?: { title: string; slug: string };
};

const DOCS_DB: Record<string, Partial<ContentItem>> = {
  "overview": {
    title: "AAYU Overview",
    description: "AAYU is a general-purpose, statically typed, offline-first programming language built around human intent.",
    body: (
      <>
        <h2 className="text-2xl font-bold mt-8 mb-4">The Philosophy</h2>
        <p className="mb-4">Programming hasn\\'t changed fundamentally since C. We still write imperative loops, manage dependencies manually, and stitch together disjointed systems. AAYU completely reimagines this paradigm by separating <strong>what</strong> you want from <strong>how</strong> it is implemented.</p>
        <p className="mb-4">AAYU introduces the <strong>Intent Engine</strong> at the core of the compiler pipeline. Instead of just parsing ASTs for syntax, AAYU builds an <em>Intent Graph</em>—a semantic understanding of your business logic—and allows the <strong>BrainOS</strong> to automatically resolve infrastructure decisions (like databases, queues, and caching) at compile-time.</p>
        <h3 className="text-xl font-bold mt-6 mb-3">Key Characteristics</h3>
        <ul className="list-disc pl-6 space-y-2 mb-6">
          <li><strong>Zero-Overhead Abstractions:</strong> Code compiles down to highly optimized native machine code via LLVM.</li>
          <li><strong>Offline-First Autonomous Engineering:</strong> BrainOS doesn\\'t require cloud API calls. The entire knowledge graph is shipped with the compiler.</li>
          <li><strong>Memory Safety without Lifetimes:</strong> AAYU uses a deterministic Arc-based memory model that eliminates Data Races without the steep learning curve of Borrow Checkers.</li>
        </ul>
      </>
    )
  },
  "why-aayu": {
    title: "Why AAYU?",
    description: "Why build a new programming language when we have Rust, Go, and TypeScript?",
    body: (
      <>
        <h2 className="text-2xl font-bold mt-8 mb-4">The Productivity Gap</h2>
        <p className="mb-4">Rust is safe but slow to write. Go is fast to write but lacks expressive type safety (until recently) and forces boilerplate. TypeScript is ubiquitous but constrained by the JS runtime and massive 
ode_modules.</p>
        <p className="mb-4">AAYU is designed to give you the <strong>performance of Rust</strong>, the <strong>concurrency of Go</strong>, and the <strong>DX of TypeScript</strong>, augmented by an autonomous AI that lives inside the compiler.</p>
        
        <div className="bg-white/5 border border-white/10 p-4 rounded-lg my-6">
          <h4 className="font-mono text-sm text-blue-400 mb-2">Example: The AAYU Difference</h4>
          <p className="text-sm text-zinc-400">In AAYU, you define entities and relationships, and BrainOS generates the CRUD scaffolding, database drivers, and REST endpoints automatically.</p>
        </div>
      </>
    )
  },
  "syntax": {
    title: "Syntax Basics",
    description: "AAYU borrows the best syntactic sugar from modern languages while remaining crisp and readable.",
    body: (
      <>
        <h2 className="text-2xl font-bold mt-8 mb-4">Hello World</h2>
        <pre className="bg-[#0d0d0d] p-4 rounded-lg border border-white/10 overflow-x-auto mb-6">
          <code className="text-sm font-mono text-zinc-300">
{n main() -> Void
do
    print("Hello, AAYU World!").
end.}
          </code>
        </pre>
        <p className="mb-4">Notice the use of <code>do ... end.</code> blocks and the <code>.</code> (dot) as a statement terminator instead of a semicolon. This forces cleaner, more sentence-like structures.</p>
      </>
    )
  },
  "variables": {
    title: "Variables & Mutability",
    description: "AAYU variables are immutable by default to prevent unintended side effects in concurrent environments.",
    body: (
      <>
        <h2 className="text-2xl font-bold mt-8 mb-4">Declaring Variables</h2>
        <p className="mb-4">Use the <code>let</code> keyword. Types are inferred automatically, but you can explicitly type them.</p>
        <pre className="bg-[#0d0d0d] p-4 rounded-lg border border-white/10 overflow-x-auto mb-6">
          <code className="text-sm font-mono text-zinc-300">
{// Immutable by default
let name = "AAYU".
let version: Number = 1.0.

// Mutable variable requires 'mut'
let mut counter = 0.
counter = counter + 1.}
          </code>
        </pre>
      </>
    )
  },
  "compiler": {
    title: "Compiler Pipeline",
    description: "Deep dive into AAYU's multi-stage compiler architecture.",
    body: (
      <>
        <h2 className="text-2xl font-bold mt-8 mb-4">The Pipeline</h2>
        <p className="mb-4">The AAYU Compiler (ayuc) doesn\\'t just turn text into machine code. It routes through the <strong>Intent Engine</strong>.</p>
        <ol className="list-decimal pl-6 space-y-3 mb-6">
          <li><strong>Lexical Analysis:</strong> Standard tokenization of *.aayu source files.</li>
          <li><strong>Parser & AST Generation:</strong> Construction of the Abstract Syntax Tree.</li>
          <li><strong>Intent Extraction (BrainOS hook):</strong> The AST is passed to BrainOS to map high-level entity declarations into the Architecture Graph.</li>
          <li><strong>Semantic Analysis:</strong> Type checking, trait resolution, and mutability validation.</li>
          <li><strong>Bytecode Generation:</strong> Conversion to AAYU Intermediate Representation (IR).</li>
          <li><strong>LLVM Lowering:</strong> LLVM backend optimization and binary generation.</li>
        </ol>
      </>
    )
  },
  "runtime": {
    title: "Runtime & VM",
    description: "How AAYU executes your code in production environments.",
    body: (
      <>
        <h2 className="text-2xl font-bold mt-8 mb-4">Memory Management</h2>
        <p className="mb-4">AAYU uses <strong>Deterministic ARC</strong> (Automatic Reference Counting) coupled with a cycle detector. There is no heavy Tracing Garbage Collector pausing your threads.</p>
        <h2 className="text-2xl font-bold mt-8 mb-4">Concurrency Model</h2>
        <p className="mb-4">AAYU utilizes <strong>Fibers</strong>—lightweight, green threads multiplexed over OS threads via a work-stealing scheduler.</p>
      </>
    )
  }
};

// Fallback generator for missing pages
const generateFallback = (slug: string) => ({
  title: slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
  description: \In-depth technical documentation for \ is being compiled.\,
  body: (
    <>
      <p className="mb-4">This section of the AAYU Language Portal covers the internal mechanisms and usage patterns for <strong>{slug}</strong>.</p>
      <div className="bg-yellow-500/10 border border-yellow-500/20 text-yellow-500 p-4 rounded-lg my-6 flex items-start gap-3">
        <span>🚧</span>
        <p className="text-sm">We are actively migrating the BrainOS knowledge graph documentation to this portal. Check back in the next nightly release for the full technical deep-dive.</p>
      </div>
    </>
  )
});

export function getAllLanguageSlugs(): string[] {
  const slugs: string[] = [];
  languageNavData.forEach(section => {
    section.items.forEach(item => {
      slugs.push(item.slug);
    });
  });
  return slugs;
}

export function getLanguageDocContent(slug: string): ContentItem | null {
  const slugs = getAllLanguageSlugs();
  const index = slugs.indexOf(slug);
  
  if (index === -1) return null;
  
  const rawData = DOCS_DB[slug] || generateFallback(slug);
  
  let prev = undefined;
  let next = undefined;
  
  if (index > 0) {
    const prevSlug = slugs[index - 1];
    prev = { slug: prevSlug, title: prevSlug.replace(/-/g, ' ') };
  }
  
  if (index < slugs.length - 1) {
    const nextSlug = slugs[index + 1];
    next = { slug: nextSlug, title: nextSlug.replace(/-/g, ' ') };
  }
  
  return {
    title: rawData.title as string,
    description: rawData.description as string,
    body: rawData.body,
    prev,
    next
  };
}
'''

with open(os.path.join(base_dir, 'language-content.tsx'), 'w', encoding='utf-8') as f:
    f.write(content)

print("Generated technical content engine.")
