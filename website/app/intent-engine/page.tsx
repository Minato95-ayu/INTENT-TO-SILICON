/* eslint-disable */
"use client";
import { Network, Database, BrainCircuit, Search, GitBranch, ArrowRight } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function IntentEnginePortal() {
  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-24">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold mb-6">
            <Network className="w-4 h-4" /> The NLP Core
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold mb-4">Intent Engine</h1>
          <p className="text-xl text-zinc-400 max-w-2xl">
            Translating human requirements into deterministic syntax trees. The Intent Engine bridges the gap between PM specifications and compiler ASTs.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 blur-3xl rounded-full" />
            <BrainCircuit className="w-8 h-8 text-blue-400 mb-6" />
            <h2 className="text-2xl font-bold mb-4">Offline NLP</h2>
            <p className="text-zinc-400">
              No API keys required. The Intent Engine runs entirely offline using optimized Tree-sitter grammars and local tokenizers to parse domain specifications into structured JSON intents.
            </p>
          </div>
          <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 blur-3xl rounded-full" />
            <Database className="w-8 h-8 text-indigo-400 mb-6" />
            <h2 className="text-2xl font-bold mb-4">Knowledge Graph</h2>
            <p className="text-zinc-400">
              Understands domain-specific rules. If you ask for a "Banking App", the Knowledge Graph automatically flags requirements like ACID compliance and double-entry ledgers.
            </p>
          </div>
        </div>

        <div className="bg-[#111] border border-white/10 rounded-2xl p-8 mb-8 text-center">
          <h3 className="text-2xl font-bold mb-4">Interactive Architecture Generation</h3>
          <p className="text-zinc-400 mb-6 max-w-2xl mx-auto">
            See the Intent Engine in action by routing a thought directly to BrainOS.
          </p>
          <Link href="/brainos/live">
            <Button className="bg-white text-black hover:bg-zinc-200 font-bold gap-2">
              Generate Architecture <ArrowRight className="w-4 h-4" />
            </Button>
          </Link>
        </div>
      </div>
    </main>
  );
}