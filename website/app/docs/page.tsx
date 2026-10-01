import Link from 'next/link';
import { Book, Code, Database, BrainCircuit, MonitorPlay, Server, Search } from 'lucide-react';

export default function DocsPage() {
  const categories = [
    { name: "Getting Started", icon: <Book className="w-6 h-6 text-purple-400" />, desc: "Installation, Hello World, and project structure.", link: "/tutorial" },
    { name: "Language Syntax", icon: <Code className="w-6 h-6 text-blue-400" />, desc: "Variables, loops, control flow, and strict typing.", link: "#" },
    { name: "Built-in Database", icon: <Database className="w-6 h-6 text-emerald-400" />, desc: "Zero-config SQLite, Models, CRUD, and Migrations.", link: "#" },
    { name: "Tensors & AI", icon: <BrainCircuit className="w-6 h-6 text-pink-400" />, desc: "Zero-copy PyTorch-style tensors and Math Engine.", link: "#" },
    { name: "Web Server", icon: <Server className="w-6 h-6 text-cyan-400" />, desc: "REST APIs, Routing, Auth, and Middleware.", link: "#" },
    { name: "UI Engine", icon: <MonitorPlay className="w-6 h-6 text-yellow-400" />, desc: "Declarative widget trees, Flexbox, and Events.", link: "#" },
  ];

  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-16">
      <div className="container mx-auto px-4 max-w-7xl">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-center mb-16 gap-8">
          <div>
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Documentation</h1>
            <p className="text-zinc-400 text-lg">Everything you need to build with AAYU.</p>
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

        {/* Categories Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-20">
          {categories.map((cat, i) => (
            <Link key={i} href={cat.link} className="block group">
              <div className="bg-[#0a0a0a] border border-white/5 p-8 rounded-2xl h-full hover:bg-[#111] hover:border-white/10 transition-all cursor-pointer">
                <div className="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  {cat.icon}
                </div>
                <h3 className="text-xl font-bold mb-2">{cat.name}</h3>
                <p className="text-zinc-500 text-sm leading-relaxed">{cat.desc}</p>
              </div>
            </Link>
          ))}
        </div>

        {/* Note about migration */}
        <div className="bg-purple-900/10 border border-purple-500/20 rounded-2xl p-8 flex items-start gap-4">
          <div className="p-2 bg-purple-500/20 rounded-lg text-purple-400">
            <Book className="w-6 h-6" />
          </div>
          <div>
            <h4 className="text-lg font-bold text-purple-100 mb-2">Documentation Migration in Progress</h4>
            <p className="text-purple-200/60 text-sm leading-relaxed">
              We are currently rewriting our entire documentation suite to reflect the new Rust Bytecode VM architecture (v1.1.0). 
              In the meantime, we highly recommend following the <Link href="/tutorial" className="text-purple-400 underline underline-offset-2">Step-by-Step Tutorial</Link> 
              which is fully updated for the latest engine.
            </p>
          </div>
        </div>

      </div>
    </main>
  );
}
