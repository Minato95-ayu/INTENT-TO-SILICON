'use client';

import { motion } from 'framer-motion';
import { ArrowRight, Sparkles, BrainCircuit, TerminalSquare, RefreshCw } from 'lucide-react';
import Link from 'next/link';

export default function BlogPage() {
  return (
    <main className="min-h-screen bg-[#050505] text-white pt-32 pb-24 selection:bg-purple-500/30">
      <div className="container mx-auto px-4 max-w-4xl">
        
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-16"
        >
          <div className="flex items-center gap-2 mb-6">
            <span className="px-3 py-1 rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20 text-xs font-bold uppercase tracking-wider">
              Manifesto
            </span>
            <span className="text-zinc-500 text-sm">October 2026</span>
          </div>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold mb-6 tracking-tight leading-tight">
            The Billion-Dollar Missing Link in <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-cyan-400">AI Software Development</span>
          </h1>
          <p className="text-xl text-zinc-400 leading-relaxed">
            Why OpenAI, Anthropic, and Google need a true &quot;Compilation Target&quot; for their AI Agents. And why forcing LLMs to write JavaScript and Python is a massive mistake.
          </p>
        </motion.div>

        {/* Content */}
        <motion.article 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="prose prose-invert prose-lg prose-purple max-w-none space-y-8"
        >
          <p className="text-zinc-300">
            If you put AAYU in front of <strong>Sam Altman, Dario Amodei, or Sundar Pichai</strong> today, their first reaction would be: <em>&quot;Why haven&apos;t our AI agents been coding in this from the start?&quot;</em>
          </p>
          <p className="text-zinc-300">
            We are living in the era of <strong>&quot;Vibe Coding&quot;</strong>, where AI Agents (like Devin, Cursor, and Claude Code) are autonomously building software. But the entire AI industry is bottlenecked. Why? Because they are forcing futuristic AI brains to write legacy, human-optimized code like React, Node, and Python.
          </p>

          <div className="my-12 p-8 rounded-2xl bg-gradient-to-b from-zinc-900 to-black border border-white/10 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-purple-500/5 blur-[100px] rounded-full pointer-events-none" />
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <BrainCircuit className="text-purple-400" />
              1. The Context Window Crisis
            </h2>
            <p className="text-zinc-400 mb-6">
              Building a large Enterprise Project (like an ERP system or E-commerce platform) involves massive architecture complexity.
            </p>
            <div className="space-y-6">
              <div className="p-4 rounded-xl bg-red-950/20 border border-red-900/30">
                <h3 className="text-red-400 font-bold mb-2">The Traditional Way (MERN / Python)</h3>
                <p className="text-sm text-zinc-400">
                  If an AI agent wants to build a project, it must juggle 50 different files: Routes, Controllers, ORMs, React Components, Dockerfiles, and Webpack configs. <strong className="text-zinc-200">100k tokens are wasted instantly.</strong> The AI suffers from &quot;Lost in the Middle&quot; syndrome and begins to hallucinate, forgetting how the database schema connects to the UI.
                </p>
              </div>
              <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-900/30">
                <h3 className="text-emerald-400 font-bold mb-2">The AAYU Way</h3>
                <p className="text-sm text-zinc-400">
                  AAYU is relentlessly compact and token-dense. An enterprise app can fit in one or two <code>.aayu</code> files. <strong className="text-zinc-200">10,000 lines of Node/React code = 1,000 lines of AAYU code.</strong> The AI agent keeps the entire project inside its context window, perfectly scaling and building without forgetting a single variable.
                </p>
              </div>
            </div>
          </div>

          <h2 className="text-3xl font-bold mt-16 mb-8 border-b border-white/10 pb-4">
            Why the AI Industry Needs AAYU
          </h2>
          <p className="text-zinc-300">
            The biggest hurdle for AI companies isn&apos;t generating code—it&apos;s <strong>DevOps and Environment Setup</strong>. AI models fail spectacularly at resolving <code>npm install</code> conflicts, Python version mismatches, and Docker port bindings. AAYU completely eliminates this class of errors.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 my-12">
            <div className="p-6 rounded-xl bg-[#0a0a0a] border border-white/5">
              <TerminalSquare className="w-8 h-8 text-cyan-400 mb-4" />
              <h3 className="font-bold text-lg mb-2">The Ultimate Target</h3>
              <p className="text-sm text-zinc-400">
                AI shouldn&apos;t write JavaScript. OpenAI and Anthropic should instruct agents: <em>&quot;Forget JS/Python, just write AAYU.&quot;</em> AAYU acts as the direct bridge from AI Intent to Silicon execution.
              </p>
            </div>
            <div className="p-6 rounded-xl bg-[#0a0a0a] border border-white/5">
              <Sparkles className="w-8 h-8 text-purple-400 mb-4" />
              <h3 className="font-bold text-lg mb-2">Zero Dependencies</h3>
              <p className="text-sm text-zinc-400">
                The agent writes code, runs <code>aayu run app.aayu</code>, and boom! It&apos;s live. No database setup, no <code>package.json</code>. This increases an agent&apos;s autonomous success rate by 10x.
              </p>
            </div>
            <div className="p-6 rounded-xl bg-[#0a0a0a] border border-white/5">
              <RefreshCw className="w-8 h-8 text-orange-400 mb-4" />
              <h3 className="font-bold text-lg mb-2">Flawless Self-Healing</h3>
              <p className="text-sm text-zinc-400">
                AAYU&apos;s strict AST compiler provides perfectly logical error messages. If the AI makes a mistake, the compiler tells it exactly where and why. The AI auto-fixes it in 1 millisecond.
              </p>
            </div>
          </div>

          <div className="mt-16 p-8 rounded-2xl bg-zinc-900 text-center border border-white/10">
            <h2 className="text-2xl font-bold mb-4">The Bottom Line</h2>
            <p className="text-lg text-zinc-300 mb-8 max-w-2xl mx-auto">
              Trying to force &quot;Vibe Coding&quot; onto JS/Python stacks is a fool&apos;s errand. Those languages were not built for AI. <strong>AAYU is the world&apos;s first AI-Native compilation target.</strong>
            </p>
            <p className="text-zinc-400 mb-8">
              AAYU is not a toy. It is 100% production-ready and poised to become the foundational layer of the Billion-Dollar AI Agentic Software Development market.
            </p>
            <Link href="/tutorial">
              <Button className="bg-white text-black hover:bg-zinc-200 font-bold px-8 py-6 rounded-full text-lg shadow-[0_0_20px_rgba(255,255,255,0.3)]">
                Start Building in AAYU <ArrowRight className="ml-2" />
              </Button>
            </Link>
          </div>
        </motion.article>
      </div>
    </main>
  );
}
