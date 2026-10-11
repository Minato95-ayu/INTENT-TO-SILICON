 
"use client";

import { motion } from "framer-motion";

export function WhyAayu() {
  return (
    <section id="why-aayu" className="py-24 border-t border-white/5">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">Why AAYU?</h2>
          <p className="text-zinc-400">The first language built from the ground up for the AI generation.</p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="p-8 rounded-2xl border border-red-500/20 bg-red-500/5"
          >
            <h3 className="text-xl font-semibold text-zinc-300 mb-6 flex items-center">
              <span className="text-red-400 mr-2">✗</span> Traditional Languages
            </h3>
            <ul className="space-y-4 text-zinc-500">
              <li>• Heavy boilerplate and configuration</li>
              <li>• Complex syntax overhead</li>
              <li>• AI is treated as an afterthought</li>
              <li>• Slow development cycle</li>
              <li>• Cloud-dependent tooling</li>
            </ul>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="p-8 rounded-2xl border border-blue-500/30 bg-blue-500/10 relative overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-purple-500/10" />
            <div className="relative z-10">
              <h3 className="text-xl font-semibold text-zinc-100 mb-6 flex items-center">
                <span className="text-blue-400 mr-2">✓</span> AAYU
              </h3>
              <ul className="space-y-4 text-zinc-300">
                <li className="flex items-center"><span className="text-blue-400 mr-2">✓</span> Human readable syntax</li>
                <li className="flex items-center"><span className="text-blue-400 mr-2">✓</span> Intent First architecture</li>
                <li className="flex items-center"><span className="text-blue-400 mr-2">✓</span> AI Native workflows</li>
                <li className="flex items-center"><span className="text-blue-400 mr-2">✓</span> Offline First ecosystem</li>
                <li className="flex items-center"><span className="text-blue-400 mr-2">✓</span> Architecture First design</li>
              </ul>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
