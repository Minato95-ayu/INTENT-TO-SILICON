import os

app_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app'

portals = {
    "intent-engine": '''
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
''',
    "architecture": '''
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
''',
    "examples": '''
"use client";
import { FileJson, Building2, HeartPulse, ShoppingCart, MessageSquare, Briefcase, Calculator, ArrowRight, Github, Download } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

const EXAMPLES = [
  { id: "hospital", title: "Hospital ERP", icon: HeartPulse, color: "text-rose-400", bg: "bg-rose-500/10", border: "border-rose-500/20", desc: "Patient management, scheduling, and medical records with strict data isolation." },
  { id: "banking", title: "Banking Core", icon: Building2, color: "text-blue-400", bg: "bg-blue-500/10", border: "border-blue-500/20", desc: "High-throughput ledger system with ACID transactions and double-entry accounting." },
  { id: "ecommerce", title: "E-Commerce", icon: ShoppingCart, color: "text-emerald-400", bg: "bg-emerald-500/10", border: "border-emerald-500/20", desc: "Inventory, cart, and order orchestration built for massive horizontal scaling." },
  { id: "crm", title: "Global CRM", icon: Briefcase, color: "text-purple-400", bg: "bg-purple-500/10", border: "border-purple-500/20", desc: "Customer relationship pipelines, sales tracking, and multi-tenant isolation." },
  { id: "chat", title: "Realtime Chat", icon: MessageSquare, color: "text-cyan-400", bg: "bg-cyan-500/10", border: "border-cyan-500/20", desc: "WebSocket driven actor model for handling millions of concurrent connections." },
  { id: "ai-agent", title: "AI Agent Platform", icon: Calculator, color: "text-yellow-400", bg: "bg-yellow-500/10", border: "border-yellow-500/20", desc: "Task queue and orchestration pipeline for autonomous LLM agents." }
];

export default function ExamplesGallery() {
  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-24">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="mb-16">
          <h1 className="text-4xl md:text-5xl font-extrabold mb-4">Examples Gallery</h1>
          <p className="text-xl text-zinc-400 max-w-2xl">
            Production-ready architectural templates generated by BrainOS and optimized by the AAYU Compiler.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {EXAMPLES.map(ex => (
            <div key={ex.id} className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-6 hover:border-white/20 transition-all flex flex-col group">
              <div className={w-12 h-12 rounded-xl \ \ border flex items-center justify-center mb-6}>
                <ex.icon className={w-6 h-6 \} />
              </div>
              <h3 className="text-xl font-bold mb-3">{ex.title}</h3>
              <p className="text-sm text-zinc-400 mb-6 flex-1">{ex.desc}</p>
              
              <div className="flex items-center gap-3 mt-auto pt-6 border-t border-white/5">
                <Button disabled variant="outline" className="flex-1 bg-transparent border-white/10 text-xs text-zinc-500 cursor-not-allowed">
                  <Download className="w-3 h-3 mr-2" /> Download
                </Button>
                <Link href={https://github.com/Minato95-ayu/AAYU/tree/main/examples/\} target="_blank" className="flex-1">
                  <Button variant="outline" className="w-full bg-transparent border-white/10 text-xs hover:bg-white/5">
                    <Github className="w-3 h-3 mr-2" /> Source
                  </Button>
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
'''
}

for route, code in portals.items():
    route_dir = os.path.join(app_dir, route)
    os.makedirs(route_dir, exist_ok=True)
    with open(os.path.join(route_dir, "page.tsx"), "w", encoding="utf-8") as f:
        f.write(code.strip() + "\\n")

print("Generated Portals: Intent Engine, Architecture Explorer, Examples Gallery.")
