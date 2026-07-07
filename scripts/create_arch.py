import os

base_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\architecture'
os.makedirs(base_dir, exist_ok=True)

arch_code = '''
"use client";

import { useState } from "react";
import { Code2, AlignLeft, Network, ShieldCheck, Zap, Cpu, Terminal, ArrowDown, ChevronRight, Binary } from "lucide-react";

const PIPELINE = [
  {
    id: "compiler",
    title: "1. AAYU Compiler CLI",
    icon: Terminal,
    color: "text-zinc-400",
    bg: "bg-zinc-900",
    desc: "The entry point. Receives raw source code or Intent Graph artifacts from BrainOS.",
    details: [
      "Zero-dependency static binary.",
      "Handles workspace resolution via aayu.mod.",
      "Initiates the compilation pipeline."
    ]
  },
  {
    id: "parser",
    title: "2. Lexer & Parser",
    icon: AlignLeft,
    color: "text-blue-400",
    bg: "bg-blue-900/30",
    desc: "Transforms raw AAYU syntax into a stream of tokens, then into an Initial Syntax Tree.",
    details: [
      "Whitespace-aware but dot-terminated syntax.",
      "Hand-written Recursive Descent Parser for maximum speed.",
      "Generates strict SyntaxError diagnostics with exact spans."
    ]
  },
  {
    id: "ast",
    title: "3. Abstract Syntax Tree (AST)",
    icon: Network,
    color: "text-purple-400",
    bg: "bg-purple-900/30",
    desc: "The structured representation of the code logic.",
    details: [
      "Nodes for Entity, Trait, Extension, and Function declarations.",
      "Preserves original spans for accurate debugger mapping.",
      "Can be visualized using 'aayu build --emit-ast'."
    ]
  },
  {
    id: "semantic",
    title: "4. Semantic & Type Analyzer",
    icon: ShieldCheck,
    color: "text-emerald-400",
    bg: "bg-emerald-900/30",
    desc: "Enforces strict type safety, validates lifetimes, and resolves symbols.",
    details: [
      "No implicit coercion. Strong typing enforced.",
      "Verifies Trait implementation compliance.",
      "Symbol Table generation and scoping rules."
    ]
  },
  {
    id: "optimizer",
    title: "5. Intent Optimizer",
    icon: Zap,
    color: "text-yellow-400",
    bg: "bg-yellow-900/30",
    desc: "High-level optimizations before lowering.",
    details: [
      "Constant folding and propagation.",
      "Dead code elimination at the module level.",
      "Inlines small functions to reduce call overhead."
    ]
  },
  {
    id: "llvm",
    title: "6. LLVM IR Lowering",
    icon: Cpu,
    color: "text-orange-400",
    bg: "bg-orange-900/30",
    desc: "Translates the optimized AST into LLVM Intermediate Representation.",
    details: [
      "Maps AAYU types directly to LLVM native types.",
      "Injects Deterministic ARC (Automatic Reference Counting) instructions.",
      "Leverages LLVM Pass Manager for aggressive O3 optimizations."
    ]
  },
  {
    id: "bytecode",
    title: "7. Target Generation",
    icon: Binary,
    color: "text-red-400",
    bg: "bg-red-900/30",
    desc: "Emits the final binary executable or AAYU Bytecode for the VM.",
    details: [
      "Can emit a standalone executable (.exe, ELF, Mach-O).",
      "Can emit .aayubc for the cross-platform AAYU VM.",
      "Strips debug symbols in release mode for tiny binaries."
    ]
  }
];

export default function ArchitecturePage() {
  const [activeId, setActiveId] = useState(PIPELINE[0].id);

  const activeStage = PIPELINE.find(p => p.id === activeId);

  return (
    <main className="min-h-screen bg-black text-white pt-24 pb-20">
      <div className="container mx-auto px-4 max-w-7xl">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4 text-transparent bg-clip-text bg-gradient-to-r from-zinc-200 to-zinc-500">
            Internal Architecture
          </h1>
          <p className="text-xl text-zinc-400 max-w-2xl mx-auto">
            Explore the complete compilation and execution pipeline of the AAYU Language.
          </p>
        </div>

        <div className="grid lg:grid-cols-12 gap-8 md:gap-12">
          
          {/* Left: Pipeline Flow */}
          <div className="lg:col-span-5 relative flex flex-col items-center">
            {/* Connecting line */}
            <div className="absolute top-8 bottom-8 w-px bg-white/10 left-1/2 -translate-x-1/2 z-0" />
            
            <div className="space-y-4 relative z-10 w-full">
              {PIPELINE.map((stage) => {
                const isActive = stage.id === activeId;
                return (
                  <div key={stage.id} className="flex flex-col items-center w-full">
                    <button 
                      onClick={() => setActiveId(stage.id)}
                      className={lex items-center w-full max-w-sm p-4 rounded-xl border transition-all duration-300 \}
                    >
                      <div className={w-12 h-12 rounded-lg flex items-center justify-center mr-4 \ border border-white/10}>
                        <stage.icon className={w-6 h-6 \} />
                      </div>
                      <div className="text-left flex-1">
                        <div className={ont-bold \}>
                          {stage.title}
                        </div>
                      </div>
                      <ChevronRight className={w-5 h-5 transition-transform \} />
                    </button>
                    {stage.id !== PIPELINE[PIPELINE.length - 1].id && (
                      <ArrowDown className="w-5 h-5 text-white/20 my-2" />
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Right: Detailed View */}
          <div className="lg:col-span-7">
            <div className="sticky top-32 bg-[#0a0a0a] border border-white/10 rounded-2xl p-8 min-h-[400px] shadow-2xl">
              {activeStage && (
                <div className="animate-in fade-in slide-in-from-right-4 duration-500">
                  <div className={w-16 h-16 rounded-2xl flex items-center justify-center mb-6 \ border border-white/10}>
                    <activeStage.icon className={w-8 h-8 \} />
                  </div>
                  <h2 className="text-3xl font-bold mb-4">{activeStage.title}</h2>
                  <p className="text-xl text-zinc-400 mb-8 leading-relaxed">
                    {activeStage.desc}
                  </p>
                  
                  <div className="space-y-4">
                    <h4 className="text-sm font-bold text-zinc-500 uppercase tracking-widest border-b border-white/10 pb-2">Technical Details</h4>
                    <ul className="space-y-4">
                      {activeStage.details.map((detail, idx) => (
                        <li key={idx} className="flex items-start gap-3 text-zinc-300 bg-white/5 p-4 rounded-xl border border-white/5">
                          <CheckIcon className="w-5 h-5 text-green-500 shrink-0 mt-0.5" />
                          <span className="leading-relaxed">{detail}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>
          </div>

        </div>
      </div>
    </main>
  );
}

function CheckIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
    </svg>
  );
}
'''

with open(os.path.join(base_dir, 'page.tsx'), 'w', encoding='utf-8') as f:
    f.write(arch_code)

print("Created Architecture page.")
