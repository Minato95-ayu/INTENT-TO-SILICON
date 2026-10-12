import React from 'react';

export default function CliPage() {
  return (
    <main className="min-h-screen pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-4xl">
        <h1 className="text-5xl font-bold mb-6">CLI & Tools</h1>
        <p className="text-xl text-zinc-400 mb-8">The current Rust VM CLI supports source/bytecode run, bytecode build, version, and help.</p>
        <div className="bg-black border border-white/10 rounded-lg p-6 font-mono text-zinc-300">
          <p><span className="text-blue-400">aayu-vm run</span> hello.aayu  <span className="text-zinc-500"># Compile with nearby aayuc and run</span></p>
          <p><span className="text-blue-400">aayu-vm build</span> hello.aayu -o hello.ayc  <span className="text-zinc-500"># Build bytecode</span></p>
          <p><span className="text-blue-400">aayu-vm run</span> hello.ayc  <span className="text-zinc-500"># Run bytecode</span></p>
          <p><span className="text-blue-400">aayu-vm --version</span>  <span className="text-zinc-500"># Show version</span></p>
        </div>
        <p className="mt-6 text-sm text-zinc-400">The `build` command does not emit a native executable. Full setup and command details are in the <a className="text-cyan-400 underline" href="/docs/5-cli/1-cli-reference">CLI reference</a>.</p>
      </div>
    </main>
  );
}
