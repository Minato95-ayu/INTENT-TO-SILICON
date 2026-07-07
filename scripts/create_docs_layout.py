import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\docs\layout.tsx'
os.makedirs(os.path.dirname(filepath), exist_ok=True)

content = '''
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Search, ChevronRight, Menu, Github, BookOpen, Code2, Bot, Layers, CheckCircle2, Box } from "lucide-react";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";

const SIDEBAR_NAV = [
  {
    title: "Getting Started",
    icon: BookOpen,
    links: [
      { title: "Introduction", href: "/docs" },
      { title: "Installation", href: "/docs/getting-started/installation" },
      { title: "Hello World", href: "/docs/getting-started/hello-world" },
    ]
  },
  {
    title: "Language",
    icon: Code2,
    links: [
      { title: "Syntax", href: "/docs/language/syntax" },
      { title: "Variables", href: "/docs/language/variables" },
      { title: "Functions", href: "/docs/language/functions" },
      { title: "Records", href: "/docs/language/records" },
      { title: "Interfaces", href: "/docs/language/interfaces" },
      { title: "Traits", href: "/docs/language/traits" },
      { title: "Generics", href: "/docs/language/generics" },
    ]
  },
  {
    title: "Compiler Pipeline",
    icon: Box,
    links: [
      { title: "Lexer", href: "/docs/compiler/lexer" },
      { title: "Parser", href: "/docs/compiler/parser" },
      { title: "AST", href: "/docs/compiler/ast" },
      { title: "Semantic Analysis", href: "/docs/compiler/semantic" },
      { title: "Optimizer", href: "/docs/compiler/optimizer" },
      { title: "LLVM Lowering", href: "/docs/compiler/llvm" },
    ]
  },
  {
    title: "Runtime",
    icon: CheckCircle2,
    links: [
      { title: "Memory (DARC)", href: "/docs/runtime/memory" },
      { title: "Standard Library", href: "/docs/runtime/stdlib" },
    ]
  },
  {
    title: "BrainOS",
    icon: Bot,
    links: [
      { title: "Orchestrator", href: "/docs/brainos/orchestrator" },
      { title: "Decision Engine", href: "/docs/brainos/decision-engine" },
    ]
  },
  {
    title: "Intent Engine",
    icon: Layers,
    links: [
      { title: "Knowledge Base", href: "/docs/intent/knowledge" },
      { title: "NLP Parser", href: "/docs/intent/nlp" },
    ]
  }
];

export default function DocsLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  // Ctrl+K to open search
  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setIsSearchOpen((open) => !open);
      }
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  return (
    <div className="min-h-screen bg-[#050505] text-white pt-16 flex flex-col md:flex-row">
      
      {/* Search Modal Overlay */}
      {isSearchOpen && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-24 px-4 bg-black/80 backdrop-blur-sm">
          <div className="bg-[#111] border border-white/10 rounded-xl w-full max-w-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center px-4 border-b border-white/10">
              <Search className="w-5 h-5 text-zinc-500" />
              <input 
                autoFocus
                placeholder="Search documentation..." 
                className="w-full bg-transparent border-none outline-none text-white px-4 py-4 text-lg placeholder:text-zinc-600"
              />
              <button onClick={() => setIsSearchOpen(false)} className="text-xs bg-white/10 px-2 py-1 rounded text-zinc-400 font-mono">ESC</button>
            </div>
            <div className="p-4 bg-[#0a0a0a]">
              <div className="text-xs font-bold text-zinc-500 uppercase mb-2">Suggestions</div>
              <div className="space-y-1">
                <Link href="/docs/language/variables" onClick={() => setIsSearchOpen(false)} className="flex items-center justify-between px-3 py-2 rounded-lg hover:bg-blue-600/20 hover:text-blue-400 group transition-colors">
                  <span className="flex items-center gap-2"><Code2 className="w-4 h-4 text-zinc-500 group-hover:text-blue-400"/> Variables in AAYU</span>
                  <ChevronRight className="w-4 h-4 text-zinc-600 group-hover:text-blue-400" />
                </Link>
                <Link href="/docs/compiler/ast" onClick={() => setIsSearchOpen(false)} className="flex items-center justify-between px-3 py-2 rounded-lg hover:bg-blue-600/20 hover:text-blue-400 group transition-colors">
                  <span className="flex items-center gap-2"><Box className="w-4 h-4 text-zinc-500 group-hover:text-blue-400"/> Abstract Syntax Tree</span>
                  <ChevronRight className="w-4 h-4 text-zinc-600 group-hover:text-blue-400" />
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Mobile Header (Docs only) */}
      <div className="md:hidden flex items-center justify-between p-4 border-b border-white/10 bg-[#0a0a0a]">
        <span className="font-bold">Documentation</span>
        <div className="flex gap-2">
          <button onClick={() => setIsSearchOpen(true)} className="p-2 bg-white/5 rounded"><Search className="w-5 h-5" /></button>
          <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="p-2 bg-white/5 rounded"><Menu className="w-5 h-5" /></button>
        </div>
      </div>

      {/* Sidebar */}
      <aside className={\ md:block w-full md:w-64 lg:w-72 border-r border-white/10 bg-[#0a0a0a] overflow-y-auto h-[calc(100vh-4rem)] sticky top-16 shrink-0}>
        
        {/* Search Bar (Sidebar) */}
        <div className="p-4 border-b border-white/5">
          <button onClick={() => setIsSearchOpen(true)} className="w-full flex items-center justify-between px-3 py-2 bg-black border border-white/10 rounded-lg text-sm text-zinc-500 hover:border-white/20 transition-colors">
            <span className="flex items-center gap-2"><Search className="w-4 h-4" /> Search...</span>
            <span className="px-1.5 py-0.5 rounded bg-white/5 font-mono text-[10px]">⌘K</span>
          </button>
        </div>

        <div className="p-4 space-y-8">
          {SIDEBAR_NAV.map((section, idx) => (
            <div key={idx}>
              <h4 className="flex items-center gap-2 text-sm font-bold text-white mb-3">
                <section.icon className="w-4 h-4 text-zinc-500" /> {section.title}
              </h4>
              <div className="flex flex-col space-y-1 pl-6 border-l border-white/5 ml-2">
                {section.links.map((link, lIdx) => {
                  const isActive = pathname === link.href;
                  return (
                    <Link 
                      key={lIdx} 
                      href={link.href}
                      className={	ext-sm py-1.5 px-2 rounded-md transition-colors \}
                    >
                      {link.title}
                    </Link>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 min-w-0 bg-[#050505]">
        <div className="max-w-4xl mx-auto px-6 lg:px-12 py-10 pb-24">
          
          {/* Breadcrumbs */}
          <div className="flex items-center gap-2 text-sm text-zinc-500 mb-8 overflow-x-auto whitespace-nowrap hide-scrollbar">
            <Link href="/docs" className="hover:text-white">Docs</Link>
            <ChevronRight className="w-4 h-4" />
            <span className="text-zinc-300 capitalize">
              {pathname === '/docs' ? 'Introduction' : pathname.split('/').slice(2).join(' / ')}
            </span>
          </div>

          {/* Authenticity Rule Badge */}
          <div className="flex justify-end mb-4">
            <div className="group relative inline-flex">
              <Button disabled variant="outline" className="h-8 text-xs border-white/10 text-zinc-500 bg-transparent gap-2 cursor-not-allowed">
                <Github className="w-3 h-3" /> Edit on GitHub
              </Button>
              <div className="absolute -top-10 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-black border border-yellow-500/50 text-yellow-500 px-3 py-1 text-xs font-bold rounded shadow-xl whitespace-nowrap pointer-events-none">
                Available in v1.0 Release
              </div>
            </div>
          </div>

          {/* Page Content */}
          <article className="prose prose-invert prose-blue max-w-none">
            {children}
          </article>
          
        </div>
      </div>
    </div>
  );
}
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Created docs layout.")
