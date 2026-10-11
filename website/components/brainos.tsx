/* eslint-disable */
"use client";

import { motion } from "framer-motion";
import { Brain, Sparkles, Workflow, Activity } from "lucide-react";

export function BrainOS() {
  return (
    <section id="brainos" className="py-24 border-t border-white/5 relative bg-zinc-950">
      <div className="absolute top-0 right-0 w-1/2 h-full opacity-10 pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-l from-purple-500/50 to-transparent blur-[100px]" />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          
          <div>
            <div className="inline-flex items-center rounded-full border border-purple-500/30 bg-purple-500/10 px-3 py-1 text-sm text-purple-300 mb-6 backdrop-blur">
              <Brain className="w-4 h-4 mr-2" />
              The Software Engineering OS
            </div>
            
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white leading-tight">
              BrainOS is your <br />
              Autonomous Engineer.
            </h2>
            
            <p className="text-lg text-zinc-400 mb-8 leading-relaxed">
              While AAYU handles the architecture, BrainOS manages the entire lifecycle. It plans, builds, verifies, and criticizes its own work until your intent is fully realized.
            </p>
            
            <div className="space-y-6">
              {[
                { title: "Planner", desc: "Breaks down human intent into a determinable DAG." },
                { title: "Executor", desc: "Writes deterministic AAYU code and builds the architecture." },
                { title: "Critic", desc: "Reviews the snapshot and auto-fixes any deviations from intent." },
              ].map((item, i) => (
                <div key={i} className="flex gap-4">
                  <div className="w-8 h-8 rounded-full bg-white/5 border border-white/10 flex items-center justify-center shrink-0 text-purple-400">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-zinc-200">{item.title}</h4>
                    <p className="text-sm text-zinc-500">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div className="relative">
            <motion.div
              initial={{ opacity: 0, rotateX: 20, y: 20 }}
              whileInView={{ opacity: 1, rotateX: 0, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              className="rounded-2xl border border-white/10 bg-black/60 backdrop-blur-xl p-8 shadow-2xl shadow-purple-500/10"
              style={{ transformPerspective: 1000 }}
            >
              <div className="flex flex-col gap-4">
                {["Task Graph", "Executor", "Critic", "Impact", "Snapshot"].map((step, i) => (
                  <div key={step} className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-xl bg-purple-500/20 border border-purple-500/30 flex items-center justify-center text-purple-400 shrink-0">
                      <Workflow className="w-5 h-5" />
                    </div>
                    <div className="flex-1 h-12 rounded-xl bg-white/5 border border-white/5 flex items-center px-4 relative overflow-hidden">
                      <motion.div 
                        initial={{ width: 0 }}
                        whileInView={{ width: "100%" }}
                        transition={{ delay: i * 0.2, duration: 0.8 }}
                        className="absolute inset-y-0 left-0 bg-purple-500/10"
                      />
                      <span className="text-sm font-medium text-zinc-300 relative z-10">{step}</span>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>
          
        </div>
      </div>
    </section>
  );
}
