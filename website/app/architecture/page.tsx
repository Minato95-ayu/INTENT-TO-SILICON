import React from 'react';
import { Cpu, Layers, Terminal } from 'lucide-react';

export default function ArchitecturePage() {
  return (
    <main className="min-h-screen pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-5xl">
        <h1 className="text-5xl font-bold mb-6">Runtime Architecture</h1>
        <p className="text-xl text-zinc-400 mb-12">How Intent-to-Silicon works under the hood.</p>
        
        <div className="bg-[#050505] border border-white/10 rounded-2xl p-8 mb-8">
          <h2 className="text-2xl font-bold mb-4">The Pipeline</h2>
          <pre className="text-zinc-400 font-mono text-sm overflow-x-auto">
{`Lexer -> Parser -> AST -> Semantic Analysis -> HIR -> MIR -> LIR -> Machine Code`}
          </pre>
          <p className="text-zinc-400 mt-4">AAYU features a world-class, multi-stage compiler pipeline that aggressively optimizes your intent before it ever touches the processor.</p>
        </div>
      </div>
    </main>
  );
}
