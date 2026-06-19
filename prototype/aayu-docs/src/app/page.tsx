import Link from "next/link";
import { ArrowRight, Code2, Terminal, Zap, Layers, Puzzle, CheckCircle2, CheckCircle, Clock } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col flex-1">
      {/* Hero Section */}
      <section className="relative px-6 py-24 md:py-32 overflow-hidden flex flex-col items-center justify-center text-center">
        {/* Abstract background blobs */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/10 rounded-full blur-[120px] -z-10 pointer-events-none" />
        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-white max-w-4xl mb-6">
          Intent-Driven <br />
          <span className="text-primary">Programming Language</span>
        </h1>
        
        <p className="text-lg md:text-xl text-gray-400 max-w-2xl mb-10 leading-relaxed">
          Aayu bridges the gap between human thought and machine execution. 
          Write code that reads like english, runs fast, and catches errors before they happen.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
          <Link href="/docs/getting-started" className="flex items-center justify-center gap-2 bg-primary hover:bg-primary-hover text-black font-semibold px-8 py-3 rounded-lg transition-all shadow-[0_0_20px_rgba(245,158,11,0.3)]">
            Get Started <ArrowRight size={18} />
          </Link>
          <a href="#core-idea" className="flex items-center justify-center gap-2 bg-surface hover:bg-surface-border text-white font-medium px-8 py-3 rounded-lg border border-surface-border transition-colors">
            Learn More
          </a>
        </div>
      </section>

      {/* Core Idea Pipeline */}
      <section id="core-idea" className="py-20 bg-surface/50 border-y border-surface-border">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-white mb-4">The Pipeline of Intent</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">From thought to execution, Aayu strictly validates every step.</p>
          </div>
          
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 md:gap-8 max-w-4xl mx-auto">
            <div className="flex-1 bg-surface border border-surface-border p-6 rounded-xl text-center w-full">
              <h3 className="text-primary font-semibold mb-2">Human Intent</h3>
              <p className="text-sm text-gray-400">Natural expression</p>
            </div>
            <ArrowRight className="hidden md:block text-gray-600 shrink-0" />
            <div className="flex-1 bg-surface border border-surface-border p-6 rounded-xl text-center w-full">
              <h3 className="text-white font-semibold mb-2">Verification</h3>
              <p className="text-sm text-gray-400">Strict AST validation</p>
            </div>
            <ArrowRight className="hidden md:block text-gray-600 shrink-0" />
            <div className="flex-1 bg-surface border border-surface-border p-6 rounded-xl text-center w-full">
              <h3 className="text-white font-semibold mb-2">Aayu Code</h3>
              <p className="text-sm text-gray-400">Expression-oriented</p>
            </div>
            <ArrowRight className="hidden md:block text-gray-600 shrink-0" />
            <div className="flex-1 bg-surface border border-surface-border p-6 rounded-xl text-center w-full">
              <h3 className="text-white font-semibold mb-2">Execution</h3>
              <p className="text-sm text-gray-400">Safe evaluation</p>
            </div>
          </div>
        </div>
      </section>

      {/* Web Framework Status Section */}
      <section className="py-24 bg-surface/50 border-y border-surface-border">
        <div className="max-w-4xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">AAYU Web Framework Status</h2>
            <p className="text-gray-400">Track our progress as we build the first Intent-Driven Web Framework.</p>
          </div>
          
          <div className="bg-background rounded-xl p-8 border border-surface-border">
            <div className="space-y-4">
              <StatusItem title="HTTP Server" done={true} />
              <StatusItem title="Routing Engine" done={true} />
              <StatusItem title="HTML Templates" done={true} />
              <StatusItem title="Forms (POST Requests)" done={true} />
              <StatusItem title="JSON APIs" done={true} />
              <StatusItem title="Database Layer" done={true} />
              <StatusItem title="Authentication" done={true} />
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-24 max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-white mb-4">A Modern Foundation</h2>
          <p className="text-gray-400 max-w-2xl mx-auto">Everything you need to build robust software, built directly into the language.</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <FeatureCard 
            icon={<Code2 className="text-primary" />}
            title="Variables & Records"
            desc="Strictly typed and strongly checked data structures that are simple to declare."
          />
          <FeatureCard 
            icon={<Layers className="text-primary" />}
            title="Collections"
            desc="Native support for dynamically typed Lists and ultra-fast Maps out of the box."
          />
          <FeatureCard 
            icon={<Terminal className="text-primary" />}
            title="Tasks & Returns"
            desc="Reusable functional components with clear inputs, operations, and return values."
          />
          <FeatureCard 
            icon={<Puzzle className="text-primary" />}
            title="Modules"
            desc="Clean namespacing and explicit 'export' syntax to build large codebases securely."
          />
          <FeatureCard 
            icon={<Zap className="text-primary" />}
            title="Standard Library"
            desc="Built-in functions for strings, math, and random evaluation for speed."
          />
          <FeatureCard 
            icon={<Code2 className="text-primary" />}
            title="Editor Tooling"
            desc="Native Language Server Protocol (LSP) providing instant Red Squiggles in VS Code."
          />
        </div>
      </section>

      {/* Built With AAYU */}
      <section className="py-24 max-w-7xl mx-auto px-6 border-t border-surface-border">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-white mb-4">What can AAYU build?</h2>
          <p className="text-gray-400 max-w-2xl mx-auto">Showcasing the power and simplicity of the AAYU ecosystem.</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Todo Application */}
          <div className="bg-surface/30 border border-emerald-500/30 p-6 rounded-xl hover:bg-surface/80 transition-colors">
            <div className="flex items-center gap-4 mb-4">
              <CheckCircle className="w-8 h-8 text-emerald-500" />
              <h3 className="text-xl font-bold text-white">Todo Application</h3>
            </div>
            <p className="text-gray-400">A complete, fully functional CRUD application proving Aayu's end-to-end capabilities.</p>
          </div>
          
          {/* Library Management System */}
          <div className="bg-surface/30 border border-emerald-500/30 p-6 rounded-xl hover:bg-surface/80 transition-colors">
            <div className="flex items-center gap-4 mb-4">
              <CheckCircle className="w-8 h-8 text-emerald-500" />
              <h3 className="text-xl font-bold text-white">Library System</h3>
            </div>
            <p className="text-gray-400">A complex application showcasing Authentication, Relationships, Multiple Entities, and Business Logic Workflows.</p>
          </div>

          <div className="flex items-center justify-center">
            <h3 className="text-2xl font-semibold text-gray-500 uppercase tracking-widest">Coming Soon</h3>
          </div>
          
          {/* Notes Application */}
          <div className="bg-surface/30 border border-surface-border p-6 rounded-xl opacity-60">
            <div className="flex items-center gap-4 mb-4">
              <Clock className="w-8 h-8 text-blue-500" />
              <h3 className="text-xl font-bold text-white">Notes App</h3>
            </div>
          </div>

          {/* CRM */}
          <div className="bg-surface/30 border border-surface-border p-6 rounded-xl opacity-60">
            <div className="flex items-center gap-4 mb-4">
              <Clock className="w-8 h-8 text-blue-500" />
              <h3 className="text-xl font-bold text-white">CRM</h3>
            </div>
          </div>

          {/* LMS */}
          <div className="bg-surface/30 border border-surface-border p-6 rounded-xl opacity-60">
            <div className="flex items-center gap-4 mb-4">
              <Clock className="w-8 h-8 text-blue-500" />
              <h3 className="text-xl font-bold text-white">LMS</h3>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

function FeatureCard({ icon, title, desc }: { icon: React.ReactNode, title: string, desc: string }) {
  return (
    <div className="bg-surface/30 border border-surface-border p-6 rounded-xl hover:bg-surface/80 transition-colors">
      <div className="bg-surface w-12 h-12 rounded-lg flex items-center justify-center border border-surface-border mb-4">
        {icon}
      </div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-gray-400 leading-relaxed text-sm">{desc}</p>
    </div>
  )
}

function StatusItem({ title, done }: { title: string, done: boolean }) {
  return (
    <div className="flex items-center justify-between p-4 bg-surface/30 rounded-lg border border-surface-border/50">
      <span className="text-white font-medium">{title}</span>
      {done ? (
        <span className="flex items-center gap-2 text-green-500 bg-green-500/10 px-3 py-1 rounded-full text-sm font-medium">
          <CheckCircle2 size={16} /> Ready
        </span>
      ) : (
        <span className="flex items-center gap-2 text-amber-500 bg-amber-500/10 px-3 py-1 rounded-full text-sm font-medium">
          <Clock size={16} /> In Progress
        </span>
      )}
    </div>
  )
}
