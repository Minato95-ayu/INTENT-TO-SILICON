/* eslint-disable */
"use client";
import { Cpu, Zap, Activity, BarChart4, FileCode2, ArrowRight } from "lucide-react";

export default function ArchitectureExplorer() {
  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-24">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-orange-500/10 border border-orange-500/20 text-orange-400 text-xs font-bold mb-6">
            <Cpu className="w-4 h-4" /> The Deep Pipeline
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold mb-4">Architecture Explorer</h1>
          <p className="text-xl text-zinc-400 max-w-2xl">
            Interactive visualization of the AAYU Compiler pipeline. Zoom into any node to see how raw text becomes LLVM bitcode.
          </p>
        </div>

        <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl h-[600px] flex items-center justify-center relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,165,0,0.05)_0%,transparent_50%)]" />
          
          <div className="text-center z-10">
            <Activity className="w-16 h-16 text-orange-500/50 mx-auto mb-6 animate-pulse" />
            <h2 className="text-2xl font-bold mb-2">Interactive Graph Engine</h2>
            <p className="text-zinc-500 mb-4 font-mono text-sm">Status: Building Visualization Node...</p>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-yellow-500/10 border border-yellow-500/20 text-yellow-500 text-xs font-bold">
              Simulation - Canvas Engine Pending v1.0
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}