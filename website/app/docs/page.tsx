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
            <p className="text-zinc-400 text-lg">Guides to the current AAYU language, Rust VM, and related project tools.</p>
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

        <div className="mb-12 rounded-xl border border-amber-500/30 bg-amber-500/5 p-5 text-sm text-amber-100">
          Some examples on this page are conceptual sketches and have not been verified as runnable programs. For executable core-language examples, use the repository regression files. The runtime database is currently a JSON-backed key-value store, not SQLite or relational SQL.
        </div>

        {/* Core Architecture */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">1. The Silicon-Direct Architecture</h2>
          <p className="text-zinc-400 mb-6 leading-relaxed">
            The current command-line tool uses a Rust bootstrap compiler to produce AAYU bytecode, then runs it in the Rust VM. Other repository tools use Python, Node.js, and their own dependencies.
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
              The VM uses a mark-and-sweep heap collector. The current core examples use inferred values and keyword-delimited blocks.
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
            The Rust runtime currently provides a JSON-backed key-value store. The model and CRUD example below is a concept sketch; SQLite, relational queries, and migrations are not implemented by this storage module.
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
            The Rust runtime contains HTTP/TCP server code. The route snippet below is illustrative; review feature coverage and deployment limits before relying on it.
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
        {/* AI & Math */}
        <div className="mb-20">
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

        {/* Standard Libraries */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">7. Pure AAYU Standard Libraries</h2>
          <p className="text-zinc-400 mb-6 leading-relaxed">
            The standard libraries are written in 100% pure AAYU (.aayu) under <code className="text-purple-300">std/</code> with zero external dependencies. They provide functional collection shortcuts, file I/O, OS interactions, and cryptography.
          </p>
          <div className="bg-[#0a0a0a] border border-white/10 rounded-xl overflow-hidden mb-6">
            <div className="bg-[#111] px-4 py-2 border-b border-white/5 text-xs text-zinc-500 font-mono">std/collections.aayu &amp; std/fs.aayu</div>
            <pre className="p-6 text-sm text-zinc-300 overflow-x-auto">
              <code>{`import "std/collections"
import "std/fs"
import "std/os"

// 1. Functional Array Shortcuts (21 pure AAYU utilities)
let nums = [10, 20, 30, 40, 50]
print("Sum:", sum(nums))          // 150
print("Min:", array_min(nums))   // 10
print("Max:", array_max(nums))   // 50
print("Mean:", mean(nums))        // 30
let slice_part = slice(nums, 1, 4) // [20, 30, 40]
let rev = reverse(nums)           // [50, 40, 30, 20, 10]
let nums_range = range(1, 10, 2)  // [1, 3, 5, 7, 9]

// 2. Pure File System & OS Queries
write_file("cache.json", "{\\"status\\": \\"active\\"}")
let raw_data = read_file("cache.json")
print("Host OS:", os_platform())
print("Working Directory:", os_cwd())`}</code>
            </pre>
          </div>
        </div>

        {/* Multi-line Strings & Type Reflection */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">8. Multi-line Strings &amp; Runtime Type Reflection</h2>
          <p className="text-zinc-400 mb-6 leading-relaxed">
            AAYU natively supports multi-line triple-quoted strings (<code className="text-purple-300">&quot;&quot;&quot;...&quot;&quot;&quot;</code>) for clean templates, poetry, or SQL queries, alongside the native <code className="text-purple-300">type()</code> runtime reflection operator.
          </p>
          <div className="bg-[#0a0a0a] border border-white/10 rounded-xl overflow-hidden">
            <div className="bg-[#111] px-4 py-2 border-b border-white/5 text-xs text-zinc-500 font-mono">reflection.aayu</div>
            <pre className="p-6 text-sm text-zinc-300 overflow-x-auto">
              <code>{`// 1. Multi-line Triple-Quoted Strings
print("""Twinkle, twinkle, little star,
How I wonder what you are!
Up above the world so high,
Like a diamond in the sky.""")

// 2. Runtime Type Inspection
let ram = 100
let name = "Ayush"
let items = [1, 2, 3]

print("Type of ram:", type(ram))     // "Int"
print("Type of name:", type(name))   // "String"
print("Type of items:", type(items)) // "Array"`}</code>
            </pre>
          </div>
        </div>

        {/* Android Mobile IDE & Termux */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">9. Mobile IDE &amp; Android Termux Support</h2>
          <p className="text-zinc-400 mb-6 leading-relaxed">
            AAYU includes a full touch-first Mobile IDE (inspired by Pydroid 3) and direct Termux CLI runtime support for offline on-device coding.
          </p>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="p-6 rounded-xl bg-zinc-900/60 border border-emerald-500/30">
              <h3 className="text-lg font-bold text-emerald-400 mb-2">AAYU Android APK &amp; PWA</h3>
              <p className="text-zinc-400 text-sm mb-4 leading-relaxed">
                Installable on Android 8.0+ devices. Features a touch symbol keyboard strip, real-time bytecode execution, and GitHub Auto-Update sync.
              </p>
              <a href="/downloads/aayu-android.apk" download className="inline-flex items-center gap-2 text-sm font-bold text-emerald-300 hover:text-emerald-200">
                Download APK (v1.1.0) &rarr;
              </a>
            </div>

            <div className="p-6 rounded-xl bg-zinc-900/60 border border-purple-500/30">
              <h3 className="text-lg font-bold text-purple-400 mb-2">Termux CLI Execution</h3>
              <p className="text-zinc-400 text-sm mb-4 leading-relaxed">
                Run natively in Termux with auto-environment detection. Zero dependencies, zero configuration.
              </p>
              <code className="text-xs bg-black px-3 py-1.5 rounded border border-white/10 text-purple-300 block font-mono">
                curl -sSL https://intent-to-silicon.com/install.sh | bash
              </code>
            </div>
          </div>
        </div>

        {/* Download Master Handbook Banner */}
        <div className="p-8 rounded-2xl bg-gradient-to-r from-purple-900/30 via-indigo-900/20 to-black border border-purple-500/40 flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <h3 className="text-xl font-bold text-white mb-2">The Ultimate AAYU Master Handbook (21 Chapters)</h3>
            <p className="text-zinc-400 text-sm max-w-xl">
              Complete engineering manual by Ayush Ghrit Kaushik. Includes all 21 chapters, memory architecture, 20 master interview problems, and full source code.
            </p>
          </div>
          <a
            href="/aayu-handbook.pdf"
            download="The_Ultimate_AAYU_Handbook_Ayush_Ghrit_Kaushik.pdf"
            className="px-6 py-3 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-sm shrink-0 shadow-lg shadow-purple-600/30 transition hover:scale-105"
          >
            Download PDF (1.8 MB)
          </a>
        </div>

      </div>
    </main>
  );
}
