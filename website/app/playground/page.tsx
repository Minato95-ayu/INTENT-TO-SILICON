import React from "react";
import { MonitorPlay, Terminal, Code2, Cpu } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function PlaygroundPage() {
  return (
    <main className="flex-1 min-h-screen pt-32 pb-20 flex items-center justify-center">
      <div className="container mx-auto px-4 max-w-3xl text-center">
        
        <div className="w-24 h-24 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-3xl flex items-center justify-center mx-auto mb-8 border border-white/10 shadow-2xl shadow-blue-500/10">
          <MonitorPlay className="w-12 h-12 text-blue-400" />
        </div>
        
        <h1 className="text-4xl md:text-5xl font-bold mb-6 text-white">
          WebAssembly Native Playground
        </h1>
        
        <p className="text-xl text-zinc-400 mb-12">
          We are currently porting the AAYU Compiler to <strong>WASM (WebAssembly)</strong> so you can write and compile Native Machine Code directly inside your browser without installing anything.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 text-left">
          <div className="bg-[#050505] border border-white/5 p-6 rounded-2xl">
            <Code2 className="w-6 h-6 text-purple-400 mb-4" />
            <h3 className="font-bold text-white mb-2">Write AAYU</h3>
            <p className="text-sm text-zinc-500">Live in-browser syntax highlighting and error checking.</p>
          </div>
          <div className="bg-[#050505] border border-white/5 p-6 rounded-2xl">
            <Cpu className="w-6 h-6 text-indigo-400 mb-4" />
            <h3 className="font-bold text-white mb-2">Compile via WASM</h3>
            <p className="text-sm text-zinc-500">The C-Backend generates machine code on the fly in Chrome.</p>
          </div>
          <div className="bg-[#050505] border border-white/5 p-6 rounded-2xl">
            <Terminal className="w-6 h-6 text-green-400 mb-4" />
            <h3 className="font-bold text-white mb-2">Instant Execution</h3>
            <p className="text-sm text-zinc-500">See your silicon-speed results directly in the output terminal.</p>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/docs">
            <Button size="lg" className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl h-12 px-8">
              Start Learning Now
            </Button>
          </Link>
          <Link href="/">
            <Button size="lg" variant="outline" className="w-full sm:w-auto border-white/10 hover:bg-white/5 text-white font-bold rounded-xl h-12 px-8">
              Back to Home
            </Button>
          </Link>
        </div>

      </div>
    </main>
  );
}
