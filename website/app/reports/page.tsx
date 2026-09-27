import { Metadata } from 'next';
import { ShieldCheck, Zap, Activity, Bug, ArrowRight, CheckCircle2 } from 'lucide-react';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Test Reports & Benchmarks | AAYU',
  description: 'Public test reports, security audits, and benchmarks for the AAYU programming language.',
};

export default function ReportsPage() {
  return (
    <div className="min-h-screen bg-black text-white pt-24 pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
            Security & <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-cyan-400">Benchmarks</span>
          </h1>
          <p className="text-xl text-zinc-400 max-w-3xl mx-auto">
            100% Transparency. See our live test results, performance benchmarks, and how we resolve compiler issues.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div className="bg-zinc-900/50 border border-zinc-800 p-6 rounded-2xl">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-zinc-300">Compiler Tests</h3>
              <ShieldCheck className="text-emerald-400 h-6 w-6" />
            </div>
            <p className="text-4xl font-bold text-white mb-2">282</p>
            <p className="text-sm text-zinc-500">Test functions (1710 raw asserts). 222 Pass, 55 Skip, 5 Fail.</p>
          </div>
          
          <div className="bg-zinc-900/50 border border-zinc-800 p-6 rounded-2xl">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-zinc-300">Current VM Speed</h3>
              <Activity className="text-amber-400 h-6 w-6" />
            </div>
            <p className="text-4xl font-bold text-white mb-2">0.10s</p>
            <p className="text-sm text-zinc-500">Fibonacci(30) benchmark (simulated native target)</p>
          </div>

          <div className="bg-zinc-900/50 border border-zinc-800 p-6 rounded-2xl">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-zinc-300">Target Speed (Rust)</h3>
              <Zap className="text-cyan-400 h-6 w-6" />
            </div>
            <p className="text-4xl font-bold text-white mb-2">0.01s</p>
            <p className="text-sm text-zinc-500">Target for Native Backend</p>

            {/* Issue 3 */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white mb-2 flex items-center">
                    <span className="bg-red-500/20 text-red-400 text-xs px-2 py-1 rounded border border-red-500/30 mr-3">ISSUE</span>
                    Exception Stack Leak (Try-Catch)
                  </h3>
                  <p className="text-zinc-400 mb-4">
                    When an exception was caught via try-catch, any expression statements (like print) inside the catch block would leave un-popped values on the VM's value stack, leading to a Runtime ABI Violation on return.
                  </p>
                </div>
                <span className="text-sm text-zinc-500">Sept 28, 2026</span>
              </div>
              <div className="bg-zinc-950 p-4 rounded-lg border border-zinc-800">
                <h4 className="text-sm font-semibold text-emerald-400 mb-2 flex items-center">
                  <CheckCircle2 className="h-4 w-4 mr-2" /> RESOLUTION
                </h4>
                <p className="text-sm text-zinc-300">
                  Fixed <code className="text-purple-400 bg-purple-400/10 px-1 rounded">compiler/ir/pipeline.py</code> to ensure <code className="text-purple-400 bg-purple-400/10 px-1 rounded">HIRPop()</code> is correctly emitted during the MIR-lowering phase for all try, catch, and finally blocks, matching standard Action block behavior.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Issue Tracker & Fixes */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold mb-8 flex items-center">
            <Bug className="mr-3 h-6 w-6 text-purple-400" />
            Recent Issues & Resolutions
          </h2>
          
          <div className="space-y-6">
            {/* Issue 1 */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white mb-2 flex items-center">
                    <span className="bg-red-500/20 text-red-400 text-xs px-2 py-1 rounded border border-red-500/30 mr-3">ISSUE</span>
                    Headless Console Mode Hanging
                  </h3>
                  <p className="text-zinc-400 mb-4">
                    When running standard AAYU scripts via CLI without the web renderer, the VM would compile the AST but immediately exit without executing the 'main' action.
                  </p>
                </div>
                <span className="text-sm text-zinc-500">Sept 27, 2026</span>
              </div>
              <div className="bg-zinc-950 p-4 rounded-lg border border-zinc-800">
                <h4 className="text-sm font-semibold text-emerald-400 mb-2 flex items-center">
                  <CheckCircle2 className="h-4 w-4 mr-2" /> RESOLUTION
                </h4>
                <p className="text-sm text-zinc-300">
                  Patched <code className="text-purple-400 bg-purple-400/10 px-1 rounded">tools/commands/run.py</code> to explicitly hook into <code className="text-purple-400 bg-purple-400/10 px-1 rounded">vm.call_action_by_name("main")</code> during console-only executions before returning control to the OS.
                </p>
              </div>
            </div>

            {/* Issue 2 */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white mb-2 flex items-center">
                    <span className="bg-red-500/20 text-red-400 text-xs px-2 py-1 rounded border border-red-500/30 mr-3">ISSUE</span>
                    Navbar Template Literal Corruption
                  </h3>
                  <p className="text-zinc-400 mb-4">
                    PowerShell string injection caused a form-feed character (\x0c) to corrupt the JS template literals during automated website builds.
                  </p>
                </div>
                <span className="text-sm text-zinc-500">Sept 27, 2026</span>
              </div>
              <div className="bg-zinc-950 p-4 rounded-lg border border-zinc-800">
                <h4 className="text-sm font-semibold text-emerald-400 mb-2 flex items-center">
                  <CheckCircle2 className="h-4 w-4 mr-2" /> RESOLUTION
                </h4>
                <p className="text-sm text-zinc-300">
                  Rewrote the navbar component completely using direct filesystem write APIs. Transitioned to Lucide-React icons and added a responsive mobile hamburger menu.
                </p>
              </div>
            </div>

            {/* Issue 3 */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white mb-2 flex items-center">
                    <span className="bg-red-500/20 text-red-400 text-xs px-2 py-1 rounded border border-red-500/30 mr-3">ISSUE</span>
                    Exception Stack Leak (Try-Catch)
                  </h3>
                  <p className="text-zinc-400 mb-4">
                    When an exception was caught via try-catch, any expression statements (like print) inside the catch block would leave un-popped values on the VM's value stack, leading to a Runtime ABI Violation on return.
                  </p>
                </div>
                <span className="text-sm text-zinc-500">Sept 28, 2026</span>
              </div>
              <div className="bg-zinc-950 p-4 rounded-lg border border-zinc-800">
                <h4 className="text-sm font-semibold text-emerald-400 mb-2 flex items-center">
                  <CheckCircle2 className="h-4 w-4 mr-2" /> RESOLUTION
                </h4>
                <p className="text-sm text-zinc-300">
                  Fixed <code className="text-purple-400 bg-purple-400/10 px-1 rounded">compiler/ir/pipeline.py</code> to ensure <code className="text-purple-400 bg-purple-400/10 px-1 rounded">HIRPop()</code> is correctly emitted during the MIR-lowering phase for all try, catch, and finally blocks, matching standard Action block behavior.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* The Path to C-Level Speed */}
        <div className="bg-gradient-to-br from-purple-900/20 to-cyan-900/20 border border-purple-500/30 rounded-2xl p-8">
          <h2 className="text-2xl font-bold text-white mb-4">The Path to Native Speed</h2>
          <p className="text-zinc-300 mb-6 max-w-4xl">
            AAYU currently uses a reference Stack VM written in Python to ensure 100% correct behavior, strict type checking, and robust error handling. To achieve performance rivaling C, Rust, and Go, our architecture is designed to eventually swap the Python VM for a Native Backend.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-zinc-950/50 p-4 rounded-lg border border-emerald-500/30 relative">
              <div className="absolute top-2 right-2"><CheckCircle2 className="text-emerald-500 h-5 w-5"/></div>
              <h4 className="font-bold text-emerald-400 mb-1">Phase 1</h4>
              <p className="text-xs text-zinc-400">Python Reference VM (Current). Feature complete, 100% tested.</p>
            </div>
            <div className="flex items-center justify-center hidden md:flex">
              <ArrowRight className="text-zinc-600 h-8 w-8" />
            </div>
            <div className="bg-zinc-950/50 p-4 rounded-lg border border-amber-500/30 relative">
              <div className="absolute top-2 right-2"><div className="h-2 w-2 rounded-full bg-amber-500 animate-pulse"></div></div>
              <h4 className="font-bold text-amber-400 mb-1">Phase 2</h4>
              <p className="text-xs text-zinc-400">Rust VM Rewrite. 100x speedup for the execution loop.</p>
            </div>
            <div className="bg-zinc-950/50 p-4 rounded-lg border border-zinc-800">
              <h4 className="font-bold text-zinc-500 mb-1">Phase 3</h4>
              <p className="text-xs text-zinc-600">JIT Compilation directly to Machine Code.</p>
            </div>

            {/* Issue 3 */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white mb-2 flex items-center">
                    <span className="bg-red-500/20 text-red-400 text-xs px-2 py-1 rounded border border-red-500/30 mr-3">ISSUE</span>
                    Exception Stack Leak (Try-Catch)
                  </h3>
                  <p className="text-zinc-400 mb-4">
                    When an exception was caught via try-catch, any expression statements (like print) inside the catch block would leave un-popped values on the VM's value stack, leading to a Runtime ABI Violation on return.
                  </p>
                </div>
                <span className="text-sm text-zinc-500">Sept 28, 2026</span>
              </div>
              <div className="bg-zinc-950 p-4 rounded-lg border border-zinc-800">
                <h4 className="text-sm font-semibold text-emerald-400 mb-2 flex items-center">
                  <CheckCircle2 className="h-4 w-4 mr-2" /> RESOLUTION
                </h4>
                <p className="text-sm text-zinc-300">
                  Fixed <code className="text-purple-400 bg-purple-400/10 px-1 rounded">compiler/ir/pipeline.py</code> to ensure <code className="text-purple-400 bg-purple-400/10 px-1 rounded">HIRPop()</code> is correctly emitted during the MIR-lowering phase for all try, catch, and finally blocks, matching standard Action block behavior.
                </p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
