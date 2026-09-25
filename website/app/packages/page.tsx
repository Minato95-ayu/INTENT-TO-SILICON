import React from 'react';
import { Package } from 'lucide-react';

export default function PackagesPage() {
  return (
    <main className="min-h-screen pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-4xl text-center">
        <Package className="w-16 h-16 text-blue-500 mx-auto mb-6" />
        <h1 className="text-5xl font-bold mb-6">AAYU Standard Library</h1>
        <p className="text-xl text-zinc-400 mb-12">AAYU comes batteries-included. No need to download gigabytes of node_modules.</p>
        <div className="grid md:grid-cols-3 gap-6 text-left">
          <div className="bg-[#050505] border border-white/10 p-6 rounded-xl">
            <h3 className="font-bold mb-2">Net / HTTP</h3>
            <p className="text-sm text-zinc-400">Built-in REST server and client.</p>
          </div>
          <div className="bg-[#050505] border border-white/10 p-6 rounded-xl">
            <h3 className="font-bold mb-2">Database</h3>
            <p className="text-sm text-zinc-400">Embedded SQLite & Schema Engine.</p>
          </div>
          <div className="bg-[#050505] border border-white/10 p-6 rounded-xl">
            <h3 className="font-bold mb-2">AI / ML</h3>
            <p className="text-sm text-zinc-400">Native Neural Networks and clustering.</p>
          </div>
        </div>
      </div>
    </main>
  );
}
