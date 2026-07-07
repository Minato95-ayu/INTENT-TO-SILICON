"""
=============================================================================
FILE: create_compiler_pipeline.py
PURPOSE: Sets up the compilation pipeline
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles sets up the compilation pipeline.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os

base_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\features\compiler'
os.makedirs(base_dir, exist_ok=True)

compiler_code = '''
"use client";

import { useState } from "react";
import { ArrowDown, Code, Brain, FileJson, Cpu, Zap, Settings, PlayCircle } from "lucide-react";
import Link from "next/link";

const PIPELINE = [
  { id: "source", label: "Source Code", icon: Code, desc: "AAYU text files (.aayu)" },
  { id: "lexer", label: "Lexer", icon: FileJson, desc: "Tokenization" },
  { id: "parser", label: "Parser", icon: Settings, desc: "Syntax analysis" },
  { id: "ast", label: "AST", icon: FileJson, desc: "Abstract Syntax Tree" },
  { id: "semantic", label: "Semantic Analysis", icon: Brain, desc: "Type checking & intent validation" },
  { id: "optimizer", label: "Optimizer", icon: Zap, desc: "Dead code elimination & loop unrolling" },
  { id: "bytecode", label: "Bytecode", icon: Cpu, desc: "AAYU IR generation" },
  { id: "runtime", label: "Runtime", icon: PlayCircle, desc: "VM execution with deterministic ARC" }
];

export default function CompilerPipelinePage() {
  const [activeStep, setActiveStep] = useState(0);

  return (
    <main className="min-h-screen bg-black text-white pt-24 pb-20">
      <div className="container mx-auto px-4 max-w-5xl">
        <div className="mb-16 text-center">
          <Link href="/language" className="text-sm text-blue-400 hover:text-blue-300 mb-4 inline-block">&larr; Back to Language Portal</Link>
          <h1 className="text-4xl font-extrabold mb-4">Interactive Compiler Pipeline</h1>
          <p className="text-zinc-400 text-lg max-w-2xl mx-auto">Explore how AAYU transforms your high-level human intent into heavily optimized, safe machine code.</p>
        </div>

        <div className="grid md:grid-cols-2 gap-12 items-center">
          
          {/* Interactive Flow Diagram */}
          <div className="flex flex-col items-center">
            {PIPELINE.map((step, index) => (
              <div key={step.id} className="flex flex-col items-center w-full">
                <button 
                  onClick={() => setActiveStep(index)}
                  className={w-64 p-4 rounded-xl border transition-all duration-300 flex items-center gap-4 shadow-lg \}
                >
                  <div className={p-2 rounded-lg \}>
                    <step.icon className="w-5 h-5" />
                  </div>
                  <div className="text-left">
                    <div className="font-bold">{step.label}</div>
                  </div>
                </button>
                
                {index < PIPELINE.length - 1 && (
                  <div className={h-8 w-px my-2 transition-colors \} />
                )}
              </div>
            ))}
          </div>

          {/* Details Panel */}
          <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-8 sticky top-32">
            <h2 className="text-2xl font-bold mb-2 text-blue-400 flex items-center gap-3">
              {(() => {
                const Icon = PIPELINE[activeStep].icon;
                return <Icon className="w-6 h-6" />;
              })()}
              {PIPELINE[activeStep].label}
            </h2>
            <p className="text-zinc-400 text-lg mb-6">{PIPELINE[activeStep].desc}</p>
            
            <div className="bg-black border border-white/5 rounded-lg p-6 font-mono text-sm text-zinc-300">
              {activeStep === 0 && <p>// Raw input file defined by user<br/>entity User has name: Text end.</p>}
              {activeStep === 1 && <p>[TOKEN_ENTITY, TOKEN_IDENT(User), TOKEN_HAS, ...]</p>}
              {activeStep === 2 && <p>Checking grammar rules... OK</p>}
              {activeStep === 3 && <pre>{"{\\n  type: 'Entity',\\n  name: 'User'\\n}"}</pre>}
              {activeStep === 4 && <p>Type checking... OK<br/>Intent extraction... OK</p>}
              {activeStep === 5 && <p>Pass: inline_functions... OK<br/>Pass: memory_arc_inject... OK</p>}
              {activeStep === 6 && <p>Opcode: ALLOC User<br/>Opcode: STORE_REF</p>}
              {activeStep === 7 && <p>Executing on AAYU VM.<br/>Memory managed by Deterministic ARC.</p>}
            </div>

            <div className="mt-8 pt-6 border-t border-white/10 flex justify-between">
              <Button 
                variant="outline" 
                onClick={() => setActiveStep(prev => Math.max(0, prev - 1))}
                disabled={activeStep === 0}
                className="border-white/10 text-white bg-transparent hover:bg-white/5"
              >
                Previous Stage
              </Button>
              <Button 
                onClick={() => setActiveStep(prev => Math.min(PIPELINE.length - 1, prev + 1))}
                disabled={activeStep === PIPELINE.length - 1}
                className="bg-white text-black hover:bg-zinc-200"
              >
                Next Stage
              </Button>
            </div>
          </div>

        </div>
      </div>
    </main>
  );
}
'''

with open(os.path.join(base_dir, 'page.tsx'), 'w', encoding='utf-8') as f:
    f.write(compiler_code)

print("Created Interactive Compiler Pipeline.")
