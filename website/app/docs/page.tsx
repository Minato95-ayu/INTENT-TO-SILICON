import Link from 'next/link';
import { Book, Code, Database, BrainCircuit, MonitorPlay, Server, Search, Terminal, Zap } from 'lucide-react';

export default function DocsPage() {
  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-16">
      <div className="container mx-auto px-4 max-w-5xl">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-center mb-16 gap-8">
          <div>
            <h1 className="text-4xl md:text-5xl font-bold mb-4">AAYU Documentation</h1>
            <p className="text-zinc-400 text-lg">The definitive guide to the Intent-to-Silicon programming language.</p>
          </div>
          
          <div className="relative w-full md:w-96">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-500" />
            <input 
              type="text" 
              placeholder="Search documentation (Cmd+K)" 
              className="w-full bg-[#111] border border-white/10 rounded-xl py-3 pl-12 pr-4 text-sm text-white focus:outline-none focus:border-purple-500/50 transition-colors"
            />
          </div>
        </div>

        {/* Core Architecture */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">1. The Silicon-Direct Architecture</h2>
          <p className="text-zinc-400 mb-6 leading-relaxed">
            AAYU is not a framework. It is a compiled language with a custom Rust bytecode VM. There is no Node.js, no V8, no Python involved in the runtime.
          </p>
          <div className="bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 font-mono text-sm text-zinc-300">
            <div className="flex flex-col gap-4">
               <div className="p-4 bg-purple-500/10 border border-purple-500/20 rounded-lg">1. You write .aayu code (UI, DB, Backend)</div>
               <div className="flex justify-center text-zinc-600">↓</div>
               <div className="p-4 bg-cyan-500/10 border border-cyan-500/20 rounded-lg">2. aayuc (Rust Compiler) parses AST and generates Native Bytecode (.ayc)</div>
               <div className="flex justify-center text-zinc-600">↓</div>
               <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-lg">3. aayu-vm (Rust VM) executes OPCODES and binds native TCP Sockets</div>
            </div>
          </div>
        </div>

        {/* Hello World */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">2. Basics & Syntax</h2>
          <p className="text-zinc-400 mb-6 leading-relaxed">
            AAYU is strongly typed, memory-safe (Mark-and-Sweep GC), and uses clean, intent-driven syntax.
          </p>
          <div className="bg-[#0a0a0a] border border-white/10 rounded-xl overflow-hidden">
            <div className="bg-[#111] px-4 py-2 border-b border-white/5 text-xs text-zinc-500 font-mono">hello.aayu</div>
            <pre className="p-6 text-sm text-zinc-300 overflow-x-auto">
              <code>{`app Basics

action main
    let x = 10
    let name = "Developer"
    
    if x > 5
        print("Hello, " + name)
    end
end

run main`}</code>
            </pre>
          </div>
        </div>

        {/* Database */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">3. Built-in Database Models</h2>
          <p className="text-zinc-400 mb-6 leading-relaxed">
            No ORMs, no SQL strings, no migrations setup. Just declare your model and the compiler handles the SQLite engine integration natively at bytecode level.
          </p>
          <div className="bg-[#0a0a0a] border border-white/10 rounded-xl overflow-hidden">
            <div className="bg-[#111] px-4 py-2 border-b border-white/5 text-xs text-zinc-500 font-mono">db.aayu</div>
            <pre className="p-6 text-sm text-zinc-300 overflow-x-auto">
              <code>{`app DataApp

model User
    id Int
    username String
    email String
end

action seed_db
    User.insert({ id: 1, username: "ayush", email: "ayush@example.com" })
    let users = User.all()
    print(users)
end

run seed_db`}</code>
            </pre>
          </div>
        </div>

        {/* Web Server & Routing */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">4. Built-in HTTP Server</h2>
          <p className="text-zinc-400 mb-6 leading-relaxed">
            The Rust VM spins up an async TCP listener internally when it encounters routing opcodes. Extreme performance, zero dependencies.
          </p>
          <div className="bg-[#0a0a0a] border border-white/10 rounded-xl overflow-hidden">
            <div className="bg-[#111] px-4 py-2 border-b border-white/5 text-xs text-zinc-500 font-mono">api.aayu</div>
            <pre className="p-6 text-sm text-zinc-300 overflow-x-auto">
              <code>{`app RestAPI

route "/api/health"
    get
        respond({ status: "ok", uptime: "99.9%" })
    end
end

route "/api/users"
    get
        return User.all()
    end
    
    post
        // Body is automatically parsed
        User.insert(request.body)
        respond({ success: true })
    end
end`}</code>
            </pre>
          </div>
        </div>

        {/* Native UI */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">5. Native Zero-HTML UI Engine</h2>
          <p className="text-zinc-400 mb-6 leading-relaxed">
            Forget HTML, CSS, or React. You write declarative AAYU widgets. The AAYU Compiler parses them, resolves inline styles, and bakes them directly into the bytecode's constant pool. The VM then serves them instantly over its built-in socket.
          </p>
          <div className="bg-[#0a0a0a] border border-white/10 rounded-xl overflow-hidden">
            <div className="bg-[#111] px-4 py-2 border-b border-white/5 text-xs text-zinc-500 font-mono">ui.aayu</div>
            <pre className="p-6 text-sm text-zinc-300 overflow-x-auto">
              <code>{`app PortfolioUI

Page HomePage
    Column width="100vw" height="100vh" backgroundColor="#06060d"
        
        Row padding="20px" justifyContent="space-between"
            Text "ayush.dev" fontWeight="bold" color="#fff"
            Button "Contact Me" backgroundColor="#a78bfa"
        end
        
        Container padding="100px"
            Heading "Built for Silicon." fontSize="48px" color="#fff"
            Text "Loved by AI." color="#22d3ee"
        end
        
    end
end

run HomePage`}</code>
            </pre>
          </div>
        </div>

        {/* AI & Math */}
        <div className="mb-10">
          <h2 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">6. Native Tensor Engine</h2>
          <p className="text-zinc-400 mb-6 leading-relaxed">
            AI math shouldn't require downloading 5GB of PyTorch/CUDA binaries. AAYU has zero-copy multi-dimensional Tensors built directly into the language syntax and VM.
          </p>
          <div className="bg-[#0a0a0a] border border-white/10 rounded-xl overflow-hidden">
            <div className="bg-[#111] px-4 py-2 border-b border-white/5 text-xs text-zinc-500 font-mono">math.aayu</div>
            <pre className="p-6 text-sm text-zinc-300 overflow-x-auto">
              <code>{`app AIMath

action train
    // Native syntax for tensor creation
    let weights = Tensor.new([3, 3], [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0])
    
    // Hardware accelerated ops
    let transposed = weights.transpose()
    let result = weights.matmul(transposed)
    
    print(result)
end

run train`}</code>
            </pre>
          </div>
        </div>

      </div>
    </main>
  );
}
