import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\page.tsx'

content = '''
"use client";

import Link from "next/link";
import { ArrowRight, Code2, Brain, Network, Cpu, Server, Layers, Terminal, Database, ShieldCheck, CheckCircle2, Loader2, Play } from "lucide-react";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";

export default function Home() {
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
    setTimeout(() => setBuildStage(5), 6000);
    setTimeout(() => {
      setIsBuilding(false);
    }, 7500);
  };

  return (
    <main className="min-h-screen bg-black text-white selection:bg-purple-500/30">
      
      {/* 
        ========================================================================
        HERO & LIVE PROJECT GENERATOR
        ========================================================================
      */}
      <section className="relative pt-32 pb-12 overflow-hidden">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-purple-900/20 rounded-full blur-[120px] pointer-events-none" />
        
        <div className="container mx-auto px-4 relative z-10 max-w-6xl">
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-sm font-medium text-zinc-300 mb-8">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              AAYU v0.1.0-alpha is now available
            </div>
            
            <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-b from-white to-white/60">
              The AI-Native <br className="hidden md:block" />
              Developer Platform
            </h1>
            
            <p className="text-xl text-zinc-400 max-w-3xl mx-auto mb-10 leading-relaxed">
              Describe your software intent in plain text. BrainOS automatically architects, evaluates, and scaffolds production-ready AAYU systems code.
            </p>

            {/* LIVE PROJECT GENERATOR */}
            <div className="max-w-4xl mx-auto bg-[#0a0a0a] border border-white/10 rounded-2xl p-6 shadow-2xl relative">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-500 to-blue-500 rounded-2xl blur opacity-20 pointer-events-none animate-pulse"></div>
              
              <div className="relative flex flex-col md:flex-row gap-4 items-center">
                <div className="flex-1 w-full relative">
                  <div className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500">
                    <Terminal className="w-5 h-5" />
                  </div>
                  <input 
                    type="text"
                    value={intentInput}
                    onChange={(e) => setIntentInput(e.target.value)}
                    disabled={isBuilding}
                    placeholder="E.g., Build a scalable Hospital ERP system..."
                    className="w-full bg-black border border-white/10 rounded-xl py-4 pl-12 pr-4 text-lg text-white placeholder:text-zinc-600 outline-none focus:border-purple-500/50 transition-colors"
                  />
                </div>
                <Button 
                  onClick={handleBuild}
                  disabled={isBuilding || !intentInput}
                  className="w-full md:w-auto h-[60px] px-8 bg-white text-black hover:bg-zinc-200 font-bold text-lg rounded-xl gap-2 transition-all"
                >
                  {isBuilding ? <Loader2 className="w-5 h-5 animate-spin" /> : <Play className="w-5 h-5 fill-current" />}
                  {isBuilding ? "Architecting..." : "Build Project"}
                </Button>
              </div>

              {/* LIVE PIPELINE ANIMATION */}
              <div className={mt-8 transition-all duration-700 overflow-hidden \}>
                <div className="border-t border-white/10 pt-8 grid grid-cols-1 md:grid-cols-5 gap-4 relative">
                  
                  {/* Connecting Line */}
                  <div className="hidden md:block absolute top-1/2 left-10 right-10 h-0.5 bg-white/10 -translate-y-1/2 z-0" />

                  {/* 1. Intent Engine */}
                  <div className={
elative z-10 flex flex-col items-center transition-all duration-500 \}>
                    <div className={w-16 h-16 rounded-full flex items-center justify-center mb-3 transition-colors duration-500 \}>
                      <Layers className={w-8 h-8 \} />
                    </div>
                    <span className="text-xs font-bold text-center">1. Intent Parsing</span>
                    {buildStage === 1 && <span className="text-[10px] text-blue-400 mt-1 animate-pulse">Extracting Domain...</span>}
                  </div>

                  {/* 2. BrainOS */}
                  <div className={
elative z-10 flex flex-col items-center transition-all duration-500 \}>
                    <div className={w-16 h-16 rounded-full flex items-center justify-center mb-3 transition-colors duration-500 \}>
                      <Brain className={w-8 h-8 \} />
                    </div>
                    <span className="text-xs font-bold text-center">2. Architecture</span>
                    {buildStage === 2 && <span className="text-[10px] text-purple-400 mt-1 animate-pulse">Evaluating Tradeoffs...</span>}
                  </div>

                  {/* 3. AAYU Source */}
                  <div className={
elative z-10 flex flex-col items-center transition-all duration-500 \}>
                    <div className={w-16 h-16 rounded-full flex items-center justify-center mb-3 transition-colors duration-500 \}>
                      <Code2 className={w-8 h-8 \} />
                    </div>
                    <span className="text-xs font-bold text-center">3. Scaffolding</span>
                    {buildStage === 3 && <span className="text-[10px] text-orange-400 mt-1 animate-pulse">Generating Code...</span>}
                  </div>

                  {/* 4. Compiler */}
                  <div className={
elative z-10 flex flex-col items-center transition-all duration-500 \}>
                    <div className={w-16 h-16 rounded-full flex items-center justify-center mb-3 transition-colors duration-500 \}>
                      <Cpu className={w-8 h-8 \} />
                    </div>
                    <span className="text-xs font-bold text-center">4. Compiler</span>
                    {buildStage === 4 && <span className="text-[10px] text-emerald-400 mt-1 animate-pulse">Lowering to LLVM IR...</span>}
                  </div>

                  {/* 5. Production */}
                  <div className={
elative z-10 flex flex-col items-center transition-all duration-500 \}>
                    <div className={w-16 h-16 rounded-full flex items-center justify-center mb-3 transition-colors duration-500 \}>
                      <Server className={w-8 h-8 \} />
                    </div>
                    <span className="text-xs font-bold text-center">5. Production Ready</span>
                    {buildStage === 5 && (
                      <Link href="/brainos/live" className="text-[10px] text-white mt-1 bg-white/20 px-2 py-1 rounded hover:bg-white/30 transition-colors">
                        View Full Report ➔
                      </Link>
                    )}
                  </div>

                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* 
        ========================================================================
        THE 3 IDENTITIES SECTION (Dedicated Portals)
        ========================================================================
      */}
      <section className="py-24 border-t border-white/10 bg-[#050505]">
        <div className="container mx-auto px-4 max-w-7xl">
          <h2 className="text-3xl md:text-5xl font-bold mb-16 text-center">The Developer Ecosystem</h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* Intent Engine */}
            <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl hover:border-blue-500/50 transition-all flex flex-col h-full group hover:-translate-y-2">
              <div className="w-14 h-14 bg-blue-900/30 rounded-xl flex items-center justify-center mb-6">
                <Layers className="w-8 h-8 text-blue-400 group-hover:scale-110 transition-transform" />
              </div>
              <h3 className="text-2xl font-bold mb-4">Intent Engine</h3>
              <p className="text-zinc-400 mb-8 flex-1 leading-relaxed">
                Transforms raw human thought and domain requirements into structured, parseable Intent IR.
              </p>
              <div className="space-y-3 mb-8">
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> Multi-Domain Knowledge Base</div>
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> AST-agnostic Output</div>
              </div>
              <Link href="/intent-engine">
                <button className="w-full py-3 bg-white/5 hover:bg-blue-600 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2">
                  Open Portal <ArrowRight className="w-4 h-4" />
                </button>
              </Link>
            </div>

            {/* BrainOS */}
            <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl hover:border-purple-500/50 transition-all relative flex flex-col h-full group hover:-translate-y-2">
              <div className="absolute top-0 right-0 px-3 py-1 bg-purple-500 text-white text-xs font-bold rounded-bl-lg rounded-tr-xl">ORCHESTRATOR</div>
              <div className="w-14 h-14 bg-purple-900/30 rounded-xl flex items-center justify-center mb-6">
                <Brain className="w-8 h-8 text-purple-400 group-hover:scale-110 transition-transform" />
              </div>
              <h3 className="text-2xl font-bold mb-4">BrainOS</h3>
              <p className="text-zinc-400 mb-8 flex-1 leading-relaxed">
                The autonomous software architect. Evaluates tradeoffs, recommends architectures, and scaffolds the AAYU codebase.
              </p>
              <div className="space-y-3 mb-8">
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> Cloud Cost Estimation</div>
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> Security Reviewer</div>
              </div>
              <Link href="/brainos">
                <button className="w-full py-3 bg-white/5 hover:bg-purple-600 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2">
                  Open Portal <ArrowRight className="w-4 h-4" />
                </button>
              </Link>
            </div>

            {/* AAYU Language */}
            <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl hover:border-orange-500/50 transition-all flex flex-col h-full group hover:-translate-y-2">
              <div className="w-14 h-14 bg-orange-900/30 rounded-xl flex items-center justify-center mb-6">
                <Code2 className="w-8 h-8 text-orange-400 group-hover:scale-110 transition-transform" />
              </div>
              <h3 className="text-2xl font-bold mb-4">AAYU Language</h3>
              <p className="text-zinc-400 mb-8 flex-1 leading-relaxed">
                A blazingly fast, statically typed systems language. Compiled via LLVM with Deterministic ARC.
              </p>
              <div className="space-y-3 mb-8">
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> Memory Safe (No GC)</div>
                <div className="flex items-center gap-2 text-sm text-zinc-300"><CheckIcon /> O3 Optimized Backend</div>
              </div>
              <Link href="/language">
                <button className="w-full py-3 bg-white/5 hover:bg-orange-600 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2">
                  Open Portal <ArrowRight className="w-4 h-4" />
                </button>
              </Link>
            </div>
          </div>
        </div>
      </section>
      
      {/* 
        ========================================================================
        AUTHENTIC STATS & QUICK LINKS
        ========================================================================
      */}
      <section className="py-12 border-t border-white/5 bg-black">
        <div className="container mx-auto px-4 max-w-6xl flex justify-between items-center opacity-60">
          <div className="text-sm">
            Status: <span className="text-yellow-500 font-bold">Alpha Development</span>
          </div>
          <div className="flex gap-6 text-sm">
            <Link href="/architecture" className="hover:text-white transition-colors">Architecture</Link>
            <Link href="/playground" className="hover:text-white transition-colors">Playground</Link>
            <Link href="/docs" className="hover:text-white transition-colors">Docs</Link>
            <span className="text-zinc-600 cursor-not-allowed">GitHub (Coming Soon)</span>
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
    f.write(content)

print("Rebuilt Homepage with Live Generator Hero.")
