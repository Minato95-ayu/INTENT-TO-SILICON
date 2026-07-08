/* eslint-disable */

"use client";

import {
  CheckCircle2,
  Loader2,
  Circle,
  Code2,
  Globe,
  Database,
  Terminal,
  BookOpen,
  Layers,
  Monitor,
  Clock,
  Sparkles,
  Package,
  Bug,
  Infinity,
} from "lucide-react";

// ─── Data ──────────────────────────────────────────────────────────────────────

type Phase = {
  id: string;
  title: string;
  status: "completed" | "in-progress" | "planned";
  description: string;
  items: string[];
  icon: React.ReactNode;
};

const phases: Phase[] = [
  {
    id: "A",
    title: "Language Core",
    status: "completed",
    description:
      "The foundational compiler pipeline — from source text to executing bytecode. Every layer hand-built from scratch.",
    items: [
      "Lexer",
      "Parser",
      "AST",
      "Semantic Analysis",
      "Type Checker",
      "Bytecode Compiler",
      "Virtual Machine",
      "Garbage Collector",
      "Module System",
      "Import System",
    ],
    icon: <Code2 className="w-5 h-5" />,
  },
  {
    id: "B",
    title: "Native HTTP Runtime",
    status: "completed",
    description:
      "A zero-dependency HTTP server built directly into the language runtime. No Express, no Koa — pure AAYU.",
    items: [
      "HTTP Server",
      "Router",
      "Request / Response",
      "Middleware",
      "JSON Body Parser",
      "Static Files",
      "WebSocket (initial)",
    ],
    icon: <Globe className="w-5 h-5" />,
  },
  {
    id: "C",
    title: "Native Storage Runtime",
    status: "completed",
    description:
      "A full relational storage engine embedded in the runtime — schema definitions, migrations, query planning, and optimization without ORMs.",
    items: [
      "Schema Engine",
      "Migration Engine",
      "Query AST",
      "Query Planner",
      "Query Optimizer",
      "Transaction Manager",
      "Validation Engine",
      "SQLite Adapter",
      "Relation Engine",
      "Index Engine",
    ],
    icon: <Database className="w-5 h-5" />,
  },
  {
    id: "CLI",
    title: "CLI & Tooling",
    status: "completed",
    description:
      "Developer experience tools — build, run, manage packages, and write code with first-class editor support.",
    items: [
      "aayu run",
      "aayu build",
      "Package Manager (apm)",
      "VS Code Extension",
    ],
    icon: <Terminal className="w-5 h-5" />,
  },
  {
    id: "STD",
    title: "Standard Library",
    status: "completed",
    description:
      "Production-grade standard modules shipping with every AAYU installation.",
    items: [
      "math",
      "json",
      "fs",
      "crypto",
      "http",
      "database",
      "process",
      "env",
    ],
    icon: <BookOpen className="w-5 h-5" />,
  },
  {
    id: "D",
    title: "Native State Runtime",
    status: "in-progress",
    description:
      "First-class application state management woven into the language — reactive, observable, and deterministic.",
    items: ["Application state management"],
    icon: <Layers className="w-5 h-5" />,
  },
  {
    id: "E",
    title: "UI Runtime v2",
    status: "in-progress",
    description:
      "A native rendering pipeline that bypasses the traditional DOM bottleneck with a custom layout engine.",
    items: ["Render Tree", "Layout Engine", "Event System", "DOM Bridge"],
    icon: <Monitor className="w-5 h-5" />,
  },
  {
    id: "F",
    title: "Scheduler Runtime",
    status: "planned",
    description:
      "Built-in task scheduling with cron-style jobs and background workers — no external dependencies.",
    items: ["Task scheduling", "Cron jobs"],
    icon: <Clock className="w-5 h-5" />,
  },
  {
    id: "G",
    title: "Animation Engine",
    status: "planned",
    description:
      "Hardware-accelerated animation primitives native to the language for fluid, 60fps interfaces.",
    items: ["Native animation system"],
    icon: <Sparkles className="w-5 h-5" />,
  },
  {
    id: "H",
    title: "Package Manager v2",
    status: "planned",
    description:
      "A full package ecosystem with a public registry, semantic versioning, and deterministic dependency resolution.",
    items: ["Registry", "Versioning", "Dependency resolution"],
    icon: <Package className="w-5 h-5" />,
  },
  {
    id: "I",
    title: "Debugger",
    status: "planned",
    description:
      "Step-through debugging with breakpoints, watch expressions, and call-stack inspection — built into the VM.",
    items: ["Step-through debugging", "Breakpoints"],
    icon: <Bug className="w-5 h-5" />,
  },
  {
    id: "J",
    title: "Self-Hosting",
    status: "planned",
    description:
      "The final milestone — the AAYU compiler rewritten entirely in AAYU. Full bootstrap.",
    items: ["AAYU compiler written in AAYU"],
    icon: <Infinity className="w-5 h-5" />,
  },
];

// ─── Helpers ───────────────────────────────────────────────────────────────────

const statusConfig = {
  completed: {
    label: "Completed",
    badge: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    dot: "bg-emerald-500",
    line: "from-emerald-500",
    icon: <CheckCircle2 className="w-4 h-4 text-emerald-400" />,
    ring: "ring-emerald-500/30",
    glow: "bg-emerald-500/20",
    iconBg: "bg-emerald-900/30 border-emerald-500/40",
  },
  "in-progress": {
    label: "In Progress",
    badge: "bg-amber-500/10 text-amber-400 border-amber-500/20",
    dot: "bg-amber-500",
    line: "from-amber-500",
    icon: <Loader2 className="w-4 h-4 text-amber-400 animate-spin" />,
    ring: "ring-amber-500/30",
    glow: "bg-amber-500/20",
    iconBg: "bg-amber-900/30 border-amber-500/40",
  },
  planned: {
    label: "Planned",
    badge: "bg-zinc-500/10 text-zinc-400 border-zinc-500/20",
    dot: "bg-zinc-600",
    line: "from-zinc-600",
    icon: <Circle className="w-4 h-4 text-zinc-500" />,
    ring: "ring-zinc-500/20",
    glow: "bg-zinc-500/10",
    iconBg: "bg-zinc-800/50 border-zinc-600/40",
  },
};

// ─── Component ─────────────────────────────────────────────────────────────────

export default function RoadmapPage() {
  const completed = phases.filter((p) => p.status === "completed");
  const inProgress = phases.filter((p) => p.status === "in-progress");
  const planned = phases.filter((p) => p.status === "planned");

  return (
    <main className="min-h-screen bg-[#000000] text-white pt-20 pb-24 selection:bg-purple-500/30">
      {/* Hero */}
      <section className="container mx-auto px-4 max-w-4xl mb-20 relative">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-purple-900/15 rounded-full blur-[120px] pointer-events-none" />

        <div className="text-center relative z-10">
          <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-sm text-zinc-400 mb-8">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            {completed.length} of {phases.length} phases shipped
          </div>

          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-5">
            The Road to{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400">
              Self-Hosting
            </span>
          </h1>
          <p className="text-lg text-zinc-400 max-w-2xl mx-auto">
            Every runtime, every engine, every optimizer — built from scratch.
            Here's where AAYU stands and where it's headed.
          </p>
        </div>
      </section>

      {/* Status Legend */}
      <section className="container mx-auto px-4 max-w-4xl mb-16">
        <div className="flex flex-wrap justify-center gap-6 text-sm">
          {(["completed", "in-progress", "planned"] as const).map((status) => (
            <div key={status} className="flex items-center gap-2">
              <span
                className={`w-3 h-3 rounded-full ${statusConfig[status].dot}`}
              />
              <span className="text-zinc-400">
                {statusConfig[status].label}
              </span>
              <span className="text-zinc-600 font-mono text-xs">
                (
                {status === "completed"
                  ? completed.length
                  : status === "in-progress"
                  ? inProgress.length
                  : planned.length}
                )
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* Timeline */}
      <section className="container mx-auto px-4 max-w-4xl">
        <div className="relative">
          {/* Vertical line */}
          <div className="absolute left-6 md:left-8 top-0 bottom-0 w-px bg-gradient-to-b from-emerald-500/50 via-amber-500/50 to-zinc-700/50" />

          <div className="space-y-6">
            {/* Section Headers + Cards */}
            <SectionHeader
              title="Completed"
              emoji="✅"
              count={completed.length}
            />
            {completed.map((phase, i) => (
              <PhaseCard key={phase.id} phase={phase} index={i} />
            ))}

            <SectionHeader
              title="In Progress"
              emoji="🔄"
              count={inProgress.length}
            />
            {inProgress.map((phase, i) => (
              <PhaseCard
                key={phase.id}
                phase={phase}
                index={completed.length + i}
              />
            ))}

            <SectionHeader
              title="Planned"
              emoji="📋"
              count={planned.length}
            />
            {planned.map((phase, i) => (
              <PhaseCard
                key={phase.id}
                phase={phase}
                index={completed.length + inProgress.length + i}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Bottom CTA */}
      <section className="container mx-auto px-4 max-w-4xl mt-24">
        <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-8 md:p-12 text-center relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(168,85,247,0.08)_0%,transparent_70%)]" />
          <div className="relative z-10">
            <h2 className="text-2xl md:text-3xl font-bold mb-4">
              Want to contribute?
            </h2>
            <p className="text-zinc-400 max-w-lg mx-auto mb-8">
              AAYU is built in public. Every phase is open to contributors —
              from the VM internals to the animation engine.
            </p>
            <a
              href="https://github.com/AayuSurana/AAYU"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 bg-white text-black font-bold px-6 py-3 rounded-xl hover:bg-zinc-200 transition-colors"
            >
              View on GitHub
              <svg
                className="w-4 h-4"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
              </svg>
            </a>
          </div>
        </div>
      </section>
    </main>
  );
}

// ─── Section Header ────────────────────────────────────────────────────────────

function SectionHeader({
  title,
  emoji,
  count,
}: {
  title: string;
  emoji: string;
  count: number;
}) {
  return (
    <div className="relative pl-16 md:pl-20 py-4">
      {/* Diamond marker on timeline */}
      <div className="absolute left-[18px] md:left-[26px] top-1/2 -translate-y-1/2 w-3 h-3 rotate-45 bg-white/20 border border-white/30" />
      <h2 className="text-xl font-bold text-white flex items-center gap-3">
        <span>{emoji}</span>
        {title}
        <span className="text-sm font-mono text-zinc-500">({count})</span>
      </h2>
    </div>
  );
}

// ─── Phase Card ────────────────────────────────────────────────────────────────

function PhaseCard({ phase, index }: { phase: Phase; index: number }) {
  const config = statusConfig[phase.status];

  return (
    <div className="relative pl-16 md:pl-20 group">
      {/* Timeline Node */}
      <div
        className={`absolute left-[13px] md:left-[21px] top-6 w-[13px] h-[13px] rounded-full ${config.dot} ring-4 ${config.ring} transition-all group-hover:scale-125`}
      />

      {/* Card */}
      <div className="bg-[#0a0a0a] border border-white/[0.08] rounded-2xl p-6 hover:border-white/[0.15] transition-all duration-300 relative overflow-hidden">
        {/* Subtle glow */}
        <div
          className={`absolute -top-12 -right-12 w-32 h-32 ${config.glow} rounded-full blur-3xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-500`}
        />

        <div className="relative z-10">
          {/* Header row */}
          <div className="flex flex-col sm:flex-row sm:items-center gap-3 mb-4">
            <div className="flex items-center gap-3">
              <div
                className={`w-9 h-9 rounded-lg border ${config.iconBg} flex items-center justify-center`}
              >
                {phase.icon}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-mono font-bold text-zinc-600 uppercase tracking-widest">
                    Phase {phase.id}
                  </span>
                  <span
                    className={`inline-flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-wider border rounded-full px-2.5 py-0.5 ${config.badge}`}
                  >
                    {config.icon}
                    {config.label}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-white mt-0.5">
                  {phase.title}
                </h3>
              </div>
            </div>
          </div>

          {/* Description */}
          <p className="text-sm text-zinc-500 leading-relaxed mb-4">
            {phase.description}
          </p>

          {/* Items */}
          <div className="flex flex-wrap gap-2">
            {phase.items.map((item) => (
              <span
                key={item}
                className="inline-flex items-center gap-1.5 text-xs bg-white/[0.04] border border-white/[0.06] text-zinc-400 px-2.5 py-1 rounded-lg"
              >
                {phase.status === "completed" && (
                  <CheckCircle2 className="w-3 h-3 text-emerald-500 shrink-0" />
                )}
                {phase.status === "in-progress" && (
                  <Loader2 className="w-3 h-3 text-amber-500 animate-spin shrink-0" />
                )}
                {phase.status === "planned" && (
                  <Circle className="w-3 h-3 text-zinc-600 shrink-0" />
                )}
                {item}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
