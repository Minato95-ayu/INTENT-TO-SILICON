"use client";

import React from "react";
import Link from "next/link";
import { Book, Code, Terminal, Zap, ChevronRight, Play, Server, Layers, Cpu, Download, Monitor, Database, GitBranch, Settings } from "lucide-react";

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
            Programming isn't just about syntax—it's about understanding how computers think. This comprehensive track takes you from an absolute beginner to a true Tech Field Legend. Learn memory, architecture, logic, and systems engineering using AAYU.
          </p>
        </div>
      </div>

      <div className="container mx-auto px-4 max-w-7xl mt-12 grid grid-cols-1 xl:grid-cols-4 gap-12">
        
        {/* Navigation Sidebar */}
        <div className="hidden xl:block xl:col-span-1">
          <div className="sticky top-28 space-y-8 overflow-y-auto max-h-[80vh] pr-4 custom-scrollbar">
            <div>
              <h3 className="font-bold text-white mb-4 uppercase tracking-wider text-sm">Getting Started</h3>
              <ul className="space-y-3 text-zinc-400 text-sm">
                <li><a href="#ch0" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 0. The Tech Field & AAYU</a></li>
                <li><a href="#ch1" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 1. The Pro Workspace & VS Code</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-bold text-white mb-4 uppercase tracking-wider text-sm">The Foundation</h3>
              <ul className="space-y-3 text-zinc-400 text-sm">
                <li><a href="#ch2" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 2. Hello Silicon (Execution)</a></li>
                <li><a href="#ch3" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 3. Data & Memory (Variables)</a></li>
                <li><a href="#ch4" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 4. The Logical Brain (If/Else)</a></li>
                <li><a href="#ch5" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 5. Automation (Loops)</a></li>
              </ul>
            </div>

            <div>
              <h3 className="font-bold text-white mb-4 uppercase tracking-wider text-sm">Advanced Engineering</h3>
              <ul className="space-y-3 text-zinc-400 text-sm">
                <li><a href="#ch6" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 6. Data Structures (Arrays/Dicts)</a></li>
                <li><a href="#ch7" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 7. Reusable Architecture (Actions)</a></li>
                <li><a href="#ch8" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 8. How Compilers Work</a></li>
                <li><a href="#ch9" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 9. The Capstone Project</a></li>
                <li><a href="#ch10" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 10. The Road Ahead</a></li>
              </ul>
            </div>
          </div>
        </div>

        {/* Content Area */}
        <div className="xl:col-span-3 space-y-24">
          
          {/* Chapter 0 */}
          <section id="ch0">
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <Zap className="w-8 h-8 text-yellow-400" /> Chapter 0: The Tech Field & AAYU
            </h2>
            <div className="prose prose-invert max-w-none text-zinc-300 space-y-6">
              <p className="text-lg">
                To be a legend in the tech field, you can't just memorize syntax. You have to understand what happens when you hit "Run". 
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 my-8">
                <div className="bg-black border border-red-500/30 p-6 rounded-xl">
                  <h4 className="text-red-400 font-bold mb-2">The Problem</h4>
                  <p className="text-sm">Languages like C++ give you ultimate hardware control and extreme speed, but they are incredibly hard to learn. Python is very easy to write, but it runs on a heavy "Virtual Machine" making it extremely slow for real systems engineering.</p>
                </div>
                <div className="bg-black border border-green-500/30 p-6 rounded-xl">
                  <h4 className="text-green-400 font-bold mb-2">The AAYU Solution</h4>
                  <p className="text-sm">AAYU is a "Native AOT Compiler". You write code that looks as simple as Python. But AAYU translates that directly into Machine Code. You get the simplicity of a high-level language with the raw silicon speed of C.</p>
                </div>
              </div>
            </div>
          </section>

          {/* Chapter 1 */}
          <section id="ch1">
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <Monitor className="w-8 h-8 text-blue-400" /> Chapter 1: The Pro Workspace (VS Code)
            </h2>
            <div className="bg-[#0f0f0f] border border-white/10 rounded-xl p-8 space-y-8">
              <p className="text-zinc-400">Legends don't code in Notepad. They use professional tools. We will set up your computer like a true software engineer.</p>
              
              <div>
                <h3 className="text-xl font-bold text-white mb-4">Step A: Install the AAYU Compiler</h3>
                <p className="text-sm text-zinc-400 mb-4">You do NOT need GitHub, Node.js, or Python to run AAYU. It is fully standalone.</p>
                <div className="bg-black p-4 rounded-lg font-mono text-sm border border-white/5 text-zinc-300">
                  <span className="text-zinc-500"># Download the native executable</span><br/>
                  <span className="text-blue-400">curl -LO https://intent-to-silicon.vercel.app/releases/aayuc.exe</span>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-bold text-white mb-4">Step B: Set Up VS Code</h3>
                <p className="text-sm text-zinc-400 mb-4">Visual Studio Code is the industry standard editor. To make your AAYU code look colorful and auto-complete, you need the AAYU extension.</p>
                <ul className="list-disc pl-5 text-zinc-300 text-sm space-y-2">
                  <li>Download and install <strong>Visual Studio Code</strong>.</li>
                  <li>Download the AAYU Extension file: <code className="bg-white/10 px-2 py-1 rounded">aayu-language-1.0.0.vsix</code></li>
                  <li>In VS Code, go to Extensions (Ctrl+Shift+X), click the three dots (...), and select <strong>"Install from VSIX..."</strong></li>
                  <li>Select the downloaded file. Now, whenever you open a <code>.aayu</code> file, it will have beautiful syntax highlighting!</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Chapter 2 */}
          <section id="ch2">
            <h2 className="text-3xl font-bold mb-6">Chapter 2: Hello Silicon</h2>
            <p className="text-zinc-400 mb-4">Create a file named <code>main.aayu</code> in your VS Code. Let's send an instruction to the CPU.</p>
            <div className="bg-[#050505] rounded-xl overflow-hidden border border-white/10 shadow-lg">
              <div className="bg-[#111] px-4 py-2 border-b border-white/10 text-xs text-zinc-500 flex items-center gap-2">
                <Code className="w-3 h-3" /> main.aayu
              </div>
              <pre className="p-6 text-sm font-mono text-zinc-300">
                <code className="text-purple-400">print</code>(<code className="text-green-400">"Commanding the silicon!"</code>)
              </pre>
            </div>
            <p className="text-zinc-400 mt-4">Run it in your terminal: <code className="bg-white/10 px-2 py-1 rounded text-white">./aayuc.exe main.aayu</code></p>
          </section>

          {/* Chapter 3 */}
          <section id="ch3">
            <h2 className="text-3xl font-bold mb-6">Chapter 3: Data & Memory</h2>
            <p className="text-zinc-400 mb-4">Computers need to remember things. When you create a <strong>variable</strong>, you are reserving a tiny block of the computer's RAM. We use the <code>let</code> keyword.</p>
            <div className="bg-[#050505] rounded-xl overflow-hidden border border-white/10 shadow-lg">
              <pre className="p-6 text-sm font-mono text-zinc-300 leading-loose">
                <code className="text-zinc-500"># Reserving memory for a number (Integer)</code><br/>
                <code className="text-blue-400">let</code> player_health = 100<br/><br/>
                <code className="text-zinc-500"># Reserving memory for text (String)</code><br/>
                <code className="text-blue-400">let</code> player_name = <code className="text-green-400">"Minato"</code><br/><br/>
                
                <code className="text-purple-400">print</code>(player_name)<br/>
                <code className="text-purple-400">print</code>(player_health)
              </pre>
            </div>
          </section>

          {/* Chapter 4 */}
          <section id="ch4">
            <h2 className="text-3xl font-bold mb-6">Chapter 4: The Logical Brain</h2>
            <p className="text-zinc-400 mb-4">Without logic, programs are just calculators. The <code>if / else</code> statement allows your code to make intelligent decisions based on data.</p>
            <div className="bg-[#050505] rounded-xl overflow-hidden border border-white/10 shadow-lg">
              <pre className="p-6 text-sm font-mono text-zinc-300 leading-loose">
                <code className="text-blue-400">let</code> password = <code className="text-green-400">"admin123"</code><br/><br/>
                <code className="text-pink-400">if</code> password == <code className="text-green-400">"admin123"</code><br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-purple-400">print</code>(<code className="text-green-400">"Access Granted to Mainframe."</code>)<br/>
                <code className="text-pink-400">else</code><br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-purple-400">print</code>(<code className="text-green-400">"Security Alert! Access Denied."</code>)<br/>
                <code className="text-pink-400">end</code>
              </pre>
            </div>
          </section>

          {/* Chapter 5 */}
          <section id="ch5">
            <h2 className="text-3xl font-bold mb-6">Chapter 5: Automation (Loops)</h2>
            <p className="text-zinc-400 mb-4">Computers never get tired. A <code>while</code> loop will repeat a block of code until a condition becomes false. Because AAYU is natively compiled, this loop will execute millions of times in less than a millisecond.</p>
            <div className="bg-[#050505] rounded-xl overflow-hidden border border-white/10 shadow-lg">
              <pre className="p-6 text-sm font-mono text-zinc-300 leading-loose">
                <code className="text-blue-400">let</code> counter = 1<br/>
                <code className="text-pink-400">while</code> counter &lt;= 5<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-purple-400">print</code>(<code className="text-green-400">"Executing task number:"</code>)<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-purple-400">print</code>(counter)<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;counter = counter + 1<br/>
                <code className="text-pink-400">end</code>
              </pre>
            </div>
          </section>

          {/* Chapter 6 */}
          <section id="ch6">
            <h2 className="text-3xl font-bold mb-6">Chapter 6: Complex Data (Arrays & Dicts)</h2>
            <p className="text-zinc-400 mb-4">In the real world, you don't just store one user's name. You store databases of users. Arrays <code>[]</code> hold lists. Dictionaries <code>{`{}`}</code> hold key-value maps.</p>
            <div className="bg-[#050505] rounded-xl overflow-hidden border border-white/10 shadow-lg">
              <pre className="p-6 text-sm font-mono text-zinc-300 leading-loose">
                <code className="text-zinc-500"># An Array (List) of items</code><br/>
                <code className="text-blue-400">let</code> servers = [<code className="text-green-400">"AWS"</code>, <code className="text-green-400">"GCP"</code>, <code className="text-green-400">"Azure"</code>]<br/><br/>
                
                <code className="text-zinc-500"># A Dictionary (Key-Value map) representing a User</code><br/>
                <code className="text-blue-400">let</code> user = {`{`}<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-green-400">"id"</code>: 101,<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-green-400">"role"</code>: <code className="text-green-400">"admin"</code>,<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-green-400">"active"</code>: 1<br/>
                {`}`}<br/><br/>
                <code className="text-purple-400">print</code>(user[<code className="text-green-400">"role"</code>])
              </pre>
            </div>
          </section>

          {/* Chapter 7 */}
          <section id="ch7">
            <h2 className="text-3xl font-bold mb-6">Chapter 7: Reusable Architecture (Actions)</h2>
            <p className="text-zinc-400 mb-4">Writing the same code over and over is bad engineering. In AAYU, we use <code>action</code> to create reusable blocks of logic (often called functions in other languages).</p>
            <div className="bg-[#050505] rounded-xl overflow-hidden border border-white/10 shadow-lg">
              <pre className="p-6 text-sm font-mono text-zinc-300 leading-loose">
                <code className="text-blue-400">action</code> calculate_damage(base_attack, multiplier)<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-blue-400">let</code> total = base_attack * multiplier<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-pink-400">return</code> total<br/>
                <code className="text-pink-400">end</code><br/><br/>
                
                <code className="text-blue-400">let</code> hit = calculate_damage(50, 2)<br/>
                <code className="text-purple-400">print</code>(hit) <code className="text-zinc-500"># Prints 100</code>
              </pre>
            </div>
          </section>

          {/* Chapter 8 */}
          <section id="ch8">
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <Settings className="w-8 h-8 text-zinc-400" /> Chapter 8: How Compilers Work
            </h2>
            <p className="text-zinc-400 mb-4">This is the secret sauce that separates normal coders from engineers. How does AAYU actually work?</p>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-black border border-white/10 p-5 rounded-xl">
                <div className="text-blue-400 font-bold mb-2">1. Lexer</div>
                <p className="text-xs text-zinc-400">Reads your code character by character and groups them into "Tokens" (Keywords, Numbers, Symbols).</p>
              </div>
              <div className="bg-black border border-white/10 p-5 rounded-xl">
                <div className="text-purple-400 font-bold mb-2">2. Parser (AST)</div>
                <p className="text-xs text-zinc-400">Takes the tokens and builds an Abstract Syntax Tree (a mathematical map of your code's logic).</p>
              </div>
              <div className="bg-black border border-white/10 p-5 rounded-xl">
                <div className="text-green-400 font-bold mb-2">3. C-Backend</div>
                <p className="text-xs text-zinc-400">AAYU traverses the AST and writes pure C code. A C compiler then turns that into the final Native <code>.exe</code>.</p>
              </div>
            </div>
          </section>

          {/* Chapter 9 */}
          <section id="ch9">
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <Cpu className="w-8 h-8 text-indigo-400" /> Chapter 9: The Capstone Project
            </h2>
            <p className="text-zinc-400 mb-4">Let's combine everything into a real-world script: A <strong>Data Analytics Engine</strong> that processes an array of data, filters it using logic, and calculates a total using loops and actions.</p>
            
            <div className="bg-[#050505] rounded-xl overflow-hidden border border-white/10 shadow-2xl shadow-blue-900/10">
              <div className="bg-[#111] px-4 py-3 border-b border-white/10 flex justify-between items-center">
                <span className="text-xs text-zinc-500 font-mono">analytics.aayu</span>
              </div>
              <pre className="p-6 text-sm font-mono text-zinc-300 leading-relaxed overflow-x-auto">
                <code className="text-zinc-500"># Reusable logic to process a single data point</code><br/>
                <code className="text-blue-400">action</code> process_data(val)<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-pink-400">if</code> val &gt; 50<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code className="text-pink-400">return</code> val * 2<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-pink-400">else</code><br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code className="text-pink-400">return</code> 0<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-pink-400">end</code><br/>
                <code className="text-pink-400">end</code><br/><br/>
                
                <code className="text-blue-400">let</code> raw_data = [10, 80, 45, 90, 20]<br/>
                <code className="text-blue-400">let</code> total_score = 0<br/>
                <code className="text-blue-400">let</code> i = 0<br/>
                <code className="text-blue-400">let</code> length = 5<br/><br/>
                
                <code className="text-pink-400">while</code> i &lt; length<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-blue-400">let</code> current = raw_data[i]<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<code className="text-blue-400">let</code> processed = process_data(current)<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;total_score = total_score + processed<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;i = i + 1<br/>
                <code className="text-pink-400">end</code><br/><br/>
                
                <code className="text-purple-400">print</code>(<code className="text-green-400">"Final Analytics Score:"</code>)<br/>
                <code className="text-purple-400">print</code>(total_score)<br/>
              </pre>
            </div>
            
            <div className="mt-8 bg-green-900/20 border border-green-500/30 p-8 rounded-xl text-center">
              <h4 className="text-green-400 font-bold mb-4 text-2xl">🎉 You are now a Legend.</h4>
              <p className="text-zinc-300 max-w-2xl mx-auto">
                You have mastered Variables, Logic, Automation, Data Structures, Reusable Architecture, and Compiler Theory. This is the exact foundation you need to build scalable software, AI models, and Native Systems in the real tech industry.
              </p>
            </div>
          </section>

          {/* Chapter 10 */}
          <section id="ch10">
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <Database className="w-8 h-8 text-pink-400" /> Chapter 10: The Road Ahead
            </h2>
            <div className="bg-[#0f0f0f] border border-white/10 rounded-xl p-8">
              <p className="text-zinc-400 mb-6">Now that you know how AAYU and programming logic works, what's next? Here is where AAYU shines in the Tech Field.</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-white font-bold flex items-center gap-2 mb-2"><GitBranch className="w-4 h-4 text-blue-400" /> Backend Systems</h4>
                  <p className="text-sm text-zinc-400">Use AAYU's speed to build web servers, APIs, and microservices that handle millions of requests without the lag of Python or Node.js.</p>
                </div>
                <div>
                  <h4 className="text-white font-bold flex items-center gap-2 mb-2"><Layers className="w-4 h-4 text-purple-400" /> OS Automation</h4>
                  <p className="text-sm text-zinc-400">Because AAYU compiles to native binaries (.exe), you can write scripts that automate your Operating System flawlessly.</p>
                </div>
              </div>
            </div>
          </section>

        </div>
      </div>
    </main>
  );
}
