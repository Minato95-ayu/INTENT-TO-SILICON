 
﻿
"use client";

import { useState } from "react";
import {
  Download, Terminal, Code2, Monitor, Box, Cpu, Brain,
  GitBranch, CheckCircle2, Copy, ExternalLink, Package
} from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      onClick={() => { navigator.clipboard.writeText(text); setCopied(true); setTimeout(() => setCopied(false), 2000); }}
      className="ml-2 text-zinc-500 hover:text-zinc-200 transition-colors"
      title="Copy"
    >
      {copied ? <CheckCircle2 className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
    </button>
  );
}

export default function DownloadCenter() {
  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-24">
      <div className="container mx-auto px-4 max-w-5xl">

        {/* Hero */}
        <div className="mb-16">
          <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold px-3 py-1.5 rounded-full mb-4">
            <Package className="w-3 h-3" /> v1.0.0 â€” Stable Release
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold mb-4 tracking-tight">
            Download <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">AAYU</span>
          </h1>
          <p className="text-xl text-zinc-400 max-w-2xl">
            Get the official AAYU Compiler, Intent Engine, and BrainOS CLI. Everything you need to build intent-first software.
          </p>
        </div>

        {/* â”€â”€ COMPILER RELEASE CHANNELS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
        <h3 className="text-lg font-bold text-zinc-500 uppercase tracking-widest mb-4">Compiler</h3>
        <div className="grid md:grid-cols-2 gap-6 mb-16">

          {/* Stable */}
          <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 w-40 h-40 bg-green-500/10 blur-[80px] rounded-full pointer-events-none" />
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-2xl font-bold flex items-center gap-2">
                  Stable{" "}
                  <span className="text-xs bg-green-500/20 text-green-400 px-2 py-0.5 rounded-full font-mono border border-green-500/20">
                    v1.0.0
                  </span>
                </h2>
                <p className="text-zinc-500 text-sm mt-1">Recommended for production use.</p>
              </div>
              <Link href="/downloads/aayu-v1.0.0-windows-x64.zip" target="_blank" rel="noopener">
                <Button variant="outline" className="border-blue-500/30 bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 gap-2">
                  <Download className="w-4 h-4" /> Download for Windows
                </Button>
              </Link>
            </div>
            <div className="space-y-3">
              <div className="flex items-center gap-3 text-sm text-zinc-300">
                <Monitor className="w-4 h-4 text-zinc-500 shrink-0" /> macOS (Apple Silicon / Intel)
              </div>
              <div className="flex items-center gap-3 text-sm text-zinc-300">
                <Terminal className="w-4 h-4 text-zinc-500 shrink-0" /> Linux (x86_64 / aarch64)
              </div>
              <div className="flex items-center gap-3 text-sm text-zinc-300">
                <Box className="w-4 h-4 text-zinc-500 shrink-0" /> Windows (WSL2 recommended)
              </div>
            </div>
          </div>

          {/* Nightly */}
          <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 w-40 h-40 bg-purple-500/10 blur-[80px] rounded-full pointer-events-none" />
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-2xl font-bold flex items-center gap-2">
                  Nightly{" "}
                  <span className="text-xs bg-purple-500/20 text-purple-400 px-2 py-0.5 rounded-full font-mono border border-purple-500/20">
                    0.1.0-alpha
                  </span>
                </h2>
                <p className="text-zinc-500 text-sm mt-1">Latest features. Expect bugs.</p>
              </div>
              <Link href="/downloads/aayu-source.zip" target="_blank" rel="noopener">
                <Button variant="outline" className="border-purple-500/30 bg-purple-500/10 text-purple-400 hover:bg-purple-500/20 gap-2">
                  <GitBranch className="w-4 h-4" /> Download Source
                </Button>
              </Link>
            </div>
            <div className="bg-black border border-white/10 rounded-lg p-4">
              <div className="text-xs font-mono text-zinc-500 mb-2">Clone nightly branch:</div>
              <div className="flex items-center">
                <code className="text-sm text-purple-400 select-all break-all">
                  wget /downloads/aayu-source.zip
                </code>
                <CopyButton text="wget /downloads/aayu-source.zip" />
              </div>
            </div>
          </div>
        </div>

        {/* â”€â”€ INTENT ENGINE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
        <h3 className="text-lg font-bold text-zinc-500 uppercase tracking-widest mb-4">Intent Engine</h3>
        <div className="bg-[#0a0a0a] border border-blue-500/20 rounded-2xl p-8 mb-16 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-blue-600/10 blur-[120px] rounded-full pointer-events-none" />
          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-6 mb-8">
            <div className="flex items-start gap-4">
              <div className="bg-blue-500/10 border border-blue-500/20 p-3 rounded-xl shrink-0">
                <Cpu className="w-8 h-8 text-blue-400" />
              </div>
              <div>
                <h2 className="text-2xl font-bold mb-1">Intent Engine</h2>
                <p className="text-zinc-400 text-sm max-w-xl">
                  The core IR compiler that translates human-readable AAYU intent code into the
                  Intent Graph IR. Powers every AAYU program â€” from syntax to LLVM bytecode.
                </p>
              </div>
            </div>
            <Link href="/downloads/aayu-source.zip" target="_blank" rel="noopener" className="shrink-0">
              <Button variant="outline" className="border-blue-500/30 bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 gap-2 w-full md:w-auto">
                <ExternalLink className="w-4 h-4" /> Download Source
              </Button>
            </Link>
          </div>

          <div className="grid md:grid-cols-3 gap-4 mb-6">
            {[
              { label: "Intent IR Compiler", desc: "Parses AAYU â†’ produces Intent Graph IR" },
              { label: "LLVM Backend", desc: "Emits native binaries via LLVM 17+" },
              { label: "Type Checker", desc: "Strong static inference â€” no implicit coercion" },
            ].map(f => (
              <div key={f.label} className="bg-black/40 border border-white/5 rounded-xl p-4">
                <div className="text-xs font-bold text-blue-400 mb-1">{f.label}</div>
                <div className="text-xs text-zinc-500">{f.desc}</div>
              </div>
            ))}
          </div>

          <div className="bg-black border border-white/10 rounded-lg p-4">
            <div className="text-xs font-mono text-zinc-500 mb-2">Build from source:</div>
            <div className="space-y-1">
              {[
                "wget /downloads/aayu-source.zip",
                "cd AAYU && cmake -B build -DCMAKE_BUILD_TYPE=Release",
                "cmake --build build --parallel",
              ].map((cmd) => (
                <div key={cmd} className="flex items-center">
                  <span className="text-zinc-600 mr-2 text-sm font-mono select-none">$</span>
                  <code className="text-sm text-zinc-300 font-mono select-all">{cmd}</code>
                  <CopyButton text={cmd} />
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* â”€â”€ BRAINOS CLI â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
        <h3 className="text-lg font-bold text-zinc-500 uppercase tracking-widest mb-4">BrainOS CLI</h3>
        <div className="bg-[#0a0a0a] border border-purple-500/20 rounded-2xl p-8 mb-16 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-purple-600/10 blur-[120px] rounded-full pointer-events-none" />
          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-6 mb-8">
            <div className="flex items-start gap-4">
              <div className="bg-purple-500/10 border border-purple-500/20 p-3 rounded-xl shrink-0">
                <Brain className="w-8 h-8 text-purple-400" />
              </div>
              <div>
                <h2 className="text-2xl font-bold mb-1">BrainOS CLI</h2>
                <p className="text-zinc-400 text-sm max-w-xl">
                  The autonomous AI operating system layer for AAYU. Runs as a local daemon,
                  manages the Intent Graph, coordinates agents, and executes BrainOS modules.
                </p>
              </div>
            </div>
            <Link href="/downloads/aayu-source.zip" target="_blank" rel="noopener" className="shrink-0">
              <Button variant="outline" className="border-purple-500/30 bg-purple-500/10 text-purple-400 hover:bg-purple-500/20 gap-2 w-full md:w-auto">
                <ExternalLink className="w-4 h-4" /> Download Source
              </Button>
            </Link>
          </div>

          <div className="grid md:grid-cols-3 gap-4 mb-6">
            {[
              { label: "brainos run", desc: "Execute any .aayu program with BrainOS context" },
              { label: "brainos agent", desc: "Spawn AI agents that reason over your codebase" },
              { label: "brainos graph", desc: "Inspect and export live Intent Graph state" },
            ].map(f => (
              <div key={f.label} className="bg-black/40 border border-white/5 rounded-xl p-4">
                <div className="text-xs font-bold text-purple-400 font-mono mb-1">{f.label}</div>
                <div className="text-xs text-zinc-500">{f.desc}</div>
              </div>
            ))}
          </div>

          <div className="bg-black border border-white/10 rounded-lg p-4">
            <div className="text-xs font-mono text-zinc-500 mb-2">Quick start after install:</div>
            <div className="space-y-1">
              {[
                "brainos --version",
                "brainos run hello.aayu",
                "brainos agent --goal \"refactor all functions to use AAYU idioms\"",
              ].map((cmd) => (
                <div key={cmd} className="flex items-center">
                  <span className="text-zinc-600 mr-2 text-sm font-mono select-none">$</span>
                  <code className="text-sm text-zinc-300 font-mono select-all">{cmd}</code>
                  <CopyButton text={cmd} />
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* â”€â”€ VS CODE EXTENSION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
        <h3 className="text-lg font-bold text-zinc-500 uppercase tracking-widest mb-4">VS Code Extension</h3>
        <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-8 mb-16 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/5 blur-[120px] rounded-full pointer-events-none" />
          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-6 mb-8">
            <div className="flex items-start gap-4">
              <div className="bg-cyan-500/10 border border-cyan-500/20 p-3 rounded-xl shrink-0">
                <Code2 className="w-8 h-8 text-cyan-400" />
              </div>
              <div>
                <h2 className="text-2xl font-bold mb-1">AAYU for VS Code</h2>
                <p className="text-zinc-400 text-sm max-w-xl">
                  First-class IDE support for AAYU. Includes syntax highlighting, Language Server Protocol (LSP),
                  Intent Graph visualizer, and in-editor BrainOS agent panel.
                </p>
              </div>
            </div>
            <Link
              href="/downloads/aayu-1.2.0.vsix"
              target="_blank" rel="noopener" className="shrink-0"
            >
              <Button variant="outline" className="border-cyan-500/30 bg-cyan-500/10 text-cyan-400 hover:bg-cyan-500/20 gap-2 w-full md:w-auto">
                <Download className="w-4 h-4" /> Download .vsix
              </Button>
            </Link>
          </div>

          <div className="grid md:grid-cols-4 gap-3 mb-6">
            {[
              "Syntax highlighting",
              "LSP autocomplete",
              "Inline diagnostics",
              "Intent Graph view",
              "BrainOS agent panel",
              "Auto-formatter",
              "Linter integration",
              "Snippet library",
            ].map(feat => (
              <div key={feat} className="flex items-center gap-2 text-xs text-zinc-400 bg-black/30 border border-white/5 rounded-lg px-3 py-2">
                <CheckCircle2 className="w-3 h-3 text-cyan-500 shrink-0" /> {feat}
              </div>
            ))}
          </div>

          <div className="bg-black border border-white/10 rounded-lg p-4">
            <div className="text-xs font-mono text-zinc-500 mb-2">Install from .vsix file in VS Code:</div>
            <div className="flex items-center mb-3">
              <span className="text-zinc-600 mr-2 text-sm font-mono select-none">$</span>
              <code className="text-sm text-cyan-400 font-mono select-all">
                code --install-extension aayu-vscode-1.0.0.vsix
              </code>
              <CopyButton text="code --install-extension aayu-vscode-1.0.0.vsix" />
            </div>
            <p className="text-xs text-zinc-600">Or: VS Code â†’ Extensions â†’ â‹¯ â†’ Install from VSIXâ€¦</p>
          </div>
        </div>

        {/* â”€â”€ INSTALLATION GUIDE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
        <h3 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">Installation Guide</h3>
        <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-8">
          <div className="space-y-8 text-zinc-300">
            <div>
              <h4 className="font-bold text-white mb-2 flex items-center gap-2">
                <span className="w-6 h-6 rounded-full bg-blue-500/20 text-blue-400 text-xs font-bold flex items-center justify-center border border-blue-500/20">1</span>
                System Requirements
              </h4>
              <ul className="text-sm text-zinc-400 space-y-1 ml-8">
                <li>â€¢ Modern 64-bit OS (Linux, macOS, Windows via WSL2)</li>
                <li>â€¢ C++ compiler â€” <code className="text-zinc-300 font-mono">clang 14+</code> or <code className="text-zinc-300 font-mono">gcc 12+</code></li>
                <li>â€¢ LLVM 17+ (for native code generation)</li>
                <li>â€¢ CMake 3.25+ (to build from source)</li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-white mb-2 flex items-center gap-2">
                <span className="w-6 h-6 rounded-full bg-blue-500/20 text-blue-400 text-xs font-bold flex items-center justify-center border border-blue-500/20">2</span>
                Verify Installation
              </h4>
              <div className="bg-black border border-white/10 p-4 rounded-lg font-mono text-sm ml-8 space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-zinc-600">$</span>
                  <span className="text-zinc-300">aayu --version</span>
                  <CopyButton text="aayu --version" />
                </div>
                <div className="text-green-400">aayu 1.0.0 (2026-07-05)</div>
                <div className="flex items-center gap-2 mt-2">
                  <span className="text-zinc-600">$</span>
                  <span className="text-zinc-300">brainos --version</span>
                  <CopyButton text="brainos --version" />
                </div>
                <div className="text-purple-400">BrainOS v1.0.0 â€” Intent Graph Runtime</div>
              </div>
            </div>
            <div>
              <h4 className="font-bold text-white mb-2 flex items-center gap-2">
                <span className="w-6 h-6 rounded-full bg-blue-500/20 text-blue-400 text-xs font-bold flex items-center justify-center border border-blue-500/20">3</span>
                SHA256 Checksums
              </h4>
              <p className="text-sm text-zinc-400 ml-8">
                All release binaries are GPG-signed by <code className="text-zinc-300 font-mono">Minato95-ayu</code>.
                SHA256 checksums are published alongside each GitHub Release in <code className="text-zinc-300 font-mono">checksums.txt</code>.
              </p>
            </div>
          </div>
        </div>

      </div>
    </main>
  );
}

