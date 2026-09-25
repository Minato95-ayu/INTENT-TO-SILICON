 
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
                    <nav className="hidden lg:flex gap-6 text-sm font-medium text-zinc-400 items-center">
            <Link href="/" className="hover:text-white transition-colors">Home</Link>
            <Link href="/docs" className="hover:text-white transition-colors">Documentation</Link>
            <Link href="/docs#ch9" className="hover:text-white transition-colors">Examples</Link>
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
          <Link href="https://github.com/Minato95-ayu/INTENT-TO-SILICON" target="_blank" rel="noreferrer">
            <div className="flex h-9 w-9 items-center justify-center rounded-md border border-white/10 hover:bg-white/10 transition-colors">
              <GitBranch className="h-4 w-4 text-white" />
              <span className="sr-only">GitHub</span>
            </div>
          </Link>
          <Link href="https://github.com/Minato95-ayu/INTENT-TO-SILICON" target="_blank">
            <Button className="bg-white text-black hover:bg-zinc-200 hidden sm:flex font-semibold shadow-[0_0_15px_rgba(255,255,255,0.3)]">
              View on GitHub
            </Button>
          </Link>
        </div>
      </div>
    </header>
  );
}
