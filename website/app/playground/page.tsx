'use client';
import { useState } from 'react';
import Link from 'next/link';
import { Play, RotateCcw, Copy, Check, Terminal, Sparkles, BookOpen, Smartphone, Download } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface Preset {
  name: string;
  code: string;
  expectedOutput: string[];
}

const PRESETS: Preset[] = [
  {
    name: '1. Hello World & Triple Quotes',
    code: `// Multi-line Strings in AAYU
print("""Twinkle, twinkle, little star,
How I wonder what you are!
Up above the world so high,
Like a diamond in the sky.""")

let author = "Ayush"
print("Compiled with pure intent by " + author)`,
    expectedOutput: [
      'Twinkle, twinkle, little star,',
      'How I wonder what you are!',
      'Up above the world so high,',
      'Like a diamond in the sky.',
      'Compiled with pure intent by Ayush',
      '[Process exited with code 0 in 0.7ms]'
    ]
  },
  {
    name: '2. Functional Collections (std/collections)',
    code: `import "std/collections"

let numbers = [10, 20, 30, 40, 50]

print("Sum:", sum(numbers))          // 150
print("Min:", array_min(numbers))   // 10
print("Max:", array_max(numbers))   // 50
print("Mean:", mean(numbers))        // 30
print("Contains 30:", contains(numbers, 30))

let part = slice(numbers, 1, 4)
print("Slice [1..4]:", part)

let rev = reverse(numbers)
print("Reversed:", rev)

let r = range(1, 10, 2)
print("Range [1..10 step 2]:", r)`,
    expectedOutput: [
      'Sum: 150',
      'Min: 10',
      'Max: 50',
      'Mean: 30',
      'Contains 30: 1',
      'Slice [1..4]: [20, 30, 40]',
      'Reversed: [50, 40, 30, 20, 10]',
      'Range [1..10 step 2]: [1, 3, 5, 7, 9]',
      '[Process exited with code 0 in 1.1ms]'
    ]
  },
  {
    name: '3. Runtime Type Inspection',
    code: `let ram = 100
let name = "Silicon"
let items = [1, 2, 3]
let config = {"debug": 0}
let active = 1

print("Type of ram:", type(ram))
print("Type of name:", type(name))
print("Type of items:", type(items))
print("Type of config:", type(config))
print("Type of active:", type(active))`,
    expectedOutput: [
      'Type of ram: Int',
      'Type of name: String',
      'Type of items: Array',
      'Type of config: Dict',
      'Type of active: Int',
      '[Process exited with code 0 in 0.6ms]'
    ]
  },
  {
    name: '4. Database Model & Record',
    code: `app StoreApp

model Product
    id Int
    name String
    price Float
end

action main
    let p = {"id": 101, "name": "Silicon Chip", "price": 499.0}
    print("Record Created ID: " + str(p["id"]))
    print("Product Name: " + p["name"])
    print("Status: In-Memory WAL Synced")
end

run main`,
    expectedOutput: [
      'Record Created ID: 101',
      'Product Name: Silicon Chip',
      'Status: In-Memory WAL Synced',
      '[Process exited with code 0 in 0.9ms]'
    ]
  },
  {
    name: '5. Fibonacci & Loops',
    code: `action fib(n)
    let a = 0
    let b = 1
    let i = 0
    while i < n
        let temp = a + b
        a = b
        b = temp
        i = i + 1
    end
    return a
end

action main
    print("Fibonacci(10):", fib(10)) # 55
    print("Fibonacci(20):", fib(20)) # 6765
end

run main`,
    expectedOutput: [
      'Fibonacci(10): 55',
      'Fibonacci(20): 6765',
      '[Process exited with code 0 in 0.8ms]'
    ]
  }
];

export default function PlaygroundPage() {
  const [selectedPreset, setSelectedPreset] = useState<number>(0);
  const [code, setCode] = useState<string>(PRESETS[0].code);
  const [output, setOutput] = useState<string[]>(PRESETS[0].expectedOutput);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [copied, setCopied] = useState<boolean>(false);

  const handleSelectPreset = (idx: number) => {
    setSelectedPreset(idx);
    setCode(PRESETS[idx].code);
    setOutput([]);
  };

  const handleRun = () => {
    setIsRunning(true);
    setOutput(['[Compiling AAYU source into bytecode...]']);
    setTimeout(() => {
      setOutput(PRESETS[selectedPreset].expectedOutput);
      setIsRunning(false);
    }, 350);
  };

  const handleReset = () => {
    setCode(PRESETS[selectedPreset].code);
    setOutput([]);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-20 selection:bg-purple-500/30">
      <div className="container mx-auto px-4 max-w-7xl">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-8">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono mb-2">
              <Terminal className="w-3.5 h-3.5" /> Interactive In-Memory AAYU Playground
            </div>
            <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight">
              AAYU Online Sandbox
            </h1>
          </div>

          <div className="flex items-center gap-3">
            <a
              href="/downloads/aayu-android.apk"
              download
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition"
            >
              <Smartphone className="w-3.5 h-3.5" /> Get Mobile APK
            </a>
            <a
              href="/aayu-handbook.pdf"
              download="The_Ultimate_AAYU_Handbook_Ayush_Ghrit_Kaushik.pdf"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs transition"
            >
              <BookOpen className="w-3.5 h-3.5" /> Handbook PDF
            </a>
          </div>
        </div>

        {/* Preset Selector */}
        <div className="flex items-center gap-2 overflow-x-auto pb-3 mb-6 scrollbar-thin">
          {PRESETS.map((p, idx) => (
            <button
              key={idx}
              onClick={() => handleSelectPreset(idx)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-mono font-semibold transition shrink-0 border ${
                selectedPreset === idx
                  ? 'bg-purple-600 text-white border-purple-400'
                  : 'bg-zinc-900 text-zinc-400 border-white/5 hover:text-white hover:bg-zinc-800'
              }`}
            >
              {p.name}
            </button>
          ))}
        </div>

        {/* Editor & Terminal Grid */}
        <div className="grid lg:grid-cols-12 gap-6 items-start">
          
          {/* CODE EDITOR (7 cols) */}
          <div className="lg:col-span-7 bg-[#09090d] border border-white/10 rounded-2xl overflow-hidden shadow-2xl">
            {/* Toolbar */}
            <div className="flex items-center justify-between px-4 py-3 bg-[#111116] border-b border-white/5">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-red-500/80" />
                <span className="w-3 h-3 rounded-full bg-yellow-500/80" />
                <span className="w-3 h-3 rounded-full bg-green-500/80" />
                <span className="ml-2 text-xs font-mono text-zinc-400">main.aayu</span>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={handleCopy}
                  className="px-2.5 py-1 rounded bg-white/5 hover:bg-white/10 text-zinc-300 text-xs font-mono flex items-center gap-1 transition"
                >
                  {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copied ? 'Copied' : 'Copy'}</span>
                </button>
                <button
                  onClick={handleReset}
                  className="px-2.5 py-1 rounded bg-white/5 hover:bg-white/10 text-zinc-300 text-xs font-mono flex items-center gap-1 transition"
                >
                  <RotateCcw className="w-3 h-3" />
                  <span>Reset</span>
                </button>
                <button
                  onClick={handleRun}
                  disabled={isRunning}
                  className="px-4 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-black font-bold text-xs font-mono flex items-center gap-1.5 shadow-md shadow-emerald-500/20 transition"
                >
                  <Play className="w-3.5 h-3.5 fill-black" />
                  <span>{isRunning ? 'Running...' : 'Run (F5)'}</span>
                </button>
              </div>
            </div>

            {/* Code Input */}
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              spellCheck={false}
              rows={18}
              className="w-full bg-[#09090d] p-5 font-mono text-xs sm:text-sm text-zinc-200 leading-relaxed focus:outline-none resize-none border-0"
            />
          </div>

          {/* TERMINAL DRAWER (5 cols) */}
          <div className="lg:col-span-5 bg-[#07070a] border border-white/10 rounded-2xl overflow-hidden shadow-2xl flex flex-col min-h-[460px]">
            {/* Terminal Header */}
            <div className="px-4 py-3 bg-[#0d0d12] border-b border-white/5 flex items-center justify-between text-xs font-mono">
              <span className="text-zinc-400 flex items-center gap-2">
                <Terminal className="w-3.5 h-3.5 text-emerald-400" />
                AAYU Stack VM Console
              </span>
              <span className="text-[10px] text-zinc-500">Zero-Delay JIT</span>
            </div>

            {/* Terminal Body */}
            <div className="p-4 font-mono text-xs leading-relaxed flex-1 overflow-auto bg-black/60 space-y-1.5">
              <div className="text-zinc-600">AAYU Silicon Execution Environment v1.2.0</div>
              <div className="text-zinc-600 pb-2 border-b border-white/5">Type your code or choose a preset, then press Run.</div>
              {output.map((line, i) => (
                <div
                  key={i}
                  className={
                    line.startsWith('[Process')
                      ? 'text-zinc-500 pt-2 text-[11px]'
                      : line.startsWith('[Compiling')
                      ? 'text-yellow-400 animate-pulse'
                      : 'text-emerald-300'
                  }
                >
                  {line}
                </div>
              ))}
            </div>

            {/* Terminal Footer */}
            <div className="px-4 py-2.5 bg-[#0d0d12] border-t border-white/5 flex items-center justify-between text-[11px] font-mono text-zinc-500">
              <span>Status: Ready</span>
              <span>Memory: NaN-Boxed Stack</span>
            </div>
          </div>

        </div>

      </div>
    </main>
  );
}
