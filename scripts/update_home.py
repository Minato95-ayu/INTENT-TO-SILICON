import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\page.tsx'

home_code = '''
"use client";

import Link from "next/link";
import { ArrowRight, Brain, Code2, Server, Cpu, Database, Zap, Layers, Network } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white selection:bg-blue-500/30 overflow-hidden pt-16">
      
      {/* 
        ========================================================================
        HERO SECTION: THE AAYU PIPELINE ANIMATION
        Human Thought -> Intent Engine -> BrainOS -> Architecture -> AAYU Language -> Compiler -> Runtime -> Production
        ========================================================================
      */}
      <section className="relative pt-20 pb-24 md:pt-32 md:pb-32 overflow-hidden flex flex-col items-center">
        {/* Background glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-500/10 rounded-full blur-[120px] pointer-events-none opacity-50" />
        
        <div className="container mx-auto px-4 relative z-10 text-center">
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6">
            The Autonomous <br className="hidden md:block"/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-emerald-400">
              Developer Operating System
            </span>
          </h1>
          <p className="text-xl md:text-2xl text-zinc-400 max-w-3xl mx-auto mb-16 leading-relaxed">
            AAYU bridges the gap between human intent and production software. It's not just a language; it's an AI-native ecosystem.
          </p>

          {/* Interactive Flow Diagram */}
          <div className="w-full max-w-6xl mx-auto bg-[#0a0a0a] border border-white/10 p-6 md:p-12 rounded-2xl shadow-2xl overflow-x-auto">
            <div className="flex flex-col md:flex-row items-center justify-between min-w-[800px] gap-4">
              
              {/* Human Thought */}
              <div className="flex flex-col items-center group">
                <div className="w-16 h-16 rounded-full bg-zinc-900 border border-zinc-700 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <span className="text-2xl">🤔</span>
                </div>
                <span className="text-sm font-bold text-zinc-300 whitespace-nowrap">Human Thought</span>
              </div>

              <div className="hidden md:flex flex-1 h-px bg-gradient-to-r from-zinc-700 to-blue-500 relative">
                <div className="absolute top-1/2 left-0 -translate-y-1/2 w-2 h-2 bg-blue-400 rounded-full animate-ping" />
              </div>

              {/* Intent Engine */}
              <div className="flex flex-col items-center group">
                <Link href="/intent-engine">
                  <div className="w-16 h-16 rounded-full bg-blue-900/30 border border-blue-500/50 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform group-hover:bg-blue-600">
                    <Layers className="w-8 h-8 text-blue-400 group-hover:text-white" />
                  </div>
                </Link>
                <span className="text-sm font-bold text-blue-300 whitespace-nowrap">Intent Engine</span>
              </div>

              <div className="hidden md:flex flex-1 h-px bg-gradient-to-r from-blue-500 to-purple-500 relative">
                <div className="absolute top-1/2 left-0 -translate-y-1/2 w-2 h-2 bg-purple-400 rounded-full animate-ping" style={{animationDelay: "200ms"}} />
              </div>

              {/* BrainOS */}
              <div className="flex flex-col items-center group">
                <Link href="/brainos">
                  <div className="w-20 h-20 rounded-full bg-purple-900/30 border border-purple-500/50 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform shadow-[0_0_30px_rgba(168,85,247,0.4)] group-hover:bg-purple-600">
                    <Brain className="w-10 h-10 text-purple-400 group-hover:text-white" />
                  </div>
                </Link>
                <span className="text-sm font-bold text-purple-300 whitespace-nowrap">BrainOS</span>
              </div>

              <div className="hidden md:flex flex-1 h-px bg-gradient-to-r from-purple-500 to-emerald-500 relative">
                <div className="absolute top-1/2 left-0 -translate-y-1/2 w-2 h-2 bg-emerald-400 rounded-full animate-ping" style={{animationDelay: "400ms"}} />
              </div>

              {/* Architecture */}
              <div className="flex flex-col items-center group">
                <Link href="/architecture">
                  <div className="w-16 h-16 rounded-full bg-emerald-900/30 border border-emerald-500/50 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform group-hover:bg-emerald-600">
                    <Network className="w-8 h-8 text-emerald-400 group-hover:text-white" />
                  </div>
                </Link>
                <span className="text-sm font-bold text-emerald-300 whitespace-nowrap">Architecture</span>
              </div>

              <div className="hidden md:flex flex-1 h-px bg-gradient-to-r from-emerald-500 to-orange-500 relative">
                <div className="absolute top-1/2 left-0 -translate-y-1/2 w-2 h-2 bg-orange-400 rounded-full animate-ping" style={{animationDelay: "600ms"}} />
              </div>

              {/* AAYU Language */}
              <div className="flex flex-col items-center group">
                <Link href="/language">
                  <div className="w-16 h-16 rounded-full bg-orange-900/30 border border-orange-500/50 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform group-hover:bg-orange-600">
                    <Code2 className="w-8 h-8 text-orange-400 group-hover:text-white" />
                  </div>
                </Link>
                <span className="text-sm font-bold text-orange-300 whitespace-nowrap">AAYU Language</span>
              </div>

              <div className="hidden md:flex flex-1 h-px bg-gradient-to-r from-orange-500 to-zinc-700 relative">
                <div className="absolute top-1/2 left-0 -translate-y-1/2 w-2 h-2 bg-zinc-400 rounded-full animate-ping" style={{animationDelay: "800ms"}} />
              </div>

              {/* Production */}
              <div className="flex flex-col items-center group">
                <div className="w-16 h-16 rounded-full bg-zinc-900 border border-zinc-700 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <Server className="w-8 h-8 text-white" />
                </div>
                <span className="text-sm font-bold text-white whitespace-nowrap">Production Code</span>
              </div>

            </div>
          </div>
          
          <div className="mt-12 flex flex-wrap justify-center gap-4">
            <Link href="/brainos/live">
              <button className="px-8 py-4 bg-white text-black rounded-full font-bold text-lg hover:bg-zinc-200 transition-colors flex items-center gap-2">
                Try Live Demo <ArrowRight className="w-5 h-5" />
              </button>
            </Link>
            <Link href="/download">
              <button className="px-8 py-4 bg-transparent border border-white/20 text-white rounded-full font-bold text-lg hover:bg-white/5 transition-colors">
                Download CLI
              </button>
            </Link>
          </div>
        </div>
      </section>

      {/* 
        ========================================================================
        THE 3 IDENTITIES SECTION
        ========================================================================
      */}
      <section className="py-24 border-t border-white/10 bg-[#050505]">
        <div className="container mx-auto px-4 max-w-7xl">
          <h2 className="text-3xl md:text-5xl font-bold mb-16 text-center">The Three Pillars of AAYU</h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* Intent Engine */}
            <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl hover:border-blue-500/50 transition-colors flex flex-col h-full">
              <div className="w-14 h-14 bg-blue-900/30 rounded-xl flex items-center justify-center mb-6">
                <Layers className="w-8 h-8 text-blue-400" />
              </div>
              <h3 className="text-2xl font-bold mb-4">Intent Engine</h3>
              <p className="text-zinc-400 mb-8 flex-1 leading-relaxed">
                Transforms raw human thought and domain requirements into structured, parseable Intent IR. It understands your business logic before any code is written.
              </p>
              <div className="space-y-3 mb-8">
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> Offline NLP Parsing</div>
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> Intent Graph Generation</div>
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> Multi-Domain Knowledge Base</div>
              </div>
              <Link href="/intent-engine">
                <button className="w-full py-3 bg-blue-600 hover:bg-blue-500 rounded-lg font-semibold transition-colors">
                  Explore Intent Engine
                </button>
              </Link>
            </div>

            {/* BrainOS */}
            <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl hover:border-purple-500/50 transition-colors relative flex flex-col h-full transform md:-translate-y-4 shadow-2xl shadow-purple-900/10">
              <div className="absolute top-0 right-0 px-3 py-1 bg-purple-500 text-white text-xs font-bold rounded-bl-lg rounded-tr-xl">CORE</div>
              <div className="w-14 h-14 bg-purple-900/30 rounded-xl flex items-center justify-center mb-6">
                <Brain className="w-8 h-8 text-purple-400" />
              </div>
              <h3 className="text-2xl font-bold mb-4">BrainOS</h3>
              <p className="text-zinc-400 mb-8 flex-1 leading-relaxed">
                The autonomous software architect. It analyzes your Intent Graph, evaluates tradeoffs, recommends architectures, and scaffolds the production-ready AAYU codebase.
              </p>
              <div className="space-y-3 mb-8">
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> Rule-Based Decision Engine</div>
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> Architecture Tradeoff Evaluator</div>
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> Automated Project Scaffolding</div>
              </div>
              <Link href="/brainos">
                <button className="w-full py-3 bg-purple-600 hover:bg-purple-500 rounded-lg font-semibold transition-colors">
                  Explore BrainOS
                </button>
              </Link>
            </div>

            {/* AAYU Language */}
            <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl hover:border-orange-500/50 transition-colors flex flex-col h-full">
              <div className="w-14 h-14 bg-orange-900/30 rounded-xl flex items-center justify-center mb-6">
                <Code2 className="w-8 h-8 text-orange-400" />
              </div>
              <h3 className="text-2xl font-bold mb-4">AAYU Language</h3>
              <p className="text-zinc-400 mb-8 flex-1 leading-relaxed">
                A blazingly fast, statically typed systems language. Compiled via LLVM with Deterministic ARC. The ultimate target for BrainOS generated code.
              </p>
              <div className="space-y-3 mb-8">
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> Deterministic ARC Memory</div>
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> Fast LLVM Backend Optimizer</div>
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> Built-in Package Manager (apm)</div>
              </div>
              <Link href="/language">
                <button className="w-full py-3 bg-orange-600 hover:bg-orange-500 rounded-lg font-semibold transition-colors">
                  Explore Language
                </button>
              </Link>
            </div>
          </div>
        </div>
      </section>

    </main>
  );
}

function CheckIcon() {
  return (
    <svg className="w-4 h-4 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
    </svg>
  );
}
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(home_code)

print("Updated page.tsx with interactive hero and 3 identities.")
