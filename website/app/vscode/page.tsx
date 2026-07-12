/* eslint-disable */

"use client";

import { Download, CheckCircle, Search, Zap, Lightbulb, Code2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import Image from "next/image";

export default function VSCodePage() {
  return (
    <main className="min-h-screen bg-black text-white pt-24 pb-20">
      <div className="container mx-auto px-4 max-w-6xl">
        
        {/* Hero Section */}
        <div className="flex flex-col md:flex-row items-center gap-12 mb-20">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-6">
              <Code2 className="w-8 h-8 text-blue-500" />
              <span className="text-xl font-bold tracking-tight">AAYU for VS Code</span>
            </div>
            <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-6 leading-tight">
              Bring the <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">BrainOS</span> directly into your editor.
            </h1>
            <p className="text-lg text-zinc-400 mb-8 max-w-lg">
              Write intent-driven code with real-time architecture feedback, intelligent autocomplete, and inline decision tracing.
            </p>
            <div className="flex flex-wrap gap-4 relative group">
              <Button disabled className="bg-blue-600/50 text-white/50 gap-2 cursor-not-allowed">
                <Download className="w-4 h-4" /> Install from Marketplace
              </Button>
              <Button disabled variant="outline" className="border-white/10 bg-transparent gap-2 text-zinc-500 cursor-not-allowed">
                Download .vsix
              </Button>
              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                <span className="px-3 py-1 bg-black border border-yellow-500/50 text-yellow-500 text-xs font-bold rounded shadow-xl">Available in v1.0 Release</span>
              </div>
            </div>
          </div>
          <div className="flex-1 w-full relative h-[400px] rounded-xl overflow-hidden border border-white/10 shadow-2xl shadow-blue-900/20 bg-[#1e1e1e]">
            {/* Mock Editor UI */}
            <div className="flex items-center px-4 h-10 bg-[#2d2d2d] border-b border-black/50">
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
              </div>
              <div className="mx-auto text-xs text-zinc-400 font-mono">server.aayu - AAYU Workspace</div>
            </div>
            <div className="p-4 font-mono text-sm leading-relaxed overflow-hidden relative">
              <div className="text-zinc-500 flex"><span className="w-8 text-right mr-4 select-none">1</span><span className="text-blue-400">entity</span> <span className="text-green-300">AuthService</span></div>
              <div className="text-zinc-500 flex"><span className="w-8 text-right mr-4 select-none">2</span><span className="text-blue-400">has</span></div>
              <div className="text-zinc-500 flex"><span className="w-8 text-right mr-4 select-none">3</span>    users: <span className="text-yellow-300">Database</span></div>
              <div className="text-zinc-500 flex"><span className="w-8 text-right mr-4 select-none">4</span>    cache: <span className="text-yellow-300">Redis</span></div>
              <div className="text-zinc-500 flex"><span className="w-8 text-right mr-4 select-none">5</span><span className="text-blue-400">end.</span></div>
              
              {/* Mock BrainOS Tooltip */}
              <div className="absolute top-20 left-20 bg-black/90 backdrop-blur border border-purple-500/50 p-3 rounded-lg shadow-xl shadow-purple-900/20 animate-pulse">
                <div className="flex items-center gap-2 mb-1">
                  <Lightbulb className="w-4 h-4 text-purple-400" />
                  <span className="text-xs font-bold text-white">BrainOS Suggestion</span>
                </div>
                <p className="text-xs text-zinc-300">High latency detected. Consider adding an LRU Cache layer before hitting the Database.</p>
                <div className="mt-2 flex gap-2">
                  <button className="text-[10px] px-2 py-1 bg-purple-600 hover:bg-purple-500 rounded text-white font-semibold">Apply Architecture</button>
                  <button className="text-[10px] px-2 py-1 bg-white/10 hover:bg-white/20 rounded text-white">Ignore</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Features Grid */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold mb-8 border-b border-white/10 pb-4">Language Server Features</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="p-6 rounded-xl bg-white/5 border border-white/10">
              <Zap className="w-6 h-6 text-yellow-400 mb-4" />
              <h3 className="font-bold mb-2">Semantic Syntax Highlighting</h3>
              <p className="text-sm text-zinc-400">Differentiates between entities, traits, implementations, and intent definitions with deep AST understanding.</p>
            </div>
            <div className="p-6 rounded-xl bg-white/5 border border-white/10">
              <Lightbulb className="w-6 h-6 text-purple-400 mb-4" />
              <h3 className="font-bold mb-2">BrainOS Inline Feedback</h3>
              <p className="text-sm text-zinc-400">Get architectural tradeoff warnings as you type. BrainOS reviews your intent graph in real-time.</p>
            </div>
            <div className="p-6 rounded-xl bg-white/5 border border-white/10">
              <Search className="w-6 h-6 text-blue-400 mb-4" />
              <h3 className="font-bold mb-2">Intelligent Autocomplete</h3>
              <p className="text-sm text-zinc-400">Context-aware suggestions powered by the offline BrainOS Knowledge Base. Never guess an API again.</p>
            </div>
          </div>
        </div>

        {/* Configuration */}
        <div>
          <h2 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">Configuration</h2>
          <div className="bg-[#0a0a0a] rounded-xl border border-white/10 p-6 overflow-x-auto">
            <pre className="text-sm font-mono text-zinc-300">
{`// .vscode/settings.json
{
  "aayu.brainos.enable": true,
  "aayu.brainos.strictMode": false,
  "aayu.format.enableOnSave": true,
  "aayu.lint.runOnType": true,
  "aayu.path": "/usr/local/bin/aayuc"
}`}
            </pre>
          </div>
        </div>

      </div>
    </main>
  );
}
