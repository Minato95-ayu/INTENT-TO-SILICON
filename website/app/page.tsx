'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ChevronRight, Terminal, Copy, Check, Bot, Sparkles, Zap, Server, Database, LayoutTemplate, ShieldCheck, Activity , Download} from 'lucide-react';

const codeString = `// Welcome to AAYU: The AI-Agent Language
app CoreApp

// 1. Built-in Database Models
model User {
      id: Int
      username: String
    }

// 2. Built-in Web Server
route "/api/users"
      get
        return User.all()
      end
    end

// 3. Built-in Tensors (Zero-Copy)
action train_ai
    let X = Tensor.new([2, 2], [1.0, 2.0, 3.0, 4.0])
    let Y = X.transpose()
    print("Training finished in 40ms.")
end

// 4. Built-in UI
Page Home
    Column
        Text("Built for Silicon. Loved by AI.")
        Button("Run AI", onClick: train_ai)
    end
end

run Home`;

export default function Home() {
  const [displayed, setDisplayed] = useState<string[]>([]);
  const [copied, setCopied] = useState(false);
  const [done, setDone] = useState(false);

  useEffect(() => {
    const lines = codeString.split('\n');
    let currentLine = 0;
    
    const interval = setInterval(() => {
      if (currentLine < lines.length) {
        setDisplayed(lines.slice(0, currentLine + 1));
        currentLine++;
      } else {
        setDone(true);
        clearInterval(interval);
      }
    }, 80);

    return () => clearInterval(interval);
  }, []);

  const handleCopy = () => {
    navigator.clipboard.writeText("curl -fsSL https://raw.githubusercontent.com/Minato95-ayu/INTENT-TO-SILICON/main/install.sh | bash");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const highlightLine = (line: string) => {
    if (line.trim().startsWith('//')) return <span className="text-zinc-500">{line}</span>;
    
    return line.split(/(\s+|"[\s\S]*?"|{|\}|\(|\))/g).map((token, i) => {
      if (!token) return null;
      if (token.startsWith('"') && token.endsWith('"')) return <span key={i} className="text-yellow-300">{token}</span>;
      if (['app', 'model', 'route', 'action', 'Page', 'run', 'end', 'let', 'get'].includes(token)) return <span key={i} className="text-purple-400 font-bold">{token}</span>;
      if (['Int', 'String', 'Tensor', 'Column', 'Text', 'Button'].includes(token)) return <span key={i} className="text-cyan-400">{token}</span>;
      if (['respond', 'print', 'all', 'new', 'transpose'].includes(token)) return <span key={i} className="text-blue-400">{token}</span>;
      return <span key={i} className="text-zinc-200">{token}</span>;
    });
  };

  return (
    <main className="min-h-screen bg-black selection:bg-purple-500/30">
      
      {/* HERO SECTION */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-purple-600/10 rounded-full blur-[120px] pointer-events-none" />
        
        <div className="container mx-auto px-4 max-w-7xl grid lg:grid-cols-2 gap-12 items-center relative z-10">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-sm text-zinc-300 mb-6">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              v1.1.0 Developer Preview
            </div>
            
            <h1 className="text-5xl lg:text-7xl font-extrabold tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-br from-white via-white to-zinc-500">
              Built for Silicon.<br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-cyan-400">
                Loved by AI.
              </span>
            </h1>
            
            <p className="text-lg text-zinc-400 mb-8 leading-relaxed max-w-xl">
              AAYU is an experimental programming language and toolchain: AAYU compiler sources, a Rust bytecode VM, and separate BrainOS, Intent Engine, website, and editor projects.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 mb-8">
              <Link href="/download">
                  <Button className="h-full px-6 bg-zinc-800 text-white hover:bg-zinc-700 font-bold rounded-xl gap-2 py-3 border border-white/10 transition-colors">
                    <Download className="w-4 h-4" /> Download AAYU
                  </Button>
                </Link>
              <Link href="/tutorial">
                <Button className="h-full px-6 bg-purple-600 text-white hover:bg-purple-500 font-bold rounded-xl gap-2 py-3">
                  <Terminal className="w-4 h-4" /> Start Tutorial
                </Button>
              </Link>
            </div>
            
            <div className="flex flex-wrap gap-4 text-sm font-semibold text-zinc-500">
              <span className="flex items-center gap-1"><Zap className="w-4 h-4 text-yellow-500"/> Rust bytecode VM</span>
              <span className="flex items-center gap-1"><ShieldCheck className="w-4 h-4 text-emerald-500"/> Compiler and runtime status is documented</span>
            </div>
          </div>

          {/* CODE SHOWCASE */}
          <div className="relative mt-8 lg:mt-0">
            <div className="absolute -inset-1 bg-gradient-to-r from-purple-500/20 to-cyan-500/20 rounded-2xl blur-xl pointer-events-none" />
            <div className="relative bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden shadow-2xl">
              <div className="flex items-center px-4 py-3 bg-[#111] border-b border-white/5">
                <div className="flex gap-1.5 mr-4">
                  <div className="w-3 h-3 rounded-full bg-red-500/80" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                  <div className="w-3 h-3 rounded-full bg-green-500/80" />
                </div>
                <span className="text-xs font-mono text-zinc-500">app.aayu</span>
              </div>
              <div className="p-5 font-mono text-[13px] leading-[1.7] min-h-[500px]">
                {displayed.map((line, i) => (
                  <div key={i} className="flex">
                    <span className="w-8 text-right text-zinc-700 text-xs select-none mr-4 mt-[3px] shrink-0">{i + 1}</span>
                    <div>{highlightLine(line)}</div>
                  </div>
                ))}
                {!done && <span className="inline-block w-2 h-5 bg-purple-400 ml-12 animate-pulse rounded-sm" />}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* PROOF SECTION: TOKEN CONSUMPTION */}
      <section className="py-24 bg-[#050505] border-y border-white/5">
         <div className="container mx-auto px-4 max-w-7xl">
         <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6">Built to save <span className="text-purple-400">Context Tokens.</span></h2>
              <p className="text-zinc-400 mb-6 leading-relaxed">
                Giving an AI a complex React/Node/SQL project burns through its context window and reduces reasoning quality. Vibe Coders struggle because AI agents lose context.
              </p>
              <ul className="space-y-4 text-zinc-300">
                <li className="flex items-start gap-3">
                  <div className="mt-1 bg-green-500/20 p-1 rounded"><Check className="w-4 h-4 text-green-400" /></div>
                  <div>
                    <strong className="text-white block">AAYU solves Context limits</strong>
                    AAYU unites the Frontend, Backend, Database, and Math into ONE file. No more tracking imports across 50 files.
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="mt-1 bg-green-500/20 p-1 rounded"><Check className="w-4 h-4 text-green-400" /></div>
                  <div>
                    <strong className="text-white block">Self-Correcting Ecosystem</strong>
                    The AAYU compiler explicitly blocks structural hallucination. There is no `npm install` for AI to hallucinate. Everything is native.
                  </div>
                </li>
              </ul>
            </div>
            
            <div className="bg-gradient-to-b from-zinc-900 to-[#0a0a0a] border border-white/10 p-8 rounded-2xl">
                <h4 className="font-mono text-xs text-zinc-500 mb-6">TOKEN CONSUMPTION (Full Stack App)</h4>
                
                <div className="mb-6">
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-red-400 font-semibold">Node.js + React (Standard)</span>
                    <span className="text-zinc-400">~8,500 Tokens</span>
                  </div>
                  <div className="h-3 bg-zinc-800 rounded-full overflow-hidden">
                    <div className="h-full bg-red-500 w-[85%]" />
                  </div>
                </div>

                <div className="mb-6">
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-yellow-400 font-semibold">Python + FastAPI + SQLAlchemy</span>
                    <span className="text-zinc-400">~4,200 Tokens</span>
                  </div>
                  <div className="h-3 bg-zinc-800 rounded-full overflow-hidden">
                    <div className="h-full bg-yellow-500 w-[42%]" />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-green-400 font-semibold">AAYU (Single File Full-Stack)</span>
                    <span className="text-zinc-400 font-bold">~300 Tokens</span>
                  </div>
                  <div className="h-3 bg-zinc-800 rounded-full overflow-hidden relative">
                    <div className="absolute inset-0 bg-green-400/20 animate-pulse" />
                    <div className="h-full bg-green-500 w-[5%]" />
                  </div>
                </div>
            </div>
         </div>
         </div>
      </section>

      {/* BENCHMARKS & SECURITY PROOF SECTION */}
      <section className="py-24 border-b border-white/5 bg-gradient-to-b from-black via-zinc-950 to-black">
        <div className="container mx-auto px-4 max-w-7xl">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-xs font-semibold text-cyan-400 mb-4">
              <ShieldCheck className="w-3.5 h-3.5" />
              Implementation Notes & Recorded Measurements
            </div>
            <h2 className="text-3xl md:text-5xl font-extrabold mb-4 tracking-tight">
              How the Project Works. <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-emerald-400">With Measured Results.</span>
            </h2>
            <p className="text-zinc-400 max-w-3xl mx-auto text-lg leading-relaxed">
              AAYU combines an AAYU compiler pipeline with a Rust VM. The repository also includes other tools with their own dependencies and maturity levels.
            </p>
          </div>

          {/* 4 CORE PROOF CARDS */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            <div className="bg-[#0c0f17] border border-cyan-500/20 p-6 rounded-2xl relative overflow-hidden group hover:border-cyan-500/40 transition-all">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center mb-4 text-cyan-400">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Rust VM</h3>
              <p className="text-zinc-400 text-xs leading-relaxed">
                The bytecode VM and runtime are implemented in Rust. This does not replace review of unsafe boundaries, bytecode validation, or application behavior.
              </p>
              <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs text-cyan-400 font-mono">
                <span>Implementation:</span>
                <span className="font-bold">Rust</span>
              </div>
            </div>

            <div className="bg-[#0c0f17] border border-emerald-500/20 p-6 rounded-2xl relative overflow-hidden group hover:border-emerald-500/40 transition-all">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mb-4 text-emerald-400">
                <Zap className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Built-in Runtime Features</h3>
              <p className="text-zinc-400 text-xs leading-relaxed">
                AAYU programs can use runtime features without adding a separate JavaScript or Python package per feature. Building the Rust toolchain and website still uses external dependencies.
              </p>
              <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs text-emerald-400 font-mono">
                <span>Repository dependencies:</span>
                <span className="font-bold">See manifests</span>
              </div>
            </div>

            <div className="bg-[#0c0f17] border border-purple-500/20 p-6 rounded-2xl relative overflow-hidden group hover:border-purple-500/40 transition-all">
              <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center mb-4 text-purple-400">
                <Server className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">HTTP Runtime</h3>
              <p className="text-zinc-400 text-xs leading-relaxed">
                The Rust runtime includes an HTTP/TCP server implementation. Review the current runtime limitations before exposing a service publicly.
              </p>
              <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs text-purple-400 font-mono">
                <span>Details:</span>
                <span className="font-bold">See runtime docs</span>
              </div>
            </div>

            <div className="bg-[#0c0f17] border border-amber-500/20 p-6 rounded-2xl relative overflow-hidden group hover:border-amber-500/40 transition-all">
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center mb-4 text-amber-400">
                <Activity className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Bytecode VM</h3>
              <p className="text-zinc-400 text-xs leading-relaxed">
                The CLI compiles AAYU source to `.ayc` bytecode and executes it in the Rust VM. Published benchmarks include workload and machine-specific measurements.
              </p>
              <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs text-amber-400 font-mono">
                <span>Build output:</span>
                <span className="font-bold">.ayc bytecode</span>
              </div>
            </div>
          </div>

          <div className="mb-16 rounded-2xl border border-white/10 bg-[#0a0a0a] p-8">
            <div className="mb-4 flex items-center gap-3">
              <Terminal className="h-5 w-5 text-cyan-400" />
              <h3 className="text-lg font-bold text-white">AAYU Core Workload Matrix</h3>
            </div>
            <p className="mb-5 max-w-3xl text-sm leading-6 text-zinc-400">
              20 correctness-checked measurements across integer addition, multiply-accumulate, conditional branches, nested loops, and floating-point accumulation. Each workload runs at four input sizes; reports include expected output and timing range. VM startup is included, so these measurements do not claim per-instruction throughput.
            </p>
            <Link href="/benchmarks" className="font-semibold text-cyan-300 hover:underline">See all 20 benchmark results →</Link>
          </div>

          {/* WHAT CAN BE BUILT TODAY */}
          <div className="border border-white/10 bg-[#0d1117] rounded-2xl p-8 md:p-10">
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <Zap className="w-6 h-6 text-purple-400" />
              Project Areas and Examples
            </h3>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-black/40 border border-white/5 rounded-xl p-5">
                <span className="text-xs font-mono text-cyan-400 font-semibold mb-2 block">01 / CRYPTO & BLOCKCHAIN</span>
                <h4 className="text-white font-bold mb-2">PoUW Autonomous Ledgers</h4>
                <p className="text-zinc-400 text-xs leading-relaxed">
                  The repository includes a NeuroLedger experiment. Treat it as a prototype example, not a production blockchain or audited cryptographic system.
                </p>
              </div>
              <div className="bg-black/40 border border-white/5 rounded-xl p-5">
                <span className="text-xs font-mono text-purple-400 font-semibold mb-2 block">02 / AI AGENT CLOUD</span>
                <h4 className="text-white font-bold mb-2">Autonomous Agent Sandboxes</h4>
                <p className="text-zinc-400 text-xs leading-relaxed">
                  The language and VM are intended to support compact programs. The compiler, runtime, and surrounding tools are still under active development.
                </p>
              </div>
              <div className="bg-black/40 border border-white/5 rounded-xl p-5">
                <span className="text-xs font-mono text-emerald-400 font-semibold mb-2 block">03 / REAL-TIME EDGE</span>
                <h4 className="text-white font-bold mb-2">High-Throughput Microservices</h4>
                <p className="text-zinc-400 text-xs leading-relaxed">
                  The repository includes a Rust HTTP server implementation. Benchmark throughput, deployment limits, and resource use should be measured for the target workload before making capacity claims.
                </p>
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* FOUNDER SECTION */}
      <section className="py-24 container mx-auto px-4 max-w-7xl">
        <div className="bg-gradient-to-br from-[#111] to-[#0a0a0a] border border-white/10 rounded-3xl p-8 md:p-12 flex flex-col md:flex-row items-center gap-12">
          <div className="w-48 h-48 md:w-64 md:h-64 shrink-0 rounded-full border-4 border-purple-500/30 overflow-hidden relative shadow-[0_0_50px_rgba(168,85,247,0.2)]">
            <img 
              src="/ayush.png" 
              alt="Ayush Ghrit Kaushik"
              className="w-full h-full object-cover"
            />
          </div>
          <div>
            <h2 className="text-3xl font-bold mb-2">Created by <span className="text-purple-400">Ayush Ghrit Kaushik</span></h2>
            <p className="text-zinc-500 font-mono text-sm mb-6">@Minato95-ayu • Creator & Lead Architect</p>
            <p className="text-zinc-300 text-lg leading-relaxed mb-6">
              "I built AAYU because modern programming has become bloated. We spend more time configuring Docker and fixing pip dependencies than actually building products. AAYU is the reset button. It is the first programming language designed from the ground up for Vibe Coders and AI Agents to build Silicon-ready empires."
            </p>
            <div className="flex gap-4">
              <a href="https://github.com/Minato95-ayu" target="_blank" rel="noopener noreferrer" className="px-5 py-2.5 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl font-semibold transition-colors">
                GitHub Profile
              </a>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}






