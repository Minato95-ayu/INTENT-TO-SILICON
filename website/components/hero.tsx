 
"use client";

import { motion } from "framer-motion";
import { ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";

const pipelineSteps = [
  { label: "Human Thought", icon: "?", color: "text-blue-400", border: "border-blue-500/30" },
  { label: "Intent Engine", icon: "⚙️", color: "text-purple-400", border: "border-purple-500/30" },
  { label: "BrainOS", icon: "🧠", color: "text-red-400", border: "border-red-500/30" },
  { label: "AAYU Language", icon: "📝", color: "text-zinc-300", border: "border-zinc-500/30" },
  { label: "Compiler", icon: "⚡", color: "text-zinc-300", border: "border-zinc-500/30" },
  { label: "Runtime", icon: "🚀", color: "text-green-400", border: "border-green-500/30" },
  { label: "Production Software", icon: "✅", color: "text-emerald-400", border: "border-emerald-500/30" }
];

export function Hero() {
  return (
    <section className="relative overflow-hidden pt-24 pb-32 lg:pt-36 lg:pb-40">
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[500px] opacity-30 pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/30 to-purple-500/30 blur-[100px] rounded-full mix-blend-screen" />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="flex flex-col gap-6"
          >
            <div className="inline-flex items-center rounded-full border border-white/10 bg-white/5 px-3 py-1 text-sm text-zinc-300 w-max backdrop-blur-sm">
              <span className="flex h-2 w-2 rounded-full bg-blue-500 mr-2 animate-pulse"></span>
              AAYU v1.0 is coming soon
            </div>
            
            <h1 className="text-5xl lg:text-7xl font-extrabold tracking-tight text-white leading-[1.1]">
              Built for <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600">
                Human Intent.
              </span>
            </h1>
            
            <p className="text-lg text-zinc-400 max-w-xl leading-relaxed">
              Write less. Build more. A modern programming language designed to be simple, fast, offline-first, and inherently AI-native.
            </p>
            
            <div className="flex flex-wrap items-center gap-4 pt-4">
              <Button size="lg" className="bg-white text-black hover:bg-zinc-200 h-12 px-8 text-base">
                Get Started
                <ChevronRight className="ml-2 h-4 w-4" />
              </Button>
              <Button size="lg" variant="outline" className="h-12 px-8 text-base border-white/10 hover:bg-white/5 bg-transparent">
                Documentation
              </Button>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
            className="relative"
          >
            <div className="rounded-xl border border-white/10 bg-black/40 backdrop-blur-xl overflow-hidden shadow-2xl shadow-blue-500/10">
              <div className="flex items-center px-4 py-3 border-b border-white/10 bg-white/5">
                <div className="flex space-x-2">
                  <div className="w-3 h-3 rounded-full bg-red-500/80" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                  <div className="w-3 h-3 rounded-full bg-green-500/80" />
                </div>
                <div className="mx-auto text-xs text-zinc-500 font-mono">main.aayu</div>
              </div>
              <div className="p-6 overflow-x-auto">
                <div className="flex flex-col gap-3">
                  {pipelineSteps.map((step, idx) => (
                    <motion.div 
                      key={idx}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.15 + 0.5 }}
                      className={`flex items-center gap-3 p-3 rounded-lg border ${step.border} bg-black/50`}
                    >
                      <span className="text-lg">{step.icon}</span>
                      <span className={`font-mono text-sm font-medium ${step.color}`}>{step.label}</span>
                      {idx < pipelineSteps.length - 1 && (
                        <div className="ml-auto text-zinc-600">↓</div>
                      )}
                    </motion.div>
                  ))}
                </div>
              </div>
              <div className="border-t border-white/10 bg-zinc-900/50 p-4 font-mono text-xs text-zinc-400">
                <div className="flex items-center gap-2">
                  <span className="text-green-400">➜</span> 
                  <span className="typing-animation">aayu build --autonomous</span>
                </div>
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 2, duration: 0.5 }}
                  className="mt-2 text-zinc-500"
                >
                  [✓] Architecture generated. Production ready in 45ms.
                </motion.div>
              </div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
}
