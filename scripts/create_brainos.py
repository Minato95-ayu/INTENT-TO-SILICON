import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\brainos\page.tsx'
os.makedirs(os.path.dirname(filepath), exist_ok=True)

content = '''
"use client";

import { ArrowRight, Brain, Layers, GitMerge, FileCode2, Cpu, ShieldCheck, Calculator, Network } from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { Button } from "@/components/ui/button";

const PIPELINE_NODES = [
  { id: "human", title: "Human Thought", icon: Network, color: "text-zinc-400", desc: "Natural language description of the software intent." },
  { id: "intent", title: "Intent Parsing", icon: Layers, color: "text-blue-400", desc: "NLP conversion into domain-specific Intent IR." },
  { id: "knowledge", title: "Knowledge Base", icon: Database, color: "text-indigo-400", desc: "Querying multi-domain ontology (Banking, ERP, etc)." },
  { id: "decision", title: "Decision Engine", icon: GitMerge, color: "text-purple-400", desc: "Evaluating architectural constraints." },
  { id: "tradeoff", title: "Tradeoff Engine", icon: Calculator, color: "text-pink-400", desc: "Optimizing for cost vs scale vs performance." },
  { id: "architecture", title: "Architecture", icon: ShieldCheck, color: "text-emerald-400", desc: "Finalizing the structural blueprint." },
  { id: "planner", title: "Planner", icon: Brain, color: "text-yellow-400", desc: "Orchestrating code generation steps." },
  { id: "code", title: "AAYU Scaffolding", icon: FileCode2, color: "text-orange-400", desc: "Generating production-ready AAYU source code." },
  { id: "compiler", title: "Compiler Lowering", icon: Cpu, color: "text-red-400", desc: "Translating to optimized LLVM bitcode." }
];

export default function BrainOSPortal() {
  const [activeNode, setActiveNode] = useState(PIPELINE_NODES[3]);

  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-24">
      <div className="container mx-auto px-4 max-w-6xl">
        
        <div className="mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-bold mb-6">
            <Brain className="w-4 h-4" /> The Orchestrator
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold mb-4">BrainOS Architecture</h1>
          <p className="text-xl text-zinc-400 max-w-2xl">
            BrainOS is an autonomous software architect. It doesn't just write code; it evaluates tradeoffs, ensures security, and builds scalable systems from raw human intent.
          </p>
        </div>

        {/* Interactive Flow Diagram */}
        <div className="grid md:grid-cols-12 gap-8">
          
          {/* Node List (Col 4) */}
          <div className="md:col-span-4 bg-[#0a0a0a] border border-white/10 rounded-2xl p-4 space-y-2 h-[600px] overflow-y-auto hide-scrollbar">
            {PIPELINE_NODES.map((node, i) => (
              <div 
                key={node.id} 
                onClick={() => setActiveNode(node)}
                className={lex items-center gap-4 p-4 rounded-xl cursor-pointer transition-all border \}
              >
                <div className={w-10 h-10 rounded-full flex items-center justify-center bg-[#050505] border border-white/5 \}>
                  <node.icon className={w-5 h-5 \} />
                </div>
                <div>
                  <h4 className="font-bold text-sm">{node.title}</h4>
                  <div className="text-[10px] text-zinc-500 font-mono mt-1">Step 0{i+1}</div>
                </div>
              </div>
            ))}
          </div>

          {/* Node Details (Col 8) */}
          <div className="md:col-span-8 bg-[#0a0a0a] border border-white/10 rounded-2xl relative overflow-hidden flex flex-col">
            <div className={bsolute top-0 right-0 w-64 h-64 blur-[100px] rounded-full opacity-20 pointer-events-none \} />
            
            <div className="p-8 border-b border-white/5">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-16 h-16 rounded-2xl bg-[#111] border border-white/10 flex items-center justify-center">
                  <activeNode.icon className={w-8 h-8 \} />
                </div>
                <div>
                  <h2 className="text-3xl font-bold">{activeNode.title}</h2>
                  <p className="text-zinc-400 mt-1">{activeNode.desc}</p>
                </div>
              </div>
            </div>

            <div className="flex-1 p-8 bg-[#050505] font-mono text-sm">
              <div className="text-zinc-500 mb-4">// Internal State Simulation</div>
              <div className="bg-[#111] border border-white/5 rounded-xl p-6">
                {activeNode.id === "decision" ? (
                  <pre className="text-purple-300 whitespace-pre-wrap leading-relaxed">
{[BrainOS Decision Engine]
Analyzing requirements for: "Scalable Banking Core"

Constraints Detected:
- High Transaction Throughput
- ACID Compliance Required
- Zero Data Loss Tolerance

Evaluating Architectures:
1. Monolith (Rejected: Does not meet scalability requirements)
2. Microservices (Rejected: High latency for ACID transactions)
3. Event-Sourced Actor Model (Selected: Optimal for high-throughput banking)

Result: Applying Actor Model pattern to generated AAYU entities.}
                  </pre>
                ) : (
                  <pre className={whitespace-pre-wrap leading-relaxed \}>
{[Module Status: Online]
Routing telemetry data...
Executing \ protocol...
Waiting for Intent IR graph input...}
                  </pre>
                )}
              </div>
            </div>

            <div className="p-6 bg-[#0a0a0a] border-t border-white/5 flex justify-end">
              <Link href="/brainos/live">
                <Button className="bg-white text-black hover:bg-zinc-200 font-bold gap-2">
                  Test Live Generator <ArrowRight className="w-4 h-4" />
                </Button>
              </Link>
            </div>
          </div>

        </div>
      </div>
    </main>
  );
}

// Dummy placeholder for Database icon since lucide-react sometimes has issues with specific exports in dynamic imports
function Database(props: any) {
  return (
    <svg {...props} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
    </svg>
  );
}
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Created BrainOS Portal with Interactive Flow Diagram.")
