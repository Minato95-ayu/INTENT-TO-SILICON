 
"use client";

import { motion } from "framer-motion";

const steps = ["Human", "Intent", "BrainOS", "Architecture", "AAYU", "Compiler", "Bytecode", "Runtime"];

export function Architecture() {
  return (
    <section className="py-24 border-t border-white/5 overflow-hidden">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">How it works</h2>
          <p className="text-zinc-400">From pure thought to production software in a unified flow.</p>
        </div>

        <div className="flex flex-wrap items-center justify-center gap-4 md:gap-8 max-w-6xl mx-auto">
          {steps.map((step, i) => (
            <div key={step} className="flex items-center">
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1, type: "spring" }}
                className="px-6 py-3 rounded-full border border-white/10 bg-white/5 backdrop-blur font-medium text-sm text-zinc-300 shadow-[0_0_15px_rgba(255,255,255,0.05)]"
              >
                {step}
              </motion.div>
              
              {i < steps.length - 1 && (
                <motion.div
                  initial={{ opacity: 0, width: 0 }}
                  whileInView={{ opacity: 1, width: "auto" }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 + 0.1 }}
                  className="hidden md:block mx-4 text-blue-500/50"
                >
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M5 12h14"></path>
                    <path d="m12 5 7 7-7 7"></path>
                  </svg>
                </motion.div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
