import { Activity, ShieldCheck, Zap, AlertTriangle, CheckCircle2 } from 'lucide-react';

export default function ReportsPage() {
  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-16">
      <div className="container mx-auto px-4 max-w-7xl">
        
        <div className="text-center mb-20">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Security & <span className="text-purple-400">Benchmarks</span></h1>
          <p className="text-zinc-400 text-lg max-w-2xl mx-auto">
            100% Transparency. See our live test results, performance benchmarks, and compiler telemetry for the new Rust VM.
          </p>
        </div>

        {/* Top KPI Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-16">
          <div className="bg-gradient-to-b from-[#111] to-[#0a0a0a] border border-green-500/20 p-6 rounded-2xl relative overflow-hidden">
            <ShieldCheck className="absolute top-6 right-6 w-8 h-8 text-green-500/20" />
            <h3 className="text-zinc-400 font-semibold mb-2">Compiler Tests</h3>
            <div className="text-4xl font-bold text-white mb-2">282</div>
            <p className="text-sm text-green-400 flex items-center gap-1"><CheckCircle2 className="w-4 h-4"/> 100% Passing (Rust VM)</p>
          </div>

          <div className="bg-gradient-to-b from-[#111] to-[#0a0a0a] border border-cyan-500/20 p-6 rounded-2xl relative overflow-hidden">
            <Zap className="absolute top-6 right-6 w-8 h-8 text-cyan-500/20" />
            <h3 className="text-zinc-400 font-semibold mb-2">Speed vs Python</h3>
            <div className="text-4xl font-bold text-white mb-2">4.5x</div>
            <p className="text-sm text-cyan-400">Faster on math/loop microbenchmarks</p>
          </div>

          <div className="bg-gradient-to-b from-[#111] to-[#0a0a0a] border border-purple-500/20 p-6 rounded-2xl relative overflow-hidden">
            <Activity className="absolute top-6 right-6 w-8 h-8 text-purple-500/20" />
            <h3 className="text-zinc-400 font-semibold mb-2">VM Execution Latency</h3>
            <div className="text-4xl font-bold text-white mb-2">40.3ms</div>
            <p className="text-sm text-purple-400">Per 1,000,000 iterations</p>
          </div>
        </div>

        {/* Detailed Benchmark Section */}
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3"><Activity className="w-6 h-6 text-purple-400"/> Live Performance Data (Oct 2026)</h2>
        <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden mb-16">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-[#111] border-b border-white/5 text-xs uppercase tracking-wider text-zinc-500">
                  <th className="p-4 font-semibold">Workload (N)</th>
                  <th className="p-4 font-semibold">Implementation</th>
                  <th className="p-4 font-semibold">Total Process (ms)</th>
                  <th className="p-4 font-semibold">In-VM (ms)</th>
                  <th className="p-4 font-semibold">Result</th>
                </tr>
              </thead>
              <tbody className="text-sm text-zinc-300 divide-y divide-white/5">
                <tr className="hover:bg-white/5 transition-colors">
                  <td className="p-4 font-mono">1,000,000</td>
                  <td className="p-4">C (-O2)</td>
                  <td className="p-4">9.0</td>
                  <td className="p-4 text-zinc-600">N/A</td>
                  <td className="p-4 text-green-400">OK</td>
                </tr>
                <tr className="bg-purple-900/10 hover:bg-purple-900/20 transition-colors">
                  <td className="p-4 font-mono text-purple-200">1,000,000</td>
                  <td className="p-4 font-bold text-purple-400">AAYU VM</td>
                  <td className="p-4 text-purple-200">48.1</td>
                  <td className="p-4 font-mono text-purple-300">40.3</td>
                  <td className="p-4 text-green-400">OK</td>
                </tr>
                <tr className="hover:bg-white/5 transition-colors">
                  <td className="p-4 font-mono">1,000,000</td>
                  <td className="p-4">Python 3.12</td>
                  <td className="p-4">179.2</td>
                  <td className="p-4 text-zinc-600">N/A</td>
                  <td className="p-4 text-green-400">OK</td>
                </tr>
                {/* 10M iterations */}
                <tr className="hover:bg-white/5 transition-colors">
                  <td className="p-4 font-mono">10,000,000</td>
                  <td className="p-4">C (-O2)</td>
                  <td className="p-4">22.3</td>
                  <td className="p-4 text-zinc-600">N/A</td>
                  <td className="p-4 text-green-400">OK</td>
                </tr>
                <tr className="bg-purple-900/10 hover:bg-purple-900/20 transition-colors">
                  <td className="p-4 font-mono text-purple-200">10,000,000</td>
                  <td className="p-4 font-bold text-purple-400">AAYU VM</td>
                  <td className="p-4 text-purple-200">417.3</td>
                  <td className="p-4 font-mono text-purple-300">410.0</td>
                  <td className="p-4 text-green-400">OK</td>
                </tr>
                <tr className="hover:bg-white/5 transition-colors">
                  <td className="p-4 font-mono">10,000,000</td>
                  <td className="p-4">Python 3.12</td>
                  <td className="p-4">1535.7</td>
                  <td className="p-4 text-zinc-600">N/A</td>
                  <td className="p-4 text-green-400">OK</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Security Audit */}
        <div className="bg-[#111] border border-red-500/20 rounded-2xl p-8 flex items-start gap-6">
          <div className="p-3 bg-red-500/10 rounded-xl text-red-400">
            <AlertTriangle className="w-8 h-8" />
          </div>
          <div>
            <h3 className="text-xl font-bold mb-2">Security Transparency Notice</h3>
            <p className="text-zinc-400 leading-relaxed mb-4">
              AAYU is currently in <strong>v1.1.0 (Developer Preview)</strong>. While the Rust VM is inherently memory-safe compared to raw C, the web server (ASGI mock) and DB layers are currently mocked or not hardened against production injection attacks. Do not use AAYU in a production environment facing the public internet until our upcoming <code>v2.0</code> Security Audit is complete.
            </p>
          </div>
        </div>

      </div>
    </main>
  );
}
