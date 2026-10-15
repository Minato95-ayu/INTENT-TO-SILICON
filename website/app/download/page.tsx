"use client";
import { useState } from 'react';
import { Terminal, Copy, Download, Cpu, Check, Smartphone, BookOpen } from 'lucide-react';

export default function DownloadPage() {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText("curl -fsSL https://intent-to-silicon.vercel.app/install.sh | bash");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  

  const sdkDownloads = [
    { os: 'Windows (SDK)', icon: <Cpu className="w-8 h-8 text-blue-400" />, desc: 'CLI & Compiler (.zip)', file: 'aayu-windows.zip', color: 'hover:border-blue-500/50' },
    { os: 'Android Mobile (APK)', icon: <Smartphone className="w-8 h-8 text-emerald-400" />, desc: 'Native Mobile IDE v1.3 · 12.5 MB (Real-time Syntax Highlighting)', file: 'aayu-android.apk', localUrl: '/downloads/aayu-android.apk', color: 'hover:border-emerald-500/50' },
    { os: 'VS Code Extension (.vsix)', icon: <Terminal className="w-8 h-8 text-cyan-400" />, desc: 'AAYU Pro Suite v1.3 · 1.3 MB (.vsix)', file: 'aayu-vscode.vsix', localUrl: '/downloads/aayu-vscode.vsix', color: 'hover:border-cyan-500/50' },
    { os: 'Master Handbook (PDF)', icon: <BookOpen className="w-8 h-8 text-purple-400" />, desc: 'Official Master PDF (3.0 MB)', file: 'The_Ultimate_AAYU_Handbook_Ayush_Ghrit_Kaushik.pdf', localUrl: '/aayu-handbook.pdf', color: 'hover:border-purple-500/50' },
    { os: 'Linux (SDK)', icon: <Cpu className="w-8 h-8 text-orange-400" />, desc: 'CLI & Compiler (.tar.gz)', file: 'aayu-linux.tar.gz', color: 'hover:border-orange-500/50' },
    { os: 'macOS (SDK)', icon: <Cpu className="w-8 h-8 text-zinc-300" />, desc: 'CLI & Compiler (.zip)', file: 'aayu-macos.zip', color: 'hover:border-zinc-500/50' }
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
            Download the native AAYU Silicon Engine, Android Mobile IDE APK, or the Official 21-Chapter Engineering Handbook.
          </p>
        </div>

        {/* SDK Section */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
            <Terminal className="w-6 h-6 text-cyan-400" /> AAYU Native Binaries, Mobile APK &amp; Handbook
          </h2>
          <p className="text-zinc-400 mb-6">Cross-platform releases built with zero external dependencies. Choose your platform below:</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {sdkDownloads.map((d, i) => (
              <div key={i} className={"bg-[#0a0a0a] border border-white/5 rounded-xl p-6 transition-all duration-300 group " + d.color}>
                <div className="flex justify-between items-start mb-4">
                  {d.icon}
                  <a href={d.localUrl || ("https://github.com/Minato95-ayu/INTENT-TO-SILICON/releases/latest/download/" + d.file)} download className="p-2 bg-white/5 hover:bg-white/10 rounded-full text-zinc-400 hover:text-white transition-colors">
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
          <h2 className="text-2xl font-bold mb-6 text-center">Quick Install (macOS / Linux)</h2>
          <div className="bg-[#0a0a0a] border border-white/10 rounded-xl p-6 max-w-2xl mx-auto">
            <div className="flex justify-between items-center mb-4">
              <span className="text-sm text-zinc-400">Terminal</span>
              <button onClick={handleCopy} className="text-zinc-400 hover:text-white flex items-center gap-2 text-sm transition-colors">
                {copied ? <><Check className="w-4 h-4 text-green-400" /> Copied!</> : <><Copy className="w-4 h-4" /> Copy</>}
              </button>
            </div>
            <pre className="text-zinc-300 font-mono text-sm overflow-x-auto whitespace-pre-wrap">
              <code className="text-purple-300">curl</code> -fsSL https://intent-to-silicon.vercel.app/install.sh | bash
              
              
            </pre>
          </div>
        </div>

            {/* Windows Install */}
        <div className="mt-8 pt-8">
          <h2 className="text-2xl font-bold mb-6 text-center">Quick Install (Windows)</h2>
          <div className="bg-[#0a0a0a] border border-white/10 rounded-xl p-6 max-w-2xl mx-auto">
            <div className="flex justify-between items-center mb-4">
              <span className="text-sm text-zinc-400">PowerShell</span>
            </div>
            <pre className="text-zinc-300 font-mono text-sm overflow-x-auto whitespace-pre-wrap">
              <code className="text-purple-300">iwr</code> -useb https://intent-to-silicon.vercel.app/install.ps1 -OutFile $env:TEMP\aayu-install.ps1; &amp; $env:TEMP\aayu-install.ps1
            </pre>
          </div>
        </div>
      </div>
    </main>
  );
}
