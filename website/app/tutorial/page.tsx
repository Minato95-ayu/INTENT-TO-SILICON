import Link from 'next/link';

export default function TutorialPage() {
  return (
    <div className="min-h-screen bg-black text-white selection:bg-purple-500/30">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
      <div className="absolute left-0 right-0 top-0 -z-10 m-auto h-[310px] w-[310px] rounded-full bg-purple-500 opacity-20 blur-[100px]"></div>
      
      <main className="container relative mx-auto px-4 pt-32 pb-24 max-w-5xl">
        <div className="mb-16 text-center">
          <div className="inline-flex items-center rounded-full border border-purple-500/30 bg-purple-500/10 px-3 py-1 text-sm font-medium text-purple-300 mb-6 backdrop-blur-sm">
            <span className="flex h-2 w-2 rounded-full bg-purple-500 mr-2 animate-pulse"></span>
            AAYU Masterclass Series
          </div>
          <h1 className="mb-6 text-5xl md:text-7xl font-extrabold tracking-tight">
            Zero to <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">Silicon</span>
          </h1>
          <p className="mx-auto max-w-2xl text-xl text-zinc-400">
            The ultimate 50-chapter curriculum by Ayush Ghrit Kaushik. Master Intent-to-Silicon programming and build AI, Games, APIs, and Web UIs with zero dependencies.
          </p>
        </div>

        {/* Phase 1 */}
        <div className="mb-12">
          <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
            <span className="flex items-center justify-center w-10 h-10 rounded-lg bg-zinc-900 border border-zinc-800 text-purple-400 text-sm">P1</span>
            Getting Started
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <ChapterCard num={1} title="The AAYU Philosophy" desc="Why Ayush created AAYU. Intent Computing explained." />
            <ChapterCard num={2} title="Installation & Setup" desc="Downloading AAYU, setting up VS Code, and terminal commands." />
            <ChapterCard num={3} title="Hello World in AAYU" desc="Your very first code. Compilation to Stack VM explained." />
            <ChapterCard num={4} title="Keywords & Syntax" desc="Variables (let), Data Types, and formatting." />
            <ChapterCard num={5} title="Loops & Conditions" desc="if/elif/else, for loops, and while loops in AAYU." />
          </div>
        </div>

        {/* Phase 2 */}
        <div className="mb-12">
          <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
            <span className="flex items-center justify-center w-10 h-10 rounded-lg bg-zinc-900 border border-zinc-800 text-blue-400 text-sm">P2</span>
            Database & API
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <ChapterCard num={6} title="The Built-in SQLite Engine" desc="Zero-config databases. Models, Fields, and Migrations." />
            <ChapterCard num={7} title="CRUD Operations" desc="insert, find, update, and delete native opcodes." />
            <ChapterCard num={8} title="HTTP Server Magic" desc="Creating a web server using the --web flag." />
            <ChapterCard num={9} title="REST APIs & Routes" desc="get, post, and handling JSON responses." />
            <ChapterCard num={10} title="Authentication" desc="Sessions and secure route handling." />
          </div>
        </div>

        {/* Phase 3 */}
        <div className="mb-12">
          <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
            <span className="flex items-center justify-center w-10 h-10 rounded-lg bg-zinc-900 border border-zinc-800 text-pink-400 text-sm">P3</span>
            Frontend UI & UX
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <ChapterCard num={11} title="Declarative UI Tree" desc="Pages, Columns, Rows, and Cards." />
            <ChapterCard num={12} title="Styling & Themes" desc="Padding, Colors, and beautiful designs natively." />
            <ChapterCard num={13} title="State Management" desc="Reactive variables and UI automatic updates." />
            <ChapterCard num={14} title="Form Handling" desc="Inputs, Buttons, and Action bindings." />
            <ChapterCard num={15} title="Building a Chat UI" desc="Step-by-step WhatsApp clone UI in AAYU." />
          </div>
        </div>

        {/* Phase 4 */}
        <div className="mb-12">
          <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
            <span className="flex items-center justify-center w-10 h-10 rounded-lg bg-zinc-900 border border-zinc-800 text-green-400 text-sm">P4</span>
            Machine Learning & AI
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <ChapterCard num={16} title="Native ML in AAYU" desc="Why AAYU doesn't need pip or NumPy." />
            <ChapterCard num={17} title="K-Means Clustering" desc="Data Science basics. Training your first model." />
            <ChapterCard num={18} title="Neural Networks" desc="Creating layers and activation functions natively." />
            <ChapterCard num={19} title="RAG Systems" desc="Retrieval-Augmented Generation basics in AAYU." />
            <ChapterCard num={20} title="AI Data Visualization" desc="Rendering model predictions on the UI." />
          </div>
        </div>

        {/* Coming Soon Note */}
        <div className="p-8 rounded-xl border border-zinc-800 bg-zinc-900/50 text-center">
          <h3 className="text-2xl font-bold mb-2">Chapters 21 - 50</h3>
          <p className="text-zinc-400 mb-6">Covering Game Development, Advanced Data Science, High-Performance Systems, and more. Being written by Ayush Ghrit Kaushik.</p>
          <div className="inline-block px-4 py-2 rounded bg-zinc-800 text-sm text-zinc-300">Unlocking Soon</div>
        </div>

      </main>
    </div>
  );
}

function ChapterCard({ num, title, desc }: { num: number, title: string, desc: string }) {
  return (
    <div className="group relative p-6 rounded-xl border border-zinc-800 bg-zinc-950/50 hover:bg-zinc-900 transition-all cursor-pointer overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
      <div className="relative z-10 flex gap-4">
        <div className="text-2xl font-black text-zinc-700 group-hover:text-purple-400 transition-colors">
          {num.toString().padStart(2, '0')}
        </div>
        <div>
          <h3 className="text-lg font-bold text-zinc-100 mb-1">{title}</h3>
          <p className="text-sm text-zinc-400">{desc}</p>
        </div>
      </div>
    </div>
  );
}