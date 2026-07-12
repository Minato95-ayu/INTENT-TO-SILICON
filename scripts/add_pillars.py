import os

p = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\page.tsx'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

ecosystem_html = '''
      {/* 
        ========================================================================
        THE 3 CORE PRODUCTS
        ========================================================================
      */}
      <section className="container mx-auto px-4 max-w-7xl pb-24">
        <h2 className="text-3xl font-bold mb-12 text-center">The AAYU Ecosystem</h2>
        <div className="grid md:grid-cols-3 gap-8">
          
          {/* 1. AAYU Language */}
          <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl">
            <div className="w-12 h-12 bg-orange-900/30 rounded-xl flex items-center justify-center mb-6">
              <Code2 className="w-6 h-6 text-orange-400" />
            </div>
            <h3 className="text-xl font-bold mb-6">AAYU Language</h3>
            <ul className="space-y-3 text-sm text-zinc-400">
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> Compiler (LLVM Backend)</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> Deterministic ARC Runtime</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> AAYU CLI</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> Built-in Formatter</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> Advanced Linter</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> Package Manager (apm)</li>
            </ul>
          </div>

          {/* 2. BrainOS */}
          <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl relative">
            <div className="absolute top-0 right-0 px-3 py-1 bg-purple-500 text-white text-xs font-bold rounded-bl-lg rounded-tr-xl">CORE</div>
            <div className="w-12 h-12 bg-purple-900/30 rounded-xl flex items-center justify-center mb-6">
              <Brain className="w-6 h-6 text-purple-400" />
            </div>
            <h3 className="text-xl font-bold mb-6">BrainOS</h3>
            <ul className="space-y-3 text-sm text-zinc-400">
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> AI Planner</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> Decision Engine</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> Recommendation Engine</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> Tradeoff Engine</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> Knowledge Graph</li>
            </ul>
          </div>

          {/* 3. Intent Engine */}
          <div className="bg-[#0a0a0a] border border-white/10 p-8 rounded-2xl">
            <div className="w-12 h-12 bg-blue-900/30 rounded-xl flex items-center justify-center mb-6">
              <Network className="w-6 h-6 text-blue-400" />
            </div>
            <h3 className="text-xl font-bold mb-6">Intent Engine</h3>
            <ul className="space-y-3 text-sm text-zinc-400">
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> Offline NLP</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> Intent IR Representation</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> Intent Parser</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> Clarification Engine</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-green-500" /> Architecture Generator</li>
            </ul>
          </div>

        </div>
      </section>
'''

c = c.replace('    </main>', ecosystem_html + '\\n    </main>')

with open(p, 'w', encoding='utf-8') as f:
    f.write(c)

print("Added 3 pillars to Homepage.")
