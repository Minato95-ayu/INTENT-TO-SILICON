 
"use client";

import { motion } from "framer-motion";

export function Roadmap() {
  const milestones = [
    { name: "Language Ecosystem", progress: 99, status: "Almost Complete", color: "bg-blue-500" },
    { name: "BrainOS", progress: 40, status: "In Development", color: "bg-purple-500" },
    { name: "Intent Engine", progress: 25, status: "Research Phase", color: "bg-indigo-500" },
  ];

  return (
    <section id="roadmap" className="py-24 border-t border-white/5">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">Roadmap to v1.0</h2>
          <p className="text-zinc-400">Track our progress towards the final production release.</p>
        </div>

        <div className="max-w-4xl mx-auto space-y-12">
          {milestones.map((item, i) => (
            <div key={item.name} className="relative">
              <div className="flex justify-between items-end mb-2">
                <div>
                  <h3 className="text-xl font-bold text-zinc-200">{item.name}</h3>
                  <p className="text-sm text-zinc-500">{item.status}</p>
                </div>
                <div className="text-2xl font-bold text-white/50">{item.progress}%</div>
              </div>
              <div className="h-4 w-full bg-white/5 rounded-full overflow-hidden border border-white/10">
                <motion.div
                  initial={{ width: 0 }}
                  whileInView={{ width: `${item.progress}%` }}
                  viewport={{ once: true }}
                  transition={{ duration: 1.5, delay: i * 0.2, ease: "easeOut" }}
                  className={`h-full ${item.color} relative overflow-hidden`}
                >
                  <div className="absolute inset-0 bg-white/20 w-full h-full animate-[shimmer_2s_infinite]" style={{ backgroundImage: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent)' }} />
                </motion.div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
