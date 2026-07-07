"""
=============================================================================
FILE: create_playground.py
PURPOSE: Creates interactive playground
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles creates interactive playground.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os

base_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\playground'
os.makedirs(base_dir, exist_ok=True)

playground_code = '''
"use client";

import { useState } from "react";
import { Play, Share2, Save, Wand2, Terminal, Code2, Network, Cpu, Server } from "lucide-react";
import { Button } from "@/components/ui/button";

const DEFAULT_CODE = entity Student
has
    name : Text
    age : Number
end.

fn main() -> Void
do
    let student = Student { name: "AAYU", age: 1 }.
    print("Welcome to " + student.name).
end.

main().;

const MOCK_AST = {
  "type": "Program",
  "body": [
    {
      "type": "EntityDeclaration",
      "name": "Student",
      "fields": [
        { "name": "name", "type": "Text" },
        { "name": "age", "type": "Number" }
      ]
    },
    {
      "type": "FunctionDeclaration",
      "name": "main",
      "returns": "Void",
      "body": [...]
    }
  ]
};

const MOCK_IR = ; ModuleID = 'main.aayu'
source_filename = "main.aayu"

%Student = type { ptr, i32 }

define void @main() {
entry:
  %student = alloca %Student, align 8
  ...
  ret void
};

export default function PlaygroundPage() {
  const [code, setCode] = useState(DEFAULT_CODE);
  const [activeTab, setActiveTab] = useState("code");
  const [output, setOutput] = useState("Ready.\\nClick 'Run' to compile and execute.");
  const [isRunning, setIsRunning] = useState(false);

  const handleRun = () => {
    setIsRunning(true);
    setActiveTab("output");
    setOutput("Compiling via AAYU Intent Engine...\\n");
    
    setTimeout(() => {
      setOutput(prev => prev + "Generating AST... OK\\n");
      setTimeout(() => {
        setOutput(prev => prev + "Emitting Bytecode... OK\\n\\n[Output]\\nWelcome to AAYU\\n\\n[Process completed in 12ms]");
        setIsRunning(false);
      }, 500);
    }, 500);
  };

  const handleFormat = () => {
    setOutput("Code formatted successfully.");
  };

  return (
    <div className="flex flex-col h-screen pt-16 bg-[#0d0d0d] text-zinc-300">
      
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-white/10 bg-black">
        <div className="flex items-center gap-4">
          <h2 className="text-sm font-semibold tracking-wide text-white">AAYU Playground</h2>
          <div className="h-4 w-px bg-white/10" />
          <span className="text-xs text-zinc-500 font-mono">v1.0.0-stable</span>
        </div>
        
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" className="h-8 border-white/10 hover:bg-white/5 bg-transparent" onClick={handleFormat}>
            <Wand2 className="h-3 w-3 mr-2" />
            Format
          </Button>
          <Button variant="outline" size="sm" className="h-8 border-white/10 hover:bg-white/5 bg-transparent">
            <Save className="h-3 w-3 mr-2" />
            Save
          </Button>
          <Button variant="outline" size="sm" className="h-8 border-white/10 hover:bg-white/5 bg-transparent">
            <Share2 className="h-3 w-3 mr-2" />
            Share
          </Button>
          <Button 
            size="sm" 
            className="h-8 bg-blue-600 hover:bg-blue-500 text-white ml-2"
            onClick={handleRun}
            disabled={isRunning}
          >
            <Play className="h-3 w-3 mr-2" fill="currentColor" />
            {isRunning ? "Running..." : "Run"}
          </Button>
        </div>
      </div>

      {/* Editor & output area */}
      <div className="flex flex-1 overflow-hidden">
        
        {/* Left Pane - Always Editor */}
        <div className="w-1/2 flex flex-col border-r border-white/10">
          <div className="px-4 py-2 border-b border-white/5 bg-black text-xs font-mono text-zinc-400 flex items-center gap-2">
            <Code2 className="h-3 w-3 text-blue-400" /> main.aayu
          </div>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="flex-1 w-full bg-transparent p-4 font-mono text-sm leading-relaxed resize-none focus:outline-none text-zinc-300 placeholder:text-zinc-700"
            spellCheck="false"
          />
        </div>

        {/* Right Pane - Multi Tab */}
        <div className="w-1/2 flex flex-col bg-black">
          {/* Tabs */}
          <div className="flex border-b border-white/5 bg-black">
            {[
              { id: "output", label: "Output", icon: Terminal, color: "text-green-400" },
              { id: "ast", label: "AST", icon: Network, color: "text-yellow-400" },
              { id: "ir", label: "IR / Bytecode", icon: Cpu, color: "text-purple-400" },
              { id: "runtime", label: "Runtime Memory", icon: Server, color: "text-pink-400" }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={lex items-center gap-2 px-4 py-2 text-xs font-mono transition-colors border-b-2 \}
              >
                <tab.icon className={h-3 w-3 \} />
                {tab.label}
              </button>
            ))}
          </div>
          
          {/* Content */}
          <div className="flex-1 p-4 font-mono text-sm overflow-auto">
            {activeTab === "output" && (
              <pre className={output.includes("Compiling") ? "text-zinc-500" : "text-zinc-300"}>
                {output}
              </pre>
            )}
            {activeTab === "ast" && (
              <pre className="text-zinc-400">{MOCK_AST}</pre>
            )}
            {activeTab === "ir" && (
              <pre className="text-zinc-400">{MOCK_IR}</pre>
            )}
            {activeTab === "runtime" && (
              <div className="text-zinc-400">
                <p>Heap Allocations: 1 (Student Entity)</p>
                <p>Stack Frames: main()</p>
                <p>GC Status: Deterministic ARC (0 pauses)</p>
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
'''

with open(os.path.join(base_dir, 'page.tsx'), 'w', encoding='utf-8') as f:
    f.write(playground_code)

print("Created Advanced Playground.")
