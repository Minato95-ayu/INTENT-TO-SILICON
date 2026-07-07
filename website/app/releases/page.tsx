/* eslint-disable */

"use client";

import { CheckCircle2, AlertTriangle, Zap, Package, GitMerge } from "lucide-react";
import Link from "next/link";

const RELEASES = [
  {
    version: "v1.0.0-stable",
    date: "July 2026",
    tag: "Latest",
    title: "The Intent Engine Era Begins",
    description: "The first stable release of AAYU, featuring the fully offline BrainOS architecture, Intent Graph Extraction, and deterministic ARC memory management.",
    features: [
      "Offline BrainOS Knowledge Base covering 20 domains.",
      "Intent Engine v1 with automated Architecture extraction.",
      "Deterministic ARC (Automatic Reference Counting) Runtime.",
      "AAYU Package Manager (apm) built-in.",
      "LLVM Backend optimization enabled by default."
    ],
    fixes: [
      "Resolved race conditions in lightweight fibers.",
      "Fixed cyclic dependencies in complex package imports."
    ],
    breaking: []
  },
  {
    version: "v0.9.0-beta",
    date: "May 2026",
    tag: "Beta",
    title: "BrainOS Integration & Toolchain Stabilization",
    description: "Introduced the rule-based Decision Engine and Tradeoff Evaluator.",
    features: [
      "Added 'aayu brainos analyze' CLI command.",
      "Implemented VS Code Extension LSP integration.",
      "Support for multi-file AAYU projects."
    ],
    fixes: [
      "Memory leak in the AST node traverser.",
      "Formatter inserting trailing commas unnecessarily."
    ],
    breaking: [
      "Changed keyword 'struct' to 'entity' to align with Intent-Driven Architecture.",
      "Semi-colons ';' replaced with dots '.' for statement termination."
    ]
  }
];

export default function ReleasesPage() {
  return (
    <main className="min-h-screen bg-black text-white pt-24 pb-20">
      <div className="container mx-auto px-4 max-w-4xl">
        
        <div className="mb-16">
          <h1 className="text-4xl font-extrabold tracking-tight mb-4">Release Notes</h1>
          <p className="text-xl text-zinc-400">Stay up to date with the latest features, fixes, and architectural upgrades in AAYU.</p>
        </div>

        <div className="space-y-16 flex flex-col relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-white/10 before:to-transparent">
          {RELEASES.map((release, i) => (
            <div key={i} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
              {/* Timeline Icon */}
              <div className="flex items-center justify-center w-10 h-10 rounded-full border border-white/10 bg-black text-blue-500 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-lg z-10">
                <GitMerge className="w-5 h-5" />
              </div>
              
              {/* Content Card */}
              <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-6 rounded-xl border border-white/10 bg-[#0a0a0a] hover:bg-white/5 transition-colors">
                <div className="flex items-center gap-3 mb-2">
                  <h2 className="text-2xl font-bold font-mono">{release.version}</h2>
                  {release.tag && (
                    <span className="px-2 py-0.5 text-xs font-bold uppercase tracking-wider rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                      {release.tag}
                    </span>
                  )}
                </div>
                <div className="text-sm text-zinc-500 font-mono mb-4">{release.date}</div>
                <h3 className="text-lg font-semibold mb-2">{release.title}</h3>
                <p className="text-zinc-400 text-sm leading-relaxed mb-6">{release.description}</p>
                
                {release.features.length > 0 && (
                  <div className="mb-4">
                    <h4 className="text-sm font-bold flex items-center gap-2 mb-2 text-green-400">
                      <Zap className="w-4 h-4" /> Features
                    </h4>
                    <ul className="space-y-1">
                      {release.features.map((f, idx) => (
                        <li key={idx} className="text-sm text-zinc-300 flex items-start gap-2">
                          <span className="text-green-500 mt-1">•</span> {f}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {release.fixes.length > 0 && (
                  <div className="mb-4">
                    <h4 className="text-sm font-bold flex items-center gap-2 mb-2 text-blue-400">
                      <CheckCircle2 className="w-4 h-4" /> Fixes
                    </h4>
                    <ul className="space-y-1">
                      {release.fixes.map((f, idx) => (
                        <li key={idx} className="text-sm text-zinc-300 flex items-start gap-2">
                          <span className="text-blue-500 mt-1">•</span> {f}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {release.breaking.length > 0 && (
                  <div>
                    <h4 className="text-sm font-bold flex items-center gap-2 mb-2 text-red-400">
                      <AlertTriangle className="w-4 h-4" /> Breaking Changes
                    </h4>
                    <ul className="space-y-1">
                      {release.breaking.map((f, idx) => (
                        <li key={idx} className="text-sm text-zinc-300 flex items-start gap-2">
                          <span className="text-red-500 mt-1">•</span> {f}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
        
      </div>
    </main>
  );
}
