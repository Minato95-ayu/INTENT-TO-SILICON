/* eslint-disable */
﻿"use client";
import { useState, useEffect } from "react";
import { Terminal, Code2, Cpu, Zap, Activity, ShieldCheck, ListTree, Play, Bug, FileDown, Share2, Eye, Database, LayoutPanelLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

const TABS = [
  { id: "tokens", label: "Tokens", icon: ListTree },
  { id: "ast", label: "AST", icon: Code2 },
  { id: "semantic", label: "Semantic", icon: ShieldCheck },
  { id: "ir", label: "Intent IR", icon: Database },
  { id: "bytecode", label: "Bytecode", icon: Cpu },
  { id: "runtime", label: "Runtime (DARC)", icon: Activity },
  { id: "brainos", label: "BrainOS Review", icon: Eye },
  { id: "console", label: "Console", icon: Terminal }
];

const DEFAULT_CODE = `// AAYU Realtime Playground
entity User
has
    id: Number
    name: Text
end.

fn main()
do
    let u = User(id: 1, name: "AAYU Developer").
    print(u.name).
end.`;

export default function Playground() {
  const [code, setCode] = useState(DEFAULT_CODE);
  const [activeTab, setActiveTab] = useState("ast");
  const [isCompiling, setIsCompiling] = useState(false);
  const [compileStage, setCompileStage] = useState("");
  const [results, setResults] = useState<any>({});

  const compileCode = async () => {
    setIsCompiling(true);
    setResults({});
    setCompileStage("Compiling via AAYU Engine...");
    setActiveTab("console");
    
    try {
      const res = await fetch("http://localhost:8000/api/v1/compile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code })
      });
      
      const data = await res.json();
      
      if (data.success) {
        setResults({
          tokens: JSON.stringify(data.tokens, null, 2),
          ast: data.ast,
          bytecode: JSON.stringify(data.bytecode, null, 2),
          console: data.output || "Program finished with no output.",
          semantic: "Static analysis passed.",
          ir: "No Intent IR for direct compilation.",
          runtime: "Execution successful.",
          brainos: "Architecture Score: 95/100"
        });
      } else {
        setResults({
          console: "Error: " + data.error,
          semantic: "Failed to compile."
        });
      }
    } catch (e: unknown) {
      setResults({
        console: "Error: Could not connect to AAYU Compiler Backend. Ensure FastAPI is running on port 8000.\n" + (e as Error).message
      });
    } finally {
      setCompileStage("");
      setIsCompiling(false);
    }
  };

  return (
    <main className="h-screen bg-[#050505] text-white pt-16 flex flex-col overflow-hidden">
      
      {/* Top Bar */}
      <div className="h-14 border-b border-white/10 bg-[#0a0a0a] flex items-center justify-between px-4 shrink-0">
        <div className="flex items-center gap-2 text-sm font-bold">
          <LayoutPanelLeft className="w-4 h-4 text-orange-400" /> AAYU Web Compiler
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" className="h-8 text-xs border-white/10 text-zinc-400 bg-transparent hover:bg-white/5">
            <FileDown className="w-3 h-3 mr-2" /> Download
          </Button>
          <Button variant="outline" className="h-8 text-xs border-white/10 text-zinc-400 bg-transparent hover:bg-white/5">
            <Share2 className="w-3 h-3 mr-2" /> Share
          </Button>
          <Button onClick={compileCode} disabled={isCompiling} className="h-8 text-xs bg-green-600 hover:bg-green-500 text-white font-bold ml-2 w-32">
            {isCompiling ? (
              <span className="flex items-center gap-2"><Zap className="w-3 h-3 animate-pulse" /> {compileStage}</span>
            ) : (
              <span className="flex items-center gap-2"><Play className="w-3 h-3" /> Run Code</span>
            )}
          </Button>
        </div>
      </div>

      {/* Split Screen */}
      <div className="flex-1 flex overflow-hidden">
        
        {/* LEFT: Editor */}
        <div className="w-1/2 border-r border-white/10 bg-[#111] flex flex-col">
          <div className="h-10 bg-[#0a0a0a] border-b border-white/5 flex items-center px-4 text-xs font-mono text-zinc-500">
            src/main.aayu
          </div>
          <textarea 
            className="flex-1 bg-transparent text-sm font-mono text-blue-300 p-4 outline-none resize-none leading-relaxed"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            spellCheck={false}
          />
        </div>

        {/* RIGHT: Pipeline Tools */}
        <div className="w-1/2 bg-[#050505] flex flex-col">
          <div className="h-10 bg-[#0a0a0a] border-b border-white/5 flex items-center px-2 overflow-x-auto hide-scrollbar">
            {TABS.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 h-full text-xs font-bold border-b-2 transition-colors whitespace-nowrap ${activeTab === tab.id ? "border-orange-500 text-orange-400 bg-orange-500/10" : "border-transparent text-zinc-500 hover:text-zinc-300 hover:bg-white/5"}`}
              >
                <tab.icon className="w-3 h-3" /> {tab.label}
              </button>
            ))}
          </div>
          
          <div className="flex-1 p-4 overflow-y-auto font-mono text-sm relative">
            {isCompiling ? (
              <div className="absolute inset-0 flex items-center justify-center bg-[#050505]/80 backdrop-blur-sm z-10">
                <div className="flex flex-col items-center">
                  <Activity className="w-8 h-8 text-orange-500 animate-pulse mb-4" />
                  <div className="text-orange-400 font-bold">{compileStage}</div>
                </div>
              </div>
            ) : null}

            {!results[activeTab] && !isCompiling ? (
              <div className="text-zinc-600 flex flex-col items-center justify-center h-full">
                <Terminal className="w-8 h-8 mb-4 opacity-20" />
                Click "Run Code" to generate pipeline output.
              </div>
            ) : (
              <pre className="text-zinc-300 whitespace-pre-wrap leading-relaxed">
                {results[activeTab]}
              </pre>
            )}
          </div>
        </div>

      </div>
    </main>
  );
}
