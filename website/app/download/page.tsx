'use client';
import { useState } from 'react';
import { Terminal, Check, Copy, Download, Box, Cpu, ArrowRight } from 'lucide-react';

export default function DownloadPage() {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText("git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git\ncd INTENT-TO-SILICON\npip install -e .\ncargo build --release --manifest-path runtime_rs/Cargo.toml");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-16 selection:bg-purple-500/30">
      <div className="container mx-auto px-4 max-w-5xl">
        
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-6 tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-500">
            Download <span className="text-purple-400">AAYU</span>
          </h1>
          <p className="text-lg text-zinc-400 max-w-2xl mx-auto">
            Get the world's first Single-File Full-Stack language for AI agents. 
            Includes the AAYU Compiler and the lightning-fast Rust Bytecode VM.
          </p>
        </div>

        {/* Primary Download Terminal */}
        <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden shadow-2xl mb-16 relative">
          <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-cyan-500/5 pointer-events-none" />
          
          <div className="flex items-center justify-between px-6 py-4 bg-[#111] border-b border-white/5">
            <div className="flex gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500/80" />
              <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
              <div className="w-3 h-3 rounded-full bg-green-500/80" />
            </div>
            <span className="text-xs font-mono text-zinc-500 flex items-center gap-2">
              <Terminal className="w-3 h-3" /> bash
            </span>
          </div>
          
          <div className="p-8 relative">
            <button 
              onClick={handleCopy}
              className="absolute top-6 right-6 p-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-zinc-400 hover:text-white transition-all flex items-center gap-2 text-sm"
            >
              {copied ? <><Check className="w-4 h-4 text-green-400" /> Copied!</> : <><Copy className="w-4 h-4" /> Copy Script</>}
            </button>
            
            <pre className="font-mono text-sm md:text-base leading-loose text-zinc-300">
              <span className="text-purple-400 select-none">❯ </span><span className="text-cyan-300">git clone</span> https://github.com/Minato95-ayu/INTENT-TO-SILICON.git<br/>
              <span className="text-purple-400 select-none">❯ </span><span className="text-cyan-300">cd</span> INTENT-TO-SILICON<br/>
              <span className="text-zinc-500"># Install the AAYU Python Compiler</span><br/>
              <span className="text-purple-400 select-none">❯ </span><span className="text-cyan-300">pip install</span> -e .<br/>
              <span className="text-zinc-500"># Build the ultra-fast Rust VM</span><br/>
              <span className="text-purple-400 select-none">❯ </span><span className="text-cyan-300">cargo build</span> --release --manifest-path runtime_rs/Cargo.toml<br/>
            </pre>
          </div>
        </div>

        {/* Requirements & Components */}
        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-[#0a0a0a] border border-white/5 p-8 rounded-2xl">
            <Box className="w-8 h-8 text-cyan-400 mb-4" />
            <h3 className="text-xl font-bold mb-2">Prerequisites</h3>
            <ul className="space-y-3 text-zinc-400 text-sm">
              <li className="flex items-center gap-2"><Check className="w-4 h-4 text-green-500" /> Python 3.12+ (For the Lexer/Parser)</li>
              <li className="flex items-center gap-2"><Check className="w-4 h-4 text-green-500" /> Rust & Cargo (For the Bytecode VM)</li>
              <li className="flex items-center gap-2"><Check className="w-4 h-4 text-green-500" /> Git (To clone the repository)</li>
            </ul>
          </div>

          <div className="bg-[#0a0a0a] border border-white/5 p-8 rounded-2xl">
            <Cpu className="w-8 h-8 text-purple-400 mb-4" />
            <h3 className="text-xl font-bold mb-2">What's Included?</h3>
            <ul className="space-y-3 text-zinc-400 text-sm">
              <li className="flex items-center gap-2"><ArrowRight className="w-4 h-4 text-purple-500" /> <b>aayu-cli</b>: The main compiler wrapper</li>
              <li className="flex items-center gap-2"><ArrowRight className="w-4 h-4 text-purple-500" /> <b>aayu-vm</b>: The Rust bytecode execution engine</li>
              <li className="flex items-center gap-2"><ArrowRight className="w-4 h-4 text-purple-500" /> <b>AAYU Stdlib</b>: AI, Tensor, UI, and DB modules</li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  );
}
