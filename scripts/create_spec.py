"""
=============================================================================
FILE: create_spec.py
PURPOSE: Generates language specification
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles generates language specification.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os

base_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\spec'
os.makedirs(base_dir, exist_ok=True)

spec_code = '''
"use client";

import { BookOpen, FileCode2, Binary, Cpu, Server, CheckCircle2, ChevronRight } from "lucide-react";
import Link from "next/link";

const SPECS = [
  {
    title: "Language Grammar",
    icon: FileCode2,
    items: ["Lexical Structure", "Keywords & Operators", "Expressions & Statements", "Intent Declarations"]
  },
  {
    title: "Intermediate Representations",
    icon: Binary,
    items: ["Abstract Syntax Tree (AST)", "Intent Graph IR", "AAYU Bytecode ISA", "LLVM Lowering Rules"]
  },
  {
    title: "VM & Runtime",
    icon: Cpu,
    items: ["Deterministic ARC Memory Model", "Fiber Scheduler", "Foreign Function Interface (FFI)", "Standard Library ABIs"]
  },
  {
    title: "BrainOS Architecture",
    icon: Server,
    items: ["Rule-Based Decision Engine", "Tradeoff Evaluator", "Knowledge Base Formats", "Production Readiness Metrics"]
  }
];

export default function SpecPage() {
  return (
    <main className="min-h-screen bg-black text-white pt-24 pb-20">
      <div className="container mx-auto px-4 max-w-5xl">
        <div className="mb-16 text-center">
          <div className="flex justify-center mb-6">
            <div className="p-4 rounded-full bg-blue-500/10 border border-blue-500/20">
              <BookOpen className="w-12 h-12 text-blue-400" />
            </div>
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
            Language Specification
          </h1>
          <p className="text-xl text-zinc-400 max-w-2xl mx-auto">
            The formal, definitive reference for the AAYU Language, Compiler, Runtime, and BrainOS Ecosystem.
          </p>
        </div>

        <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-8 mb-16 shadow-2xl">
          <div className="flex items-start gap-4 mb-8 border-b border-white/10 pb-6">
            <CheckCircle2 className="w-8 h-8 text-green-500 shrink-0 mt-1" />
            <div>
              <h2 className="text-2xl font-bold mb-2">Version 1.0 (Draft)</h2>
              <p className="text-zinc-400 leading-relaxed">
                This specification is currently in Draft state for the upcoming v1.0 release. It is intended for compiler engineers, toolchain authors, and advanced developers who need to understand the exact mechanics of the language.
              </p>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {SPECS.map((spec, i) => (
              <div key={i} className="group">
                <h3 className="text-xl font-bold mb-4 flex items-center gap-3 text-white group-hover:text-blue-400 transition-colors">
                  <spec.icon className="w-5 h-5" />
                  {spec.title}
                </h3>
                <ul className="space-y-2 pl-8 border-l border-white/10 ml-2">
                  {spec.items.map((item, j) => (
                    <li key={j}>
                      <Link href="#" className="flex items-center justify-between text-zinc-400 hover:text-white transition-colors py-1 group/link">
                        <span>{item}</span>
                        <ChevronRight className="w-4 h-4 opacity-0 group-hover/link:opacity-100 transition-opacity text-blue-500" />
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
        
        <div className="text-center">
          <p className="text-zinc-500 text-sm">Full PDF Specification will be available upon the v1.0 stable release.</p>
        </div>
      </div>
    </main>
  );
}
'''

with open(os.path.join(base_dir, 'page.tsx'), 'w', encoding='utf-8') as f:
    f.write(spec_code)

print("Created Spec page.")
