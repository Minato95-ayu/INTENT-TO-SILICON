import Link from 'next/link';

export default function TutorialPage() {
  return (
    <div className="min-h-screen bg-black text-white selection:bg-purple-500/30">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
      <div className="absolute left-0 right-0 top-0 -z-10 m-auto h-[310px] w-[310px] rounded-full bg-purple-500 opacity-20 blur-[100px]"></div>
      
      <main className="container relative mx-auto px-4 pt-32 pb-24 max-w-6xl">
        <div className="mb-16 text-center">
          <div className="inline-flex items-center rounded-full border border-purple-500/30 bg-purple-500/10 px-3 py-1 text-sm font-medium text-purple-300 mb-6 backdrop-blur-sm">
            <span className="flex h-2 w-2 rounded-full bg-purple-500 mr-2 animate-pulse"></span>
            AAYU Masterclass Series
          </div>
          <h1 className="mb-6 text-5xl md:text-7xl font-extrabold tracking-tight">
            Zero to <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">Silicon</span>
          </h1>
          <p className="mx-auto max-w-3xl text-xl text-zinc-400">
            The ultimate 50-chapter curriculum designed by Ayush Ghrit Kaushik. Master Intent-to-Silicon programming and build AI, Games, APIs, Graphs, and Web UIs with zero dependencies.
          </p>
        </div>

        {/* Phase 1 */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold mb-6 flex items-center gap-3 border-b border-zinc-800 pb-4">
            <span className="flex items-center justify-center w-10 h-10 rounded-lg bg-zinc-900 border border-zinc-700 text-purple-400 text-sm">P1</span>
            Core Logic & Syntax (The Foundation)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <ChapterCard num={1} title="The AAYU Philosophy" desc="Understanding Intent Computing. Why Ayush created a language from scratch to replace bloated stacks." />
            <ChapterCard num={2} title="Installation & Tooling" desc="Setting up the VS Code extension, checking the CLI, and running your first terminal commands." />
            <ChapterCard num={3} title="Hello World in AAYU" desc="Writing your first AAYU app. Behind the scenes: Lexer to Stack VM compilation explained." />
            <ChapterCard num={4} title="Keywords & Variables" desc="Deep dive into 'let', dynamic typing, constants, and memory-safe garbage collection." />
            <ChapterCard num={5} title="Loops & Conditions" desc="Mastering control flow: if, elif, else, and high-performance loop logic in the VM." />
          </div>
        </div>

        {/* Phase 2 */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold mb-6 flex items-center gap-3 border-b border-zinc-800 pb-4">
            <span className="flex items-center justify-center w-10 h-10 rounded-lg bg-zinc-900 border border-zinc-700 text-blue-400 text-sm">P2</span>
            Database & API (Backend Mastery)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <ChapterCard num={6} title="The Built-in SQLite Engine" desc="Zero-config databases. Defining 'model' schemas, auto-migrations, and data types." />
            <ChapterCard num={7} title="CRUD Operations" desc="Native database querying. Insert, find, update, and delete records instantly." />
            <ChapterCard num={8} title="HTTP Server Magic" desc="Firing up the high-speed ASGI server using the '--web' flag in one command." />
            <ChapterCard num={9} title="REST APIs & Routes" desc="Creating 'route' blocks, handling GET/POST, and structuring JSON API responses." />
            <ChapterCard num={10} title="Authentication & Security" desc="Managing user sessions, cookies, and securing routes from unauthorized access." />
          </div>
        </div>

        {/* Phase 3 */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold mb-6 flex items-center gap-3 border-b border-zinc-800 pb-4">
            <span className="flex items-center justify-center w-10 h-10 rounded-lg bg-zinc-900 border border-zinc-700 text-pink-400 text-sm">P3</span>
            Frontend UI & UX (Visual Design)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <ChapterCard num={11} title="Declarative UI Tree" desc="Building interfaces natively using Page, Column, Row, and Stack widgets." />
            <ChapterCard num={12} title="Beautiful Styling" desc="Colors, padding, margins, and borders. Making your app look premium out of the box." />
            <ChapterCard num={13} title="Reactive State" desc="State management made easy. Watch your UI update instantly when variables change." />
            <ChapterCard num={14} title="Interactive Forms" desc="Handling user input, buttons, password fields, and binding onClick actions." />
            <ChapterCard num={15} title="Project: WhatsApp Clone" desc="Putting it all together to build a fully functional real-time chat UI." />
          </div>
        </div>

        {/* Phase 4 */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold mb-6 flex items-center gap-3 border-b border-zinc-800 pb-4">
            <span className="flex items-center justify-center w-10 h-10 rounded-lg bg-zinc-900 border border-zinc-700 text-green-400 text-sm">P4</span>
            Machine Learning & AI (Data Science)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <ChapterCard num={16} title="Native AI Engine" desc="Why AAYU doesn't need external libraries like PyTorch or Scikit-Learn." />
            <ChapterCard num={17} title="K-Means Clustering" desc="Training your first unsupervised clustering model entirely in AAYU bytecode." />
            <ChapterCard num={18} title="Neural Networks" desc="Building layers, weights, biases, and activation functions from scratch natively." />
            <ChapterCard num={19} title="RAG Systems" desc="Retrieval-Augmented Generation basics. Processing documents for AI context." />
            <ChapterCard num={20} title="AI Data Pipelines" desc="Cleaning, normalizing, and streaming data directly from the AAYU database into models." />
          </div>
        </div>

        {/* Phase 5 */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold mb-6 flex items-center gap-3 border-b border-zinc-800 pb-4">
            <span className="flex items-center justify-center w-10 h-10 rounded-lg bg-zinc-900 border border-zinc-700 text-yellow-400 text-sm">P5</span>
            Graphs & Data Visualization (Analytics)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <ChapterCard num={21} title="The Chart Widget" desc="Rendering native Line Charts, Bar Graphs, and Pie Charts directly in your AAYU UI." />
            <ChapterCard num={22} title="Real-time Data Streaming" desc="Feeding live API/Database metrics into graphs for live dashboards." />
            <ChapterCard num={23} title="Plotting ML Predictions" desc="Visualizing K-Means clusters and Neural Network boundaries dynamically." />
            <ChapterCard num={24} title="Interactive Graphs" desc="Adding hover states, tooltips, and zoom functionality to your data plots." />
            <ChapterCard num={25} title="Project: Admin Dashboard" desc="Building a beautiful financial dashboard with analytics and live data charts." />
          </div>
        </div>

        {/* Phase 6 */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold mb-6 flex items-center gap-3 border-b border-zinc-800 pb-4">
            <span className="flex items-center justify-center w-10 h-10 rounded-lg bg-zinc-900 border border-zinc-700 text-red-400 text-sm">P6</span>
            Game Development (AAYU Game Engine)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <ChapterCard num={26} title="Game Loop & Ticks" desc="Understanding the core event loop, FPS management, and delta time." />
            <ChapterCard num={27} title="The Canvas Widget" desc="Drawing 2D shapes, sprites, and handling pixel-perfect rendering." />
            <ChapterCard num={28} title="Physics & Collision" desc="Implementing gravity, velocity, and AABB collision detection natively." />
            <ChapterCard num={29} title="Keyboard & Mouse Input" desc="Binding player movement, jumping, and shooting to real-time events." />
            <ChapterCard num={30} title="Project: Flappy Bird" desc="Building a complete, playable 2D game in a single .aayu file." />
          </div>
        </div>

        {/* Coming Soon Note */}
        <div className="p-8 rounded-xl border border-zinc-800 bg-zinc-900/50 text-center max-w-2xl mx-auto">
          <h3 className="text-2xl font-bold mb-2">Chapters 31 - 50</h3>
          <p className="text-zinc-400 mb-6">Advanced topics including Multi-threading, Cloud Deployment, and Custom VM Extensions. Curated exclusively by Ayush Ghrit Kaushik.</p>
          <div className="inline-block px-4 py-2 rounded bg-zinc-800 text-sm font-semibold tracking-wide text-zinc-300">SYLLABUS UNDER CONSTRUCTION</div>
        </div>

      </main>
    </div>
  );
}

function ChapterCard({ num, title, desc }: { num: number, title: string, desc: string }) {
  return (
    <div className="group relative p-6 rounded-xl border border-zinc-800 bg-zinc-950/50 hover:bg-zinc-900 transition-all cursor-pointer overflow-hidden hover:shadow-[0_0_20px_rgba(168,85,247,0.1)]">
      <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
      <div className="relative z-10 flex flex-col h-full">
        <div className="text-3xl font-black text-zinc-800 group-hover:text-purple-400 transition-colors mb-3">
          {num.toString().padStart(2, '0')}
        </div>
        <div>
          <h3 className="text-xl font-bold text-zinc-100 mb-2">{title}</h3>
          <p className="text-sm text-zinc-400 leading-relaxed">{desc}</p>
        </div>
      </div>
    </div>
  );
}