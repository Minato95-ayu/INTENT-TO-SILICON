"""
=============================================================================
FILE: create_showcase.py
PURPOSE: Creates showcase/demo files
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles creates showcase/demo files.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os

base_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\showcase'
os.makedirs(base_dir, exist_ok=True)

showcase_code = '''
"use client";

import { ExternalLink, Star, Code2, Layers, Shield, Cpu } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

const PROJECTS = [
  {
    title: "TravelOS",
    category: "Official",
    description: "A complete global travel booking platform powered entirely by AAYU. Handles 100k+ concurrent searches.",
    image: "/globe.svg",
    tags: ["Intent Architecture", "Redis Caching", "PostgreSQL"],
    github: "#"
  },
  {
    title: "Topptic",
    category: "Official",
    description: "Real-time multiplayer collaboration whiteboard built with AAYU WebSockets and green fibers.",
    image: "/window.svg",
    tags: ["WebSockets", "Concurrency", "High Throughput"],
    github: "#"
  },
  {
    title: "BrainOS Engine",
    category: "Core",
    description: "The autonomous architect itself is built in AAYU. A masterclass in rule-based decision trees and NLP parsing.",
    image: "/file.svg",
    tags: ["Compiler", "Machine Learning", "Offline-First"],
    github: "https://github.com/Minato95-ayu/INTENT-TO-SILICON"
  },
  {
    title: "AAYU Commerce",
    category: "Community",
    description: "An open-source Shopify alternative scaffolding. Generated 90% by Intent Graph.",
    image: "/next.svg",
    tags: ["E-commerce", "Stripe API", "GraphQL"],
    github: "#"
  }
];

export default function ShowcasePage() {
  return (
    <main className="min-h-screen bg-black text-white pt-24 pb-20">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="mb-16 text-center">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
            Built with AAYU
          </h1>
          <p className="text-xl text-zinc-400 max-w-2xl mx-auto">
            Discover production-ready applications, open-source templates, and core tools built entirely on the AAYU Language.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {PROJECTS.map((project, i) => (
            <div key={i} className="group rounded-2xl bg-[#0a0a0a] border border-white/10 overflow-hidden hover:border-white/20 transition-all shadow-xl">
              <div className="h-48 bg-zinc-900 border-b border-white/10 flex items-center justify-center relative overflow-hidden">
                {/* Mock abstract image */}
                <div className="absolute inset-0 opacity-20 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-blue-500 via-transparent to-transparent group-hover:scale-110 transition-transform duration-700" />
                <h3 className="text-4xl font-extrabold text-white/50 tracking-widest">{project.title.toUpperCase()}</h3>
              </div>
              <div className="p-8">
                <div className="flex items-center gap-3 mb-4">
                  <h2 className="text-2xl font-bold">{project.title}</h2>
                  <span className={px-2 py-0.5 text-xs font-bold uppercase tracking-wider rounded border \}>
                    {project.category}
                  </span>
                </div>
                <p className="text-zinc-400 leading-relaxed mb-6 h-12">{project.description}</p>
                <div className="flex flex-wrap gap-2 mb-8">
                  {project.tags.map((tag, j) => (
                    <span key={j} className="px-2 py-1 bg-white/5 rounded text-xs text-zinc-300 font-mono">
                      {tag}
                    </span>
                  ))}
                </div>
                <div className="flex items-center gap-4 border-t border-white/10 pt-6">
                  <a href={project.github} target="_blank" rel="noreferrer" className="flex-1">
                    <Button variant="outline" className="w-full bg-white/5 border-white/10 hover:bg-white/10 text-white gap-2">
                      <Code2 className="w-4 h-4" /> Source Code
                    </Button>
                  </a>
                  <Button className="flex-1 bg-white text-black hover:bg-zinc-200 gap-2">
                    <ExternalLink className="w-4 h-4" /> Live Demo
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
'''

with open(os.path.join(base_dir, 'page.tsx'), 'w', encoding='utf-8') as f:
    f.write(showcase_code)

print("Created Showcase page.")
