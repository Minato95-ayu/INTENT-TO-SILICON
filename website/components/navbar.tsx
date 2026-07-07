 
"use client";

import Link from "next/link";
import Image from "next/image";
import { GitBranch, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header className={`fixed top-0 z-50 w-full transition-all duration-300 ${scrolled ? "border-b border-white/10 bg-black/80 backdrop-blur-md" : "bg-transparent"}`}>
      <div className="container mx-auto flex h-16 items-center justify-between px-4 max-w-7xl">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center space-x-3 group">
            <Image src="/aayu-logo.png" alt="AAYU Logo" width={32} height={32} className="object-contain group-hover:scale-110 transition-transform" />
            <span className="font-bold text-xl tracking-tight text-white">AAYU</span>
          </Link>
          <nav className="hidden lg:flex gap-6 text-sm font-medium text-zinc-400">
            <Link href="/language" className="hover:text-white transition-colors">Language</Link>
            <Link href="/brainos" className="hover:text-white transition-colors">BrainOS</Link>
            <Link href="/intent-engine" className="hover:text-white transition-colors">Intent Engine</Link>
            <Link href="/docs" className="hover:text-white transition-colors">Docs</Link>
            <Link href="/packages" className="hover:text-white transition-colors">Packages</Link>
            <Link href="/playground" className="hover:text-white transition-colors">Playground</Link>
            <Link href="/learn" className="hover:text-white text-blue-400 transition-colors">Learn</Link>
          </nav>
        </div>
        <div className="flex items-center gap-4">
          <button className="hidden md:flex items-center gap-2 px-3 py-1.5 text-sm text-zinc-400 bg-white/5 border border-white/10 rounded-md hover:bg-white/10 transition-colors" onClick={() => document.dispatchEvent(new KeyboardEvent('keydown', {'key': 'k', 'ctrlKey': true}))}>
            <Search className="w-4 h-4" />
            <span>Search...</span>
            <kbd className="hidden sm:inline-block ml-2 px-1.5 py-0.5 text-xs font-mono bg-white/10 rounded">Ctrl K</kbd>
          </button>
          <Link href="/download" className="hidden sm:block text-sm font-medium text-zinc-400 hover:text-white transition-colors">
            Download
          </Link>
          <Link href="https://github.com/Minato95-ayu/AAYU" target="_blank" rel="noreferrer">
            <div className="flex h-9 w-9 items-center justify-center rounded-md border border-white/10 hover:bg-white/10 transition-colors">
              <GitBranch className="h-4 w-4 text-white" />
              <span className="sr-only">GitHub</span>
            </div>
          </Link>
          <Link href="/docs/installation">
            <Button className="bg-white text-black hover:bg-zinc-200 hidden sm:flex font-semibold shadow-[0_0_15px_rgba(255,255,255,0.3)]">
              Get Started
            </Button>
          </Link>
        </div>
      </div>
    </header>
  );
}
