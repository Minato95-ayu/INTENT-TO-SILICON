 

"use client";

import { CheckCircle2, Construction, Activity } from "lucide-react";

const STATUS_ITEMS = [
  { name: "AAYU Language", status: "stable" },
  { name: "Compiler", status: "stable" },
  { name: "Runtime", status: "stable" },
  { name: "Package Manager", status: "stable" },
  { name: "Formatter", status: "stable" },
  { name: "Linter", status: "stable" },
  { name: "VS Code Extension", status: "wip" },
  { name: "BrainOS", status: "wip" },
  { name: "Intent Engine", status: "wip" },
  { name: "Documentation", status: "wip" },
  { name: "Developer Website", status: "wip" },
];

export default function StatusPage() {
  return (
    <main className="min-h-screen bg-black text-white pt-24 pb-20">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="mb-12">
          <h1 className="text-4xl font-extrabold tracking-tight mb-4 flex items-center gap-4">
            <Activity className="w-10 h-10 text-blue-500" />
            Ecosystem Status
          </h1>
          <p className="text-xl text-zinc-400">Current progress and stability of the AAYU v1.0 milestone.</p>
        </div>

        <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden shadow-2xl">
          <div className="grid grid-cols-1 divide-y divide-white/5">
            {STATUS_ITEMS.map((item, i) => (
              <div key={i} className="flex items-center justify-between p-6 hover:bg-white/5 transition-colors">
                <span className="text-lg font-medium">{item.name}</span>
                {item.status === "stable" ? (
                  <span className="flex items-center gap-2 px-3 py-1 rounded-full bg-green-500/10 border border-green-500/20 text-green-400 text-sm font-bold tracking-wide uppercase">
                    <CheckCircle2 className="w-4 h-4" /> Stable
                  </span>
                ) : (
                  <span className="flex items-center gap-2 px-3 py-1 rounded-full bg-yellow-500/10 border border-yellow-500/20 text-yellow-400 text-sm font-bold tracking-wide uppercase">
                    <Construction className="w-4 h-4" /> WIP
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
