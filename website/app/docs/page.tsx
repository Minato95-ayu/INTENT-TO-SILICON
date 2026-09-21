"use client";

import React from "react";
import Link from "next/link";
import { Book, Code, Terminal, Zap, ChevronRight, Play, Server, Layers, Cpu, Download } from "lucide-react";

export default function DocsPage() {
  return (
    <main className="flex-1 min-h-screen pt-24 pb-20">
      {/* Header */}
      <div className="bg-[#0a0a0a] border-b border-white/10 pb-12 pt-8">
        <div className="container mx-auto px-4 max-w-5xl">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
            AAYU: Zero to Legend
          </h1>
          <p className="text-xl text-zinc-400 max-w-3xl">
            The complete guide to mastering AAYU. Whether you have never written a line of code or you are a seasoned developer, this guide will take you from absolute zero to building blazing-fast logic in AAYU.
          </p>
        </div>
      </div>

      <div className="container mx-auto px-4 max-w-5xl mt-12 grid grid-cols-1 lg:grid-cols-4 gap-12">
        
        {/* Navigation Sidebar */}
        <div className="hidden lg:block lg:col-span-1">
          <div className="sticky top-28 space-y-8">
            <div>
              <h3 className="font-bold text-white mb-4 uppercase tracking-wider text-sm">Getting Started</h3>
              <ul className="space-y-3 text-zinc-400 text-sm">
                <li><a href="#why-aayu" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> Why AAYU?</a></li>
                <li><a href="#installation" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> Installation</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-bold text-white mb-4 uppercase tracking-wider text-sm">Zero to Legend Course</h3>
              <ul className="space-y-3 text-zinc-400 text-sm">
                <li><a href="#hello-world" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 1. Hello World</a></li>
                <li><a href="#variables" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 2. Variables</a></li>
                <li><a href="#conditions" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 3. Conditions (If/Else)</a></li>
                <li><a href="#loops" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 4. Loops</a></li>
                <li><a href="#project" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 5. First Project</a></li>
              </ul>
            </div>
          </div>
        </div>

        {/* Content Area */}
        <div className="lg:col-span-3 space-y-20">
          
          {/* Section: Why AAYU */}
          <section id="why-aayu">
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <Zap className="w-8 h-8 text-yellow-400" /> First Choice: Why AAYU?
            </h2>
            <div className="prose prose-invert max-w-none text-zinc-300">
              <p className="text-lg">
                The tech field is full of languages. C++ is incredibly fast but hard to learn. Python is very easy to learn but executes extremely slowly. 
              </p>
              <p className="mt-4">
                <strong>AAYU solves this.</strong> It gives you the simple, clean, and beautiful syntax of Python, but behind the scenes, AAYU generates Native Machine Code. This means your AAYU programs run at <em>silicon speed</em> (like C or Rust). 
              </p>
              <div className="bg-blue-900/20 border border-blue-500/30 p-6 rounded-xl mt-6">
                <h4 className="text-blue-400 font-bold mb-2">No Complex Setup!</h4>
                <p className="text-sm">Unlike other languages where you need to make GitHub accounts, learn Git, install Node.js, Python VMs, or complex environments ?" AAYU is just one single executable file. Download it and run it. That's it.</p>
              </div>
            </div>
          </section>

          {/* Section: Installation */}
          <section id="installation">
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <Download className="w-8 h-8 text-green-400" /> Installation
            </h2>
            <div className="bg-[#0f0f0f] border border-white/10 rounded-xl p-6">
              <p className="text-zinc-400 mb-4">We don't send you to GitHub or ask you to install heavy packages. Just download the compiler directly.</p>
              <div className="bg-black p-4 rounded-lg font-mono text-sm border border-white/5 text-zinc-300">
                <span className="text-zinc-500"># 1. Download the AAYU Compiler executable (aayuc.exe)</span><br/>
                <span className="text-blue-400">curl -LO https://intent-to-silicon.vercel.app/releases/aayuc.exe</span><br/><br/>
                
                <span className="text-zinc-500"># 2. Run your code!</span><br/>
                <span className="text-green-400">./aayuc.exe mycode.aayu</span>
              </div>
            </div>
          </section>

          <hr className="border-white/5" />

          {/* COURSE STARTS */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-center">
            <h2 className="text-2xl font-bold text-white mb-2">The "Zero to Legend" Course</h2>
            <p className="text-white/80">Learn programming logic from scratch with AAYU.</p>
          </div>

          {/* 1. Hello World */}
          <section id="hello-world">
            <h2 className="text-3xl font-bold mb-6">1. Your First Program</h2>
            <p className="text-zinc-400 mb-4">In programming, we always start by making the computer say hello. Create a file called <code>hello.aayu</code>.</p>
            <div className="bg-[#050505] rounded-xl overflow-hidden border border-white/10">
              <div className="bg-[#111] px-4 py-2 border-b border-white/10 text-xs text-zinc-500 flex items-center gap-2">
                <Code className="w-3 h-3" /> hello.aayu
              </div>
              <pre className="p-6 text-sm font-mono text-zinc-300">
                <code className="text-purple-400">print</code>(<code className="text-green-400">"Hello, World! I am learning AAYU."</code>)
              </pre>
            </div>
            <p className="text-zinc-400 mt-4">Run it, and you'll see your message printed on the screen instantly.</p>
          </section>

          {/* 2. Variables */}
          <section id="variables">
            <h2 className="text-3xl font-bold mb-6">2. Variables (Storing Data)</h2>
            <p className="text-zinc-400 mb-4">A variable is like a box where you can store data. In AAYU, you create a box using the <code>let</code> keyword.</p>
            <div className="bg-[#050505] rounded-xl overflow-hidden border border-white/10">
              <div className="bg-[#111] px-4 py-2 border-b border-white/10 text-xs text-zinc-500">Variables Example</div>
              <pre className="p-6 text-sm font-mono text-zinc-300">
                <code className="text-blue-400">let</code> name = <code className="text-green-400">"Minato"</code><br/>
                <code className="text-blue-400">let</code> score = 100<br/><br/>
                <code className="text-purple-400">print</code>(name)<br/>
                <code className="text-purple-400">print</code>(score)
              </pre>
            </div>
          </section>

          {/* 3. Conditions */}
          <section id="conditions">
            <h2 className="text-3xl font-bold mb-6">3. Conditions (Logic & Decisions)</h2>
            <p className="text-zinc-400 mb-4">Computers need to make decisions. "If this happens, do that. Otherwise, do something else." We use <code>if</code> and <code>else</code>.</p>
            <div className="bg-[#050505] rounded-xl overflow-hidden border border-white/10">
              <pre className="p-6 text-sm font-mono text-zinc-300">
                <code className="text-blue-400">let</code> age = 18<br/><br/>
                <code className="text-pink-400">if</code> age &gt;= 18<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-purple-400">print</code>(<code className="text-green-400">"You are an adult!"</code>)<br/>
                <code className="text-pink-400">else</code><br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-purple-400">print</code>(<code className="text-green-400">"You are a kid."</code>)<br/>
                <code className="text-pink-400">end</code>
              </pre>
            </div>
          </section>

          {/* 4. Loops */}
          <section id="loops">
            <h2 className="text-3xl font-bold mb-6">4. Loops (Doing things repeatedly)</h2>
            <p className="text-zinc-400 mb-4">Loops are the superpower of computers. They can do a task millions of times in a millisecond. AAYU's native compiler makes loops run at silicon-speed.</p>
            <div className="bg-[#050505] rounded-xl overflow-hidden border border-white/10">
              <pre className="p-6 text-sm font-mono text-zinc-300">
                <code className="text-blue-400">let</code> i = 0<br/>
                <code className="text-pink-400">while</code> i &lt; 5<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-purple-400">print</code>(<code className="text-green-400">"AAYU is super fast!"</code>)<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;i = i + 1<br/>
                <code className="text-pink-400">end</code>
              </pre>
            </div>
          </section>

          {/* 5. Project */}
          <section id="project">
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <Cpu className="w-8 h-8 text-indigo-400" /> 5. The Legend Level: Your First Project
            </h2>
            <p className="text-zinc-400 mb-4">Let's combine everything we learned (Variables, Conditions, Loops) into a logical project: <strong>A Number Counter & Classifier</strong>.</p>
            <p className="text-zinc-400 mb-6">This program will count from 1 to 10, and tell us if the number is small or large.</p>
            
            <div className="bg-[#050505] rounded-xl overflow-hidden border border-white/10 shadow-2xl shadow-blue-900/10">
              <div className="bg-[#111] px-4 py-3 border-b border-white/10 flex justify-between items-center">
                <span className="text-xs text-zinc-500 font-mono">classifier.aayu</span>
                <span className="flex gap-2"><span className="w-3 h-3 rounded-full bg-red-500/50"></span><span className="w-3 h-3 rounded-full bg-yellow-500/50"></span><span className="w-3 h-3 rounded-full bg-green-500/50"></span></span>
              </div>
              <pre className="p-6 text-sm font-mono text-zinc-300 leading-relaxed">
                <code className="text-zinc-500"># Setting up our starting point</code><br/>
                <code className="text-blue-400">let</code> number = 1<br/>
                <code className="text-blue-400">let</code> limit = 10<br/><br/>
                
                <code className="text-zinc-500"># Start the loop</code><br/>
                <code className="text-pink-400">while</code> number &lt;= limit<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-purple-400">print</code>(number)<br/><br/>
                
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-zinc-500"># Make a decision</code><br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-pink-400">if</code> number &lt; 5<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code className="text-purple-400">print</code>(<code className="text-green-400">"This is a small number."</code>)<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-pink-400">else</code><br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code className="text-purple-400">print</code>(<code className="text-green-400">"This is a large number!"</code>)<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-pink-400">end</code><br/><br/>

                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-zinc-500"># Move to the next number</code><br/>
                &nbsp;&nbsp;&nbsp;&nbsp;number = number + 1<br/>
                <code className="text-pink-400">end</code><br/>
              </pre>
            </div>
            
            <div className="mt-8 bg-green-900/20 border border-green-500/30 p-6 rounded-xl">
              <h4 className="text-green-400 font-bold mb-2 text-xl">🎉 Congratulations! You are a Legend.</h4>
              <p className="text-zinc-300">You just learned the core fundamentals of Programming Logic using AAYU. By running this code, AAYU will automatically translate it into Native C code and run it at maximum hardware speed. You have taken your first step in the tech field!</p>
            </div>
          </section>

        </div>
      </div>
    </main>
  );
}
