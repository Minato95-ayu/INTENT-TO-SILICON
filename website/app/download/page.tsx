'use client';
import { useState } from 'react';
import { Terminal, Download, Box, Cpu, ArrowRight, Monitor, Apple, HardDrive } from 'lucide-react';
import Link from 'next/link';

export default function DownloadPage() {
  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-16 selection:bg-purple-500/30">
      <div className="container mx-auto px-4 max-w-5xl">
        
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-6 tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-500">
            Download <span className="text-purple-400">AAYU</span>
          </h1>
          <p className="text-lg text-zinc-400 max-w-2xl mx-auto">
            Get the world's first Single-File Full-Stack language for AI agents. 
            Standalone executables ready to run on any platform.
          </p>
        </div>

        {/* Primary Download Buttons */}
        <div className="grid md:grid-cols-3 gap-6 mb-16">
          {/* Windows */}
          <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden hover:border-blue-500/50 transition-colors group">
            <div className="p-8 flex flex-col items-center text-center">
              <Monitor className="w-16 h-16 text-blue-400 mb-6 group-hover:scale-110 transition-transform duration-300" />
              <h3 className="text-2xl font-bold mb-2">Windows</h3>
              <p className="text-zinc-400 text-sm mb-8">Windows 10 / 11 (64-bit)</p>
              <a 
                href="/downloads/AAYU_Windows_Installer.exe" 
                download
                className="w-full py-3 px-4 bg-white/5 hover:bg-blue-500/20 text-white border border-white/10 hover:border-blue-500/50 rounded-lg font-medium transition-all flex items-center justify-center gap-2"
              >
                <Download className="w-4 h-4" /> Download .exe
              </a>
            </div>
          </div>

          {/* Linux */}
          <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden hover:border-orange-500/50 transition-colors group">
            <div className="p-8 flex flex-col items-center text-center">
              <HardDrive className="w-16 h-16 text-orange-400 mb-6 group-hover:scale-110 transition-transform duration-300" />
              <h3 className="text-2xl font-bold mb-2">Linux / TailsOS</h3>
              <p className="text-zinc-400 text-sm mb-8">Ubuntu, Debian, Fedora, Tails</p>
              <a 
                href="/downloads/aayu-linux" 
                download
                className="w-full py-3 px-4 bg-white/5 hover:bg-orange-500/20 text-white border border-white/10 hover:border-orange-500/50 rounded-lg font-medium transition-all flex items-center justify-center gap-2"
              >
                <Download className="w-4 h-4" /> Download Binary
              </a>
            </div>
          </div>

          {/* macOS */}
          <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden hover:border-zinc-300/50 transition-colors group">
            <div className="p-8 flex flex-col items-center text-center">
              <Apple className="w-16 h-16 text-zinc-300 mb-6 group-hover:scale-110 transition-transform duration-300" />
              <h3 className="text-2xl font-bold mb-2">macOS</h3>
              <p className="text-zinc-400 text-sm mb-8">Apple Silicon (M1/M2) & Intel</p>
              <a 
                href="/downloads/aayu-macos" 
                download
                className="w-full py-3 px-4 bg-white/5 hover:bg-zinc-300/20 text-white border border-white/10 hover:border-zinc-300/50 rounded-lg font-medium transition-all flex items-center justify-center gap-2"
              >
                <Download className="w-4 h-4" /> Download Binary
              </a>
            </div>
          </div>
        </div>

        {/* Mobile Platforms */}
        <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-8 mb-16 flex flex-col md:flex-row items-center justify-between">
            <div>
                <h3 className="text-2xl font-bold mb-2">Android (Termux)</h3>
                <p className="text-zinc-400 max-w-xl">
                    AAYU can be installed directly on your Android phone using Termux. Run powerful AAYU models and databases right from your pocket.
                </p>
            </div>
            <a 
                href="/downloads/aayu-termux-install.sh" 
                download
                className="mt-6 md:mt-0 shrink-0 py-3 px-6 bg-green-500/10 hover:bg-green-500/20 text-green-400 border border-green-500/30 rounded-lg font-medium transition-all flex items-center gap-2"
            >
                <Download className="w-5 h-5" /> Download APK / Binary
            </a>
        </div>

        {/* Requirements & Components */}
        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-[#0a0a0a] border border-white/5 p-8 rounded-2xl">
            <Box className="w-8 h-8 text-cyan-400 mb-4" />
            <h3 className="text-xl font-bold mb-2">No Dependencies</h3>
            <p className="text-zinc-400 text-sm leading-relaxed">
              The AAYU executable is fully standalone. You do not need to install Python, Node.js, or Rust. Simply download the binary, add it to your PATH, and you are ready to write intent-to-silicon code.
            </p>
          </div>

          <div className="bg-[#0a0a0a] border border-white/5 p-8 rounded-2xl">
            <Cpu className="w-8 h-8 text-purple-400 mb-4" />
            <h3 className="text-xl font-bold mb-2">What's Inside?</h3>
            <ul className="space-y-3 text-zinc-400 text-sm">
              <li className="flex items-center gap-2"><ArrowRight className="w-4 h-4 text-purple-500" /> <b>aayu CLI</b>: The complete developer toolkit</li>
              <li className="flex items-center gap-2"><ArrowRight className="w-4 h-4 text-purple-500" /> <b>Built-in SQLite</b>: Zero-config database engine</li>
              <li className="flex items-center gap-2"><ArrowRight className="w-4 h-4 text-purple-500" /> <b>HTTP Server</b>: Native ASGI web server included</li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  );
}
