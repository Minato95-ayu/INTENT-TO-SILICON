import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\page.tsx'

content = '''
"use client";

import Link from "next/link";
import { ArrowRight, Code2, Brain, Terminal, Database, FileJson, Play, LayoutPanelLeft, Search, Download, ChevronRight, Hash, Network, ListTree, Zap, ShieldCheck, Activity } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";

export default function DeveloperDashboard() {
  const [intentInput, setIntentInput] = useState("");
  const [isBuilding, setIsBuilding] = useState(false);
  const [buildStage, setBuildStage] = useState(0);

  const handleBuild = () => {
    if (!intentInput.trim()) return;
    setIsBuilding(true);
    setBuildStage(1);
    setTimeout(() => setBuildStage(2), 1500);
    setTimeout(() => setBuildStage(3), 3000);
    setTimeout(() => setBuildStage(4), 4500);
    setTimeout(() => {
      setIsBuilding(false);
    }, 6000);
  };

  return (
    <main className="min-h-screen bg-[#000000] text-white pt-20 selection:bg-purple-500/30">
      
      {/* 
        ========================================================================
        HERO: LIVE BRAINOS GENERATOR
        ========================================================================
      */}
      <section className="container mx-auto px-4 max-w-6xl mb-24 relative">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-purple-900/20 rounded-full blur-[120px] pointer-events-none" />
        
        <div className="text-center mb-12 relative z-10">
          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-4">
            Build Production Software <br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400">From Human Intent.</span>
          </h1>
          <p className="text-lg text-zinc-400 max-w-2xl mx-auto mb-8">
            The AI-Native Developer Operating System. No manual boilerplate. Pure algorithmic scaffolding compiled directly to LLVM.
          </p>
          
          <div className="max-w-3xl mx-auto bg-[#0a0a0a] border border-white/10 rounded-2xl p-4 shadow-2xl relative">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-500 to-blue-500 rounded-2xl blur opacity-20 pointer-events-none"></div>
            <div className="relative flex flex-col md:flex-row gap-4">
              <input 
                type="text"
                value={intentInput}
                onChange={(e) => setIntentInput(e.target.value)}
                disabled={isBuilding}
                placeholder="E.g., Build a highly scalable Banking Core..."
                className="flex-1 bg-[#111] border border-white/5 rounded-xl px-4 py-4 text-white outline-none focus:border-purple-500/50"
              />
              <Button onClick={handleBuild} disabled={isBuilding || !intentInput} className="h-auto px-8 bg-white text-black hover:bg-zinc-200 font-bold text-lg rounded-xl">
                {isBuilding ? "Architecting..." : "Generate"}
              </Button>
            </div>
            
            {/* Live Pipeline Animation */}
            {buildStage > 0 && (
              <div className="mt-8 pt-8 border-t border-white/10 grid grid-cols-4 gap-4 text-center animate-in fade-in slide-in-from-top-4">
                <div className={	ransition-opacity duration-500 \}>
                  <div className="w-12 h-12 mx-auto bg-blue-900/30 border border-blue-500/50 rounded-full flex items-center justify-center mb-2">
                    <Database className="w-5 h-5 text-blue-400" />
                  </div>
                  <span className="text-xs font-bold text-zinc-300">1. Intent IR</span>
                </div>
                <div className={	ransition-opacity duration-500 \}>
                  <div className="w-12 h-12 mx-auto bg-purple-900/30 border border-purple-500/50 rounded-full flex items-center justify-center mb-2">
                    <Brain className="w-5 h-5 text-purple-400" />
                  </div>
                  <span className="text-xs font-bold text-zinc-300">2. BrainOS Tradeoffs</span>
                </div>
                <div className={	ransition-opacity duration-500 \}>
                  <div className="w-12 h-12 mx-auto bg-orange-900/30 border border-orange-500/50 rounded-full flex items-center justify-center mb-2">
                    <Code2 className="w-5 h-5 text-orange-400" />
                  </div>
                  <span className="text-xs font-bold text-zinc-300">3. AAYU Scaffolding</span>
                </div>
                <div className={	ransition-opacity duration-500 \}>
                  <div className="w-12 h-12 mx-auto bg-emerald-900/30 border border-emerald-500/50 rounded-full flex items-center justify-center mb-2">
                    <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                  </div>
                  {buildStage === 4 ? (
                    <Link href="/brainos/live" className="text-xs font-bold text-white bg-white/20 px-2 py-1 rounded">View Report ➔</Link>
                  ) : (
                    <span className="text-xs font-bold text-zinc-300">4. LLVM Ready</span>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* 
        ========================================================================
        DASHBOARD GRID
        ========================================================================
      */}
      <section className="container mx-auto px-4 max-w-7xl pb-24">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
          
          {/* Quick Actions (Col span 3) */}
          <div className="md:col-span-3 space-y-6">
            
            {/* Install Command */}
            <div className="bg-[#0a0a0a] border border-white/10 p-5 rounded-2xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-24 h-24 bg-green-500/10 blur-2xl rounded-full" />
              <h3 className="text-sm font-bold text-zinc-400 mb-3 uppercase tracking-wider">Install CLI</h3>
              <div className="bg-black border border-white/10 rounded-lg p-3 flex justify-between items-center cursor-pointer hover:border-green-500/50 transition-colors">
                <code className="text-sm text-green-400">curl -fsSL aayu.dev | bash</code>
                <Download className="w-4 h-4 text-zinc-500" />
              </div>
              <p className="text-xs text-zinc-500 mt-3">v0.1.0-alpha (macOS, Linux, WSL)</p>
            </div>

            {/* Docs Search */}
            <div className="bg-[#0a0a0a] border border-white/10 p-5 rounded-2xl">
              <h3 className="text-sm font-bold text-zinc-400 mb-3 uppercase tracking-wider">Documentation</h3>
              <Link href="/docs">
                <div className="bg-black border border-white/10 rounded-lg p-3 flex justify-between items-center text-sm text-zinc-500 hover:border-blue-500/50 hover:text-white transition-colors cursor-pointer">
                  <div className="flex items-center gap-2"><Search className="w-4 h-4"/> Search Docs...</div>
                  <span className="font-mono text-[10px] bg-white/10 px-1 rounded">⌘K</span>
                </div>
              </Link>
              <div className="mt-4 flex flex-wrap gap-2">
                <Link href="/docs/language/syntax" className="text-xs bg-white/5 hover:bg-white/10 px-2 py-1 rounded text-zinc-300">Syntax</Link>
                <Link href="/docs/compiler/ast" className="text-xs bg-white/5 hover:bg-white/10 px-2 py-1 rounded text-zinc-300">AST</Link>
                <Link href="/docs/runtime/memory" className="text-xs bg-white/5 hover:bg-white/10 px-2 py-1 rounded text-zinc-300">Memory</Link>
              </div>
            </div>
            
            {/* Recent Releases */}
            <div className="bg-[#0a0a0a] border border-white/10 p-5 rounded-2xl">
              <h3 className="text-sm font-bold text-zinc-400 mb-3 uppercase tracking-wider">Releases</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-blue-500"/> v0.1.0-alpha</span>
                  <span className="text-zinc-500 text-xs">Latest</span>
                </div>
                <div className="flex items-center justify-between text-sm opacity-50">
                  <span className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-purple-500"/> nightly-build</span>
                  <span className="text-zinc-500 text-xs">Today</span>
                </div>
              </div>
            </div>

          </div>

          {/* Main Playground Preview (Col span 9) */}
          <div className="md:col-span-9 bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden flex flex-col group">
            <div className="flex items-center justify-between px-4 py-3 bg-[#111] border-b border-white/5">
              <div className="flex items-center gap-2">
                <LayoutPanelLeft className="w-4 h-4 text-blue-400" />
                <span className="text-sm font-bold text-zinc-300">Interactive Playground</span>
              </div>
              <Link href="/playground">
                <Button size="sm" variant="outline" className="h-7 text-xs border-white/10 bg-transparent hover:bg-white/10 hover:text-white">
                  Open IDE <ArrowRight className="w-3 h-3 ml-1" />
                </Button>
              </Link>
            </div>
            
            <div className="flex-1 flex flex-col md:flex-row min-h-[400px]">
              {/* Code */}
              <div className="flex-1 p-4 border-r border-white/5 font-mono text-sm leading-relaxed text-zinc-300 relative">
                <div className="text-zinc-600 mb-2">// Build your logic here</div>
                <div className="text-blue-400">entity <span className="text-white">User</span></div>
                <div className="text-blue-400">has</div>
                <div className="pl-4">id: <span className="text-emerald-400">Number</span></div>
                <div className="pl-4">name: <span className="text-emerald-400">Text</span></div>
                <div className="text-blue-400">end.</div>
                
                <div className="absolute inset-0 bg-gradient-to-t from-[#0a0a0a] to-transparent pointer-events-none" />
              </div>
              
              {/* Pipeline Output preview */}
              <div className="flex-1 bg-black p-4 relative overflow-hidden">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(59,130,246,0.1)_0%,transparent_70%)]" />
                <h4 className="text-xs font-bold text-zinc-500 uppercase tracking-widest mb-4">Compiler Pipeline</h4>
                
                <div className="space-y-4 relative z-10">
                  <div className="flex items-center gap-3 text-sm text-zinc-400">
                    <ListTree className="w-4 h-4 text-blue-400" /> AST Generation <span className="text-green-500 ml-auto">0.2ms</span>
                  </div>
                  <div className="w-0.5 h-4 bg-white/10 ml-1.5" />
                  <div className="flex items-center gap-3 text-sm text-zinc-400">
                    <ShieldCheck className="w-4 h-4 text-emerald-400" /> Semantic Check <span className="text-green-500 ml-auto">1.1ms</span>
                  </div>
                  <div className="w-0.5 h-4 bg-white/10 ml-1.5" />
                  <div className="flex items-center gap-3 text-sm text-zinc-400">
                    <Zap className="w-4 h-4 text-yellow-400" /> LLVM Optimization <span className="text-green-500 ml-auto">2.4ms</span>
                  </div>
                  <div className="w-0.5 h-4 bg-white/10 ml-1.5" />
                  <div className="flex items-center gap-3 text-sm text-zinc-400">
                    <Terminal className="w-4 h-4 text-orange-400" /> Native Binary <span className="text-green-500 ml-auto">0.8ms</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Examples Grid (Col span 12) */}
          <div className="md:col-span-12 mt-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">Production Examples</h2>
              <Link href="/examples" className="text-blue-400 hover:text-blue-300 text-sm font-bold flex items-center gap-1">
                View All <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {['Banking Core', 'Hospital ERP', 'AI Agent Engine', 'E-Commerce Core'].map((name, i) => (
                <div key={i} className="bg-[#0a0a0a] border border-white/10 p-4 rounded-xl hover:border-blue-500/50 transition-colors cursor-pointer group">
                  <FileJson className="w-6 h-6 text-blue-400 mb-3 group-hover:scale-110 transition-transform" />
                  <h4 className="font-bold text-sm text-zinc-200">{name}</h4>
                  <p className="text-xs text-zinc-500 mt-1">Full Architecture & Source</p>
                </div>
              ))}
            </div>
          </div>

        </div>
      </section>

    </main>
  );
}

function CheckCircle2(props: any) {
  return (
    <svg {...props} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
    </svg>
  );
}
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated Homepage to Developer OS Dashboard.")
