import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\download\page.tsx'

download_code = '''
"use client";

import { Download, Terminal, Apple, Windows, Code2, Copy, CheckCircle2, AlertTriangle, ShieldCheck } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";

export default function DownloadPage() {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText("curl -sSf https://aayu.dev/install.sh | sh");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <main className="min-h-screen bg-black text-white pt-24 pb-20">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-extrabold tracking-tight mb-6">Download AAYU</h1>
          <p className="text-xl text-zinc-400 max-w-2xl mx-auto">
            Get the compiler, package manager, and offline BrainOS engine all in a single zero-dependency binary.
          </p>
        </div>

        {/* Global Alert for Authenticity Rule */}
        <div className="max-w-3xl mx-auto mb-12 p-4 rounded-lg bg-yellow-500/10 border border-yellow-500/30 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-yellow-500 shrink-0 mt-0.5" />
          <p className="text-sm text-yellow-200">
            <strong>Release Status:</strong> The AAYU compiler is currently in active development. Binary downloads below are marked as <span className="px-2 py-0.5 rounded bg-yellow-500/20">Coming in v1.0</span> until the CI/CD release pipeline is finalized.
          </p>
        </div>

        {/* Primary Install Method */}
        <div className="max-w-3xl mx-auto mb-16">
          <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-8 relative shadow-2xl">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2"><Terminal className="w-5 h-5 text-zinc-400" /> Recommended Installation (Linux / macOS)</h2>
            <div className="flex items-center gap-4 bg-black border border-white/10 rounded-xl p-4">
              <code className="text-green-400 font-mono text-sm flex-1 overflow-x-auto">
                curl -sSf https://aayu.dev/install.sh | sh
              </code>
              <button 
                onClick={handleCopy}
                className="p-2 hover:bg-white/10 rounded-lg transition-colors group relative shrink-0"
              >
                {copied ? <CheckCircle2 className="w-5 h-5 text-green-500" /> : <Copy className="w-5 h-5 text-zinc-400 group-hover:text-white" />}
                <span className="absolute -top-8 left-1/2 -translate-x-1/2 bg-white text-black text-xs font-bold px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">Copy</span>
              </button>
            </div>
            <p className="text-sm text-zinc-500 mt-4 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-500" /> Installer script is digitally signed. (Currently in simulated preview).
            </p>
          </div>
        </div>

        {/* OS Specific Downloads */}
        <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          
          {/* Windows */}
          <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-6 flex flex-col h-full hover:border-blue-500/50 transition-colors">
            <Windows className="w-10 h-10 mb-4 text-blue-400" />
            <h3 className="text-xl font-bold mb-2">Windows (x64)</h3>
            <p className="text-sm text-zinc-400 mb-6 flex-1">Installer (.msi) and standalone .zip archive.</p>
            <div className="space-y-2 relative group">
              <Button disabled className="w-full bg-white/5 border border-white/10 text-zinc-500 cursor-not-allowed">Download .msi</Button>
              <Button disabled className="w-full bg-transparent border border-white/10 text-zinc-600 cursor-not-allowed">Download .zip</Button>
              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                <span className="px-3 py-1 bg-black border border-yellow-500/50 text-yellow-500 text-xs font-bold rounded shadow-xl">Coming in v1.0</span>
              </div>
            </div>
          </div>

          {/* macOS */}
          <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-6 flex flex-col h-full hover:border-zinc-500/50 transition-colors">
            <Apple className="w-10 h-10 mb-4 text-zinc-300" />
            <h3 className="text-xl font-bold mb-2">macOS (Apple Silicon)</h3>
            <p className="text-sm text-zinc-400 mb-6 flex-1">Universal binary for M1/M2/M3 and Intel Macs.</p>
            <div className="space-y-2 relative group">
              <Button disabled className="w-full bg-white/5 border border-white/10 text-zinc-500 cursor-not-allowed">Download .pkg</Button>
              <Button disabled className="w-full bg-transparent border border-white/10 text-zinc-600 cursor-not-allowed">Download .tar.gz</Button>
              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                <span className="px-3 py-1 bg-black border border-yellow-500/50 text-yellow-500 text-xs font-bold rounded shadow-xl">Coming in v1.0</span>
              </div>
            </div>
          </div>

          {/* Linux */}
          <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-6 flex flex-col h-full hover:border-orange-500/50 transition-colors">
            <Terminal className="w-10 h-10 mb-4 text-orange-400" />
            <h3 className="text-xl font-bold mb-2">Linux (x64 / ARM64)</h3>
            <p className="text-sm text-zinc-400 mb-6 flex-1">Statically linked binaries for Ubuntu, Debian, Alpine.</p>
            <div className="space-y-2 relative group">
              <Button disabled className="w-full bg-white/5 border border-white/10 text-zinc-500 cursor-not-allowed">Download .deb</Button>
              <Button disabled className="w-full bg-transparent border border-white/10 text-zinc-600 cursor-not-allowed">Download .tar.gz</Button>
              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                <span className="px-3 py-1 bg-black border border-yellow-500/50 text-yellow-500 text-xs font-bold rounded shadow-xl">Coming in v1.0</span>
              </div>
            </div>
          </div>

        </div>

      </div>
    </main>
  );
}
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(download_code)

print("Updated download page with Authenticity rule.")
