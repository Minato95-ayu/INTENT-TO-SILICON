import React from "react";
import Link from "next/link";
import { ArrowLeft, CheckCircle2, Zap, Layers, RefreshCw } from "lucide-react";

export default function ReleaseNotes() {
  return (
    <main className="min-h-screen bg-black text-white pt-24 pb-20">
      <div className="container mx-auto px-4 max-w-4xl">
        <Link href="/" className="inline-flex items-center text-zinc-400 hover:text-white mb-8 transition-colors">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Home
        </Link>
        
        <div className="mb-12">
          <div className="inline-flex items-center gap-2 bg-purple-500/10 text-purple-400 px-3 py-1 rounded-full text-sm font-medium mb-4">
            Release Notes
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4">AAYU v0.7.3 is here</h1>
          <p className="text-xl text-zinc-400">
            The Render Pipeline Stabilization & Diff Engine Update
          </p>
        </div>

        <div className="prose prose-invert max-w-none">
          <p className="text-lg text-zinc-300 mb-8 leading-relaxed">
            We are excited to announce a massive overhaul to AAYU's UI Architecture. 
            Version 0.7.3 introduces a Flutter-style custom render pipeline built entirely from scratch, replacing native widget wrappers with a high-performance drawing engine.
          </p>

          <div className="grid md:grid-cols-2 gap-6 mb-12">
            <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-6">
              <div className="w-10 h-10 bg-blue-500/10 rounded-xl flex items-center justify-center mb-4">
                <Layers className="w-5 h-5 text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Immutable RenderTree</h3>
              <p className="text-zinc-400">
                The VM now emits an immutable RenderTree. Nodes use <code className="text-sm bg-white/5 px-1 rounded">key</code> and <code className="text-sm bg-white/5 px-1 rounded">parent_id</code> to track UI state declaratively, enabling advanced reconciliation.
              </p>
            </div>
            
            <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-6">
              <div className="w-10 h-10 bg-emerald-500/10 rounded-xl flex items-center justify-center mb-4">
                <RefreshCw className="w-5 h-5 text-emerald-400" />
              </div>
              <h3 className="text-xl font-semibold mb-2">V1 Diff Engine</h3>
              <p className="text-zinc-400">
                AAYU now performs a deep diff between the old and new RenderTree. Layout and Paint phases are completely skipped if no changes are detected, saving immense CPU overhead.
              </p>
            </div>

            <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-6">
              <div className="w-10 h-10 bg-orange-500/10 rounded-xl flex items-center justify-center mb-4">
                <Zap className="w-5 h-5 text-orange-400" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Multi-Phase Pipeline</h3>
              <p className="text-zinc-400">
                Separated rendering into distinct phases: Style Resolution ➔ Layout Engine (Caching Dimensions) ➔ Paint Phase ➔ DisplayList generation.
              </p>
            </div>

            <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-6">
              <div className="w-10 h-10 bg-purple-500/10 rounded-xl flex items-center justify-center mb-4">
                <CheckCircle2 className="w-5 h-5 text-purple-400" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Frame Scheduler</h3>
              <p className="text-zinc-400">
                A new 60-FPS Frame Scheduler intercepts the Event Queue to batch multiple state changes into a single render pass.
              </p>
            </div>
          </div>

          <h2 className="text-2xl font-bold mb-4 border-b border-white/10 pb-2">Technical Deep Dive</h2>
          <p className="text-zinc-300 mb-6">
            Previously, AAYU mapped its UI components directly to Tkinter native widgets. While functional, this limited custom visual effects and animation capabilities. 
            By building a custom <strong>DisplayList</strong> and painting it onto a single blank canvas, AAYU now controls every pixel.
          </p>

          <pre className="bg-[#0a0a0a] border border-white/10 rounded-xl p-4 overflow-x-auto text-sm text-zinc-300 mb-8 font-mono">
{`Compiler
   │
Bytecode
   │
VM
   │
State Store
   │
RenderTree (Immutable)
   │
Diff Engine (Reconciliation)
   │
StyleResolver ➔ Layout ➔ Paint
   │
Display List (Drawing Commands)
   │
Renderer (Canvas)`}
          </pre>

          <h2 className="text-2xl font-bold mb-4 border-b border-white/10 pb-2">Try the new Demos</h2>
          <p className="text-zinc-300 mb-6">
            You can verify the new Diff Engine using the updated counter app, or test the declarative UI building blocks with the eCommerce demo.
          </p>
          <pre className="bg-[#0a0a0a] border border-white/10 rounded-xl p-4 overflow-x-auto text-sm text-zinc-300 mb-8 font-mono">
{`# Run the counter app to test state diffing
python -m tools.cli run examples/counter.aayu --renderer desktop

# Run the ecommerce layout
python -m tools.cli run examples/ecommerce.aayu --renderer desktop`}
          </pre>
        </div>
      </div>
    </main>
  );
}
