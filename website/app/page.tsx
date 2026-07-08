/* eslint-disable */

"use client";

import Link from "next/link";
import {
  ArrowRight,
  Code2,
  Terminal,
  Database,
  FileJson,
  Play,
  Search,
  Download,
  ChevronRight,
  Zap,
  ShieldCheck,
  Layers,
  Server,
  Globe,
  Package,
  Cpu,
  HardDrive,
  Monitor,
  GitBranch,
  Box,
  Workflow,
  Braces,
  CircuitBoard,
  Sparkles,
  Check,
  Copy,
  ExternalLink,
} from "lucide-react";
import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";

/* ─────────────────────────────────────────────
   Animated typing hook
   ───────────────────────────────────────────── */
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

/* ─────────────────────────────────────────────
   Pipeline stage component
   ───────────────────────────────────────────── */
function PipelineStage({ label, icon: Icon, color, delay }: { label: string; icon: any; color: string; delay: number }) {
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setVisible(true), delay);
    return () => clearTimeout(t);
  }, [delay]);
  return (
    <div className={`flex flex-col items-center transition-all duration-700 ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"}`}>
      <div className={`w-11 h-11 rounded-xl border ${color} flex items-center justify-center mb-2 backdrop-blur-sm`}>
        <Icon className="w-5 h-5" />
      </div>
      <span className="text-[11px] font-semibold text-zinc-400 text-center leading-tight">{label}</span>
    </div>
  );
}

/* ─────────────────────────────────────────────
   Connector arrow between pipeline stages
   ───────────────────────────────────────────── */
function PipelineArrow({ delay }: { delay: number }) {
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setVisible(true), delay);
    return () => clearTimeout(t);
  }, [delay]);
  return (
    <div className={`transition-all duration-500 ${visible ? "opacity-100" : "opacity-0"}`}>
      <ChevronRight className="w-4 h-4 text-zinc-600" />
    </div>
  );
}

/* ═════════════════════════════════════════════
   MAIN PAGE COMPONENT
   ═════════════════════════════════════════════ */
export default function HomePage() {
  const [copied, setCopied] = useState(false);

  const heroCode = [
    'app CRM.',
    '',
    'storage Main.',
    '',
    'model User {',
    '    id Int.',
    '    name String.',
    '    email String.',
    '}',
    '',
    'task main {',
    '    show "Hello from AAYU".',
    '',
    '    insert User {',
    '        name = "Ayush".',
    '        email = "ayush@aayu.dev".',
    '    }.',
    '',
    '    let users = find User.',
    '    show users.',
    '}.',
  ];

  const { displayed, done } = useTypingEffect(heroCode, 22, 200);

  const handleCopy = () => {
    navigator.clipboard.writeText(heroCode.join("\n"));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  /* ──── Pipeline stages data ──── */
  const pipelineStages = [
    { label: "Source", icon: Code2, color: "border-blue-500/50 bg-blue-500/10 text-blue-400" },
    { label: "Lexer", icon: Braces, color: "border-cyan-500/50 bg-cyan-500/10 text-cyan-400" },
    { label: "Parser", icon: GitBranch, color: "border-indigo-500/50 bg-indigo-500/10 text-indigo-400" },
    { label: "AST", icon: Workflow, color: "border-violet-500/50 bg-violet-500/10 text-violet-400" },
    { label: "Bytecode", icon: CircuitBoard, color: "border-purple-500/50 bg-purple-500/10 text-purple-400" },
    { label: "VM", icon: Cpu, color: "border-fuchsia-500/50 bg-fuchsia-500/10 text-fuchsia-400" },
    { label: "Runtime", icon: Zap, color: "border-amber-500/50 bg-amber-500/10 text-amber-400" },
  ];

  const runtimeTargets = [
    { label: "HTTP", icon: Globe, color: "border-green-500/50 bg-green-500/10 text-green-400" },
    { label: "Storage", icon: Database, color: "border-orange-500/50 bg-orange-500/10 text-orange-400" },
    { label: "UI", icon: Monitor, color: "border-pink-500/50 bg-pink-500/10 text-pink-400" },
  ];

  /* ──── Syntax highlighting helper ──── */
  function highlightLine(line: string) {
    if (!line) return <span>&nbsp;</span>;

    const keywords = /\b(app|storage|model|task|let|show|insert|find|update|delete|if|else|each|while|return)\b/g;
    const types = /\b(Int|String|Bool|Float|List|Map)\b/g;
    const strings = /"[^"]*"/g;
    const comments = /\/\/.*$/g;

    let result = line;
    const spans: { start: number; end: number; className: string; text: string }[] = [];

    let m;
    while ((m = strings.exec(line)) !== null) {
      spans.push({ start: m.index, end: m.index + m[0].length, className: "text-emerald-400", text: m[0] });
    }
    while ((m = keywords.exec(line)) !== null) {
      if (!spans.some((s) => m!.index >= s.start && m!.index < s.end)) {
        spans.push({ start: m.index, end: m.index + m[0].length, className: "text-purple-400 font-semibold", text: m[0] });
      }
    }
    while ((m = types.exec(line)) !== null) {
      if (!spans.some((s) => m!.index >= s.start && m!.index < s.end)) {
        spans.push({ start: m.index, end: m.index + m[0].length, className: "text-cyan-400", text: m[0] });
      }
    }

    spans.sort((a, b) => a.start - b.start);
    if (spans.length === 0) return <span className="text-zinc-300">{line}</span>;

    const parts: JSX.Element[] = [];
    let lastEnd = 0;
    spans.forEach((s, i) => {
      if (s.start > lastEnd) {
        parts.push(<span key={`t${i}`} className="text-zinc-300">{line.slice(lastEnd, s.start)}</span>);
      }
      parts.push(<span key={`s${i}`} className={s.className}>{s.text}</span>);
      lastEnd = s.end;
    });
    if (lastEnd < line.length) {
      parts.push(<span key="end" className="text-zinc-300">{line.slice(lastEnd)}</span>);
    }
    return <>{parts}</>;
  }

  /* ──── Core products data ──── */
  const coreProducts = [
    {
      title: "AAYU Language",
      description: "Full compiler pipeline with type system, semantic analysis, and bytecode generation. Stack-based VM with mark-and-sweep garbage collection.",
      icon: Code2,
      color: "from-purple-500 to-violet-600",
      borderColor: "border-purple-500/30",
      glowColor: "bg-purple-500/20",
      features: ["Lexer → Parser → AST → Bytecode", "Stack-based Virtual Machine", "Mark-and-Sweep GC", "Static Type System", "Standard Library"],
    },
    {
      title: "AAYU Runtime",
      description: "Native HTTP server, Storage Operating System, and UI engine — all built from scratch with zero external dependencies.",
      icon: Server,
      color: "from-blue-500 to-cyan-500",
      borderColor: "border-blue-500/30",
      glowColor: "bg-blue-500/20",
      badge: "CORE",
      features: ["Native HTTP Server & Router", "Storage OS with Query Planner", "Schema & Migration Engine", "UI Render Tree & Layout", "State Management"],
    },
    {
      title: "AAYU CLI",
      description: "Build, run, test, and manage AAYU applications from the terminal. Integrated development workflow with hot reload.",
      icon: Terminal,
      color: "from-emerald-500 to-green-500",
      borderColor: "border-emerald-500/30",
      glowColor: "bg-emerald-500/20",
      features: ["aayu run app.aayu", "aayu build app.aayu", "aayu test", "aayu init", "Hot Reload"],
    },
    {
      title: "AAYU Packages",
      description: "First-class package manager for sharing and reusing AAYU modules. Dependency resolution, versioning, and registry.",
      icon: Package,
      color: "from-orange-500 to-amber-500",
      borderColor: "border-orange-500/30",
      glowColor: "bg-orange-500/20",
      features: ["apm install <pkg>", "apm publish", "Dependency Resolution", "Semantic Versioning", "Central Registry"],
    },
  ];

  /* ──── Stdlib data ──── */
  const stdlibModules = [
    { name: "math", desc: "Arithmetic, trigonometry, random" },
    { name: "json", desc: "Parse and serialize JSON" },
    { name: "fs", desc: "File system operations" },
    { name: "crypto", desc: "Hashing, encryption, tokens" },
    { name: "http", desc: "HTTP client utilities" },
    { name: "database", desc: "Query builder, transactions" },
    { name: "process", desc: "System processes, signals" },
    { name: "env", desc: "Environment variables" },
  ];

  /* ──── Production examples ──── */
  const productionExamples = [
    { name: "CRM System", desc: "Contacts, deals, pipeline management", lines: 280, icon: "📊" },
    { name: "Hospital ERP", desc: "Patient records, scheduling, billing", lines: 420, icon: "🏥" },
    { name: "E-Commerce Platform", desc: "Products, cart, checkout, payments", lines: 350, icon: "🛒" },
    { name: "Portfolio App", desc: "Projects, blog, contact form", lines: 120, icon: "💼" },
  ];

  /* ═══════════════════════════════ RENDER ═══════════════════════════════ */
  return (
    <main className="min-h-screen bg-[#000000] text-white pt-20 selection:bg-purple-500/30 overflow-hidden">

      {/* ================================================================
          HERO SECTION
          ================================================================ */}
      <section className="relative container mx-auto px-4 max-w-7xl mb-32">
        {/* Background glows */}
        <div className="absolute top-[-100px] left-1/2 -translate-x-1/2 w-[900px] h-[500px] bg-purple-900/15 rounded-full blur-[150px] pointer-events-none" />
        <div className="absolute top-[100px] right-[-200px] w-[400px] h-[400px] bg-blue-900/10 rounded-full blur-[120px] pointer-events-none" />

        {/* Hero content */}
        <div className="relative z-10 grid lg:grid-cols-2 gap-16 items-center">
          {/* Left — tagline */}
          <div>
            <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 rounded-full px-4 py-1.5 mb-8">
              <Sparkles className="w-3.5 h-3.5 text-purple-400" />
              <span className="text-xs font-semibold text-zinc-400">v2.0.0 — Application Language + Runtime Platform</span>
            </div>

            <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 leading-[1.05]">
              The Application{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400">
                Language.
              </span>
            </h1>

            <p className="text-lg md:text-xl text-zinc-400 max-w-xl mb-10 leading-relaxed">
              Write apps, not configurations. AAYU compiles your intent into native HTTP servers, databases, and UIs — with zero dependencies.
            </p>

            {/* Install command */}
            <div className="flex flex-col sm:flex-row gap-4 mb-8">
              <div className="flex-1 max-w-md bg-[#0a0a0a] border border-white/10 rounded-xl px-5 py-3.5 flex items-center justify-between group hover:border-purple-500/40 transition-colors">
                <code className="text-sm text-green-400 font-mono">pip install aayu-lang</code>
                <button onClick={handleCopy} className="text-zinc-500 hover:text-white transition-colors ml-3">
                  {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
                </button>
              </div>
              <Link href="https://github.com/Minato95-ayu/INTENT-TO-SILICON" target="_blank">
                <Button className="h-full px-6 bg-white text-black hover:bg-zinc-200 font-bold rounded-xl gap-2">
                  <GitBranch className="w-4 h-4" /> GitHub
                  <ExternalLink className="w-3 h-3 ml-1 opacity-50" />
                </Button>
              </Link>
            </div>

            {/* Quick links */}
            <div className="flex flex-wrap gap-3">
              <Link href="/docs" className="text-xs bg-white/5 hover:bg-white/10 border border-white/5 px-3 py-1.5 rounded-lg text-zinc-400 hover:text-white transition-colors">
                Documentation
              </Link>
              <Link href="/playground" className="text-xs bg-white/5 hover:bg-white/10 border border-white/5 px-3 py-1.5 rounded-lg text-zinc-400 hover:text-white transition-colors">
                Playground
              </Link>
              <Link href="/examples" className="text-xs bg-white/5 hover:bg-white/10 border border-white/5 px-3 py-1.5 rounded-lg text-zinc-400 hover:text-white transition-colors">
                Examples
              </Link>
            </div>
          </div>

          {/* Right — Code showcase */}
          <div className="relative">
            <div className="absolute -inset-1 bg-gradient-to-r from-purple-500/20 via-blue-500/20 to-cyan-500/20 rounded-2xl blur-xl pointer-events-none" />
            <div className="relative bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden shadow-2xl">
              {/* Title bar */}
              <div className="flex items-center justify-between px-4 py-3 bg-[#111] border-b border-white/5">
                <div className="flex items-center gap-3">
                  <div className="flex gap-1.5">
                    <div className="w-3 h-3 rounded-full bg-red-500/80" />
                    <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                    <div className="w-3 h-3 rounded-full bg-green-500/80" />
                  </div>
                  <span className="text-xs font-mono text-zinc-500">crm.aayu</span>
                </div>
                <button onClick={handleCopy} className="text-zinc-500 hover:text-white transition-colors">
                  {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
                </button>
              </div>

              {/* Code area */}
              <div className="p-5 font-mono text-[13px] leading-[1.8] min-h-[420px] relative">
                {displayed.map((line, i) => (
                  <div key={i} className="flex">
                    <span className="w-8 text-right text-zinc-700 text-xs select-none mr-4 mt-[3px] shrink-0">{i + 1}</span>
                    <div>{highlightLine(line)}</div>
                  </div>
                ))}
                {!done && (
                  <span className="inline-block w-2 h-5 bg-purple-400 ml-12 animate-pulse rounded-sm" />
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ================================================================
          COMPILER PIPELINE VISUALIZATION
          ================================================================ */}
      <section className="container mx-auto px-4 max-w-6xl mb-32 relative">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-900/5 via-blue-900/5 to-transparent rounded-3xl blur-3xl pointer-events-none" />

        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            The Full Pipeline.{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400">From Source to Runtime.</span>
          </h2>
          <p className="text-zinc-500 max-w-2xl mx-auto">
            AAYU compiles your code through a complete pipeline — Lexer, Parser, AST, Semantic Analysis, Bytecode Generation — then executes on a stack-based VM with garbage collection.
          </p>
        </div>

        <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-8 md:p-12 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-purple-500/50 to-transparent" />

          {/* Main pipeline */}
          <div className="flex flex-wrap items-center justify-center gap-3 md:gap-4 mb-10">
            {pipelineStages.map((stage, i) => (
              <div key={i} className="flex items-center gap-3 md:gap-4">
                <PipelineStage label={stage.label} icon={stage.icon} color={stage.color} delay={i * 200} />
                {i < pipelineStages.length - 1 && <PipelineArrow delay={i * 200 + 100} />}
              </div>
            ))}
          </div>

          {/* Fan-out to runtimes */}
          <div className="flex items-center justify-center gap-2 mb-6">
            <div className="w-px h-8 bg-gradient-to-b from-amber-500/50 to-transparent" />
          </div>

          <div className="flex items-center justify-center gap-6 md:gap-10">
            {runtimeTargets.map((rt, i) => (
              <PipelineStage key={i} label={rt.label} icon={rt.icon} color={rt.color} delay={1600 + i * 200} />
            ))}
          </div>

          <p className="text-center text-xs text-zinc-600 mt-8 font-mono">
            Runtime Manager orchestrates HTTP, Storage, and UI subsystems natively
          </p>
        </div>
      </section>

      {/* ================================================================
          AAYU CODE EXAMPLES — Side-by-side
          ================================================================ */}
      <section className="container mx-auto px-4 max-w-7xl mb-32">
        <div className="text-center mb-14">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Write Less. Build Everything.</h2>
          <p className="text-zinc-500 max-w-2xl mx-auto">
            AAYU replaces Express, Prisma, React, and configuration files with a single, expressive language.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* HTTP Example */}
          <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden">
            <div className="px-4 py-3 bg-[#111] border-b border-white/5 flex items-center gap-2">
              <Globe className="w-4 h-4 text-green-400" />
              <span className="text-xs font-mono text-zinc-500">server.aayu</span>
              <span className="ml-auto text-[10px] font-bold text-green-400 bg-green-500/10 border border-green-500/20 px-2 py-0.5 rounded">HTTP Runtime</span>
            </div>
            <div className="p-5 font-mono text-[13px] leading-[1.9] text-zinc-300">
              <div><span className="text-purple-400 font-semibold">app</span> WebAPI.</div>
              <div>&nbsp;</div>
              <div><span className="text-purple-400 font-semibold">route</span> <span className="text-emerald-400">&quot;/api/users&quot;</span> {`{`}</div>
              <div className="pl-4"><span className="text-purple-400 font-semibold">get</span> {`{`}</div>
              <div className="pl-8"><span className="text-purple-400 font-semibold">let</span> users = <span className="text-purple-400 font-semibold">find</span> User.</div>
              <div className="pl-8"><span className="text-purple-400 font-semibold">respond</span> users.</div>
              <div className="pl-4">{`}`}.</div>
              <div className="pl-4"><span className="text-purple-400 font-semibold">post</span> {`{`}</div>
              <div className="pl-8"><span className="text-purple-400 font-semibold">insert</span> User <span className="text-purple-400 font-semibold">from</span> body.</div>
              <div className="pl-8"><span className="text-purple-400 font-semibold">respond</span> <span className="text-emerald-400">&quot;Created&quot;</span>.</div>
              <div className="pl-4">{`}`}.</div>
              <div>{`}`}.</div>
            </div>
          </div>

          {/* Storage Example */}
          <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden">
            <div className="px-4 py-3 bg-[#111] border-b border-white/5 flex items-center gap-2">
              <Database className="w-4 h-4 text-orange-400" />
              <span className="text-xs font-mono text-zinc-500">storage.aayu</span>
              <span className="ml-auto text-[10px] font-bold text-orange-400 bg-orange-500/10 border border-orange-500/20 px-2 py-0.5 rounded">Storage Runtime</span>
            </div>
            <div className="p-5 font-mono text-[13px] leading-[1.9] text-zinc-300">
              <div><span className="text-purple-400 font-semibold">storage</span> Main.</div>
              <div>&nbsp;</div>
              <div><span className="text-purple-400 font-semibold">model</span> <span className="text-cyan-400">Product</span> {`{`}</div>
              <div className="pl-4">id <span className="text-cyan-400">Int</span>.</div>
              <div className="pl-4">name <span className="text-cyan-400">String</span>.</div>
              <div className="pl-4">price <span className="text-cyan-400">Float</span>.</div>
              <div className="pl-4">active <span className="text-cyan-400">Bool</span>.</div>
              <div>{`}`}</div>
              <div>&nbsp;</div>
              <div><span className="text-purple-400 font-semibold">task</span> seed {`{`}</div>
              <div className="pl-4"><span className="text-purple-400 font-semibold">insert</span> Product {`{`}</div>
              <div className="pl-8">name = <span className="text-emerald-400">&quot;AAYU Pro&quot;</span>.</div>
              <div className="pl-8">price = 49.99.</div>
              <div className="pl-8">active = true.</div>
              <div className="pl-4">{`}`}.</div>
              <div>{`}`}.</div>
            </div>
          </div>
        </div>
      </section>

      {/* ================================================================
          4 CORE PRODUCTS
          ================================================================ */}
      <section className="container mx-auto px-4 max-w-7xl mb-32">
        <div className="text-center mb-14">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">The AAYU Ecosystem</h2>
          <p className="text-zinc-500 max-w-2xl mx-auto">
            Four integrated products. One unified platform. Zero external dependencies.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {coreProducts.map((product, i) => (
            <div key={i} className={`bg-[#0a0a0a] border ${product.borderColor} p-8 rounded-2xl relative group hover:border-opacity-60 transition-all duration-300`}>
              {/* Glow */}
              <div className={`absolute top-0 right-0 w-40 h-40 ${product.glowColor} blur-3xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none`} />

              {product.badge && (
                <div className="absolute top-0 right-0 px-3 py-1 bg-gradient-to-r from-blue-500 to-cyan-500 text-white text-[10px] font-bold rounded-bl-xl rounded-tr-2xl tracking-wider">
                  {product.badge}
                </div>
              )}

              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${product.color} flex items-center justify-center mb-6 shadow-lg`}>
                <product.icon className="w-6 h-6 text-white" />
              </div>

              <h3 className="text-xl font-bold mb-3">{product.title}</h3>
              <p className="text-sm text-zinc-500 mb-6 leading-relaxed">{product.description}</p>

              <ul className="space-y-2.5">
                {product.features.map((feat, j) => (
                  <li key={j} className="flex items-center gap-2.5 text-sm text-zinc-400">
                    <CheckCircle className="w-4 h-4 text-green-500 shrink-0" />
                    <span className={feat.startsWith("aayu ") || feat.startsWith("apm ") ? "font-mono text-xs" : ""}>{feat}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* ================================================================
          STANDARD LIBRARY
          ================================================================ */}
      <section className="container mx-auto px-4 max-w-5xl mb-32">
        <div className="text-center mb-14">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Batteries Included.</h2>
          <p className="text-zinc-500 max-w-xl mx-auto">
            A comprehensive standard library so you never need to bolt on third-party utilities.
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {stdlibModules.map((mod, i) => (
            <div key={i} className="bg-[#0a0a0a] border border-white/10 rounded-xl p-4 hover:border-purple-500/30 transition-colors group cursor-default">
              <code className="text-sm font-bold text-purple-400 group-hover:text-purple-300 transition-colors">{mod.name}</code>
              <p className="text-xs text-zinc-600 mt-1.5">{mod.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ================================================================
          ARCHITECTURE DEEP DIVE — Storage Runtime
          ================================================================ */}
      <section className="container mx-auto px-4 max-w-6xl mb-32 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-orange-900/5 via-transparent to-transparent rounded-3xl blur-3xl pointer-events-none" />

        <div className="text-center mb-14">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Native Storage{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-amber-400">Operating System.</span>
          </h2>
          <p className="text-zinc-500 max-w-2xl mx-auto">
            Not an ORM wrapper. AAYU&apos;s Storage Runtime is a full database operating system — Schema Engine, Migration Engine, Query AST, Planner, Optimizer, Transaction Manager, with SQLite and Postgres adapters.
          </p>
        </div>

        <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-8 md:p-12 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-orange-500/50 to-transparent" />

          <div className="grid md:grid-cols-3 gap-6">
            {[
              { title: "Schema Engine", desc: "Declarative model definitions with automatic migrations, constraints, indexes, and relations.", icon: Layers },
              { title: "Query Planner", desc: "Query AST → Logical Plan → Optimized Physical Plan. Cost-based optimization with index awareness.", icon: Workflow },
              { title: "Transaction Manager", desc: "ACID transactions with savepoints, rollback, isolation levels. Connection pooling built in.", icon: ShieldCheck },
              { title: "Migration Engine", desc: "Automatic schema diffing, versioned migrations, rollback support. Zero-downtime schema evolution.", icon: GitBranch },
              { title: "Storage Adapters", desc: "SQLite for development, Postgres for production. Same AAYU code, swap with one line.", icon: HardDrive },
              { title: "Query Optimizer", desc: "Predicate pushdown, join reordering, projection pruning. Generates efficient SQL from AAYU queries.", icon: Zap },
            ].map((item, i) => (
              <div key={i} className="p-5 rounded-xl border border-white/5 hover:border-orange-500/20 transition-colors">
                <item.icon className="w-5 h-5 text-orange-400 mb-3" />
                <h4 className="font-bold text-sm mb-2">{item.title}</h4>
                <p className="text-xs text-zinc-500 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ================================================================
          PRODUCTION EXAMPLES
          ================================================================ */}
      <section className="container mx-auto px-4 max-w-7xl mb-32">
        <div className="flex items-center justify-between mb-10">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold mb-2">Production Examples</h2>
            <p className="text-zinc-500 text-sm">Real-world applications built entirely in AAYU.</p>
          </div>
          <Link href="/examples" className="text-purple-400 hover:text-purple-300 text-sm font-bold flex items-center gap-1 transition-colors">
            View All <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-5">
          {productionExamples.map((example, i) => (
            <div key={i} className="bg-[#0a0a0a] border border-white/10 p-6 rounded-2xl hover:border-purple-500/40 transition-all duration-300 cursor-pointer group relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-purple-500/5 blur-2xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />

              <span className="text-3xl mb-4 block">{example.icon}</span>
              <h4 className="font-bold text-sm text-zinc-200 mb-1 group-hover:text-white transition-colors">{example.name}</h4>
              <p className="text-xs text-zinc-600 mb-3">{example.desc}</p>
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono text-zinc-700">{example.lines} lines</span>
                <ArrowRight className="w-3.5 h-3.5 text-zinc-700 group-hover:text-purple-400 group-hover:translate-x-1 transition-all" />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ================================================================
          QUICK START / CTA
          ================================================================ */}
      <section className="container mx-auto px-4 max-w-4xl mb-32 relative">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-900/10 via-blue-900/10 to-cyan-900/10 rounded-3xl blur-3xl pointer-events-none" />

        <div className="relative bg-[#0a0a0a] border border-white/10 rounded-2xl p-10 md:p-16 text-center overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-purple-500/40 to-transparent" />
          <div className="absolute bottom-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-blue-500/40 to-transparent" />

          <h2 className="text-3xl md:text-4xl font-bold mb-4">Get Started in 30 Seconds.</h2>
          <p className="text-zinc-500 mb-10 max-w-lg mx-auto">
            Install AAYU, create a file, run it. No boilerplate, no configuration files, no dependency hell.
          </p>

          <div className="bg-black border border-white/10 rounded-xl p-6 max-w-lg mx-auto text-left font-mono text-sm mb-10 space-y-3">
            <div className="flex items-center gap-3">
              <span className="text-zinc-600 select-none">$</span>
              <span className="text-green-400">pip install aayu-lang</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-zinc-600 select-none">$</span>
              <span className="text-blue-400">aayu init myapp</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-zinc-600 select-none">$</span>
              <span className="text-purple-400">aayu run myapp/main.aayu</span>
            </div>
            <div className="border-t border-white/5 pt-3 mt-3">
              <span className="text-emerald-400">✓ Compiled in 12ms</span>
            </div>
            <div>
              <span className="text-emerald-400">✓ VM started — Hello from AAYU</span>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/docs">
              <Button className="px-8 py-3 bg-white text-black hover:bg-zinc-200 font-bold rounded-xl text-base h-auto">
                Read the Docs <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
            <Link href="https://github.com/Minato95-ayu/INTENT-TO-SILICON" target="_blank">
              <Button variant="outline" className="px-8 py-3 border-white/10 bg-transparent hover:bg-white/5 hover:text-white font-bold rounded-xl text-base h-auto">
                <GitBranch className="w-4 h-4 mr-2" /> Star on GitHub
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* ================================================================
          LANGUAGE STATS BAR
          ================================================================ */}
      <section className="border-t border-white/5 py-16">
        <div className="container mx-auto px-4 max-w-5xl">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {[
              { value: "v2.0.0", label: "Latest Release" },
              { value: "8", label: "Stdlib Modules" },
              { value: "0", label: "Dependencies" },
              { value: "12ms", label: "Avg Compile" },
            ].map((stat, i) => (
              <div key={i}>
                <div className="text-2xl md:text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400">
                  {stat.value}
                </div>
                <div className="text-xs text-zinc-600 mt-1 font-medium uppercase tracking-wider">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

    </main>
  );
}

/* ─────────────────────────────────────────────
   CheckCircle icon (inline SVG)
   ───────────────────────────────────────────── */
function CheckCircle(props: any) {
  return (
    <svg {...props} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
    </svg>
  );
}
