"use client";

import React from "react";
import Link from "next/link";
import { Book, Code, Terminal, Zap, ChevronRight, Play, Server, Layers, Cpu, Download, Monitor, Database, GitBranch, Settings, AlertTriangle } from "lucide-react";

export default function DocsPage() {
  return (
    <main className="flex-1 min-h-screen pt-24 pb-20">
      <div className="bg-[#0a0a0a] border-b border-white/10 pb-12 pt-8">
        <div className="container mx-auto px-4 max-w-5xl">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
            AAYU: Zero to Legend (Complete Course)
          </h1>
          <p className="text-xl text-zinc-400 max-w-3xl">
            Zero se coding seekho, AAYU ko apni pehli language bana ke. AAYU is an Intent-to-Silicon language that goes from human-readable code to silicon-ready native binaries. Tested on AAYU v1.1.0.
          </p>
        </div>
      </div>

      <div className="container mx-auto px-4 max-w-7xl mt-12 grid grid-cols-1 xl:grid-cols-4 gap-12">
        
        {/* Sidebar */}
        <div className="hidden xl:block xl:col-span-1">
          <div className="sticky top-28 space-y-8 overflow-y-auto max-h-[80vh] pr-4 custom-scrollbar">
            <div>
              <h3 className="font-bold text-white mb-4 uppercase tracking-wider text-sm">Getting Started</h3>
              <ul className="space-y-3 text-zinc-400 text-sm">
                <li><a href="#ch0" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 0. Shuru Karne Se Pehle</a></li>
                <li><a href="#ch1" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 1. AAYU Under the Hood</a></li>
                <li><a href="#ch2" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 2. Setup & Commands</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-4 uppercase tracking-wider text-sm">Language Basics</h3>
              <ul className="space-y-3 text-zinc-400 text-sm">
                <li><a href="#ch2-1" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> Hello World</a></li>
                <li><a href="#ch2-2" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> Variables & Memory</a></li>
                <li><a href="#ch2-3" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> Decisions (If/Else)</a></li>
                <li><a href="#ch2-4" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> Loops (For/While)</a></li>
                <li><a href="#ch2-5" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> Actions (Functions)</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-4 uppercase tracking-wider text-sm">Projects & Real-World</h3>
              <ul className="space-y-3 text-zinc-400 text-sm">
                <li><a href="#ch3" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 3. Project Organization & Git</a></li>
                <li><a href="#ch4" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 4. 6 Legend Projects</a></li>
                <li><a href="#ch5" className="hover:text-blue-400 transition-colors flex items-center"><ChevronRight className="w-3 h-3 mr-2" /> 5. Limits, FAQ & Creator</a></li>
              </ul>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="xl:col-span-3 prose prose-invert max-w-none prose-pre:bg-[#0a0a0a] prose-pre:border prose-pre:border-white/10 prose-headings:scroll-mt-28">
          
          <div className="bg-yellow-900/20 border border-yellow-700/50 p-6 rounded-xl mb-12" id="ch0">
            <h3 className="text-yellow-500 font-bold flex items-center text-xl mt-0 mb-4">
              <AlertTriangle className="mr-2 h-5 w-5" /> 0. Shuru karne se pehle ye padho
            </h3>
            <p className="text-zinc-300 mb-2">In cheezon ke bina kuch bhi nahi chalega:</p>
            <ul className="text-zinc-300 space-y-2 mt-4">
              <li><strong>Khud AAYU:</strong> Official installer <Link href="/download" className="text-blue-400">Download page</Link> se download karo. Iske bina `aayu` ek recognised command hi nahi hai.</li>
              <li><strong>GCC (ek C compiler):</strong> Sirf <code>aayu build</code> ke liye. <code>aayu run</code> ko iski zarurat nahi hai, par <code>aayu build</code> (native/fast wala path) bina gcc ke compiler error dega. Windows pe iske liye MinGW-w64 install karna padta hai.</li>
              <li><strong>Terminal:</strong> Is course ka har command terminal window me type hota hai, code editor ke play button me nahi.</li>
            </ul>
          </div>

          <h2 id="ch1" className="text-3xl font-bold border-b border-white/10 pb-4 flex items-center text-white">
            <Cpu className="mr-3 text-blue-400" /> 1. AAYU Andar Se Kaise Kaam Karta Hai
          </h2>
          <p className="text-zinc-300">
            <strong>aayu run (VM):</strong> Live translator jaisa. Bytecode padhta hai aur usi waqt line-by-line chalata hai. Turant shuru, seekhne aur chhote programs ke liye badhiya. <br/>
            <strong>aayu build (Native):</strong> Kitaab ek baar print jaisa. Code -&gt; C -&gt; gcc -O3 -&gt; ek asli machine-code program. Python se ~2 se 3 guna tez (fib(30) sirf ~29 ms me). PC pe gcc install hona zaroori.
          </p>

          <pre className="bg-[#111] p-4 rounded-lg overflow-x-auto text-sm text-green-400 border border-zinc-800">
{`┌─────────────────────────────────────────┐
│              AAYU Source (.aayu)        │
├──────┬──────┬──────┬──────┬─────────────┤
│Lexer │Parser│ AST  │Seman-│   IR        │
│      │      │      │tic   │Pipeline     │
├──────┴──────┴──────┴──────┼─────────────┤
│         HIR → MIR → LIR   │  Bytecode   │
├───────────────────────────┼─────────────┤
│ aayu run: Stack-based VM  │ aayu build  │
└───────────────────────────┴─────────────┘`}
          </pre>

          <h2 id="ch2" className="text-3xl font-bold border-b border-white/10 pb-4 flex items-center text-white mt-16">
            <Code className="mr-3 text-blue-400" /> 2. Setup aur Commands
          </h2>
          
          <h3 id="ch2-1" className="text-2xl font-semibold mt-8 text-white">Lesson 1: Pehla Program</h3>
          <p className="text-zinc-300"><code>print(...)</code> screen pe kuch dikhata hai. Text double quotes ke andar likhte hain.</p>
          <pre className="bg-[#111] p-4 rounded-lg text-blue-300">
{`print("Hello, AAYU!")`}
          </pre>

          <h3 id="ch2-2" className="text-2xl font-semibold mt-8 text-white">Lesson 2: Variables</h3>
          <p className="text-zinc-300">Variable ek naam wala dabba hai jisme value rehti hai. <code>let</code> se banao; baad me badalne ke liye <code>let</code> mat likho.</p>
          <pre className="bg-[#111] p-4 rounded-lg text-blue-300">
{`let name = "Riya"
let age = 15
print("Name: " + name)

age = 20
print(age)`}
          </pre>

          <h3 id="ch2-3" className="text-2xl font-semibold mt-8 text-white">Lesson 3: Decisions (if/else)</h3>
          <p className="text-zinc-300"><code>if</code> tabhi code chalata hai jab condition sach ho. Comparisons: <code>&gt;, &lt;, &gt;=, &lt;=, ==, !=</code>. AAYU me <code>else if</code> nahi hai: ek if ke andar doosra if rakho, ya kai if blocks ek ke baad ek likho.</p>
          <pre className="bg-[#111] p-4 rounded-lg text-blue-300">
{`let marks = 82
if marks >= 40
    print("Pass")
    if marks >= 75
        print("Distinction!")
    end
else
    print("Fail")
end`}
          </pre>

          <h3 id="ch2-4" className="text-2xl font-semibold mt-8 text-white">Lesson 4: Loops</h3>
          <p className="text-zinc-300"><code>while</code> condition sach rehne tak repeat karta hai. <code>for</code> list ke har item pe jaata hai.</p>
          <pre className="bg-[#111] p-4 rounded-lg text-blue-300">
{`let i = 1
while i <= 5
    let result = 7 * i
    print("7 x " + i + " = " + result)
    i = i + 1
end

let fruits = ["apple", "mango", "kiwi"]
for f in fruits
    print(f)
end`}
          </pre>

          <h3 id="ch2-5" className="text-2xl font-semibold mt-8 text-white">Lesson 5: Actions (Functions)</h3>
          <p className="text-zinc-300"><code>action</code> code ka naam wala block hai jo tum baar baar use kar sakte ho.</p>
          <pre className="bg-[#111] p-4 rounded-lg text-blue-300">
{`action square(n)
    return n * n
end

print(square(9))  # Prints 81`}
          </pre>

          <h2 id="ch3" className="text-3xl font-bold border-b border-white/10 pb-4 flex items-center text-white mt-16">
            <Layers className="mr-3 text-blue-400" /> 3. Project Organise Karo: Folders, Import, Git
          </h2>
          <p className="text-zinc-300">
            Har project ke liye ek folder banao. Reusable code ko <code>lib/</code> me rakho aur usay <code>import</code> karo. Git se apna code online GitHub par save karo (<code>git init</code>, <code>git add .</code>, <code>git commit</code>, <code>git push</code>).
          </p>
          <pre className="bg-[#111] p-4 rounded-lg text-blue-300">
{`# lib/grades.aayu
action grade_for(avg)
    if avg >= 90
        return "A+"
    end
    return "F"
end

# main.aayu
import lib.grades
print("Score 95 -> " + grade_for(95))`}
          </pre>

          <h2 id="ch4" className="text-3xl font-bold border-b border-white/10 pb-4 flex items-center text-white mt-16">
            <Zap className="mr-3 text-blue-400" /> 4. Chhe (6) Legend Projects
          </h2>

          <h3 className="text-xl font-semibold mt-6 text-white">Project 1: Calculator</h3>
          <pre className="bg-[#111] p-4 rounded-lg text-blue-300">
{`action divide(a, b)
    if b == 0
        return "Error: cannot divide by zero"
    end
    return a / b
end
print(divide(20, 5))`}
          </pre>

          <h3 className="text-xl font-semibold mt-6 text-white">Project 2: Number Guessing (Binary Search)</h3>
          <p className="text-zinc-300">Computer secret number dhundhta hai range ko aadha karke.</p>

          <h3 className="text-xl font-semibold mt-6 text-white">Project 3: Todo Tracker</h3>
          <pre className="bg-[#111] p-4 rounded-lg text-blue-300">
{`let tasks = [
    {"title": "Finish homework", "done": 1},
    {"title": "Practice AAYU", "done": 0}
]
for t in tasks
    if t["done"] == 1
        print("[x] " + t["title"])
    else
        print("[ ] " + t["title"])
    end
end`}
          </pre>

          <h3 className="text-xl font-semibold mt-6 text-white">Project 4: Student Report Card</h3>
          <p className="text-zinc-300">Dictionaries aur lists ko ek sath use karna seekho.</p>

          <h3 className="text-xl font-semibold mt-6 text-white">Project 5: Shop Bill with Discount</h3>
          <p className="text-zinc-300">Maths logic aur conditions ka best example.</p>

          <h3 className="text-xl font-semibold mt-6 text-white">Project 6: Prime Number Finder</h3>
          <p className="text-zinc-300">Math helpers aur nested loops.</p>

          <h2 id="ch5" className="text-3xl font-bold border-b border-white/10 pb-4 flex items-center text-white mt-16">
            <Monitor className="mr-3 text-blue-400" /> 5. Limits, FAQ & Creator
          </h2>
          
          <h3 className="text-xl font-semibold mt-6 text-white">Creator ke Bare Me</h3>
          <p className="text-zinc-300">
            <strong>Ayush Ghrit Kaushik</strong> (@Minato95-ayu) ek self-taught full-stack aur AI/ML developer hain, AAYU programming language aur Intent-to-Silicon research project ke creator hain.
            <br/><br/>
            <em>"I built AAYU because I believe programming should be accessible, lightning-fast, and free of bloated ecosystems. Mission: respect the developer’s time and the computer’s resources."</em>
            <br/><br/>
            <strong>Links:</strong><br/>
            GitHub: <a href="https://github.com/Minato95-ayu" className="text-blue-400" target="_blank">github.com/Minato95-ayu</a><br/>
            Instagram: <a href="https://instagram.com/aa.yu_s" className="text-blue-400" target="_blank">instagram.com/aa.yu_s</a>
          </p>

          <h3 className="text-xl font-semibold mt-8 text-white">FAQ</h3>
          <p className="text-zinc-300">
            <strong>Kya AAYU se main aaj real apps bana sakta hoon?</strong><br/>
            Console programs, AI logics, aur backend systems yes! Full web UI mode pe abhi kaam chal raha hai.
            <br/><br/>
            <strong>Kya mera code fast chalega?</strong><br/>
            <code>aayu build</code> number-heavy code ke liye Python se ~2-3x tez chalta hai natively.
          </p>

        </div>
      </div>
    </main>
  );
}
