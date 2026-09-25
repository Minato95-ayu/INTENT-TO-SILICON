import React from 'react';
import { Map } from 'lucide-react';

export default function RoadmapPage() {
  return (
    <main className="min-h-screen pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-4xl">
        <h1 className="text-5xl font-bold mb-6">The Future of AAYU</h1>
        <p className="text-xl text-zinc-400 mb-12">Our vision for the next decade of software engineering.</p>
        <ul className="space-y-6">
          <li className="flex items-center gap-4">
            <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center text-green-500 font-bold">✓</div>
            <div className="text-xl">Core Compiler & VM</div>
          </li>
          <li className="flex items-center gap-4">
            <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center text-green-500 font-bold">✓</div>
            <div className="text-xl">Memory Safe Structs & GC</div>
          </li>
          <li className="flex items-center gap-4">
            <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-500 font-bold">↻</div>
            <div className="text-xl">WebAssembly (WASM) Playground</div>
          </li>
          <li className="flex items-center gap-4">
            <div className="w-8 h-8 rounded-full bg-zinc-800 flex items-center justify-center text-zinc-500 font-bold">○</div>
            <div className="text-xl">AAYU Package Manager Registry</div>
          </li>
        </ul>
      </div>
    </main>
  );
}
