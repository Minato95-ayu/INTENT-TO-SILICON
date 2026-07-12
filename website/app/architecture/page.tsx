/* eslint-disable */
"use client";

import { useState } from "react";
import {
  Cpu,
  FileCode2,
  ListTree,
  ShieldCheck,
  Binary,
  HardDrive,
  Box,
  MemoryStick,
  Cog,
  Globe,
  Database,
  Monitor,
  Layers,
  ChevronDown,
  ChevronRight,
  Server,
  Route,
  ArrowLeftRight,
  Plug,
  Radio,
  TableProperties,
  GitBranch,
  Search,
  ClipboardList,
  Gauge,
  Lock,
  Columns2,
  TreePine,
  LayoutDashboard,
  MousePointerClick,
  Code2,
  Library,
  Hash,
  FileJson,
  FolderOpen,
  KeyRound,
  Wifi,
  Terminal,
  Settings,
} from "lucide-react";

/* ──────────────────────────────────────────────────────────────────────
   TYPES
   ────────────────────────────────────────────────────────────────────── */
interface PipelineNode {
  id: string;
  label: string;
  sublabel: string;
  icon: React.ReactNode;
  accent: string; // tailwind color class prefix e.g. "blue"
  bgGlow: string;
}

interface RuntimeGroup {
  id: string;
  label: string;
  icon: React.ReactNode;
  accent: string;
  items: { label: string; icon: React.ReactNode }[];
}

/* ──────────────────────────────────────────────────────────────────────
   DATA
   ────────────────────────────────────────────────────────────────────── */
const compilerPipeline: PipelineNode[] = [
  {
    id: "source",
    label: ".aayu Source Code",
    sublabel: "Human-readable AAYU source files",
    icon: <FileCode2 className="w-5 h-5" />,
    accent: "blue",
    bgGlow: "rgba(59,130,246,0.12)",
  },
  {
    id: "lexer",
    label: "Lexer",
    sublabel: "Tokenization — breaks source into tokens",
    icon: <Code2 className="w-5 h-5" />,
    accent: "blue",
    bgGlow: "rgba(59,130,246,0.10)",
  },
  {
    id: "parser",
    label: "Parser",
    sublabel: "Grammar analysis — validates token structure",
    icon: <ListTree className="w-5 h-5" />,
    accent: "blue",
    bgGlow: "rgba(59,130,246,0.08)",
  },
  {
    id: "ast",
    label: "AST",
    sublabel: "Abstract Syntax Tree — structured IR",
    icon: <TreePine className="w-5 h-5" />,
    accent: "blue",
    bgGlow: "rgba(59,130,246,0.08)",
  },
  {
    id: "semantic",
    label: "Semantic Analysis",
    sublabel: "Type checking, scope resolution, validation",
    icon: <ShieldCheck className="w-5 h-5" />,
    accent: "blue",
    bgGlow: "rgba(59,130,246,0.06)",
  },
  {
    id: "bytecode-compiler",
    label: "Bytecode Compiler",
    sublabel: "Compiles validated AST to AAYU bytecode",
    icon: <Binary className="w-5 h-5" />,
    accent: "cyan",
    bgGlow: "rgba(6,182,212,0.10)",
  },
  {
    id: "ayc",
    label: "AAYU Bytecode (.ayc)",
    sublabel: "Portable bytecode format for the VM",
    icon: <HardDrive className="w-5 h-5" />,
    accent: "cyan",
    bgGlow: "rgba(6,182,212,0.12)",
  },
];

const runtimes: RuntimeGroup[] = [
  {
    id: "http",
    label: "HTTP Runtime",
    icon: <Globe className="w-5 h-5" />,
    accent: "green",
    items: [
      { label: "Server", icon: <Server className="w-4 h-4" /> },
      { label: "Router", icon: <Route className="w-4 h-4" /> },
      { label: "Request / Response", icon: <ArrowLeftRight className="w-4 h-4" /> },
      { label: "Middleware", icon: <Plug className="w-4 h-4" /> },
      { label: "WebSocket", icon: <Radio className="w-4 h-4" /> },
    ],
  },
  {
    id: "storage",
    label: "Storage Runtime",
    icon: <Database className="w-5 h-5" />,
    accent: "orange",
    items: [
      { label: "Schema Engine", icon: <TableProperties className="w-4 h-4" /> },
      { label: "Migration Engine", icon: <GitBranch className="w-4 h-4" /> },
      { label: "Query AST", icon: <Search className="w-4 h-4" /> },
      { label: "Planner", icon: <ClipboardList className="w-4 h-4" /> },
      { label: "Optimizer", icon: <Gauge className="w-4 h-4" /> },
      { label: "Transaction Manager", icon: <Lock className="w-4 h-4" /> },
      { label: "SQLite / Postgres Adapter", icon: <Columns2 className="w-4 h-4" /> },
    ],
  },
  {
    id: "ui",
    label: "UI Runtime",
    icon: <Monitor className="w-5 h-5" />,
    accent: "green",
    items: [
      { label: "Render Tree", icon: <TreePine className="w-4 h-4" /> },
      { label: "Layout Engine", icon: <LayoutDashboard className="w-4 h-4" /> },
      { label: "Event System", icon: <MousePointerClick className="w-4 h-4" /> },
      { label: "DOM Bridge", icon: <Columns2 className="w-4 h-4" /> },
    ],
  },
  {
    id: "state",
    label: "State Runtime",
    icon: <Layers className="w-5 h-5" />,
    accent: "green",
    items: [],
  },
];

const stdlibModules = [
  { label: "math", icon: <Hash className="w-4 h-4" /> },
  { label: "json", icon: <FileJson className="w-4 h-4" /> },
  { label: "fs", icon: <FolderOpen className="w-4 h-4" /> },
  { label: "crypto", icon: <KeyRound className="w-4 h-4" /> },
  { label: "http", icon: <Wifi className="w-4 h-4" /> },
  { label: "database", icon: <Database className="w-4 h-4" /> },
  { label: "process", icon: <Terminal className="w-4 h-4" /> },
  { label: "env", icon: <Settings className="w-4 h-4" /> },
];

/* ──────────────────────────────────────────────────────────────────────
   ACCENT HELPERS
   ────────────────────────────────────────────────────────────────────── */
const accentMap: Record<string, { border: string; text: string; bg: string; glow: string }> = {
  blue: {
    border: "border-blue-500/40",
    text: "text-blue-400",
    bg: "bg-blue-500/10",
    glow: "from-blue-500/20",
  },
  cyan: {
    border: "border-cyan-500/40",
    text: "text-cyan-400",
    bg: "bg-cyan-500/10",
    glow: "from-cyan-500/20",
  },
  purple: {
    border: "border-purple-500/40",
    text: "text-purple-400",
    bg: "bg-purple-500/10",
    glow: "from-purple-500/20",
  },
  green: {
    border: "border-emerald-500/40",
    text: "text-emerald-400",
    bg: "bg-emerald-500/10",
    glow: "from-emerald-500/20",
  },
  orange: {
    border: "border-orange-500/40",
    text: "text-orange-400",
    bg: "bg-orange-500/10",
    glow: "from-orange-500/20",
  },
};

/* ──────────────────────────────────────────────────────────────────────
   CONNECTOR LINE  (vertical)
   ────────────────────────────────────────────────────────────────────── */
function Connector({ color = "blue" }: { color?: string }) {
  const c = accentMap[color] ?? accentMap.blue;
  return (
    <div className="flex flex-col items-center py-1">
      <div className={`w-px h-8 ${c.border.replace("border-", "bg-")} opacity-60`} />
      <div className={`w-2 h-2 rounded-full ${c.bg} ${c.border} border`} />
      <div className={`w-px h-8 ${c.border.replace("border-", "bg-")} opacity-60`} />
    </div>
  );
}

/* ──────────────────────────────────────────────────────────────────────
   BIG CONNECTOR (between compiler and VM)
   ────────────────────────────────────────────────────────────────────── */
function BigConnector() {
  return (
    <div className="flex flex-col items-center py-2">
      <div className="w-px h-6 bg-purple-500/40" />
      <div className="w-3 h-3 rounded-full bg-purple-500/20 border border-purple-500/50 animate-pulse" />
      <div className="w-px h-6 bg-purple-500/40" />
    </div>
  );
}

/* ──────────────────────────────────────────────────────────────────────
   PIPELINE NODE CARD
   ────────────────────────────────────────────────────────────────────── */
function PipelineCard({ node }: { node: PipelineNode }) {
  const a = accentMap[node.accent] ?? accentMap.blue;
  return (
    <div
      className={`relative w-full max-w-md mx-auto group`}
    >
      {/* glow */}
      <div
        className="absolute -inset-px rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-sm pointer-events-none"
        style={{ background: node.bgGlow }}
      />
      <div
        className={`relative bg-[#0a0a0a] ${a.border} border rounded-xl px-5 py-4 flex items-center gap-4 transition-all duration-300 hover:border-opacity-80`}
      >
        <div className={`flex-shrink-0 w-10 h-10 rounded-lg ${a.bg} flex items-center justify-center ${a.text}`}>
          {node.icon}
        </div>
        <div className="min-w-0">
          <h3 className="text-sm font-bold text-zinc-100 leading-tight">{node.label}</h3>
          <p className="text-xs text-zinc-500 mt-0.5 leading-snug">{node.sublabel}</p>
        </div>
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────────────────────────────
   RUNTIME EXPANDABLE CARD
   ────────────────────────────────────────────────────────────────────── */
function RuntimeCard({ runtime }: { runtime: RuntimeGroup }) {
  const [open, setOpen] = useState(false);
  const a = accentMap[runtime.accent] ?? accentMap.green;

  return (
    <div className="bg-[#0a0a0a] border border-white/[0.08] rounded-xl overflow-hidden transition-all duration-300 hover:border-white/[0.15]">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center gap-3 px-4 py-3.5 text-left group"
      >
        <div className={`flex-shrink-0 w-9 h-9 rounded-lg ${a.bg} flex items-center justify-center ${a.text}`}>
          {runtime.icon}
        </div>
        <span className="text-sm font-bold text-zinc-200 flex-1">{runtime.label}</span>
        {runtime.items.length > 0 && (
          <span className="text-zinc-600 group-hover:text-zinc-400 transition-colors">
            {open ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
          </span>
        )}
      </button>

      {open && runtime.items.length > 0 && (
        <div className="px-4 pb-4 pt-1 border-t border-white/5">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {runtime.items.map((item) => (
              <div
                key={item.label}
                className={`flex items-center gap-2.5 px-3 py-2 rounded-lg bg-white/[0.02] border border-white/[0.05] text-xs text-zinc-400`}
              >
                <span className={a.text}>{item.icon}</span>
                {item.label}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

/* ──────────────────────────────────────────────────────────────────────
   PAGE
   ────────────────────────────────────────────────────────────────────── */
export default function ArchitecturePage() {
  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-32 selection:bg-purple-500/30">
      {/* Background radial glow */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[900px] h-[500px] bg-blue-900/10 rounded-full blur-[140px]" />
        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[700px] h-[400px] bg-purple-900/10 rounded-full blur-[120px]" />
      </div>

      <div className="container mx-auto px-4 max-w-5xl relative z-10">

        {/* ── HEADER ──────────────────────────────────────────────── */}
        <header className="mb-20 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold mb-6">
            <Cpu className="w-4 h-4" /> System Architecture
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
            How AAYU{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-emerald-400">
              Works
            </span>
          </h1>
          <p className="text-lg text-zinc-400 max-w-2xl mx-auto">
            From human-readable <code className="text-blue-400 font-mono text-sm">.aayu</code> source
            to a full-stack virtual machine — every stage of the compilation and execution pipeline.
          </p>
        </header>

        {/* ── SECTION: COMPILER PIPELINE ─────────────────────────── */}
        <section className="mb-6">
          <div className="flex items-center gap-2 mb-8 justify-center">
            <div className="h-px flex-1 max-w-[80px] bg-gradient-to-r from-transparent to-blue-500/30" />
            <span className="text-xs font-bold uppercase tracking-[0.2em] text-blue-400">
              Compiler Pipeline
            </span>
            <div className="h-px flex-1 max-w-[80px] bg-gradient-to-l from-transparent to-blue-500/30" />
          </div>

          <div className="flex flex-col items-center">
            {compilerPipeline.map((node, i) => (
              <div key={node.id} className="w-full">
                <PipelineCard node={node} />
                {i < compilerPipeline.length - 1 && (
                  <Connector color={i < 4 ? "blue" : "cyan"} />
                )}
              </div>
            ))}
          </div>
        </section>

        {/* ── BIG CONNECTOR ──────────────────────────────────────── */}
        <BigConnector />

        {/* ── SECTION: AAYU VM ───────────────────────────────────── */}
        <section className="mb-16">
          <div className="relative max-w-2xl mx-auto">
            {/* VM outer frame */}
            <div className="border border-purple-500/30 rounded-2xl overflow-hidden bg-[#07050c]/80 backdrop-blur-sm">
              {/* VM header bar */}
              <div className="px-5 py-4 bg-purple-500/[0.06] border-b border-purple-500/20 flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-purple-500/15 flex items-center justify-center text-purple-400">
                  <Box className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-lg font-extrabold text-purple-300 leading-tight">AAYU VM</h2>
                  <p className="text-xs text-purple-400/60">Bytecode execution engine</p>
                </div>
              </div>

              <div className="p-5 space-y-6">

                {/* ── Memory Manager ────────────────── */}
                <div>
                  <div className="flex items-center gap-2 mb-3">
                    <MemoryStick className="w-4 h-4 text-purple-400" />
                    <span className="text-sm font-bold text-purple-300">Memory Manager</span>
                  </div>
                  <div className="grid grid-cols-3 gap-2">
                    {["Stack", "Heap", "Garbage Collector"].map((m) => (
                      <div
                        key={m}
                        className="text-center text-xs text-zinc-400 bg-purple-500/[0.05] border border-purple-500/[0.12] rounded-lg py-2.5 px-2"
                      >
                        {m}
                      </div>
                    ))}
                  </div>
                </div>

                {/* ── Runtime Manager ───────────────── */}
                <div>
                  <div className="flex items-center gap-2 mb-3">
                    <Cog className="w-4 h-4 text-purple-400" />
                    <span className="text-sm font-bold text-purple-300">Runtime Manager</span>
                  </div>
                  <div className="space-y-2">
                    {runtimes.map((rt) => (
                      <RuntimeCard key={rt.id} runtime={rt} />
                    ))}
                  </div>
                </div>

                {/* ── Standard Library ──────────────── */}
                <div>
                  <div className="flex items-center gap-2 mb-3">
                    <Library className="w-4 h-4 text-purple-400" />
                    <span className="text-sm font-bold text-purple-300">Standard Library</span>
                  </div>
                  <div className="grid grid-cols-4 gap-2">
                    {stdlibModules.map((m) => (
                      <div
                        key={m.label}
                        className="flex items-center gap-2 text-xs text-zinc-400 bg-white/[0.02] border border-white/[0.06] rounded-lg py-2 px-3"
                      >
                        <span className="text-purple-400">{m.icon}</span>
                        <span className="font-mono">{m.label}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── LEGEND ─────────────────────────────────────────────── */}
        <section className="max-w-2xl mx-auto">
          <div className="bg-[#0a0a0a] border border-white/[0.08] rounded-xl px-6 py-5">
            <h3 className="text-xs font-bold uppercase tracking-[0.15em] text-zinc-500 mb-4">Legend</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-blue-500/30 border border-blue-500/50" />
                <span className="text-zinc-400">Compiler Frontend</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-cyan-500/30 border border-cyan-500/50" />
                <span className="text-zinc-400">Bytecode Backend</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-purple-500/30 border border-purple-500/50" />
                <span className="text-zinc-400">Virtual Machine</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-emerald-500/30 border border-emerald-500/50" />
                <span className="text-zinc-400">Runtimes</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-orange-500/30 border border-orange-500/50" />
                <span className="text-zinc-400">Storage Engine</span>
              </div>
            </div>
          </div>
        </section>

      </div>
    </main>
  );
}