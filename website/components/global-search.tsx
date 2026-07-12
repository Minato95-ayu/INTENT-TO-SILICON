/* eslint-disable */
﻿"use client";

import { useEffect, useState, useRef } from "react";
import { Search, FileText, Brain, Box, Terminal, BookOpen, X } from "lucide-react";
import { useRouter } from "next/navigation";

const SEARCH_DATA = [
  { title: "Compiler Pipeline", url: "/language/compiler", category: "Language", icon: Terminal },
  { title: "Memory & GC Runtime", url: "/language/runtime", category: "Language", icon: Terminal },
  { title: "Interfaces & Traits", url: "/docs/interfaces", category: "Documentation", icon: BookOpen },
  { title: "Generics", url: "/docs/generics", category: "Documentation", icon: BookOpen },
  { title: "BrainOS Decision Engine", url: "/brainos", category: "BrainOS", icon: Brain },
  { title: "Intent Graph Extraction", url: "/intent-engine", category: "Intent Engine", icon: FileText },
  { title: "Playground Editor", url: "/playground", category: "Platform", icon: Box },
  { title: "Package Registry", url: "/packages", category: "Ecosystem", icon: Box },
  { title: "AAYU Standard Library", url: "/docs/standard-library", category: "Documentation", icon: BookOpen },
];

export function GlobalSearch() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((o) => !o);
      }
      if (e.key === "Escape") {
        setOpen(false);
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, []);

  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 100);
      // setQuery("");
    }
  }, [open]);

  if (!open) return null;

  const filtered = SEARCH_DATA.filter(item => 
    item.title.toLowerCase().includes(query.toLowerCase()) || 
    item.category.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="fixed inset-0 z-[100] flex items-start justify-center pt-[15vh] sm:pt-[20vh]">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity" 
        onClick={() => setOpen(false)}
      />
      
      {/* Search Modal */}
      <div className="relative w-full max-w-xl mx-4 overflow-hidden rounded-xl border border-white/10 bg-[#0d0d0d] shadow-2xl animate-in fade-in zoom-in-95 duration-200">
        
        {/* Search Input */}
        <div className="flex items-center px-4 border-b border-white/10">
          <Search className="h-5 w-5 text-zinc-500" />
          <input
            ref={inputRef}
            className="flex-1 h-14 bg-transparent border-0 px-4 text-base text-white placeholder:text-zinc-500 focus:outline-none focus:ring-0"
            placeholder="Search documentation, API, packages..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-xs font-mono bg-white/5 rounded border border-white/10 text-zinc-500">ESC</kbd>
        </div>

        {/* Results list */}
        <div className="max-h-[60vh] overflow-y-auto p-2">
          {filtered.length === 0 ? (
            <div className="py-14 text-center text-sm text-zinc-500">
              No results found for "{query}".
            </div>
          ) : (
            <div className="space-y-1">
              {filtered.map((item, i) => (
                <button
                  key={i}
                  className="w-full flex items-center gap-3 px-3 py-3 text-left rounded-lg hover:bg-white/5 transition-colors focus:bg-white/10 focus:outline-none group"
                  onClick={() => {
                    router.push(item.url);
                    setOpen(false);
                  }}
                >
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-white/5 border border-white/10 text-zinc-400 group-hover:text-blue-400 group-hover:bg-blue-500/10 group-hover:border-blue-500/20 transition-colors">
                    <item.icon className="h-4 w-4" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-sm font-medium text-zinc-200 group-hover:text-white transition-colors">{item.title}</span>
                    <span className="text-xs text-zinc-500">{item.category}</span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
        
        {/* Footer */}
        <div className="flex items-center px-4 py-3 border-t border-white/5 bg-black/50 text-xs text-zinc-500">
          <div className="flex gap-4">
            <span className="flex items-center gap-1"><kbd className="px-1.5 py-0.5 rounded bg-white/5 border border-white/10 font-mono">â†‘â†“</kbd> to navigate</span>
            <span className="flex items-center gap-1"><kbd className="px-1.5 py-0.5 rounded bg-white/5 border border-white/10 font-mono">â†µ</kbd> to select</span>
          </div>
        </div>
      </div>
    </div>
  );
}

