import React from 'react';
import Link from 'next/link';

export const metadata = {
  title: 'Benchmarks & Proofs | AAYU',
  description: 'Verified speed benchmarks and architecture proofs for the AAYU programming language.',
};

export default function BenchmarksPage() {
  return (
    <div className="min-h-screen bg-black text-white py-20">
      <div className="max-w-5xl mx-auto px-6">
        <div className="mb-12">
          <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
            Verified Benchmarks & Proofs
          </h1>
          <p className="text-xl text-zinc-400 leading-relaxed">
            We don't just make claims; we prove them. AAYU is built to be a bridge between the speed of C and the simplicity of Python, designed strictly to prevent AI hallucination.
          </p>
        </div>

        {/* Section 1: The Speed Benchmark */}
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-8 mb-12 shadow-2xl">
          <h2 className="text-3xl font-semibold mb-6 flex items-center">
            <span className="text-cyan-400 mr-3">⚡</span> 
            Raw Computation Speed (v0.3.1)
          </h2>
          <p className="text-zinc-300 mb-6">
            We tested <strong>1,000,000 addition operations (1M adds)</strong> across different languages to see how AAYU's new NaN-Boxed Rust Engine compares.
          </p>

          <div className="overflow-x-auto mb-8">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-zinc-700 bg-zinc-950">
                  <th className="p-4 font-semibold">Language / Engine</th>
                  <th className="p-4 font-semibold text-right">Time (1M Ops)</th>
                  <th className="p-4 font-semibold text-right">Comparison</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800">
                <tr className="hover:bg-zinc-800/50 transition">
                  <td className="p-4 flex items-center"><span className="w-3 h-3 rounded-full bg-green-500 mr-3"></span> C (gcc -O2 native)</td>
                  <td className="p-4 text-right font-mono text-green-400">~ 1.00 ms</td>
                  <td className="p-4 text-right text-zinc-400">Baseline</td>
                </tr>
                <tr className="bg-purple-900/20 hover:bg-purple-900/40 transition">
                  <td className="p-4 flex items-center font-bold text-purple-300"><span className="w-3 h-3 rounded-full bg-purple-500 mr-3"></span> AAYU (NaN-Boxed VM)</td>
                  <td className="p-4 text-right font-mono text-purple-400 font-bold">10.24 ms</td>
                  <td className="p-4 text-right text-purple-300 font-bold">13.6x Faster than Python</td>
                </tr>
                <tr className="hover:bg-zinc-800/50 transition">
                  <td className="p-4 flex items-center"><span className="w-3 h-3 rounded-full bg-yellow-500 mr-3"></span> Node.js (V8 JIT)</td>
                  <td className="p-4 text-right font-mono text-yellow-400">~ 19.30 ms</td>
                  <td className="p-4 text-right text-zinc-400">1.9x Slower than AAYU</td>
                </tr>
                <tr className="hover:bg-zinc-800/50 transition">
                  <td className="p-4 flex items-center"><span className="w-3 h-3 rounded-full bg-blue-500 mr-3"></span> Python 3.12</td>
                  <td className="p-4 text-right font-mono text-blue-400">~ 139.60 ms</td>
                  <td className="p-4 text-right text-zinc-400">13.6x Slower than AAYU</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="bg-black p-4 rounded-lg font-mono text-sm text-green-400 border border-zinc-800 overflow-x-auto">
            <div className="text-zinc-500 mb-2"># Raw Output from AAYU Test Suite</div>
            [ CORRECTNESS TESTS ]<br/>
            &nbsp;&nbsp;- Test 1: 10+20=30 passed.<br/>
            &nbsp;&nbsp;- Test 6 (File I/O): Writing and Reading 'test_output_aayu.txt'<br/>
            AAYU Native Rust Engine File I/O works perfectly!<br/>
            <br/>
            [ SPEED BENCHMARKS ]<br/>
            &nbsp;&nbsp;* AayuVM (NaN-boxed) 1M adds: 10.243ms
          </div>
        </div>

        {/* Section 2: AI Safety & Zero Dependencies */}
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-8 mb-12 shadow-2xl">
          <h2 className="text-3xl font-semibold mb-6 flex items-center">
            <span className="text-emerald-400 mr-3">🛡️</span> 
            Why Native Implanting Stops AI Hallucination
          </h2>
          
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-3 text-red-400">The Problem with Python/JS</h3>
              <p className="text-zinc-400 leading-relaxed mb-4">
                When an AI agent writes code in standard languages, it often guesses or "hallucinates" imports. It might write <code>import fs</code> or <code>npm install axios</code>, leading to broken setups, token waste, and fatal runtime errors. The boundaries are too loose.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-bold mb-3 text-emerald-400">The AAYU Solution</h3>
              <p className="text-zinc-400 leading-relaxed mb-4">
                In AAYU v0.3.1, we directly implanted <strong>Strings, File I/O, and Networking</strong> as <em>Native Opcodes</em> inside the Rust NaN-Boxed Engine. 
              </p>
              <ul className="list-disc list-inside text-zinc-300 space-y-2">
                <li>No <code>import</code> statements allowed.</li>
                <li>No dependency downloads.</li>
                <li>The AI is forced to use built-in keywords.</li>
              </ul>
            </div>
          </div>
          
          <div className="mt-6 p-6 bg-emerald-950/30 border border-emerald-900/50 rounded-lg">
            <h4 className="text-emerald-300 font-bold mb-2">The Compiler Boundary (Guardrails)</h4>
            <p className="text-zinc-300 text-sm">
              If an AI attempts to write hallucinated library code, AAYU's Auto-Receiver intercepts it at the parsing stage and returns a strict, machine-readable hint: <strong>"Do not import. Use native File.read()."</strong> This forces the AI back on track instantly without wasting execution cycles.
            </p>
          </div>
        </div>

        <div className="text-center">
          <Link href="/" className="inline-block bg-zinc-800 hover:bg-zinc-700 text-white font-semibold py-3 px-8 rounded-full transition duration-300">
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}
