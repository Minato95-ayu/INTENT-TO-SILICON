import React from 'react';
import { Code2, Zap, ShieldCheck } from 'lucide-react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function LanguagePage() {
  return (
    <main className="min-h-screen pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-5xl">
        <h1 className="text-5xl font-bold mb-6">The AAYU Language</h1>
        <p className="text-xl text-zinc-400 mb-12">A keyword-delimited language with an evolving implementation. See the current syntax reference for the tested core.</p>
        
        <div className="grid md:grid-cols-2 gap-8 mb-16">
          <div className="bg-[#050505] border border-white/10 rounded-2xl p-8">
            <ShieldCheck className="w-8 h-8 text-blue-500 mb-4" />
            <h3 className="text-2xl font-bold mb-4">Runtime Memory Model</h3>
            <p className="text-zinc-400">The Rust VM uses a mark-and-sweep heap collector. The project does not claim that memory errors or leaks are impossible.</p>
          </div>
          <div className="bg-[#050505] border border-white/10 rounded-2xl p-8">
            <Zap className="w-8 h-8 text-yellow-500 mb-4" />
            <h3 className="text-2xl font-bold mb-4">Compile to Bytecode</h3>
            <p className="text-zinc-400">The current CLI compiles `.aayu` source into `.ayc` bytecode for execution by the Rust VM. It does not currently emit a native standalone application.</p>
          </div>
        </div>

        <Link href="/docs">
          <Button size="lg" className="bg-white text-black hover:bg-zinc-200">Read the Full Documentation</Button>
        </Link>
      </div>
    </main>
  );
}
