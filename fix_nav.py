content = '''"use client";

import Link from "next/link";
import Image from "next/image";
import { GitBranch, Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header className={ixed top-0 z-50 w-full transition-all duration-300 \}>
      <div className="container mx-auto flex h-16 items-center justify-between px-4 max-w-7xl">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center space-x-3 group">
            <Image src="/aayu-logo.png" alt="AAYU Logo" width={32} height={32} className="object-contain group-hover:scale-110 transition-transform" />
            <span className="font-bold text-xl tracking-tight text-white">AAYU</span>
          </Link>
          <nav className="hidden lg:flex gap-6 text-sm font-medium text-zinc-400 items-center">
            <Link href="/" className="hover:text-white transition-colors">Home</Link>
            <Link href="/docs" className="hover:text-white transition-colors">Documentation</Link>
            <Link href="/tutorial" className="hover:text-white transition-colors text-purple-400 font-bold">Tutorial</Link>
            <Link href="/examples" className="hover:text-white transition-colors">Examples</Link>
            <Link href="/download" className="hover:text-white transition-colors flex items-center gap-1">
              <span className="relative flex h-2 w-2 mr-1">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
              </span>
              Download
            </Link>
          </nav>
        </div>
        <div className="flex items-center gap-4">
          <Link href="https://github.com/Minato95-ayu/INTENT-TO-SILICON" target="_blank" rel="noreferrer" className="hidden sm:flex">
            <div className="flex h-9 w-9 items-center justify-center rounded-md border border-white/10 hover:bg-white/10 transition-colors">
              <GitBranch className="h-4 w-4 text-white" />
              <span className="sr-only">GitHub</span>
            </div>
          </Link>
          <Link href="https://github.com/Minato95-ayu/INTENT-TO-SILICON" target="_blank" className="hidden sm:flex">
            <Button className="bg-white text-black hover:bg-zinc-200 hidden sm:flex font-semibold shadow-[0_0_15px_rgba(255,255,255,0.3)]">
              View on GitHub
            </Button>
          </Link>
          <button 
            className="lg:hidden text-zinc-400 hover:text-white p-2"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>
      
      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="lg:hidden bg-black/95 border-b border-white/10 px-4 py-6 flex flex-col gap-6 text-base font-medium">
          <Link href="/" onClick={() => setMobileMenuOpen(false)} className="text-zinc-400 hover:text-white transition-colors block">Home</Link>
          <Link href="/docs" onClick={() => setMobileMenuOpen(false)} className="text-zinc-400 hover:text-white transition-colors block">Documentation</Link>
          <Link href="/tutorial" onClick={() => setMobileMenuOpen(false)} className="text-purple-400 font-bold hover:text-purple-300 transition-colors block">Tutorial</Link>
          <Link href="/examples" onClick={() => setMobileMenuOpen(false)} className="text-zinc-400 hover:text-white transition-colors block">Examples</Link>
          <Link href="/download" onClick={() => setMobileMenuOpen(false)} className="text-zinc-400 hover:text-white transition-colors flex items-center gap-2">
            <span className="relative flex h-2 w-2 mr-1">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
            </span>
            Download AAYU
          </Link>
          <div className="pt-4 border-t border-zinc-800 flex flex-col gap-4">
            <Link href="https://github.com/Minato95-ayu/INTENT-TO-SILICON" target="_blank" className="flex items-center gap-2 text-zinc-400 hover:text-white">
              <GitBranch className="h-5 w-5" />
              GitHub Repository
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
'''
with open('D:/INTENT-TO-SILICON/website/components/navbar.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
