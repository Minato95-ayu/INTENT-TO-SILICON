"use client";
import { BookOpen, Clock, Code2, Cpu, Rocket, ChevronRight, Play } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

const LESSONS = [
  { id: "01_hello_world", title: "1. Hello World", desc: "Learn the basics of AAYU syntax and page rendering." },
  { id: "02_pages_layouts", title: "2. Pages & Layouts", desc: "Structure your app using Containers, Rows, and Columns." },
  { id: "03_state_management", title: "3. State Management", desc: "Make your app dynamic using the 'state' keyword." },
  { id: "04_actions_events", title: "4. Actions & Events", desc: "Handle user input and button clicks with actions." },
  { id: "05_final_project", title: "5. Final Project", desc: "Build a complete Todo application from scratch." }
];

export default function LearnPage() {
  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-24">
      <div className="container mx-auto px-4 max-w-4xl">
        
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded-full px-4 py-1.5 mb-6 text-sm font-semibold">
            <Clock className="w-4 h-4" /> 15-Minute Crash Course
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold mb-6">
            Learn AAYU in 15 Minutes
          </h1>
          <p className="text-xl text-zinc-400 max-w-2xl mx-auto">
            Forget boilerplate. Forget complex configurations. By the end of this interactive course, you'll be building native apps with pure intent.
          </p>
        </div>

        {/* Start Button */}
        <div className="flex justify-center mb-20">
          <Link href="/docs/installation">
            <Button className="h-14 px-8 bg-white text-black hover:bg-zinc-200 text-lg font-bold rounded-xl gap-2 shadow-[0_0_30px_rgba(255,255,255,0.2)]">
              <Play className="w-5 h-5" /> Start Course
            </Button>
          </Link>
        </div>

        {/* Curriculum */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold mb-6 border-b border-white/10 pb-4">Curriculum</h2>
          {LESSONS.map((lesson, idx) => (
            <div key={idx} className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-6 flex items-center justify-between group hover:border-purple-500/30 transition-all">
              <div>
                <h3 className="text-xl font-bold mb-1 group-hover:text-purple-400 transition-colors">{lesson.title}</h3>
                <p className="text-zinc-400">{lesson.desc}</p>
              </div>
              <Link href="/docs/quick-start">
                <Button variant="ghost" className="rounded-full w-10 h-10 p-0 text-zinc-500 group-hover:text-white group-hover:bg-white/10">
                  <ChevronRight className="w-5 h-5" />
                </Button>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
