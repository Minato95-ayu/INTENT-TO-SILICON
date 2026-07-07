import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\docs\page.tsx'

content = '''
"use client";

import Link from "next/link";
import { BookOpen, Code2, Bot, Box, ArrowRight, Activity, Terminal } from "lucide-react";

const DOCS_CATEGORIES = [
  {
    title: "Getting Started",
    icon: BookOpen,
    desc: "Install AAYU and write your first Hello World.",
    href: "/docs/getting-started/installation"
  },
  {
    title: "Language Guide",
    icon: Code2,
    desc: "Learn AAYU's syntax, variables, functions, and generics.",
    href: "/docs/language/syntax"
  },
  {
    title: "Compiler Architecture",
    icon: Box,
    desc: "Deep dive into Lexer, Parser, AST, and LLVM Lowering.",
    href: "/docs/compiler/lexer"
  },
  {
    title: "BrainOS Orchestrator",
    icon: Bot,
    desc: "Understand how BrainOS scaffolds and architects code.",
    href: "/docs/brainos/orchestrator"
  },
  {
    title: "Runtime & Memory",
    icon: Activity,
    desc: "Learn how Deterministic ARC manages memory safely.",
    href: "/docs/runtime/memory"
  },
  {
    title: "CLI Reference",
    icon: Terminal,
    desc: "Explore aayu build, run, and apm package manager.",
    href: "/docs/cli"
  }
];

export default function DocsHomepage() {
  return (
    <>
      <h1 className="text-4xl font-extrabold mb-4">AAYU Documentation</h1>
      <p className="text-xl text-zinc-400 mb-12">
        Welcome to the official documentation for the AAYU Language and the BrainOS ecosystem.
      </p>

      <div className="grid md:grid-cols-2 gap-6">
        {DOCS_CATEGORIES.map((cat, i) => (
          <Link key={i} href={cat.href} className="group p-6 bg-[#111] border border-white/10 rounded-2xl hover:border-blue-500/50 hover:bg-[#151515] transition-all">
            <div className="w-12 h-12 bg-[#1a1a1a] rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <cat.icon className="w-6 h-6 text-blue-400" />
            </div>
            <h2 className="text-xl font-bold mb-2 flex items-center gap-2">
              {cat.title} <ArrowRight className="w-4 h-4 opacity-0 -ml-2 group-hover:opacity-100 group-hover:ml-0 transition-all text-blue-400" />
            </h2>
            <p className="text-zinc-400 text-sm">
              {cat.desc}
            </p>
          </Link>
        ))}
      </div>
    </>
  );
}
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Created Docs Homepage.")
