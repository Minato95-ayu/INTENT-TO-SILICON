import React from 'react';

export default function CliPage() {
  return (
    <main className="min-h-screen pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-4xl">
        <h1 className="text-5xl font-bold mb-6">CLI & Tools</h1>
        <p className="text-xl text-zinc-400 mb-8">Master the AAYU Command Line Interface.</p>
        <div className="bg-black border border-white/10 rounded-lg p-6 font-mono text-zinc-300">
          <p><span className="text-blue-400">aayuc build</span> main.aayu  <span className="text-zinc-500"># Build native binary</span></p>
          <p><span className="text-blue-400">aayuc run</span> main.aayu    <span className="text-zinc-500"># Run in fast VM mode</span></p>
          <p><span className="text-blue-400">aayuc fmt</span> main.aayu    <span className="text-zinc-500"># Format source code</span></p>
        </div>
      </div>
    </main>
  );
}
