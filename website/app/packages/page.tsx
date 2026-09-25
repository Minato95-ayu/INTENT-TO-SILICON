import React from 'react';
import { Package, Cpu, Database, Globe, Calculator, Shield, HardDrive, Network, FileJson, TerminalSquare, Search, Layout } from 'lucide-react';

export default function PackagesPage() {
  const modules = [
    { name: "ai", desc: "Neural Networks & Inference Engine", icon: <Cpu className="w-6 h-6 text-purple-400 mb-3" /> },
    { name: "ml", desc: "Native Machine Learning & Clustering", icon: <Package className="w-6 h-6 text-pink-400 mb-3" /> },
    { name: "db", desc: "Enterprise Database & Schema Engine", icon: <Database className="w-6 h-6 text-orange-400 mb-3" /> },
    { name: "http", desc: "High-Performance REST Routing", icon: <Globe className="w-6 h-6 text-blue-400 mb-3" /> },
    { name: "math", desc: "Tensor Math & Advanced Calc", icon: <Calculator className="w-6 h-6 text-emerald-400 mb-3" /> },
    { name: "crypto", desc: "AES Encryption, Hashing, JWT", icon: <Shield className="w-6 h-6 text-red-400 mb-3" /> },
    { name: "fs", desc: "Asynchronous File System I/O", icon: <HardDrive className="w-6 h-6 text-yellow-400 mb-3" /> },
    { name: "net", desc: "Raw TCP Sockets & WebSockets", icon: <Network className="w-6 h-6 text-cyan-400 mb-3" /> },
    { name: "json", desc: "Native JSON Parser & Serializer", icon: <FileJson className="w-6 h-6 text-green-400 mb-3" /> },
    { name: "os", desc: "Process & Thread Management", icon: <TerminalSquare className="w-6 h-6 text-zinc-400 mb-3" /> },
    { name: "regex", desc: "Pattern Matching & Text", icon: <Search className="w-6 h-6 text-indigo-400 mb-3" /> },
    { name: "ui", desc: "Declarative UI Widget Engine", icon: <Layout className="w-6 h-6 text-rose-400 mb-3" /> },
  ];

  return (
    <main className="min-h-screen pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-5xl text-center">
        <Package className="w-16 h-16 text-blue-500 mx-auto mb-6" />
        <h1 className="text-5xl font-bold mb-6">AAYU Standard Library</h1>
        <p className="text-xl text-zinc-400 mb-12">AAYU comes batteries-included. No need to download gigabytes of node_modules.</p>
        
        <div className="grid md:grid-cols-4 sm:grid-cols-2 gap-6 text-left">
          {modules.map((mod, i) => (
            <div key={i} className="bg-[#050505] border border-white/10 p-6 rounded-xl hover:border-purple-500/50 transition-colors">
              {mod.icon}
              <h3 className="font-bold mb-2 text-lg">{mod.name}</h3>
              <p className="text-sm text-zinc-400 leading-relaxed">{mod.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
