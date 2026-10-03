"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import { Play } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Playground() {
  const [code, setCode] = useState(`app Hello

action main
    print("Hello AAYU!")
end

run main`);
  const [output, setOutput] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);

  const handleRun = async () => {
    setIsRunning(true);
    setOutput(null);
    try {
      const res = await fetch("http://localhost:3000/api/v1/compile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code })
      });
      const data = await res.json();
      if (res.ok && data.output) {
        setOutput(data.output.join("\\n"));
      } else {
        setOutput(data.error || "Compilation failed.");
      }
    } catch (e) {
      setOutput("Error: AAYU API server is not running on localhost:3000.\nRun 'python -m tools.cli run api/playground.aayu --web' to start the local backend.");
    }
    setIsRunning(false);
  };

  return (
    <section id="playground" className="py-24 relative border-t border-white/10">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">Experience AAYU</h2>
          <p className="text-zinc-400">Interactive playground connecting to the AAYU Compiler Backend.</p>
        </div>

        <div className="max-w-4xl mx-auto">
          <div className="rounded-xl border border-white/10 overflow-hidden bg-zinc-950 shadow-2xl">
            <div className="flex items-center justify-between px-4 py-3 border-b border-white/10 bg-zinc-900/50">
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-zinc-700" />
                <div className="w-3 h-3 rounded-full bg-zinc-700" />
                <div className="w-3 h-3 rounded-full bg-zinc-700" />
              </div>
              <Button onClick={handleRun} disabled={isRunning} size="sm" className="bg-blue-600 hover:bg-blue-700 text-white h-8">
                <Play className="w-4 h-4 mr-1" /> Run Code
              </Button>
            </div>
            
            <div className="grid md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-white/10 min-h-[300px]">
              <div className="p-4 font-mono text-sm bg-[#0a0a0a] flex flex-col">
                <textarea 
                  value={code} 
                  onChange={(e) => setCode(e.target.value)}
                  className="w-full h-full bg-transparent text-zinc-300 resize-none outline-none"
                  spellCheck={false}
                />
              </div>
              
              <div className="p-4 font-mono text-sm bg-black relative whitespace-pre-wrap">
                <div className="text-zinc-500 mb-2 border-b border-white/5 pb-2">Output</div>
                {isRunning && (
                  <div className="text-zinc-400 animate-pulse">Compiling and running...</div>
                )}
                {output && !isRunning && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className={output.startsWith("Error:") ? "text-red-400" : "text-emerald-400"}
                  >
                    {output}
                  </motion.div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

