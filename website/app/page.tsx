'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { Terminal, Code2, Zap, Server, Database, BrainCircuit, Cpu, Layers, Layout, ArrowRight, Download, CheckCircle2, Shield, Lock, Globe, MessageSquare, Image as ImageIcon, FileJson, FileDigit, Boxes, FileCode2 } from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState(0);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  const libraries = [
    { name: "aayu-gemini", desc: "Native Google Gemini AI integration", icon: <BrainCircuit className="w-6 h-6 text-blue-400" /> },
    { name: "aayu-ml", desc: "Built-in machine learning models & clustering", icon: <Layers className="w-6 h-6 text-purple-400" /> },
    { name: "aayu-auth", desc: "JWT, Session, and OAuth ready", icon: <Shield className="w-6 h-6 text-emerald-400" /> },
    { name: "aayu-crypto", desc: "Blazing fast cryptography & hashing", icon: <Lock className="w-6 h-6 text-zinc-400" /> },
    { name: "aayu-http", desc: "High-performance async HTTP client", icon: <Globe className="w-6 h-6 text-cyan-400" /> },
    { name: "aayu-vision", desc: "Computer vision and image processing", icon: <ImageIcon className="w-6 h-6 text-rose-400" /> },
    { name: "aayu-rag", desc: "Retrieval-Augmented Generation toolkit", icon: <Database className="w-6 h-6 text-orange-400" /> },
    { name: "aayu-dataframe", desc: "Pandas-like data manipulation", icon: <FileJson className="w-6 h-6 text-green-400" /> },
    { name: "aayu-math", desc: "Advanced mathematical computing", icon: <FileDigit className="w-6 h-6 text-yellow-400" /> }
  ];

  const comparisons = [
    { lang: "AAYU (JIT)", speed: 98, color: "bg-blue-500", time: "50ms" },
    { lang: "Rust", speed: 100, color: "bg-orange-500", time: "48ms" },
    { lang: "Go", speed: 85, color: "bg-cyan-500", time: "80ms" },
    { lang: "Node.js", speed: 60, color: "bg-green-500", time: "180ms" },
    { lang: "Python", speed: 15, color: "bg-yellow-500", time: "1.2s" },
  ];

  const tabs = [
    {
      name: "1. Full-Stack in One File",
      icon: <Server className="w-4 h-4 mr-2" />,
      code: `app AAYUGram

// 1. Database Model (SQLite Built-in)
model Post
    username String
    content String
    likes Int
end

// 2. REST API Route
route "/api/feed"
    get
        let posts = Post.all()
        respond(posts)
    end
end

// 3. Declarative UI
Page Home
    Column padding="20px"
        Heading "AAYUGram" color="#E1306C"
        Button "Create Post" onClick="createPost"
    end
end`,
      output: `[AAYU] Compiling AAYUGram.aayu -> Rust JIT Engine...
[AAYU] SQLite In-Memory Database Initialized.
[AAYU] Migrated model 'Post' successfully.
[AAYU] Web Server started on http://localhost:3000
[AAYU] API Server started on http://localhost:8080
--------------------------------------------------
=> Visit http://localhost:3000 to see your UI
=> API ready at GET /api/feed`
    },
    {
      name: "2. Native AI/ML",
      icon: <BrainCircuit className="w-4 h-4 mr-2" />,
      code: `app AIAssistant

import aayu-gemini
import aayu-ml

action analyze_data
    // Train a model locally
    let dataset = ml::load("data.csv")
    let model = ml::KMeans(clusters: 3)
    model.train(dataset)
    
    // Call Gemini API natively
    let prompt = "Summarize these clusters: " + model.summary()
    let response = gemini::generate(prompt)
    
    print(response)
end`,
      output: `[AAYU] Importing aayu-gemini (v1.0.0)...
[AAYU] Importing aayu-ml (v1.0.0)...
[ML] Training KMeans with 3 clusters on 10,000 rows...
[ML] Converged in 12 iterations (14ms).
[Gemini] Sending prompt via HTTP/2 stream...
[Gemini] Response: "The clusters represent 3 distinct user segments..."
=> Execution completed in 850ms.`
    }
  ];

  return (
    <div className="min-h-screen bg-[#050505] text-zinc-300 font-sans selection:bg-blue-500/30 overflow-x-hidden">
      
      {/* GLOW BACKGROUND */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-blue-600/20 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-purple-600/20 blur-[120px] rounded-full pointer-events-none" />

      {/* HERO SECTION */}
      <div className="relative max-w-7xl mx-auto px-6 pt-32 pb-20 flex flex-col items-center text-center">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium mb-8 animate-fade-in">
          <Zap className="w-4 h-4" />
          <span>AAYU v1.1.0 is now live</span>
        </div>
        
        <h1 className="text-6xl md:text-8xl font-black tracking-tighter text-white mb-6 leading-[1.1]">
          INTENT TO <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400">SILICON.</span>
        </h1>
        
        <p className="text-xl md:text-2xl text-zinc-400 max-w-3xl mb-10 font-light">
          The first <strong className="text-zinc-200">single-file full-stack</strong> programming language. 
          Database, Backend, Frontend, and AI — all in one native binary. Zero dependencies.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
          <Link href="/download" className="group relative inline-flex items-center justify-center px-8 py-4 bg-white text-black font-bold rounded-xl transition-all hover:scale-105 active:scale-95">
            <Download className="w-5 h-5 mr-2" />
            Download Executable
          </Link>
          <Link href="/playground" className="group inline-flex items-center justify-center px-8 py-4 bg-zinc-900 border border-zinc-800 text-white font-semibold rounded-xl hover:bg-zinc-800 transition-all">
            <Terminal className="w-5 h-5 mr-2 group-hover:text-blue-400 transition-colors" />
            Try in Playground
          </Link>
        </div>
      </div>

      {/* PROOF OF CONCEPT - INTERACTIVE CODE EDITOR */}
      <div className="max-w-6xl mx-auto px-6 py-12 relative z-10">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold text-white mb-4">The Proof is in the Code</h2>
          <p className="text-zinc-400">No configuration files. No package.json. No Dockerfiles.</p>
        </div>

        <div className="bg-[#0c0c0e] rounded-2xl border border-zinc-800/50 shadow-2xl overflow-hidden flex flex-col md:flex-row">
          
          {/* Editor Side */}
          <div className="w-full md:w-1/2 border-b md:border-b-0 md:border-r border-zinc-800/50 flex flex-col">
            <div className="flex bg-[#121215] border-b border-zinc-800/50 overflow-x-auto">
              {tabs.map((tab, idx) => (
                <button
                  key={idx}
                  onClick={() => setActiveTab(idx)}
                  className={`flex items-center px-6 py-3 text-sm font-medium transition-colors border-b-2 whitespace-nowrap ${
                    activeTab === idx 
                      ? 'border-blue-500 text-blue-400 bg-blue-500/5' 
                      : 'border-transparent text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800/30'
                  }`}
                >
                  {tab.icon}
                  {tab.name}
                </button>
              ))}
            </div>
            <div className="p-4 bg-[#0c0c0e] flex-1 overflow-auto">
              <pre className="font-mono text-[13px] leading-loose">
                <code className="text-zinc-300">
                  {tabs[activeTab].code.split('\n').map((line, i) => (
                    <div key={i} className="table-row">
                      <span className="table-cell text-zinc-700 pr-4 select-none">{i + 1}</span>
                      <span className="table-cell">
                        {line.replace(/\b(app|model|route|get|post|action|Page|end|let|return)\b/g, '$$$1')}
                      </span>
                    </div>
                  ))}
                </code>
              </pre>
            </div>
          </div>
          
          {/* Terminal Side */}
          <div className="w-full md:w-1/2 bg-[#050505] flex flex-col">
            <div className="flex items-center px-4 py-3 bg-[#0a0a0a] border-b border-zinc-800/50">
              <div className="flex space-x-2">
                <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
                <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
              </div>
              <span className="ml-4 text-xs font-mono text-zinc-500">aayu run main.aayu</span>
            </div>
            <div className="p-6 font-mono text-sm flex-1 overflow-auto">
              <pre className="text-zinc-400 leading-relaxed whitespace-pre-wrap">
                {tabs[activeTab].output}
              </pre>
            </div>
          </div>
        </div>
      </div>

      {/* PERFORMANCE BENCHMARKS */}
      <div className="max-w-7xl mx-auto px-6 py-20 border-t border-zinc-800/50">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-white mb-4">C-Level Performance</h2>
          <p className="text-zinc-400">AAYU compiles down to an optimized Rust-based JIT interpreter. Benchmarked on calculating Fibonacci(25).</p>
        </div>

        <div className="max-w-3xl mx-auto bg-[#0a0a0c] p-8 rounded-2xl border border-zinc-800">
          <div className="space-y-6">
            {comparisons.map((item, idx) => (
              <div key={idx} className="relative">
                <div className="flex justify-between mb-1 text-sm font-medium">
                  <span className={idx === 0 ? "text-blue-400 font-bold" : "text-zinc-400"}>{item.lang}</span>
                  <span className="text-zinc-500">{item.time}</span>
                </div>
                <div className="w-full bg-zinc-900 rounded-full h-3 overflow-hidden">
                  <div 
                    className={`h-3 rounded-full ${item.color} ${isLoaded ? 'transition-all duration-1000 ease-out' : 'w-0'}`}
                    style={{ width: isLoaded ? `${item.speed}%` : '0%' }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* OFFICIAL LIBRARIES GRID */}
      <div className="max-w-7xl mx-auto px-6 py-20 border-t border-zinc-800/50">
        <div className="flex flex-col items-center mb-16 text-center">
          <Boxes className="w-12 h-12 text-blue-500 mb-6" />
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">The AAYU Ecosystem</h2>
          <p className="text-zinc-400 max-w-2xl text-lg">
            Stop pip installing. Stop npm installing. AAYU comes with an incredible standard library built specifically for modern Agentic workflows and Full-Stack apps.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {libraries.map((lib, i) => (
            <div key={i} className="bg-zinc-900/40 border border-zinc-800 p-6 rounded-2xl hover:bg-zinc-800/50 transition-colors group cursor-default">
              <div className="mb-4 p-3 bg-zinc-900 rounded-xl inline-block border border-zinc-800 group-hover:border-zinc-600 transition-colors">
                {lib.icon}
              </div>
              <h3 className="text-lg font-bold text-white mb-2">{lib.name}</h3>
              <p className="text-zinc-400 text-sm">{lib.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* FOOTER */}
      <footer className="border-t border-zinc-900 mt-20">
        <div className="max-w-7xl mx-auto px-6 py-12 flex flex-col md:flex-row items-center justify-between">
          <div className="flex items-center space-x-2 mb-4 md:mb-0">
            <div className="w-6 h-6 rounded bg-blue-500 flex items-center justify-center">
              <span className="text-white font-bold text-xs">A</span>
            </div>
            <span className="text-white font-semibold tracking-tight">AAYU</span>
            <span className="text-zinc-600 text-sm ml-2">v1.1.0</span>
          </div>
          
          <div className="flex space-x-6 text-sm text-zinc-500">
            <Link href="/tutorial" className="hover:text-white transition-colors">Tutorial</Link>
            <Link href="/docs" className="hover:text-white transition-colors">Documentation</Link>
            <Link href="https://github.com/Minato95-ayu/INTENT-TO-SILICON" className="hover:text-white transition-colors">GitHub</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
