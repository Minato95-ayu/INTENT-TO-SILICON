"use client";
import { useState } from 'react';
import { Terminal, Copy, Download, Monitor, Apple, Code2, Cpu } from 'lucide-react';

export default function DownloadPage() {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText("git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git\ncd INTENT-TO-SILICON\npip install -e .");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = (e: any) => {
    e.preventDefault();
    alert("v1.1.0 binaries are currently building in our CI pipeline! Please use the 'Build From Source' option below for now, or check back later.");
  };

  const ideDownloads = [
    { os: 'Windows', icon: <Monitor className="w-8 h-8 text-blue-400" />, desc: 'AAYU Studio Installer (.exe)', file: 'aayu-studio-windows-x64.exe', color: 'hover:border-blue-500/50' },
    { os: 'macOS', icon: <Apple className="w-8 h-8 text-zinc-300" />, desc: 'Apple Silicon & Intel (.dmg)', file: 'aayu-studio-mac-universal.dmg', color: 'hover:border-zinc-500/50' },
    { os: 'Linux', icon: <Terminal className="w-8 h-8 text-orange-400" />, desc: 'AppImage for Linux (.AppImage)', file: 'aayu-studio-linux.AppImage', color: 'hover:border-orange-500/50' }
  ];

  const sdkDownloads = [
    { os: 'Windows (SDK)', icon: <Cpu className="w-8 h-8 text-blue-400" />, desc: 'CLI & Compiler (.zip)', file: 'aayuc-windows-v1.1.0.zip', color: 'hover:border-blue-500/50' },
    { os: 'macOS (SDK)', icon: <Cpu className="w-8 h-8 text-zinc-300" />, desc: 'CLI & Compiler (.tar.gz)', file: 'aayuc-macos-v1.1.0.tar.gz', color: 'hover:border-zinc-500/50' },
    { os: 'Linux (SDK)', icon: <Cpu className="w-8 h-8 text-orange-400" />, desc: 'CLI & Compiler (.tar.gz)', file: 'aayuc-linux-v1.1.0.tar.gz', color: 'hover:border-orange-500/50' }
  ];

  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-24 selection:bg-purple-500/30">
      <div className="container mx-auto px-4 max-w-5xl">
        
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-6 tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-500">
            Download <span className="text-purple-400">AAYU</span>
          </h1>
          <p className="text-lg text-zinc-400 max-w-2xl mx-auto">
            Get the world's first Single-File Full-Stack language. Download AAYU Studio (IDE) for a visual experience, or the AAYU SDK for terminal usage.
          </p>
        </div>

        {/* IDE Section */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
            <Code2 className="w-6 h-6 text-purple-400" /> AAYU Studio (Official IDE)
          </h2>
          <p className="text-zinc-400 mb-6">The ultimate AI-powered code editor for AAYU. Includes built-in AI agents, syntax highlighting, and visual execution.</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {ideDownloads.map((d, i) => (
              <div key={i} className={"bg-[#0a0a0a] border border-white/5 rounded-xl p-6 transition-all duration-300 group " + d.color}>
                <div className="flex justify-between items-start mb-4">
                  {d.icon}
                  <a href="https://github.com/Minato95-ayu/INTENT-TO-SILICON/releases/download/v1.1.0/" onClick={handleDownload} className="p-2 bg-white/5 hover:bg-white/10 rounded-full text-zinc-400 hover:text-white transition-colors">
                    <Download className="w-4 h-4" />
                  </a>
                </div>
                <h3 className="text-lg font-bold mb-1">{d.os}</h3>
                <p className="text-sm text-zinc-500">{d.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* SDK Section */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
            <Terminal className="w-6 h-6 text-cyan-400" /> AAYU SDK (Compiler & CLI)
          </h2>
          <p className="text-zinc-400 mb-6">The standalone intent-to-silicon compiler, VM, and standard library. Best for CI/CD pipelines and terminal power users.</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {sdkDownloads.map((d, i) => (
              <div key={i} className={"bg-[#0a0a0a] border border-white/5 rounded-xl p-6 transition-all duration-300 group " + d.color}>
                <div className="flex justify-between items-start mb-4">
                  {d.icon}
                  <a href="https://github.com/Minato95-ayu/INTENT-TO-SILICON/releases/download/v1.1.0/" onClick={handleDownload} className="p-2 bg-white/5 hover:bg-white/10 rounded-full text-zinc-400 hover:text-white transition-colors">
                    <Download className="w-4 h-4" />
                  </a>
                </div>
                <h3 className="text-lg font-bold mb-1">{d.os}</h3>
                <p className="text-sm text-zinc-500">{d.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Source Code */}
        <div className="mt-16 border-t border-white/10 pt-16">
          <h2 className="text-2xl font-bold mb-6 text-center">Build From Source</h2>
          <div className="bg-[#0a0a0a] border border-white/10 rounded-xl p-6 max-w-2xl mx-auto">
            <div className="flex justify-between items-center mb-4">
              <span className="text-sm text-zinc-400">Terminal</span>
              <button onClick={handleCopy} className="text-zinc-400 hover:text-white flex items-center gap-2 text-sm transition-colors">
                {copied ? <><Check className="w-4 h-4 text-green-400" /> Copied!</> : <><Copy className="w-4 h-4" /> Copy</>}
              </button>
            </div>
            <pre className="text-zinc-300 font-mono text-sm overflow-x-auto whitespace-pre-wrap">
              <code className="text-purple-300">git clone</code> https://github.com/Minato95-ayu/INTENT-TO-SILICON.git{'
'}
              <code className="text-purple-300">cd</code> INTENT-TO-SILICON{'
'}
              <code className="text-purple-300">pip install</code> -e .
            </pre>
          </div>
        </div>

      </div>
    </main>
  );
}

