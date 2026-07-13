"use client";
import { Play, Download, GitBranch, ArrowRight, CheckCircle2, MessageSquare, CloudSun, Briefcase, ListTodo, Calculator, FileText, User } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

const EXAMPLES = [
  { id: "01_hello_world", title: "Hello World", icon: Play, desc: "The absolute basics. Render a single page with text." },
  { id: "02_counter", title: "Counter", icon: Calculator, desc: "Introduction to State Management and Actions." },
  { id: "03_login", title: "Login Screen", icon: User, desc: "Form inputs, data binding, and state interaction." },
  { id: "04_todo", title: "Todo App", icon: ListTodo, desc: "A classic Todo application demonstrating list manipulation." },
  { id: "05_calculator", title: "Calculator", icon: Calculator, desc: "A fully functional calculator layout with math operations." },
  { id: "06_dashboard", title: "Analytics Dashboard", icon: Briefcase, desc: "Complex layouts using rows, columns, and cards." },
  { id: "07_notes", title: "Notes App", icon: FileText, desc: "A two-pane layout for viewing and editing notes." },
  { id: "08_chat_ui", title: "Chat UI", icon: MessageSquare, desc: "A real-time messaging interface layout." },
  { id: "09_weather_ui", title: "Weather Forecast", icon: CloudSun, desc: "A beautiful weather widget displaying dynamic data." },
  { id: "10_whatsapp_clone", title: "WhatsApp Clone", icon: MessageSquare, desc: "A full-scale WhatsApp clone with sidebars, chats, and state routing." }
];

export default function ExamplesGallery() {
  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-24">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="mb-16">
          <h1 className="text-4xl md:text-5xl font-extrabold mb-4">Examples Gallery</h1>
          <p className="text-xl text-zinc-400 max-w-2xl">
            10 fully working, progressively complex projects that you can copy, run, and learn from.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {EXAMPLES.map(ex => (
            <div key={ex.id} className="bg-[#0a0a0a] border border-white/10 rounded-2xl p-6 hover:border-white/20 transition-all flex flex-col group">
              <div className="w-12 h-12 rounded-xl border border-white/10 flex items-center justify-center bg-white/5 mb-4 group-hover:bg-purple-500/10 transition-colors">
                <ex.icon className="w-6 h-6 text-zinc-300 group-hover:text-purple-400" />
              </div>
              <h3 className="text-xl font-bold mb-3">{ex.title}</h3>
              <p className="text-sm text-zinc-400 mb-6 flex-1">{ex.desc}</p>
              
              <div className="flex items-center gap-3 mt-auto pt-6 border-t border-white/5">
                <Link href={`https://github.com/Minato95-ayu/INTENT-TO-SILICON/tree/main/examples/${ex.id}`} target="_blank" className="flex-1">
                  <Button variant="outline" className="w-full bg-transparent border-white/10 text-xs hover:bg-white/5">
                    <GitBranch className="w-3 h-3 mr-2" /> View Source
                  </Button>
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}