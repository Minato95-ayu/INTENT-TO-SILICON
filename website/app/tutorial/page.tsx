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
        <PhaseSection badge="P1" color="purple" title="Core Logic & Syntax (The Foundation)" level="Beginner">
          <ChapterCard num={1} title="The AAYU Philosophy" desc="Understanding Intent Computing. Why Ayush created a language from scratch to replace bloated stacks." />
          <ChapterCard num={2} title="Installation & Tooling" desc="Setting up the VS Code extension, checking the CLI, and running your first terminal commands." />
          <ChapterCard num={3} title="Hello World in AAYU" desc="Writing your first AAYU app. Behind the scenes: Lexer to Stack VM compilation explained." />
          <ChapterCard num={4} title="Keywords & Variables" desc="Deep dive into 'let', dynamic typing, constants, and memory-safe garbage collection." />
          <ChapterCard num={5} title="Loops & Conditions" desc="Mastering control flow: if, elif, else, and high-performance loop logic in the VM." />
        </PhaseSection>

        {/* Phase 2 */}
        <PhaseSection badge="P2" color="blue" title="Database & API (Backend Mastery)" level="Beginner">
          <ChapterCard num={6} title="The Built-in SQLite Engine" desc="Zero-config databases. Defining 'model' schemas, auto-migrations, and data types." />
          <ChapterCard num={7} title="CRUD Operations" desc="Native database querying. Insert, find, update, and delete records instantly." />
          <ChapterCard num={8} title="HTTP Server Magic" desc="Firing up the high-speed ASGI server using the '--web' flag in one command." />
          <ChapterCard num={9} title="REST APIs & Routes" desc="Creating 'route' blocks, handling GET/POST, and structuring JSON API responses." />
          <ChapterCard num={10} title="Authentication & Security" desc="Managing user sessions, cookies, and securing routes from unauthorized access." />
        </PhaseSection>

        {/* Phase 3 */}
        <PhaseSection badge="P3" color="pink" title="Frontend UI & UX (Visual Design)" level="Intermediate">
          <ChapterCard num={11} title="Declarative UI Tree" desc="Building interfaces natively using Page, Column, Row, and Stack widgets." />
          <ChapterCard num={12} title="Beautiful Styling" desc="Colors, padding, margins, and borders. Making your app look premium out of the box." />
          <ChapterCard num={13} title="Reactive State" desc="State management made easy. Watch your UI update instantly when variables change." />
          <ChapterCard num={14} title="Interactive Forms" desc="Handling user input, buttons, password fields, and binding onClick actions." />
          <ChapterCard num={15} title="Project: WhatsApp Clone" desc="Putting it all together to build a fully functional real-time chat UI." />
        </PhaseSection>

        {/* Phase 4 */}
        <PhaseSection badge="P4" color="green" title="Machine Learning & AI (Data Science)" level="Intermediate">
          <ChapterCard num={16} title="Native AI Engine" desc="Why AAYU doesn't need external libraries like PyTorch or Scikit-Learn." />
          <ChapterCard num={17} title="K-Means Clustering" desc="Training your first unsupervised clustering model entirely in AAYU bytecode." />
          <ChapterCard num={18} title="Neural Networks" desc="Building layers, weights, biases, and activation functions from scratch natively." />
          <ChapterCard num={19} title="RAG Systems" desc="Retrieval-Augmented Generation basics. Processing documents for AI context." />
          <ChapterCard num={20} title="AI Data Pipelines" desc="Cleaning, normalizing, and streaming data directly from the AAYU database into models." />
        </PhaseSection>

        {/* Phase 5 */}
        <PhaseSection badge="P5" color="yellow" title="Graphs & Data Visualization (Analytics)" level="Intermediate">
          <ChapterCard num={21} title="The Chart Widget" desc="Rendering native Line Charts, Bar Graphs, and Pie Charts directly in your AAYU UI." />
          <ChapterCard num={22} title="Real-time Data Streaming" desc="Feeding live API/Database metrics into graphs for live dashboards." />
          <ChapterCard num={23} title="Plotting ML Predictions" desc="Visualizing K-Means clusters and Neural Network boundaries dynamically." />
          <ChapterCard num={24} title="Interactive Graphs" desc="Adding hover states, tooltips, and zoom functionality to your data plots." />
          <ChapterCard num={25} title="Project: Admin Dashboard" desc="Building a beautiful financial dashboard with analytics and live data charts." />
        </PhaseSection>

        {/* Phase 6 */}
        <PhaseSection badge="P6" color="red" title="Game Development (AAYU Game Engine)" level="Advanced">
          <ChapterCard num={26} title="Game Loop & Ticks" desc="Understanding the core event loop, FPS management, and delta time." />
          <ChapterCard num={27} title="The Canvas Widget" desc="Drawing 2D shapes, sprites, and handling pixel-perfect rendering." />
          <ChapterCard num={28} title="Physics & Collision" desc="Implementing gravity, velocity, and AABB collision detection natively." />
          <ChapterCard num={29} title="Keyboard & Mouse Input" desc="Binding player movement, jumping, and shooting to real-time events." />
          <ChapterCard num={30} title="Project: Flappy Bird" desc="Building a complete, playable 2D game in a single .aayu file." />
        </PhaseSection>

        {/* Phase 7 */}
        <PhaseSection badge="P7" color="cyan" title="Advanced Engineering (Pro Patterns)" level="Advanced">
          <ChapterCard num={31} title="Actions & Closures" desc="Deep dive into 'action' blocks, closures, higher-order functions, and callback patterns." />
          <ChapterCard num={32} title="Error Handling & Exceptions" desc="Using try/catch/throw blocks, custom error types, and graceful failure recovery." />
          <ChapterCard num={33} title="Async & Concurrency" desc="Understanding AAYU's async runtime, parallel task execution, and non-blocking I/O." />
          <ChapterCard num={34} title="WebSocket Magic" desc="Building real-time bi-directional communication channels for live apps." />
          <ChapterCard num={35} title="File I/O & Streams" desc="Reading, writing, and streaming files. CSV parsing, JSON import/export." />
        </PhaseSection>

        {/* Phase 8 */}
        <PhaseSection badge="P8" color="orange" title="Package Ecosystem (Extensibility)" level="Advanced">
          <ChapterCard num={36} title="The Package System" desc="Understanding AAYU's official package registry, importing, and versioning." />
          <ChapterCard num={37} title="Building Your Own Package" desc="Creating, structuring, signing, and publishing reusable AAYU packages." />
          <ChapterCard num={38} title="Foreign Library Bridges" desc="Calling C, Rust, Python, and JavaScript libraries from AAYU code." />
          <ChapterCard num={39} title="The AAYU LSP" desc="How the Language Server Protocol powers VS Code autocomplete and diagnostics." />
          <ChapterCard num={40} title="Project: Full-Stack Social App" desc="Building a complete Instagram-like social media platform." />
        </PhaseSection>

        {/* Phase 9 */}
        <PhaseSection badge="P9" color="emerald" title="DevOps & Deployment (Ship It!)" level="Expert">
          <ChapterCard num={41} title="Docker & Containers" desc="Containerizing your AAYU application for cloud deployment." />
          <ChapterCard num={42} title="CI/CD Pipelines" desc="Setting up GitHub Actions for automated testing and deployment." />
          <ChapterCard num={43} title="Cloud Deployment" desc="Deploying to Vercel, Railway, and AWS with one command." />
          <ChapterCard num={44} title="Monitoring & Logging" desc="Built-in telemetry, structured logging, and performance monitoring." />
          <ChapterCard num={45} title="Project: Production API" desc="Building and deploying a production-grade REST API with auth, rate limiting, and monitoring." />
        </PhaseSection>

        {/* Phase 10 */}
        <PhaseSection badge="P10" color="amber" title="Mastery & Beyond (Compiler Hacking)" level="Expert">
          <ChapterCard num={46} title="Compiler Internals" desc="Understanding AAYU's 7-stage compiler: Lexer→Parser→AST→HIR→MIR→LIR→Bytecode." />
          <ChapterCard num={47} title="VM & Bytecode Deep Dive" desc="How the stack-based virtual machine executes instructions, GC internals." />
          <ChapterCard num={48} title="Custom Opcodes & Extensions" desc="Extending the AAYU VM with your own custom bytecode instructions." />
          <ChapterCard num={49} title="Contributing to AAYU" desc="How to contribute to the open-source AAYU compiler and runtime." />
          <ChapterCard num={50} title="The Future of Intent Computing" desc="Ayush's vision for AAYU, the roadmap, and where intent-to-silicon goes next." />
        </PhaseSection>

      </main>
    </div>
  );
}

const colorMap: Record<string, { badge: string; border: string; text: string; level: string }> = {
  purple: { badge: "bg-zinc-900 border-zinc-700 text-purple-400", border: "border-purple-500/20", text: "text-purple-400", level: "bg-purple-500/10 text-purple-300 border-purple-500/30" },
  blue: { badge: "bg-zinc-900 border-zinc-700 text-blue-400", border: "border-blue-500/20", text: "text-blue-400", level: "bg-blue-500/10 text-blue-300 border-blue-500/30" },
  pink: { badge: "bg-zinc-900 border-zinc-700 text-pink-400", border: "border-pink-500/20", text: "text-pink-400", level: "bg-pink-500/10 text-pink-300 border-pink-500/30" },
  green: { badge: "bg-zinc-900 border-zinc-700 text-green-400", border: "border-green-500/20", text: "text-green-400", level: "bg-green-500/10 text-green-300 border-green-500/30" },
  yellow: { badge: "bg-zinc-900 border-zinc-700 text-yellow-400", border: "border-yellow-500/20", text: "text-yellow-400", level: "bg-yellow-500/10 text-yellow-300 border-yellow-500/30" },
  red: { badge: "bg-zinc-900 border-zinc-700 text-red-400", border: "border-red-500/20", text: "text-red-400", level: "bg-red-500/10 text-red-300 border-red-500/30" },
  cyan: { badge: "bg-zinc-900 border-zinc-700 text-cyan-400", border: "border-cyan-500/20", text: "text-cyan-400", level: "bg-cyan-500/10 text-cyan-300 border-cyan-500/30" },
  orange: { badge: "bg-zinc-900 border-zinc-700 text-orange-400", border: "border-orange-500/20", text: "text-orange-400", level: "bg-orange-500/10 text-orange-300 border-orange-500/30" },
  emerald: { badge: "bg-zinc-900 border-zinc-700 text-emerald-400", border: "border-emerald-500/20", text: "text-emerald-400", level: "bg-emerald-500/10 text-emerald-300 border-emerald-500/30" },
  amber: { badge: "bg-zinc-900 border-zinc-700 text-amber-400", border: "border-amber-500/20", text: "text-amber-400", level: "bg-amber-500/10 text-amber-300 border-amber-500/30" },
};

function PhaseSection({ badge, color, title, level, children }: { badge: string; color: string; title: string; level: string; children: React.ReactNode }) {
  const c = colorMap[color] || colorMap.purple;
  return (
    <div className="mb-16">
      <h2 className="text-3xl font-bold mb-6 flex items-center gap-3 border-b border-zinc-800 pb-4 flex-wrap">
        <span className={`flex items-center justify-center w-10 h-10 rounded-lg border text-sm ${c.badge}`}>{badge}</span>
        <span className="flex-1">{title}</span>
        <span className={`text-xs font-medium px-3 py-1 rounded-full border ${c.level}`}>{level}</span>
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {children}
      </div>
    </div>
  );
}

function ChapterCard({ num, title, desc }: { num: number; title: string; desc: string }) {
  return (
    <Link href={`/tutorial/chapter-${num}`} className="block">
      <div className="group relative p-6 rounded-xl border border-zinc-800 bg-zinc-950/50 hover:bg-zinc-900 transition-all cursor-pointer overflow-hidden hover:shadow-[0_0_20px_rgba(168,85,247,0.15)] hover:border-purple-500/30 h-full">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
        <div className="relative z-10 flex flex-col h-full">
          <div className="flex items-center justify-between mb-3">
            <div className="text-3xl font-black text-zinc-800 group-hover:text-purple-400 transition-colors">
              {num.toString().padStart(2, '0')}
            </div>
            <svg className="w-5 h-5 text-zinc-700 group-hover:text-purple-400 group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </div>
          <div>
            <h3 className="text-xl font-bold text-zinc-100 mb-2 group-hover:text-white">{title}</h3>
            <p className="text-sm text-zinc-400 leading-relaxed">{desc}</p>
          </div>
        </div>
      </div>
    </Link>
  );
}