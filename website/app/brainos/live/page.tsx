/* eslint-disable */

"use client";

import { useState, useEffect } from "react";
import { Brain, Search, Database, HardDrive, Cpu, Zap, FolderTree, Code2, Server, ArrowRight, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function LiveDemoPage() {
  const [input, setInput] = useState("Build a scalable Social Media platform like Instagram");
  const [isProcessing, setIsProcessing] = useState(false);
  const [stage, setStage] = useState(0); // 0: Idle, 1: Domain, 2: Modules, 3: Tradeoffs, 4: Cost, 5: Architecture, 6: Structure, 7: Code

  const handleSimulate = () => {
    setIsProcessing(true);
    setStage(0);
    
    // Simulate progression
    setTimeout(() => setStage(1), 800);
    setTimeout(() => setStage(2), 2000);
    setTimeout(() => setStage(3), 3500);
    setTimeout(() => setStage(4), 5000);
    setTimeout(() => setStage(5), 6500);
    setTimeout(() => setStage(6), 8000);
    setTimeout(() => setStage(7), 9500);
    setTimeout(() => setIsProcessing(false), 9500);
  };

  return (
    <main className="min-h-screen bg-black text-white pt-24 pb-20">
      <div className="container mx-auto px-4 max-w-6xl">
        
        <div className="text-center mb-12">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-purple-900/30 rounded-full border border-purple-500/50 flex items-center justify-center shadow-[0_0_30px_rgba(168,85,247,0.4)]">
              <Brain className="w-8 h-8 text-purple-400" />
            </div>
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">Live BrainOS Architecture</h1>
          <p className="text-xl text-zinc-400">Type your intent and watch the autonomous architect design, evaluate, and scaffold your project.</p>
        </div>

        {/* Input Section */}
        <div className="max-w-3xl mx-auto mb-16 relative">
          <div className="absolute -inset-1 bg-gradient-to-r from-purple-500 to-blue-500 rounded-2xl blur opacity-20"></div>
          <div className="relative bg-[#0a0a0a] border border-white/10 p-2 rounded-2xl flex items-center shadow-2xl">
            <Search className="w-6 h-6 text-zinc-500 ml-4 mr-2" />
            <input 
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isProcessing}
              className="flex-1 bg-transparent border-none outline-none text-lg text-white placeholder:text-zinc-600 h-14"
              placeholder="E.g., Build a scalable banking system..."
            />
            <Button 
              onClick={handleSimulate} 
              disabled={isProcessing}
              className="bg-purple-600 hover:bg-purple-500 h-12 px-8 rounded-xl font-bold gap-2 text-white"
            >
              {isProcessing ? <Loader2 className="w-5 h-5 animate-spin" /> : "Architect Project"}
            </Button>
          </div>
        </div>

        {/* Output Canvas */}
        {(stage > 0) && (
          <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-6 md:p-10 shadow-2xl space-y-12">
            
            {/* 1. Detected Domain */}
            <div className="transition-all duration-700">
              <h3 className="text-sm font-bold text-zinc-500 uppercase tracking-widest mb-4">1. Knowledge Base Match</h3>
              <div className="flex items-center gap-4 p-4 rounded-xl bg-purple-500/10 border border-purple-500/20">
                <Database className="w-6 h-6 text-purple-400" />
                <div>
                  <div className="font-bold text-lg text-purple-300">Domain Detected: Social Media / Media Sharing</div>
                  <div className="text-sm text-zinc-400">High Read-to-Write Ratio (100:1) • Eventual Consistency Acceptable</div>
                </div>
              </div>
            </div>

            {/* 2. Required Modules */}
            <div className="transition-all duration-700">
              <h3 className="text-sm font-bold text-zinc-500 uppercase tracking-widest mb-4">2. Core Modules Extracted</h3>
              <div className="flex flex-wrap gap-3">
                {['User Authentication', 'Follower Graph', 'Media CDN API', 'Feed Algorithm', 'Push Notifications'].map((mod, i) => (
                  <span key={i} className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-sm font-medium">
                    {mod}
                  </span>
                ))}
              </div>
            </div>

            {/* 3. Tradeoffs */}
            <div className="transition-all duration-700">
              <h3 className="text-sm font-bold text-zinc-500 uppercase tracking-widest mb-4">3. Tradeoff Engine Analysis</h3>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="p-5 rounded-xl border border-red-500/20 bg-red-500/5">
                  <h4 className="font-bold text-red-400 mb-2 flex items-center gap-2"><HardDrive className="w-4 h-4"/> Direct RDBMS Query</h4>
                  <p className="text-sm text-zinc-400">Querying feeds directly from PostgreSQL will collapse under high concurrent read load.</p>
                </div>
                <div className="p-5 rounded-xl border border-green-500/20 bg-green-500/5">
                  <h4 className="font-bold text-green-400 mb-2 flex items-center gap-2"><Zap className="w-4 h-4"/> Redis Fan-out on Write</h4>
                  <p className="text-sm text-zinc-400">Recommended: Pre-compute feeds and push to Redis in-memory cache for O(1) reads.</p>
                </div>
              </div>
            </div>

            {/* 4. Cost Estimates */}
            <div className="transition-all duration-700">
              <h3 className="text-sm font-bold text-zinc-500 uppercase tracking-widest mb-4">4. Cloud Cost Estimation (1M MAU)</h3>
              <div className="flex items-center gap-8 p-6 rounded-xl bg-blue-500/10 border border-blue-500/20">
                <div className="flex-1">
                  <div className="text-sm text-blue-300 font-bold mb-1">Compute (AAYU Runtime)</div>
                  <div className="text-3xl font-extrabold text-white">~$120<span className="text-lg text-zinc-500 font-normal">/mo</span></div>
                  <div className="text-xs text-zinc-400 mt-1">Extremely low CPU usage due to LLVM native binary.</div>
                </div>
                <div className="w-px h-16 bg-white/10 hidden md:block"></div>
                <div className="flex-1">
                  <div className="text-sm text-yellow-300 font-bold mb-1">Memory (Redis + DB)</div>
                  <div className="text-3xl font-extrabold text-white">~$450<span className="text-lg text-zinc-500 font-normal">/mo</span></div>
                  <div className="text-xs text-zinc-400 mt-1">High memory cost due to fan-out feed architecture.</div>
                </div>
              </div>
            </div>

            {/* 5 & 6. Architecture & Folder Structure */}
            <div className="transition-all duration-700">
              
              {/* Architecture Diagram */}
              <div>
                <h3 className="text-sm font-bold text-zinc-500 uppercase tracking-widest mb-4">5. Proposed Architecture</h3>
                <div className="bg-zinc-900 border border-zinc-700 rounded-xl p-6 flex flex-col items-center">
                  <div className="px-4 py-2 bg-blue-600 rounded-lg text-xs font-bold w-full text-center mb-3">Client App</div>
                  <ArrowRight className="w-4 h-4 text-zinc-500 rotate-90 mb-3" />
                  <div className="px-4 py-2 bg-orange-600 rounded-lg text-xs font-bold w-full text-center mb-3">AAYU API Gateway</div>
                  <div className="flex w-full gap-4 justify-center">
                    <div className="flex flex-col items-center">
                      <ArrowRight className="w-4 h-4 text-zinc-500 rotate-90 mb-3" />
                      <div className="px-4 py-2 bg-purple-600 rounded-lg text-xs font-bold">Redis (Feed)</div>
                    </div>
                    <div className="flex flex-col items-center">
                      <ArrowRight className="w-4 h-4 text-zinc-500 rotate-90 mb-3" />
                      <div className="px-4 py-2 bg-emerald-600 rounded-lg text-xs font-bold">Postgres (Users)</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Folder Structure */}
              <div className="transition-all duration-700">
                <h3 className="text-sm font-bold text-zinc-500 uppercase tracking-widest mb-4">6. Scaffolded Workspace</h3>
                <div className="bg-[#1e1e1e] border border-white/10 rounded-xl p-4 font-mono text-sm text-zinc-300">
                  <div className="flex items-center gap-2 text-blue-400 mb-1"><FolderTree className="w-4 h-4"/> instagram_clone</div>
                  <div className="pl-4 border-l border-white/10 ml-2 space-y-1 mt-2">
                    <div className="flex items-center gap-2"><FolderTree className="w-4 h-4 text-zinc-500"/> src</div>
                    <div className="pl-4 border-l border-white/10 ml-2 space-y-1">
                      <div className="flex items-center gap-2"><FolderTree className="w-4 h-4 text-zinc-500"/> entities</div>
                      <div className="pl-4 text-orange-300">user.aayu</div>
                      <div className="pl-4 text-orange-300">post.aayu</div>
                      <div className="flex items-center gap-2 mt-1"><FolderTree className="w-4 h-4 text-zinc-500"/> services</div>
                      <div className="pl-4 text-orange-300">feed_service.aayu</div>
                      <div className="flex items-center gap-2 mt-1"><FolderTree className="w-4 h-4 text-zinc-500"/> infrastructure</div>
                      <div className="pl-4 text-orange-300">redis_client.aayu</div>
                      <div className="pl-4 text-orange-300">db_client.aayu</div>
                    </div>
                    <div className="text-yellow-300 mt-2 flex items-center gap-2"><Code2 className="w-4 h-4 text-zinc-500"/> aayu.mod</div>
                  </div>
                </div>
              </div>
            </div>

            {/* 7. Scaffolded Code */}
            <div className="transition-all duration-700">
              <h3 className="text-sm font-bold text-zinc-500 uppercase tracking-widest mb-4 flex justify-between items-center">
                <span>7. Generated AAYU Code (feed_service.aayu)</span>
                <span className="text-xs px-2 py-1 bg-green-500/20 text-green-400 rounded border border-green-500/30">Ready to Compile</span>
              </h3>
              <div className="bg-[#1e1e1e] border border-white/10 rounded-xl p-6 font-mono text-sm overflow-x-auto">
                <pre>
<code className="text-zinc-300">
<span className="text-blue-400">import</span> redis_client<br/>
<span className="text-blue-400">import</span> db_client<br/><br/>
<span className="text-purple-400">trait</span> FeedService<br/>
<span className="text-purple-400">has</span><br/>
&nbsp;&nbsp;&nbsp;&nbsp;cache : redis_client.Connection<br/>
&nbsp;&nbsp;&nbsp;&nbsp;db    : db_client.Connection<br/>
<span className="text-purple-400">end</span>.<br/><br/>
<span className="text-blue-400">extend</span> FeedService<br/>
<span className="text-blue-400">has</span><br/>
&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-yellow-300">fn</span> get_user_feed(user_id: Number) -&gt; List[Post]<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-yellow-300">do</span><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-zinc-500"># BrainOS injected Redis lookup first for O(1) latency</span><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-blue-400">let</span> cached_feed = self.cache.get_list(eed_ + user_id).<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-blue-400">if</span> cached_feed != null<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-blue-400">do</span><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-yellow-300">return</span> cached_feed.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-blue-400">end</span>.<br/><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-zinc-500"># Fallback to DB</span><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-yellow-300">return</span> self.db.query_feed(user_id).<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-yellow-300">end</span>.<br/>
<span className="text-blue-400">end</span>.
</code>
                </pre>
              </div>
            </div>

          </div>
        )}

      </div>
    </main>
  );
}
