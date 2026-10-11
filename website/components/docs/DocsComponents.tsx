/* eslint-disable */

"use client";

import { useState } from "react";
import { CheckCircle2, Copy, Play, ArrowRight } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export function CodeBlock({ code, lang = "aayu", playgroundUrl }: { code: string, lang?: string, playgroundUrl?: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code.trim());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="my-6 rounded-xl overflow-hidden bg-[#111] border border-white/10 group">
      <div className="flex items-center justify-between px-4 py-2 bg-[#0a0a0a] border-b border-white/5">
        <span className="text-xs font-mono text-zinc-500 uppercase">{lang}</span>
        <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <button onClick={handleCopy} className="flex items-center gap-1.5 text-xs text-zinc-400 hover:text-white transition-colors bg-white/5 px-2 py-1 rounded">
            {copied ? <CheckCircle2 className="w-3.5 h-3.5 text-green-500" /> : <Copy className="w-3.5 h-3.5" />}
            {copied ? "Copied" : "Copy"}
          </button>
          {playgroundUrl && (
            <Link href={playgroundUrl}>
              <button className="flex items-center gap-1.5 text-xs text-blue-400 hover:text-blue-300 transition-colors bg-blue-500/10 border border-blue-500/20 px-2 py-1 rounded">
                <Play className="w-3.5 h-3.5 fill-current" /> Run
              </button>
            </Link>
          )}
        </div>
      </div>
      <div className="p-4 overflow-x-auto">
        <pre className="text-sm font-mono text-zinc-300 whitespace-pre">
          {code.trim()}
        </pre>
      </div>
    </div>
  );
}

export function ErrorBlock({ wrong, correct, errorMsg }: { wrong: string, correct: string, errorMsg: string }) {
  return (
    <div className="my-8 grid md:grid-cols-2 gap-4">
      <div className="rounded-xl border border-red-500/20 bg-red-500/5 overflow-hidden">
        <div className="px-4 py-2 bg-red-500/10 border-b border-red-500/20 text-xs font-bold text-red-400 flex items-center gap-2">
          <span>❌ Wrong</span>
        </div>
        <div className="p-4">
          <pre className="text-sm font-mono text-zinc-300 whitespace-pre">{wrong.trim()}</pre>
        </div>
        <div className="px-4 py-3 bg-[#0a0a0a] border-t border-white/5">
          <div className="text-xs font-mono text-red-400">Compiler Error:</div>
          <div className="text-sm text-zinc-400 mt-1">{errorMsg}</div>
        </div>
      </div>

      <div className="rounded-xl border border-green-500/20 bg-green-500/5 overflow-hidden">
        <div className="px-4 py-2 bg-green-500/10 border-b border-green-500/20 text-xs font-bold text-green-400 flex items-center gap-2">
          <span>✅ Correct</span>
        </div>
        <div className="p-4">
          <pre className="text-sm font-mono text-zinc-300 whitespace-pre">{correct.trim()}</pre>
        </div>
        <div className="px-4 py-3 bg-[#0a0a0a] border-t border-white/5 flex items-center h-[70px]">
          <div className="text-sm text-green-400">Compiles successfully.</div>
        </div>
      </div>
    </div>
  );
}

export function PipelineDiagram({ stages }: { stages: string[] }) {
  return (
    <div className="my-8 p-6 bg-[#0a0a0a] border border-white/10 rounded-xl overflow-x-auto flex flex-col md:flex-row items-center gap-2">
      {stages.map((stage, i) => (
        <div key={i} className="flex flex-col md:flex-row items-center gap-2 shrink-0">
          <div className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-sm font-bold text-zinc-300">
            {stage}
          </div>
          {i < stages.length - 1 && (
            <>
              <ArrowRight className="w-5 h-5 text-zinc-600 hidden md:block" />
              <div className="w-px h-6 bg-zinc-700 md:hidden" />
            </>
          )}
        </div>
      ))}
    </div>
  );
}

export function PageNav({ prev, next }: { prev?: {title: string, href: string}, next?: {title: string, href: string} }) {
  return (
    <div className="mt-16 pt-8 border-t border-white/10 flex items-center justify-between">
      {prev ? (
        <Link href={prev.href} className="group flex flex-col gap-1">
          <span className="text-xs text-zinc-500 font-bold uppercase tracking-wider">Previous</span>
          <span className="text-blue-400 group-hover:text-blue-300 font-medium transition-colors">← {prev.title}</span>
        </Link>
      ) : <div />}
      
      {next ? (
        <Link href={next.href} className="group flex flex-col items-end gap-1">
          <span className="text-xs text-zinc-500 font-bold uppercase tracking-wider">Next</span>
          <span className="text-blue-400 group-hover:text-blue-300 font-medium transition-colors">{next.title} →</span>
        </Link>
      ) : <div />}
    </div>
  );
}
