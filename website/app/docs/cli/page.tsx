import React from 'react';
import Link from 'next/link';
import { Terminal, ShieldCheck, FolderPlus, Info, Smartphone, Cpu, CheckCircle } from 'lucide-react';

export default function CliPage() {
  return (
    <main className="min-h-screen bg-[#050505] text-white pt-28 pb-20">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="mb-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-mono mb-4">
            <Terminal className="w-3.5 h-3.5" /> AAYU Toolchain v1.2.0
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4">AAYU CLI & Tooling</h1>
          <p className="text-lg text-zinc-400">
            A single, zero-dependency binary (<code className="text-purple-300">aayu</code>) with embedded compiler, silicon stack VM, and Android Termux detection.
          </p>
        </div>

        {/* Command Reference Cards */}
        <div className="grid gap-6 mb-12">
          
          {/* Run Command */}
          <div className="bg-[#0a0a0d] border border-white/10 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-3">
              <span className="px-2.5 py-1 rounded-md bg-purple-500/20 text-purple-300 font-mono text-sm font-semibold">aayu run</span>
              <h3 className="text-lg font-semibold text-white">Execute AAYU Source or Bytecode</h3>
            </div>
            <p className="text-zinc-400 text-sm mb-4">
              Directly compiles in-memory and executes pure AAYU source files (<code className="text-zinc-300">.ay</code>, <code className="text-zinc-300">.aa</code>, <code className="text-zinc-300">.aayu</code>) or precompiled bytecode (<code className="text-zinc-300">.ayc</code>).
            </p>
            <div className="bg-black/80 border border-white/5 rounded-xl p-4 font-mono text-xs text-zinc-300 space-y-1">
              <div><span className="text-emerald-400">aayu run</span> main.ay <span className="text-zinc-500"># Direct compile &amp; run</span></div>
              <div><span className="text-emerald-400">aayu run</span> app.ayc --jit <span className="text-zinc-500"># Run bytecode with C-level JIT acceleration</span></div>
              <div><span className="text-emerald-400">aayu</span> script.aayu <span className="text-zinc-500"># Shorthand invocation</span></div>
            </div>
          </div>

          {/* Check Command */}
          <div className="bg-[#0a0a0d] border border-white/10 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-3">
              <span className="px-2.5 py-1 rounded-md bg-cyan-500/20 text-cyan-300 font-mono text-sm font-semibold">aayu check</span>
              <h3 className="text-lg font-semibold text-white">Syntax &amp; Structural Verification</h3>
            </div>
            <p className="text-zinc-400 text-sm mb-4">
              Validates tokens, AST nodes, and emitter compatibility without executing code or spinning up runtime servers.
            </p>
            <div className="bg-black/80 border border-white/5 rounded-xl p-4 font-mono text-xs text-zinc-300">
              <div><span className="text-cyan-400">aayu check</span> app.aayu</div>
              <div className="text-zinc-500 mt-1"># Output: [AAYU Check] Syntax OK: &apos;app.aayu&apos; (Generated 131 bytes bytecode)</div>
            </div>
          </div>

          {/* Init Command */}
          <div className="bg-[#0a0a0d] border border-white/10 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-3">
              <span className="px-2.5 py-1 rounded-md bg-emerald-500/20 text-emerald-300 font-mono text-sm font-semibold">aayu init</span>
              <h3 className="text-lg font-semibold text-white">Scaffold New Intent Project</h3>
            </div>
            <p className="text-zinc-400 text-sm mb-4">
              Initializes a clean, standard AAYU project structure with boilerplate <code className="text-zinc-300">main.aayu</code>, <code className="text-zinc-300">aayu.json</code>, and <code className="text-zinc-300">.gitignore</code>.
            </p>
            <div className="bg-black/80 border border-white/5 rounded-xl p-4 font-mono text-xs text-zinc-300 space-y-1">
              <div><span className="text-emerald-400">aayu init</span> neuro_app</div>
              <div><span className="text-zinc-400">cd</span> neuro_app</div>
              <div><span className="text-emerald-400">aayu run</span> main.aayu</div>
            </div>
          </div>

          {/* Info & Termux Command */}
          <div className="bg-[#0a0a0d] border border-white/10 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-3">
              <span className="px-2.5 py-1 rounded-md bg-amber-500/20 text-amber-300 font-mono text-sm font-semibold">aayu info</span>
              <h3 className="text-lg font-semibold text-white">System, Architecture &amp; Termux Info</h3>
            </div>
            <p className="text-zinc-400 text-sm mb-4">
              Prints diagnostic details including OS, CPU architecture, JIT capability, and automatically detects Android Termux environment.
            </p>
            <div className="bg-black/80 border border-white/5 rounded-xl p-4 font-mono text-xs text-zinc-300 space-y-1">
              <div><span className="text-amber-400">aayu info</span> <span className="text-zinc-500"># or: aayu sysinfo</span></div>
              <div className="text-zinc-500 mt-2">==================================================</div>
              <div className="text-zinc-300">Engine Version:   1.2.0 (Self-Hosted Intent-to-Silicon)</div>
              <div className="text-zinc-300">Operating System: android / linux / windows</div>
              <div className="text-zinc-300">Environment:      Android Termux (v0.118+)</div>
              <div className="text-zinc-300">VM Runtime:       AAYU High-Speed Silicon Stack VM</div>
              <div className="text-zinc-500">==================================================</div>
            </div>
          </div>

        </div>

        {/* Termux Section */}
        <div className="bg-gradient-to-r from-emerald-500/10 to-transparent border border-emerald-500/20 rounded-2xl p-8 mb-12">
          <div className="flex items-center gap-3 mb-4">
            <Smartphone className="w-6 h-6 text-emerald-400" />
            <h2 className="text-2xl font-bold text-white">Android Termux &amp; Mobile Setup</h2>
          </div>
          <p className="text-zinc-300 text-sm mb-4 leading-relaxed">
            AAYU binaries are built statically with zero dynamic dependencies. You can download and run AAYU directly on any Android smartphone using Termux without root privileges:
          </p>
          <div className="bg-black/90 border border-white/10 rounded-xl p-4 font-mono text-xs text-emerald-300 space-y-2 overflow-x-auto">
            <div><span className="text-zinc-500"># Download &amp; install AAYU in Termux:</span></div>
            <div>curl -sSL https://intent-to-silicon.com/install.sh | bash</div>
            <div><span className="text-zinc-500"># Check environment and start coding:</span></div>
            <div>aayu info</div>
            <div>aayu init my_mobile_app</div>
          </div>
        </div>

        <div className="text-center">
          <Link href="/tutorial/chapter-1" className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold transition-colors">
            Start AAYU 50-Chapter Tutorial &rarr;
          </Link>
        </div>
      </div>
    </main>
  );
}
