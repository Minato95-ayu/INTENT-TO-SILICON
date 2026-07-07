 
"use client";

import { motion } from "framer-motion";
import { Zap, Shield, Cpu, Package, LayoutTemplate, Bug, Wrench, Search, Code, Brain } from "lucide-react";

const features = [
  { name: "Compiler", icon: <Cpu className="h-5 w-5" />, desc: "Fast multi-pass native compiler architecture." },
  { name: "Runtime", icon: <Zap className="h-5 w-5" />, desc: "High-performance stack-based virtual machine." },
  { name: "Package Manager", icon: <Package className="h-5 w-5" />, desc: "Offline-first dependency resolution." },
  { name: "Type System", icon: <Shield className="h-5 w-5" />, desc: "Strong structural typing and generics." },
  { name: "Debugger", icon: <Bug className="h-5 w-5" />, desc: "Native step-through debugging tools." },
  { name: "Formatter", icon: <LayoutTemplate className="h-5 w-5" />, desc: "Idempotent, canonical code formatting." },
  { name: "Linter", icon: <Wrench className="h-5 w-5" />, desc: "Strict static analysis for code quality." },
  { name: "Reflection", icon: <Search className="h-5 w-5" />, desc: "Runtime type introspection." },
  { name: "Standard Library", icon: <Code className="h-5 w-5" />, desc: "Comprehensive batteries-included stdlib." },
  { name: "BrainOS Ready", icon: <Brain className="h-5 w-5" />, desc: "Native integration with the Intent Engine." },
];

export function Features() {
  return (
    <section id="features" className="py-24 border-t border-white/5 relative bg-zinc-950/50">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">A complete ecosystem</h2>
          <p className="text-zinc-400">Everything you need to build production software, built directly into the language.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {features.map((feature, i) => (
            <motion.div
              key={feature.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05, duration: 0.5 }}
              className="group relative p-6 rounded-2xl border border-white/5 bg-white/[0.02] hover:bg-white/[0.04] transition-colors"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl" />
              <div className="relative z-10">
                <div className="w-10 h-10 rounded-lg bg-zinc-900 border border-white/10 flex items-center justify-center text-zinc-300 mb-4 group-hover:text-blue-400 transition-colors">
                  {feature.icon}
                </div>
                <h3 className="font-semibold text-zinc-100 mb-2">{feature.name}</h3>
                <p className="text-sm text-zinc-500">{feature.desc}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
