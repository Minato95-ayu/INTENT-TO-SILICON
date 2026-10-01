'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ChevronRight, Terminal, Copy, Check, Bot, Sparkles, Zap, Server, Database, LayoutTemplate } from 'lucide-react';

const codeString = // Welcome to AAYU: The AI-Agent Language
app CoreApp

// 1. Built-in Database Models
model User
    id Int
    username String
end

// 2. Built-in Web Server
route "/api/users"
    get
        let users = User.all()
        respond(users)
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
        Text("Hello AAYU!")
        Button("Run AI", onClick: train_ai)
    end
end

run Home;

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
    }, 150);

    return () => clearInterval(interval);
  }, []);

  const handleCopy = () => {
    navigator.clipboard.writeText("git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git");
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
              v1.1.0 is now live — Built for AI Agents
            </div>
            
            <h1 className="text-5xl lg:text-7xl font-extrabold tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-br from-white via-white to-zinc-500">
              The Language for <br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-cyan-400">
                AI Coding Agents.
              </span>
            </h1>
            
            <p className="text-lg text-zinc-400 mb-8 leading-relaxed max-w-xl">
              AAYU is a Single-File Full-Stack programming language. We replaced the chaos of Webpack, pip, and Docker with a unified Rust-based Bytecode VM. Built-in Database, Server, Zero-Copy Tensors, and UI. Fast, honest, and zero-config.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 mb-8">
              <div className="flex items-center bg-[#111] border border-white/10 rounded-xl px-4 py-3">
                <span className="text-purple-400 font-mono text-sm mr-3">$</span>
                <code className="text-sm font-mono text-zinc-300">git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON</code>
                <button onClick={handleCopy} className="text-zinc-500 hover:text-white transition-colors ml-3">
                  {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
                </button>
              </div>
              <Link href="/tutorial">
                <Button className="h-full px-6 bg-purple-600 text-white hover:bg-purple-500 font-bold rounded-xl gap-2 py-3">
                  <Terminal className="w-4 h-4" /> Start Tutorial
                </Button>
              </Link>
            </div>
            
            <div className="flex flex-wrap gap-4 text-sm font-semibold text-zinc-500">
              <span className="flex items-center gap-1"><Zap className="w-4 h-4 text-yellow-500"/> ~4.5x Faster than Python</span>
              <span className="flex items-center gap-1"><Server className="w-4 h-4 text-cyan-500"/> Native Rust VM</span>
              <span className="flex items-center gap-1"><Database className="w-4 h-4 text-emerald-500"/> Zero-Copy Tensors</span>
            </div>
          </div>

          {/* CODE SHOWCASE */}
          <div className="relative">
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

      {/* CORE PHILOSOPHY / EXTREME HONESTY */}
      <section className="bg-[#050505] border-y border-white/5 py-24">
        <div className="container mx-auto px-4 max-w-7xl">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold mb-4">No Fake Benchmarks. <span className="text-purple-400">Just Real Engineering.</span></h2>
            <p className="text-zinc-400 max-w-3xl mx-auto text-lg">
              We are not trying to beat C. AAYU is an interpreted Bytecode VM written in Rust. It takes ~40ms to run a 1M loop, making it roughly <strong>5x faster than Python</strong>, but it is not C. Our goal is ecosystem unity, not raw mathematical C-speed.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-[#0a0a0a] border border-white/5 p-8 rounded-2xl hover:border-purple-500/30 transition-all">
              <Bot className="w-10 h-10 text-purple-400 mb-6" />
              <h3 className="text-xl font-bold mb-3">Zero Hallucinations</h3>
              <p className="text-zinc-400 text-sm leading-relaxed">
                AI agents (Cursor, Copilot, Gemini) break when they guess missing packages. AAYU has Database, Auth, UI, and Tensors built directly into the Rust Runtime.
              </p>
            </div>

            <div className="bg-[#0a0a0a] border border-white/5 p-8 rounded-2xl hover:border-cyan-500/30 transition-all">
              <LayoutTemplate className="w-10 h-10 text-cyan-400 mb-6" />
              <h3 className="text-xl font-bold mb-3">Single-File Full-Stack</h3>
              <p className="text-zinc-400 text-sm leading-relaxed">
                Forget 
pm install, equirements.txt, or Dockerizing Postgres. AAYU brings models, routes, logic, and declarative UI into one beautiful .aayu file.
              </p>
            </div>

            <div className="bg-[#0a0a0a] border border-white/5 p-8 rounded-2xl hover:border-emerald-500/30 transition-all">
              <Database className="w-10 h-10 text-emerald-400 mb-6" />
              <h3 className="text-xl font-bold mb-3">AI & Tensors Native</h3>
              <p className="text-zinc-400 text-sm leading-relaxed">
                PyTorch and Pandas functionality are not external libraries. AAYU natively maps multidimensional strided Tensors (Zero-Copy) inside its memory heap.
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
