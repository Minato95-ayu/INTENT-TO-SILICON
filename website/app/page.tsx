/* eslint-disable */
"use client";

import Link from "next/link";
import React, { useState, useEffect } from "react";
import { Copy, Check, Download, GitBranch, ExternalLink, Bot, Zap, Terminal, Globe, Lock, Cpu, Database, Braces, Sparkles, Layout } from 'lucide-react';
import { Button } from "@/components/ui/button";

function useTypingEffect(lines: string[], speed = 35, lineDelay = 400) {
  const [displayed, setDisplayed] = useState<string[]>([]);
  const [done, setDone] = useState(false);

  useEffect(() => {
    let cancelled = false;
    async function run() {
      const result: string[] = [];
      for (let i = 0; i < lines.length; i++) {
        if (cancelled) return;
        result.push("");
        for (let j = 0; j < lines[i].length; j++) {
          if (cancelled) return;
          result[i] = lines[i].slice(0, j + 1);
          setDisplayed([...result]);
          await new Promise((r) => setTimeout(r, speed));
        }
        await new Promise((r) => setTimeout(r, lineDelay));
      }
      if (!cancelled) setDone(true);
    }
    run();
    return () => { cancelled = true; };
  }, []);

  return { displayed, done };
}

function highlightLine(line: string) {
  if (!line) return <span>&nbsp;</span>;
  const keywords = /\b(app|model|route|action|end|run|get|print|let|if)\b/g;
  const types = /\b(Int|String|Bool|Float)\b/g;
  const strings = /"[^"]*"/g;
  
  let result = line;
  const spans: { start: number; end: number; className: string; text: string }[] = [];
  
  let m;
  while ((m = strings.exec(line)) !== null) {
    spans.push({ start: m.index, end: m.index + m[0].length, className: "text-emerald-400", text: m[0] });
  }
  while ((m = keywords.exec(line)) !== null) {
    if (!spans.some((s) => m!.index >= s.start && m!.index < s.end)) {
      spans.push({ start: m.index, end: m.index + m[0].length, className: "text-purple-400 font-bold", text: m[0] });
    }
  }
  while ((m = types.exec(line)) !== null) {
    if (!spans.some((s) => m!.index >= s.start && m!.index < s.end)) {
      spans.push({ start: m.index, end: m.index + m[0].length, className: "text-cyan-400", text: m[0] });
    }
  }
  
  spans.sort((a, b) => a.start - b.start);
  if (spans.length === 0) return <span className="text-zinc-300">{line}</span>;
  
  const parts: React.ReactNode[] = [];
  let lastIndex = 0;
  spans.forEach((span, i) => {
    if (span.start > lastIndex) {
      parts.push(<span key={`text-${i}`} className="text-zinc-300">{line.slice(lastIndex, span.start)}</span>);
    }
    parts.push(<span key={`span-${i}`} className={span.className}>{span.text}</span>);
    lastIndex = span.end;
  });
  if (lastIndex < line.length) {
    parts.push(<span key="text-end" className="text-zinc-300">{line.slice(lastIndex)}</span>);
  }
  return <>{parts}</>;
}

export default function HomePage() {
  const [copied, setCopied] = useState(false);
  const heroCode = [
    'app MetaClone',
    '',
    'model User',
    '    id Int',
    '    name String',
    'end',
    '',
    'route "/api/users"',
    '    get',
    '        let users = User.all()',
    '        print("Fetching users...")',
    '    end',
    'end',
    '',
    'run MetaClone'
  ];

  const { displayed, done } = useTypingEffect(heroCode, 20, 200);

  const handleCopy = () => {
    navigator.clipboard.writeText("aayu run app.aayu");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <main className="min-h-screen bg-[#000000] text-white pt-20 selection:bg-purple-500/30 overflow-hidden font-sans">
      
      {/* HERO SECTION */}
      <section className="relative container mx-auto px-4 max-w-7xl mb-32">
        <div className="absolute top-[-100px] left-1/2 -translate-x-1/2 w-[900px] h-[500px] bg-purple-900/20 rounded-full blur-[150px] pointer-events-none" />
        
        <div className="relative z-10 grid lg:grid-cols-2 gap-16 items-center pt-10">
          <div>
            <div className="inline-flex items-center gap-2 bg-purple-500/10 border border-purple-500/20 rounded-full px-4 py-1.5 mb-8">
              <Bot className="w-4 h-4 text-purple-400" />
              <span className="text-sm font-semibold text-purple-300">The #1 Language for AI Agents & Vibe Coders</span>
            </div>

            <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 leading-[1.05]">
              Built for <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-cyan-400">Silicon.</span> <br />
              Loved by <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-400">AI.</span>
            </h1>

            <p className="text-lg text-zinc-400 max-w-xl mb-10 leading-relaxed">
              AAYU is a single-file, zero-dependency language natively compiled in Rust. No <code className="text-white">npm</code>, no <code className="text-white">pip</code>, no virtualenvs. 
              Build Facebook, Meta, or Google-scale systems instantly. Runs securely anywhere—from Windows CMD to Tails OS.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 mb-8">
              <div className="flex-1 max-w-md bg-[#0a0a0a] border border-white/10 rounded-xl px-5 py-3.5 flex items-center justify-between">
                <code className="text-sm text-green-400 font-mono">aayu run app.aayu</code>
                <button onClick={handleCopy} className="text-zinc-500 hover:text-white transition-colors ml-3">
                  {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
                </button>
              </div>
              <Link href="/tutorial">
                <Button className="h-full px-6 bg-purple-600 text-white hover:bg-purple-500 font-bold rounded-xl gap-2">
                  <Terminal className="w-4 h-4" /> Start Tutorial
                </Button>
              </Link>
            </div>
            
            <div className="flex gap-4 text-sm font-semibold text-zinc-500">
              <span className="flex items-center gap-1"><Check className="w-4 h-4 text-green-500"/> Zero Config</span>
              <span className="flex items-center gap-1"><Check className="w-4 h-4 text-green-500"/> Native REPL</span>
              <span className="flex items-center gap-1"><Check className="w-4 h-4 text-green-500"/> Cross-Platform (Rust VM)</span>
            </div>
          </div>

          {/* CODE SHOWCASE */}
          <div className="relative">
            <div className="absolute -inset-1 bg-gradient-to-r from-purple-500/20 to-cyan-500/20 rounded-2xl blur-xl pointer-events-none" />
            <div className="relative bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden shadow-2xl">
              <div className="flex items-center px-4 py-3 bg-[#111] border-b border-white/5">
                <div className="flex gap-1.5 mr-4">
                  <div className="w-3 h-3 rounded-full bg-red-500/80" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                  <div className="w-3 h-3 rounded-full bg-green-500/80" />
                </div>
                <span className="text-xs font-mono text-zinc-500">main.aayu</span>
              </div>
              <div className="p-5 font-mono text-[13px] leading-[1.8] min-h-[380px]">
                {displayed.map((line, i) => (
                  <div key={i} className="flex">
                    <span className="w-8 text-right text-zinc-700 text-xs select-none mr-4 mt-[3px] shrink-0">{i + 1}</span>
                    <div>{highlightLine(line)}</div>
                  </div>
                ))}
                {!done && <span className="inline-block w-2 h-5 bg-purple-400 ml-12 animate-pulse rounded-sm" />}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* VALUE PROPOSITION: AI & VIBE CODERS */}
      <section className="bg-[#050505] border-y border-white/5 py-24">
        <div className="container mx-auto px-4 max-w-7xl">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold mb-4">Designed for the <span className="text-purple-400">Future of Code.</span></h2>
            <p className="text-zinc-400 max-w-2xl mx-auto">AAYU is ready for AI agents to build and you can build anything from scratch. AAYU solves the fundamental problems faced by modern AI coding agents and human "Vibe Coders". No more hallucinated packages or broken environments.</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* AI Agent Pitch */}
            <div className="bg-[#0a0a0a] border border-white/5 p-8 rounded-2xl hover:border-purple-500/30 transition-all">
              <Bot className="w-10 h-10 text-purple-400 mb-6" />
              <h3 className="text-xl font-bold mb-3">Zero AI Hallucinations</h3>
              <p className="text-zinc-400 text-sm leading-relaxed">
                AI agents (Cursor, Gemini, Claude) struggle with missing packages and hallucinated `pip installs`. AAYU has Database, Auth, UI, and Server built directly into its Rust VM. AI can't hallucinate what is already native.
              </p>
            </div>

            {/* Vibe Coder Pitch */}
            <div className="bg-[#0a0a0a] border border-white/5 p-8 rounded-2xl hover:border-cyan-500/30 transition-all">
              <Sparkles className="w-10 h-10 text-cyan-400 mb-6" />
              <h3 className="text-xl font-bold mb-3">The Vibe Coder Dream</h3>
              <p className="text-zinc-400 text-sm leading-relaxed">
                Write code like English or Math. No `virtualenv`, no Webpack, no Dockerfiles needed for local dev. Build a full-stack App in a single `.aayu` file. It's so simple, anyone can build a tech empire.
              </p>
            </div>

            {/* Privacy OS Pitch */}
            <div className="bg-[#0a0a0a] border border-white/5 p-8 rounded-2xl hover:border-emerald-500/30 transition-all">
              <Lock className="w-10 h-10 text-emerald-400 mb-6" />
              <h3 className="text-xl font-bold mb-3">Tails OS & Privacy Ready</h3>
              <p className="text-zinc-400 text-sm leading-relaxed">
                Compiled to a static standalone binary via Rust. Put `aayu.exe` on a USB stick, boot into Tails OS, run it from CMD/PowerShell, and leave zero trace. Ultimate portability and security for hackers and creators.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* PROOF SECTION */}
      <section className="py-24 container mx-auto px-4 max-w-7xl">
         <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6">Built to save <span className="text-purple-400">Context Tokens.</span></h2>
              <p className="text-zinc-400 mb-6 leading-relaxed">
                Giving an AI a 5,000-line React/Node/SQL project burns through its context window and reduces logic quality. 
              </p>
              <ul className="space-y-4 text-zinc-300">
                <li className="flex items-start gap-3">
                  <div className="mt-1 bg-green-500/20 p-1 rounded"><Check className="w-4 h-4 text-green-400" /></div>
                  <div>
                    <strong className="text-white block">.aayu-context.md Auto-Generation</strong>
                    AAYU's compiler automatically maps your entire project architecture into a tiny 300-token summary file specifically formatted for LLMs.
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="mt-1 bg-green-500/20 p-1 rounded"><Check className="w-4 h-4 text-green-400" /></div>
                  <div>
                    <strong className="text-white block">Strict End Bounds</strong>
                    No Python indentation errors. AAYU uses explicit `end` blocks, preventing the #1 cause of AI code generation failures.
                  </div>
                </li>
              </ul>
            </div>
            <div className="bg-gradient-to-b from-zinc-900 to-[#0a0a0a] border border-white/10 p-8 rounded-2xl">
                <h4 className="font-mono text-xs text-zinc-500 mb-4">TOKEN CONSUMPTION (Full Stack App)</h4>
                
                <div className="mb-6">
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-red-400">Node.js + React (Standard)</span>
                    <span className="text-zinc-400">~8,500 Tokens</span>
                  </div>
                  <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
                    <div className="h-full bg-red-500 w-[85%]" />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-green-400">AAYU (.aayu-context map)</span>
                    <span className="text-zinc-400">~300 Tokens</span>
                  </div>
                  <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
                    <div className="h-full bg-green-500 w-[5%]" />
                  </div>
                </div>
            </div>
         </div>
      </section>

    </main>
  );
}

