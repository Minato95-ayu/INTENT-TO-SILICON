'use client';

import Link from 'next/link';
import { useState } from 'react';
import { Terminal, Code2, Zap, Server, Database, BrainCircuit, Cpu, Layers, Layout, ArrowRight, Download, CheckCircle2 } from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState(0);

  const tabs = [
    {
      name: "1. Full-Stack Web",
      icon: <Server className="w-4 h-4 mr-2" />,
      code: `// Built-in Database Models
model User
    id Int
    username String
end

// Built-in Web Server
route "/api/users"
    get
        let users = User.all()
        respond(users)
    end
end`,
      output: `[AAYU] Compiling AAYUGram.aayu -> Rust JIT Engine...
[AAYU] SQLite In-Memory Database Initialized.
[AAYU] Migrated model 'User' successfully.

Server listening on http://localhost:3000
[Worker #1] GET /api/users -> 200 OK (0.2ms)`
    },
    {
      name: "2. Native AI & Math",
      icon: <BrainCircuit className="w-4 h-4 mr-2" />,
      code: `// Zero-Copy Native Tensors
action train_ai
    print("Training K-Means Model...")
    let data = [[1, 2], [1, 4], [10, 2]]
    let model = ml::kmeans_fit(data, 2, 100)
    
    let pred = ml::kmeans_predict(model, [10, 3])
    print("Cluster Assignment: " + pred)
end
run train_ai`,
      output: `[AAYU] Compiling Math Engine (AVX2/Neon)...
Training K-Means Model...
[AAYU JIT] Silicon-Level Execution Triggered
Cluster Assignment: 1.0

Execution finished in 4.1ms`
    },
    {
      name: "3. JIT Speed (10M Loop)",
      icon: <Zap className="w-4 h-4 mr-2" />,
      code: `// Benchmarking the JIT Compiler
action sum_bench
    let sum = 0
    for i in 0..10000000
        sum = sum + i
    end
    print(sum)
end
run sum_bench`,
      output: `[AAYU JIT] Tier 2 Speculative Compiler Triggered...
[AAYU JIT] Compiling to Native Machine Code...
[AAYU JIT] Native Execution Start:

49999995000000
AAYU_VM_NS 50.0ms (0.05 seconds)`
    },
    {
      name: "4. Declarative UI",
      icon: <Layout className="w-4 h-4 mr-2" />,
      code: `// Flutter-like Declarative UI
state counter = 0

action increment
    counter = counter + 1
end

Page Home
    Column
        heading "AAYU Native UI"
        button "Click Me" onClick=increment
        text "Clicks: " + counter
    end
end
run Home`,
      output: `[AAYU UI] Compiling Declarative Widget Tree...
ENCODING WIDGET COLUMN -> 2
ENCODING WIDGET BUTTON -> 8

--- AAYU Performance Metrics ---
Initial Render Time: 0.00 ms
Total Frames Painted: 1
Peak Memory Usage: 0.00 MB`
    }
  ];

  return (
    <div className="min-h-screen bg-black text-white selection:bg-purple-500/30 font-sans overflow-x-hidden">
      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-6 sm:px-12 lg:px-24 max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-16">
        
        {/* Background Glows */}
        <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute top-[20%] right-[-10%] w-[400px] h-[400px] bg-blue-600/10 rounded-full blur-[100px] pointer-events-none" />

        {/* Left Copy */}
        <div className="flex-1 space-y-8 z-10 relative">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-900 border border-zinc-800 text-xs font-medium text-zinc-300">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            v1.2.0 JIT Engine Released
          </div>
          
          <h1 className="text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.1]">
            Silicon-Level <br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-cyan-400">
              Hardware Speed.
            </span>
          </h1>
          
          <p className="text-xl text-zinc-400 max-w-xl leading-relaxed">
            The world's first single-file full-stack language for the AI era. 
            AAYU packs a Database, Web Server, UI, and Math Engine into a blistering-fast 
            <strong className="text-white font-semibold"> Tier-2 JIT Rust VM.</strong> Zero dependencies. Zero hallucinations.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 pt-4">
            <Link href="/download" className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white rounded-xl font-semibold transition-all shadow-[0_0_20px_rgba(147,51,234,0.3)] hover:shadow-[0_0_30px_rgba(147,51,234,0.5)]">
              <Download className="w-5 h-5" />
              Download AAYU Installer
            </Link>
            <Link href="/tutorial" className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-white rounded-xl font-medium transition-all">
              <Code2 className="w-5 h-5" />
              Read Documentation
            </Link>
          </div>
        </div>

        {/* Right Code Block (Hero) */}
        <div className="flex-1 w-full max-w-2xl z-10">
          <div className="rounded-2xl border border-zinc-800 bg-zinc-950 shadow-2xl overflow-hidden">
            <div className="flex items-center px-4 py-3 bg-zinc-900 border-b border-zinc-800">
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500/80" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                <div className="w-3 h-3 rounded-full bg-green-500/80" />
              </div>
              <span className="ml-4 text-xs font-mono text-zinc-500">QuickStart.ps1</span>
            </div>
            <div className="p-6 font-mono text-sm leading-relaxed text-zinc-300">
              <div className="text-zinc-500 mb-2"># 1. Install via Windows Installer or Termux</div>
              <div><span className="text-purple-400">wget</span> https://intent-to-silicon.vercel.app/downloads/AAYU_Windows_Installer.exe</div>
              
              <div className="text-zinc-500 mt-6 mb-2"># 2. Initialize a Full-Stack AI Project in 1 File</div>
              <div><span className="text-purple-400">aayu</span> init my-app <span className="text-zinc-500">&&</span> <span className="text-cyan-400">cd</span> my-app</div>
              
              <div className="text-zinc-500 mt-6 mb-2"># 3. Run with JIT Engine natively (0 dependencies)</div>
              <div><span className="text-purple-400">aayu</span> run app.aayu --jit --web</div>
              
              <div className="mt-4 text-emerald-400/90 text-xs">
                [AAYU] Tier-2 Compiler Triggered...<br/>
                [AAYU] Server running on :3000 (0.8ms cold start)
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Bar */}
      <section className="border-y border-zinc-900 bg-zinc-950/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-10 grid grid-cols-2 md:grid-cols-4 gap-8 divide-x divide-zinc-900">
          <div className="px-4 text-center">
            <div className="text-3xl font-extrabold text-white mb-1">50 ms</div>
            <div className="text-sm text-zinc-500 font-medium tracking-wide uppercase mt-2">10M Iteration JIT Speed</div>
          </div>
          <div className="px-4 text-center">
            <div className="text-3xl font-extrabold text-white mb-1">0</div>
            <div className="text-sm text-zinc-500 font-medium tracking-wide uppercase mt-2">Dependencies (No npm/pip)</div>
          </div>
          <div className="px-4 text-center">
            <div className="text-3xl font-extrabold text-white mb-1">1 File</div>
            <div className="text-sm text-zinc-500 font-medium tracking-wide uppercase mt-2">Complete Full-Stack Architecture</div>
          </div>
          <div className="px-4 text-center">
            <div className="text-3xl font-extrabold text-white mb-1">4+</div>
            <div className="text-sm text-zinc-500 font-medium tracking-wide uppercase mt-2">Native Engines (DB, UI, ML, HTTP)</div>
          </div>
        </div>
      </section>

      {/* Benchmarks Section (The TezzNative Killer) */}
      <section className="py-24 px-6 sm:px-12 max-w-7xl mx-auto relative">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold mb-4">Engineered for Raw Bare-Metal Speed</h2>
          <p className="text-zinc-400 max-w-2xl mx-auto">
            AAYU's Tier-2 JIT Compiler converts bytecode directly into native CPU machine instructions, completely bypassing interpreter overhead.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Bench 1 */}
          <div className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4 opacity-10"><Zap className="w-24 h-24 text-cyan-500" /></div>
            <div className="flex justify-between items-end mb-6 relative z-10">
              <h3 className="text-lg font-semibold">10,000,000 Iteration Loop</h3>
              <span className="text-xs text-emerald-400 font-medium">Lower is Better</span>
            </div>
            <div className="space-y-5 relative z-10">
              <div>
                <div className="flex justify-between text-sm mb-1"><span className="text-cyan-400 font-medium">AAYU JIT (Native)</span><span>50 ms</span></div>
                <div className="h-2 bg-zinc-950 rounded-full overflow-hidden"><div className="h-full bg-cyan-500 w-[15%]" /></div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1"><span className="text-zinc-400">C (GCC -O2)</span><span className="text-zinc-400">22 ms</span></div>
                <div className="h-2 bg-zinc-950 rounded-full overflow-hidden"><div className="h-full bg-zinc-600 w-[10%]" /></div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1"><span className="text-purple-400">AAYU Interpreter (VM)</span><span>716 ms</span></div>
                <div className="h-2 bg-zinc-950 rounded-full overflow-hidden"><div className="h-full bg-purple-500 w-[70%]" /></div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1"><span className="text-zinc-400">Python 3.12</span><span className="text-zinc-400">1147 ms</span></div>
                <div className="h-2 bg-zinc-950 rounded-full overflow-hidden"><div className="h-full bg-zinc-600 w-[100%]" /></div>
              </div>
            </div>
          </div>

          {/* Bench 2 */}
          <div className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4 opacity-10"><Server className="w-24 h-24 text-emerald-500" /></div>
            <div className="flex justify-between items-end mb-6 relative z-10">
              <h3 className="text-lg font-semibold">Project Setup Time</h3>
              <span className="text-xs text-emerald-400 font-medium">Faster is Better</span>
            </div>
            <div className="space-y-5 relative z-10">
              <div>
                <div className="flex justify-between text-sm mb-1"><span className="text-cyan-400 font-medium">AAYU (Single File)</span><span>0 sec</span></div>
                <div className="h-2 bg-zinc-950 rounded-full overflow-hidden"><div className="h-full bg-cyan-500 w-[5%]" /></div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1"><span className="text-zinc-400">Python (pip install)</span><span className="text-zinc-400">45 sec</span></div>
                <div className="h-2 bg-zinc-950 rounded-full overflow-hidden"><div className="h-full bg-zinc-600 w-[45%]" /></div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1"><span className="text-zinc-400">Node+Next.js (npm i)</span><span className="text-zinc-400">120+ sec</span></div>
                <div className="h-2 bg-zinc-950 rounded-full overflow-hidden"><div className="h-full bg-zinc-600 w-[100%]" /></div>
              </div>
            </div>
          </div>

          {/* Bench 3 */}
          <div className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4 opacity-10"><Layers className="w-24 h-24 text-purple-500" /></div>
            <div className="flex justify-between items-end mb-6 relative z-10">
              <h3 className="text-lg font-semibold">Full-Stack Dependencies</h3>
              <span className="text-xs text-emerald-400 font-medium">Lower is Better</span>
            </div>
            <div className="space-y-5 relative z-10">
              <div>
                <div className="flex justify-between text-sm mb-1"><span className="text-cyan-400 font-medium">AAYU Core</span><span>0 MB</span></div>
                <div className="h-2 bg-zinc-950 rounded-full overflow-hidden"><div className="h-full bg-cyan-500 w-[5%]" /></div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1"><span className="text-zinc-400">Go (Binaries)</span><span className="text-zinc-400">~15 MB</span></div>
                <div className="h-2 bg-zinc-950 rounded-full overflow-hidden"><div className="h-full bg-zinc-600 w-[15%]" /></div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1"><span className="text-zinc-400">Node (node_modules)</span><span className="text-zinc-400">~350 MB</span></div>
                <div className="h-2 bg-zinc-950 rounded-full overflow-hidden"><div className="h-full bg-zinc-600 w-[100%]" /></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Code Showcase Tabbed UI */}
      <section className="py-20 px-6 sm:px-12 max-w-7xl mx-auto border-t border-zinc-900">
        <div className="text-center mb-10">
          <div className="text-xs font-bold tracking-widest text-purple-400 uppercase mb-2">Live Code Showcase</div>
          <h2 className="text-3xl lg:text-4xl font-bold">Experience the Syntax in Action</h2>
          <p className="text-zinc-400 mt-4 max-w-2xl mx-auto">
            Explore interactive code examples showing how AAYU elegantly unifies frontend, backend, database, and native hardware math.
          </p>
        </div>

        <div className="bg-zinc-900/30 border border-zinc-800 rounded-2xl overflow-hidden shadow-2xl">
          {/* Tab Headers */}
          <div className="flex flex-wrap border-b border-zinc-800 bg-zinc-950/50">
            {tabs.map((tab, idx) => (
              <button
                key={idx}
                onClick={() => setActiveTab(idx)}
                className={`flex items-center px-6 py-4 text-sm font-medium transition-colors ${
                  activeTab === idx 
                    ? 'text-cyan-400 border-b-2 border-cyan-400 bg-zinc-900/50' 
                    : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/30'
                }`}
              >
                {tab.icon}
                {tab.name}
              </button>
            ))}
          </div>
          
          {/* Tab Content */}
          <div className="flex flex-col lg:flex-row min-h-[400px]">
            {/* Left: Code */}
            <div className="flex-1 p-6 lg:p-8 bg-zinc-950/80 lg:border-r border-zinc-800 relative">
              <div className="absolute top-4 right-4 text-xs font-mono text-zinc-600">example.aayu</div>
              <pre className="font-mono text-sm leading-relaxed overflow-x-auto text-zinc-300">
                <code dangerouslySetInnerHTML={{
                  __html: tabs[activeTab].code
                    .replace(/\b(model|end|route|get|let|action|run|for|in|state|Page|Column|button|heading|text|print)\b/g, '<span class="text-purple-400">$1</span>')
                    .replace(/\b(Int|String)\b/g, '<span class="text-blue-400">$1</span>')
                    .replace(/\b(User|ml::kmeans_fit|ml::kmeans_predict|math::|User\.all)\b/g, '<span class="text-cyan-400">$1</span>')
                    .replace(/("[^"]*")/g, '<span class="text-emerald-400">$1</span>')
                    .replace(/\/\/.*/g, '<span class="text-zinc-500">$&</span>')
                }} />
              </pre>
            </div>
            
            {/* Right: Output */}
            <div className="flex-1 p-6 lg:p-8 bg-zinc-900/30">
              <div className="flex justify-between items-center mb-6">
                <div className="flex items-center gap-2 text-xs font-mono text-emerald-400">
                  <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  Executable Output (Native x64)
                </div>
                <div className="text-xs font-mono text-zinc-500">Exit: 0</div>
              </div>
              <pre className="font-mono text-sm leading-relaxed text-zinc-400 whitespace-pre-wrap">
                {tabs[activeTab].output}
              </pre>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="py-24 px-6 sm:px-12 max-w-7xl mx-auto border-t border-zinc-900">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="p-8 rounded-2xl bg-zinc-900/30 border border-zinc-800 hover:border-purple-500/30 transition-colors">
            <Database className="w-8 h-8 text-purple-400 mb-6" />
            <h3 className="text-xl font-bold mb-3">Built-in SQLite Engine</h3>
            <p className="text-zinc-400 text-sm leading-relaxed">No ORMs to configure. Declare a <code className="text-purple-300">model</code> and AAYU handles the schema migrations and transactions entirely in memory or disk with ACID compliance.</p>
          </div>
          <div className="p-8 rounded-2xl bg-zinc-900/30 border border-zinc-800 hover:border-cyan-500/30 transition-colors">
            <Cpu className="w-8 h-8 text-cyan-400 mb-6" />
            <h3 className="text-xl font-bold mb-3">Tier-2 JIT Compiler</h3>
            <p className="text-zinc-400 text-sm leading-relaxed">A highly speculative JIT compiler that converts hot loops directly into C machine instructions at runtime for blistering speed on x86/ARM.</p>
          </div>
          <div className="p-8 rounded-2xl bg-zinc-900/30 border border-zinc-800 hover:border-blue-500/30 transition-colors">
            <Layers className="w-8 h-8 text-blue-400 mb-6" />
            <h3 className="text-xl font-bold mb-3">Zero Dependencies</h3>
            <p className="text-zinc-400 text-sm leading-relaxed">No npm. No pip. No cargo. Every feature you need to build a modern app is compiled directly into the 12MB AAYU executable.</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-zinc-900 py-12 text-center text-zinc-500 text-sm">
        <p>&copy; {new Date().getFullYear()} AAYU Language & Intent-to-Silicon.</p>
        <p className="mt-2 text-zinc-600">Created by Ayush Ghrit Kaushik. Engineered for the AI Era.</p>
      </footer>
    </div>
  );
}
