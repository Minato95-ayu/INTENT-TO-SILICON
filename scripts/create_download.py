import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\download\page.tsx'
os.makedirs(os.path.dirname(filepath), exist_ok=True)

content = '''
"use client";

import { Download, Terminal, CheckCircle2, AlertTriangle, Code2, Monitor, Box, Github } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function DownloadCenter() {
  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-24">
      <div className="container mx-auto px-4 max-w-5xl">
        
        <div className="mb-16">
          <h1 className="text-4xl md:text-5xl font-extrabold mb-4">Download AAYU</h1>
          <p className="text-xl text-zinc-400 max-w-2xl">
            Get the official AAYU Compiler and BrainOS CLI. Choose a release channel that fits your needs.
          </p>
        </div>

        {/* Release Channels */}
        <div className="grid md:grid-cols-2 gap-6 mb-16">
          
          {/* Stable */}
          <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-green-500/10 blur-3xl rounded-full" />
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-2xl font-bold flex items-center gap-2">
                  Stable Release <span className="text-xs bg-green-500/20 text-green-400 px-2 py-0.5 rounded-full font-mono border border-green-500/20">v1.0.0</span>
                </h2>
                <p className="text-zinc-500 text-sm mt-1">Recommended for production use.</p>
              </div>
              <div className="group relative">
                <Button disabled variant="outline" className="border-white/10 bg-transparent text-zinc-500 gap-2 cursor-not-allowed">
                  <Download className="w-4 h-4" /> Download
                </Button>
                <div className="absolute -top-10 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-black border border-yellow-500/50 text-yellow-500 px-3 py-1 text-xs font-bold rounded shadow-xl whitespace-nowrap pointer-events-none z-10">
                  Coming in v1.0
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-center gap-3 text-sm text-zinc-300">
                <Monitor className="w-4 h-4 text-zinc-500" /> macOS (Apple Silicon / Intel)
              </div>
              <div className="flex items-center gap-3 text-sm text-zinc-300">
                <Terminal className="w-4 h-4 text-zinc-500" /> Linux (x86_64, aarch64)
              </div>
              <div className="flex items-center gap-3 text-sm text-zinc-300">
                <Box className="w-4 h-4 text-zinc-500" /> Windows (WSL2 recommended)
              </div>
            </div>
          </div>

          {/* Nightly */}
          <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-purple-500/10 blur-3xl rounded-full" />
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-2xl font-bold flex items-center gap-2">
                  Nightly Build <span className="text-xs bg-purple-500/20 text-purple-400 px-2 py-0.5 rounded-full font-mono border border-purple-500/20">0.1.0-alpha</span>
                </h2>
                <p className="text-zinc-500 text-sm mt-1">Latest features. Expect bugs.</p>
              </div>
              <div className="group relative">
                <Button disabled variant="outline" className="border-white/10 bg-transparent text-zinc-500 gap-2 cursor-not-allowed">
                  <Download className="w-4 h-4" /> Download
                </Button>
                <div className="absolute -top-10 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-black border border-yellow-500/50 text-yellow-500 px-3 py-1 text-xs font-bold rounded shadow-xl whitespace-nowrap pointer-events-none z-10">
                  Coming in v1.0
                </div>
              </div>
            </div>

            <div className="bg-black border border-white/10 rounded-lg p-4">
              <div className="text-xs font-mono text-zinc-500 mb-2">Install via curl:</div>
              <code className="text-sm text-purple-400 select-all">curl -fsSL https://aayu.dev/install-nightly.sh | bash</code>
            </div>
          </div>
        </div>

        {/* Ecosystem Tools */}
        <h3 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">Ecosystem Tools</h3>
        
        <div className="grid md:grid-cols-2 gap-6 mb-16">
          <div className="bg-[#111] p-6 rounded-xl border border-white/5 flex items-center justify-between group cursor-pointer hover:border-blue-500/50 transition-colors">
            <div className="flex items-center gap-4">
              <Code2 className="w-8 h-8 text-blue-400" />
              <div>
                <h4 className="font-bold">VS Code Extension</h4>
                <p className="text-sm text-zinc-500">Syntax highlighting, LSP, formatting.</p>
              </div>
            </div>
            <div className="group relative">
              <span className="text-xs font-bold text-yellow-500 border border-yellow-500/20 bg-yellow-500/10 px-2 py-1 rounded">Planned</span>
            </div>
          </div>

          <div className="bg-[#111] p-6 rounded-xl border border-white/5 flex items-center justify-between group cursor-pointer hover:border-zinc-500/50 transition-colors">
            <div className="flex items-center gap-4">
              <Github className="w-8 h-8 text-zinc-400" />
              <div>
                <h4 className="font-bold">Source Code</h4>
                <p className="text-sm text-zinc-500">Build from scratch.</p>
              </div>
            </div>
            <div className="group relative">
              <span className="text-xs font-bold text-yellow-500 border border-yellow-500/20 bg-yellow-500/10 px-2 py-1 rounded">Available in v1.0</span>
            </div>
          </div>
        </div>

        {/* Verification & Docs */}
        <h3 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">Installation Guide</h3>
        <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-8">
          <div className="space-y-6 text-zinc-300">
            <div>
              <h4 className="font-bold text-white mb-2">1. System Requirements</h4>
              <p className="text-sm text-zinc-400">AAYU requires a modern 64-bit OS and a C++ compiler (clang or gcc) for the LLVM backend linking phase.</p>
            </div>
            <div>
              <h4 className="font-bold text-white mb-2">2. Verify Installation</h4>
              <div className="bg-black border border-white/10 p-3 rounded-lg font-mono text-sm text-zinc-300">
                $ aayu --version<br/>
                <span className="text-zinc-500">aayu 1.0.0 (2026-07-05)</span>
              </div>
            </div>
            <div>
              <h4 className="font-bold text-white mb-2">3. Checksums</h4>
              <p className="text-sm text-zinc-400">All binaries will be signed. SHA256 checksums will be provided alongside the v1.0 release artifacts.</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Created Download Center.")
