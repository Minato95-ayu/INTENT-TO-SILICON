'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
  Cpu, 
  Layers, 
  Terminal, 
  ShieldCheck, 
  Zap, 
  Database, 
  Network, 
  Code2, 
  GitBranch, 
  CheckCircle2, 
  ArrowRight,
  Sparkles,
  Server,
  FileCode2
} from 'lucide-react';

const OPCODES = [
  { op: '0x00', name: 'OP_HALT', width: '1 byte', stack: '[] -> []', desc: 'Terminates execution cleanly' },
  { op: '0x01', name: 'OP_PUSH_CONST', width: '3 bytes', stack: '[] -> [val]', desc: 'Pushes 16-bit constant from pool' },
  { op: '0x02', name: 'OP_POP', width: '1 byte', stack: '[val] -> []', desc: 'Pops top stack value' },
  { op: '0x05', name: 'OP_LOAD_VAR', width: '2 bytes', stack: '[] -> [val]', desc: 'Loads local variable from slot 0..255' },
  { op: '0x06', name: 'OP_STORE_VAR', width: '2 bytes', stack: '[val] -> []', desc: 'Stores top stack item to local slot' },
  { op: '0x10', name: 'OP_ADD', width: '1 byte', stack: '[a, b] -> [a+b]', desc: 'Polymorphic add (Int, Float, Str, Arr)' },
  { op: '0x11', name: 'OP_SUB', width: '1 byte', stack: '[a, b] -> [a-b]', desc: 'Numeric subtract (Int, Float)' },
  { op: '0x12', name: 'OP_MUL', width: '1 byte', stack: '[a, b] -> [a*b]', desc: 'Numeric multiply (Int, Float)' },
  { op: '0x13', name: 'OP_DIV', width: '1 byte', stack: '[a, b] -> [a/b]', desc: 'Numeric division with zero check' },
  { op: '0x20', name: 'OP_JMP', width: '3 bytes', stack: '[] -> []', desc: 'Unconditional jump to 16-bit offset' },
  { op: '0x21', name: 'OP_JMP_IF_FALSE', width: '3 bytes', stack: '[cond] -> []', desc: 'Jumps if popped condition is false' },
  { op: '0x22', name: 'OP_CALL', width: '3 bytes', stack: '[fn, args] -> [res]', desc: 'Invokes function or action frame' },
  { op: '0x23', name: 'OP_RET', width: '1 byte', stack: '[res] -> [res]', desc: 'Returns from action frame' },
  { op: '0x26', name: 'OP_CMP_EQ', width: '1 byte', stack: '[a, b] -> [bool]', desc: 'Equality comparison (a == b)' },
  { op: '0x29', name: 'OP_CMP_LT', width: '1 byte', stack: '[a, b] -> [bool]', desc: 'Less-than comparison (a < b)' },
  { op: '0x30', name: 'OP_STORE_STATE', width: '3 bytes', stack: '[val] -> []', desc: 'Persists key-value state to RAM & WAL' },
  { op: '0x31', name: 'OP_LOAD_STATE', width: '3 bytes', stack: '[] -> [val]', desc: 'Reads key-value state from RAM' },
  { op: '0x51', name: 'OP_PRINT', width: '1 byte', stack: '[val] -> []', desc: 'Native stdout print with newline' },
];

const DIRECTORY_TREE = [
  { dir: 'compiler/', tech: 'Pure .aayu (5,661 lines)', desc: 'Self-hosted Lexer, Parser, AST, Analyzer, and Bytecode Emitter.' },
  { dir: 'runtime_rs/', tech: 'Rust (Bare-Metal)', desc: 'Silicon VM, NaN-boxed stack, JIT, Memory Manager, multi-threaded TCP.' },
  { dir: 'compiler_bootstrap/', tech: 'Rust (Zero-dep)', desc: 'Minimal seed compiler for 100% reproducible cold builds.' },
  { dir: 'bin/', tech: 'Native Binaries', desc: 'Official signed binaries (aayu, aayu-vm, aayuc) & seed bytecode aayuc.ayc.' },
  { dir: 'tests/', tech: 'AAYU & PowerShell', desc: 'Formal verification suite and automated test harness (run_tests.ps1).' },
  { dir: 'examples/', tech: 'Pure .aayu', desc: 'Production examples: Todo API, Chat Server, NeuroLedger, Auth System.' },
  { dir: 'std/', tech: 'Native Standard Lib', desc: 'Built-in modules: HTTP, JSON, Database, Math, Crypto, Vision.' },
  { dir: 'website/', tech: 'Next.js 15, React', desc: 'Interactive documentation, playground, and learning syllabus.' },
  { dir: 'vscode-aayu/', tech: 'TypeScript / LSP', desc: 'Official VS Code extension for syntax highlighting and language server.' },
];

export default function ArchitecturePage() {
  const [activeTab, setActiveTab] = useState<'compiler' | 'vm' | 'bootstrap'>('compiler');

  return (
    <main className="min-h-screen pt-28 pb-24 bg-black text-white selection:bg-indigo-500/30">
      <div className="container mx-auto px-4 max-w-6xl">
        
        {/* Header Banner */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-950/60 border border-indigo-500/30 text-indigo-400 text-xs font-semibold mb-6">
            <Sparkles className="w-3.5 h-3.5" />
            INTENT-TO-SILICON ARCHITECTURAL BLUEPRINT
          </div>
          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight mb-6 bg-gradient-to-b from-white via-zinc-200 to-zinc-500 bg-clip-text text-transparent">
            System Design & Architecture
          </h1>
          <p className="text-lg text-zinc-400 leading-relaxed">
            How AAYU eliminates 1,200+ dependencies, achieves sub-millisecond cold boot, and executes full-stack apps from a single source file without Python or Node.js.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4 mt-8">
            <a 
              href="https://github.com/Minato95-ayu/INTENT-TO-SILICON/blob/main/COMPILER_CONFIDENCE_REPORT.md" 
              target="_blank" 
              rel="noreferrer"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 text-white font-semibold text-sm hover:bg-indigo-500 transition-colors shadow-lg shadow-indigo-500/20"
            >
              <ShieldCheck className="w-4 h-4" />
              Compiler Confidence Report
            </a>
            <a 
              href="https://github.com/Minato95-ayu/INTENT-TO-SILICON/blob/main/ARCHITECTURE.md" 
              target="_blank" 
              rel="noreferrer"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white text-black font-semibold text-sm hover:bg-zinc-200 transition-colors"
            >
              <FileCode2 className="w-4 h-4" />
              View Full ARCHITECTURE.md on GitHub
            </a>
            <Link
              href="/playground"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-zinc-900 border border-white/10 text-zinc-200 font-semibold text-sm hover:bg-zinc-800 transition-colors"
            >
              Test in Live Playground
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        {/* 3 Core Layers Interactive Switcher */}
        <div className="mb-20">
          <div className="flex border-b border-zinc-800 gap-2 mb-8 overflow-x-auto pb-2">
            <button
              onClick={() => setActiveTab('compiler')}
              className={`flex items-center gap-2 px-5 py-3 rounded-lg text-sm font-semibold transition-all ${
                activeTab === 'compiler'
                  ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/40'
                  : 'text-zinc-400 hover:text-white hover:bg-zinc-900'
              }`}
            >
              <Code2 className="w-4 h-4" />
              1. Self-Hosted Compiler Layer (.aayu)
            </button>
            <button
              onClick={() => setActiveTab('vm')}
              className={`flex items-center gap-2 px-5 py-3 rounded-lg text-sm font-semibold transition-all ${
                activeTab === 'vm'
                  ? 'bg-cyan-600/20 text-cyan-400 border border-cyan-500/40'
                  : 'text-zinc-400 hover:text-white hover:bg-zinc-900'
              }`}
            >
              <Cpu className="w-4 h-4" />
              2. Silicon Virtual Machine (Rust)
            </button>
            <button
              onClick={() => setActiveTab('bootstrap')}
              className={`flex items-center gap-2 px-5 py-3 rounded-lg text-sm font-semibold transition-all ${
                activeTab === 'bootstrap'
                  ? 'bg-emerald-600/20 text-emerald-400 border border-emerald-500/40'
                  : 'text-zinc-400 hover:text-white hover:bg-zinc-900'
              }`}
            >
              <GitBranch className="w-4 h-4" />
              3. Reproducibility & Bootstrap
            </button>
          </div>

          {activeTab === 'compiler' && (
            <div className="bg-zinc-950 border border-zinc-800 rounded-2xl p-6 sm:p-8">
              <div className="flex items-center justify-between mb-6 flex-wrap gap-4">
                <div>
                  <span className="text-xs uppercase font-bold tracking-widest text-indigo-400">Layer 1: Self-Hosted Compiler</span>
                  <h3 className="text-2xl font-bold text-white mt-1">compiler/*.aayu (5,661 Lines of Pure AAYU)</h3>
                </div>
                <span className="px-3 py-1 rounded-full text-xs font-semibold bg-indigo-950 text-indigo-300 border border-indigo-800/60">
                  Zero Python • 100% Native AAYU
                </span>
              </div>
              <p className="text-zinc-300 text-sm leading-relaxed mb-6">
                The AAYU compiler is completely self-hosted and written in its own syntax. It processes full-stack source code through 5 tightly integrated stages to generate silicon-ready bytecode (.ayc):
              </p>
              <div className="grid grid-cols-1 md:grid-cols-5 gap-3 mb-6">
                <div className="p-4 bg-zinc-900/60 border border-zinc-800 rounded-xl">
                  <div className="text-xs font-mono text-indigo-400 mb-1">01. LEXER</div>
                  <h4 className="font-semibold text-white text-sm">lexer.aayu</h4>
                  <p className="text-xs text-zinc-400 mt-2">LZR Tokenizer with line & column tracking. Skips comments and normalizes tokens.</p>
                </div>
                <div className="p-4 bg-zinc-900/60 border border-zinc-800 rounded-xl">
                  <div className="text-xs font-mono text-indigo-400 mb-1">02. PARSER</div>
                  <h4 className="font-semibold text-white text-sm">parser.aayu</h4>
                  <p className="text-xs text-zinc-400 mt-2">Recursive descent AST generator for Models, Routes, Pages, Actions, Loops.</p>
                </div>
                <div className="p-4 bg-zinc-900/60 border border-zinc-800 rounded-xl">
                  <div className="text-xs font-mono text-indigo-400 mb-1">03. ANALYZER</div>
                  <h4 className="font-semibold text-white text-sm">analyzer.aayu</h4>
                  <p className="text-xs text-zinc-400 mt-2">Scope resolution, symbol table binding, and compile-time invariant checking.</p>
                </div>
                <div className="p-4 bg-zinc-900/60 border border-zinc-800 rounded-xl">
                  <div className="text-xs font-mono text-indigo-400 mb-1">04. EMITTER</div>
                  <h4 className="font-semibold text-white text-sm">compiler.aayu</h4>
                  <p className="text-xs text-zinc-400 mt-2">Variable-length bytecode emission with two-pass jump offset patching.</p>
                </div>
                <div className="p-4 bg-zinc-900/60 border border-zinc-800 rounded-xl">
                  <div className="text-xs font-mono text-indigo-400 mb-1">05. UI ENGINE</div>
                  <h4 className="font-semibold text-white text-sm">ui_renderer.aayu</h4>
                  <p className="text-xs text-zinc-400 mt-2">Transpiles declarative widget trees directly into DOM structures.</p>
                </div>
              </div>
              <div className="p-4 bg-black/60 border border-zinc-800 rounded-xl font-mono text-xs text-zinc-300">
                <span className="text-zinc-500"># Verify compiler self-hosting:</span><br/>
                <span className="text-indigo-400">.\bin\aayuc.exe</span> compiler\aayuc.aayu -o bin\aayuc.ayc <span className="text-emerald-400"># Emits 32,043 bytes clean seed bytecode</span>
              </div>
            </div>
          )}

          {activeTab === 'vm' && (
            <div className="bg-zinc-950 border border-zinc-800 rounded-2xl p-6 sm:p-8">
              <div className="flex items-center justify-between mb-6 flex-wrap gap-4">
                <div>
                  <span className="text-xs uppercase font-bold tracking-widest text-cyan-400">Layer 2: Execution Engine</span>
                  <h3 className="text-2xl font-bold text-white mt-1">runtime_rs/ (Silicon Virtual Machine & JIT)</h3>
                </div>
                <span className="px-3 py-1 rounded-full text-xs font-semibold bg-cyan-950 text-cyan-300 border border-cyan-800/60">
                  Rust For Speed Only • NanBox 64-Bit Stack
                </span>
              </div>
              <p className="text-zinc-300 text-sm leading-relaxed mb-6">
                Written in Rust exclusively for bare-metal speed and memory safety. The VM uses NaN-boxing to encode all dynamically typed values into 64-bit hardware registers with zero pointer chasing:
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="p-4 bg-zinc-900/60 border border-zinc-800 rounded-xl">
                  <div className="flex items-center gap-2 text-cyan-400 text-sm font-semibold mb-2">
                    <Zap className="w-4 h-4" />
                    Sub-Millisecond Cold Boot
                  </div>
                  <p className="text-xs text-zinc-400 leading-relaxed">
                    Cold boots in &lt;1.5ms with ~14MB idle memory footprint. Ideal for serverless micro-functions, CLI tools, and edge controllers.
                  </p>
                </div>
                <div className="p-4 bg-zinc-900/60 border border-zinc-800 rounded-xl">
                  <div className="flex items-center gap-2 text-cyan-400 text-sm font-semibold mb-2">
                    <Network className="w-4 h-4" />
                    Multi-Threaded Panic Guard
                  </div>
                  <p className="text-xs text-zinc-400 leading-relaxed">
                    TCP requests are served in dedicated thread pools with 5s socket timeouts and <code className="text-cyan-300">catch_unwind</code>. One client failure never halts the server.
                  </p>
                </div>
                <div className="p-4 bg-zinc-900/60 border border-zinc-800 rounded-xl">
                  <div className="flex items-center gap-2 text-cyan-400 text-sm font-semibold mb-2">
                    <Database className="w-4 h-4" />
                    RAM Cache + WAL Storage
                  </div>
                  <p className="text-xs text-zinc-400 leading-relaxed">
                    In-memory hash table persistence backed by Write-Ahead Log (WAL) SSD flush. Zero SQL injection surface.
                  </p>
                </div>
              </div>
              <div className="p-4 bg-black/60 border border-zinc-800 rounded-xl font-mono text-xs text-zinc-300">
                <span className="text-zinc-500"># Direct bytecode execution:</span><br/>
                <span className="text-cyan-400">.\bin\aayu-vm.exe</span> app.ayc <span className="text-emerald-400"># Dispatches opcodes in ~79ns per instruction</span>
              </div>
            </div>
          )}

          {activeTab === 'bootstrap' && (
            <div className="bg-zinc-950 border border-zinc-800 rounded-2xl p-6 sm:p-8">
              <div className="flex items-center justify-between mb-6 flex-wrap gap-4">
                <div>
                  <span className="text-xs uppercase font-bold tracking-widest text-emerald-400">Layer 3: Reproducibility</span>
                  <h3 className="text-2xl font-bold text-white mt-1">compiler_bootstrap/ (Self-Hosting Nirvana)</h3>
                </div>
                <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-950 text-emerald-300 border border-emerald-800/60">
                  Zero Hidden Dependencies • 100% Cold Reproducible
                </span>
              </div>
              <p className="text-zinc-300 text-sm leading-relaxed mb-6">
                To guarantee that anyone cloning the repository can build from complete scratch without relying on pre-existing binaries, AAYU maintains a minimal, zero-dependency bootstrap compiler:
              </p>
              <div className="space-y-3 mb-6 font-mono text-xs">
                <div className="p-3 bg-zinc-900 border border-zinc-800 rounded-lg flex items-center gap-3">
                  <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 font-bold">STAGE 1</span>
                  <span className="text-zinc-300">cargo build --release --manifest-path compiler_bootstrap/Cargo.toml</span>
                </div>
                <div className="p-3 bg-zinc-900 border border-zinc-800 rounded-lg flex items-center gap-3">
                  <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 font-bold">STAGE 2</span>
                  <span className="text-zinc-300">.\bin\aayuc.exe compiler\aayuc.aayu -o bin\aayuc.ayc (Re-generates Seed Bytecode)</span>
                </div>
                <div className="p-3 bg-zinc-900 border border-zinc-800 rounded-lg flex items-center gap-3">
                  <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 font-bold">STAGE 3</span>
                  <span className="text-zinc-300">.\bin\aayu-vm.exe bin\aayuc.ayc (Pure Self-Hosted Execution)</span>
                </div>
              </div>
              <p className="text-xs text-zinc-400 leading-relaxed">
                This closes the self-hosting circle completely: no hidden binaries, no external Python scripts, and no unverified dependencies.
              </p>
            </div>
          )}
        </div>

        {/* Directory Map Table */}
        <div className="mb-20">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-white">Repository Directory Layout</h2>
            <p className="text-zinc-400 text-sm mt-1">Crystalline organization ensuring zero confusion for contributors and AI agents.</p>
          </div>
          <div className="border border-zinc-800 rounded-2xl overflow-hidden bg-zinc-950">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-zinc-900/80 border-b border-zinc-800 text-zinc-300 font-mono text-xs uppercase">
                  <tr>
                    <th className="py-3 px-4">Directory</th>
                    <th className="py-3 px-4">Core Technology</th>
                    <th className="py-3 px-4">Architectural Purpose</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-800/60 font-mono text-xs">
                  {DIRECTORY_TREE.map((item, idx) => (
                    <tr key={idx} className="hover:bg-zinc-900/30 transition-colors">
                      <td className="py-3.5 px-4 font-bold text-indigo-400">{item.dir}</td>
                      <td className="py-3.5 px-4 text-zinc-300">{item.tech}</td>
                      <td className="py-3.5 px-4 text-zinc-400 font-sans text-xs">{item.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* NaN-Box Memory Model */}
        <div className="mb-20">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-white">The 64-Bit NaN-Box Memory Model</h2>
            <p className="text-zinc-400 text-sm mt-1">High-performance value tagging without heap allocation or pointer dereferencing.</p>
          </div>
          <div className="bg-zinc-950 border border-zinc-800 rounded-2xl p-6 sm:p-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-white text-base mb-3">IEEE-754 Quiet NaN Bit Allocation</h4>
                <p className="text-zinc-400 text-xs leading-relaxed mb-4">
                  In IEEE-754, numbers where bits 62..51 are all 1 and bit 50 is 1 are Quiet NaNs. AAYU uses the remaining 48 bits to pack 48-bit pointers, integers, booleans, and references directly inside the double-precision float space:
                </p>
                <div className="space-y-2 font-mono text-xs">
                  <div className="p-2.5 rounded bg-zinc-900 border border-zinc-800 flex justify-between">
                    <span className="text-zinc-400">Float64</span>
                    <span className="text-cyan-400">val &lt; 0x7FF8_0000_0000_0000</span>
                  </div>
                  <div className="p-2.5 rounded bg-zinc-900 border border-zinc-800 flex justify-between">
                    <span className="text-zinc-400">Int48</span>
                    <span className="text-indigo-400">0x7FF8 | (value & 0xFFFF_FFFF_FFFF)</span>
                  </div>
                  <div className="p-2.5 rounded bg-zinc-900 border border-zinc-800 flex justify-between">
                    <span className="text-zinc-400">Bool</span>
                    <span className="text-emerald-400">0x7FFA | (0 or 1)</span>
                  </div>
                  <div className="p-2.5 rounded bg-zinc-900 border border-zinc-800 flex justify-between">
                    <span className="text-zinc-400">Null</span>
                    <span className="text-zinc-500">0x7FFB | 0</span>
                  </div>
                  <div className="p-2.5 rounded bg-zinc-900 border border-zinc-800 flex justify-between">
                    <span className="text-zinc-400">Heap Ptrs (Str, Arr, Dict)</span>
                    <span className="text-purple-400">0x7FFC..0x7FFE | 48-bit Heap Index</span>
                  </div>
                </div>
              </div>

              <div>
                <h4 className="font-semibold text-white text-base mb-3">Why This Dominates Traditional VMs</h4>
                <ul className="space-y-3 text-xs text-zinc-300">
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 mt-0.5 shrink-0" />
                    <span><strong>Zero Memory Indirection:</strong> Primitive numbers and booleans reside directly on the CPU register stack—no malloc or GC scan needed.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 mt-0.5 shrink-0" />
                    <span><strong>100% Cache Line Efficiency:</strong> 8 values fit inside a standard 64-byte L1 CPU cache line, enabling ultra-fast arithmetic loops.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 mt-0.5 shrink-0" />
                    <span><strong>Type-Safe Polymorphism:</strong> Branch prediction checks type tags in &lt;1ns before arithmetic dispatch.</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Bytecode ISA Table */}
        <div className="mb-20">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-white">Bytecode Instruction Set (ISA)</h2>
            <p className="text-zinc-400 text-sm mt-1">Silicon VM opcode definitions, widths, and stack effects.</p>
          </div>
          <div className="border border-zinc-800 rounded-2xl overflow-hidden bg-zinc-950">
            <div className="overflow-x-auto max-h-96">
              <table className="w-full text-left text-sm">
                <thead className="bg-zinc-900/90 border-b border-zinc-800 text-zinc-300 font-mono text-xs uppercase sticky top-0">
                  <tr>
                    <th className="py-3 px-4">Hex</th>
                    <th className="py-3 px-4">Instruction</th>
                    <th className="py-3 px-4">Width</th>
                    <th className="py-3 px-4">Stack Transition</th>
                    <th className="py-3 px-4">Description</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-800/60 font-mono text-xs">
                  {OPCODES.map((item, idx) => (
                    <tr key={idx} className="hover:bg-zinc-900/30 transition-colors">
                      <td className="py-3 px-4 text-cyan-400 font-bold">{item.op}</td>
                      <td className="py-3 px-4 text-white font-bold">{item.name}</td>
                      <td className="py-3 px-4 text-zinc-400">{item.width}</td>
                      <td className="py-3 px-4 text-indigo-300">{item.stack}</td>
                      <td className="py-3 px-4 text-zinc-400 font-sans text-xs">{item.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="text-center p-12 bg-gradient-to-b from-zinc-900/60 to-black border border-zinc-800 rounded-3xl">
          <h3 className="text-2xl font-bold text-white mb-3">Ready to build on AAYU?</h3>
          <p className="text-zinc-400 text-sm max-w-xl mx-auto mb-6">
            Explore our interactive tutorials, test in the browser playground, or clone the self-hosted repo.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              href="/tutorial"
              className="px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm transition-colors"
            >
              Start 50-Chapter Masterclass
            </Link>
            <Link
              href="/download"
              className="px-6 py-3 rounded-xl bg-zinc-900 hover:bg-zinc-800 border border-white/10 text-zinc-200 font-semibold text-sm transition-colors"
            >
              Download Binaries (v1.2.0)
            </Link>
          </div>
        </div>

      </div>
    </main>
  );
}
