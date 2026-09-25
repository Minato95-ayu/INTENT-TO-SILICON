import Link from "next/link";
import { Monitor, Apple, Terminal, Download, Code2, Cpu, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function DownloadPage() {
  return (
    <main className="min-h-screen bg-black text-zinc-300 pt-24 pb-20 selection:bg-red-500/30">
      <div className="container mx-auto px-4 max-w-6xl">
        
        {/* Header Section */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-6">
          <div className="inline-flex items-center rounded-full border border-red-500/30 bg-red-500/10 px-3 py-1 text-sm font-medium text-red-400 backdrop-blur-sm">
            <span className="flex h-2 w-2 rounded-full bg-red-500 mr-2 animate-pulse"></span>
            AAYU v1.1.0 is now available
          </div>
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight text-white">
            Download <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-orange-500">AAYU</span>
          </h1>
          <p className="text-xl text-zinc-400">
            Write your intent. Compile to silicon. Get the zero-dependency, full-stack programming language for your system.
          </p>
        </div>

        {/* OS Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-20">
          
          {/* Windows Card */}
          <div className="group relative rounded-2xl border border-zinc-800 bg-zinc-900/50 p-8 hover:bg-zinc-900 transition-colors">
            <div className="absolute inset-0 bg-gradient-to-b from-red-500/5 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div className="relative">
              <div className="h-12 w-12 rounded-xl bg-zinc-800 flex items-center justify-center mb-6 text-white group-hover:scale-110 group-hover:bg-red-500 transition-all">
                <Monitor size={24} />
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">Windows</h3>
              <p className="text-zinc-400 mb-6 min-h-[48px]">Windows 10, 11 (x64 and ARM64). Pre-compiled native executable.</p>
              
              <Link href="/releases/aayu.exe" target="_blank">
                <Button className="w-full bg-white text-black hover:bg-zinc-200 font-semibold mb-4">
                  <Download className="mr-2 h-4 w-4" /> Download .exe
                </Button>
              </Link>
              
              <div className="bg-black/50 rounded-lg p-3 border border-zinc-800/50">
                <span className="text-xs text-zinc-500 uppercase tracking-wider mb-2 block font-sans">Recommended (Bypass SmartScreen)</span>
                <code className="text-sm text-zinc-300 font-mono block break-all">
                  irm https://intent-to-silicon.vercel.app/releases/aayu.exe -OutFile aayu.exe
                </code>
              </div>
            </div>
          </div>

          {/* macOS Card */}
          <div className="group relative rounded-2xl border border-zinc-800 bg-zinc-900/50 p-8 hover:bg-zinc-900 transition-colors">
            <div className="absolute inset-0 bg-gradient-to-b from-red-500/5 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div className="relative">
              <div className="h-12 w-12 rounded-xl bg-zinc-800 flex items-center justify-center mb-6 text-white group-hover:scale-110 group-hover:bg-red-500 transition-all">
                <Apple size={24} />
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">macOS</h3>
              <p className="text-zinc-400 mb-6 min-h-[48px]">macOS 12.0+ (Apple Silicon M1/M2/M3 & Intel).</p>
              
              <Link href="/releases/aayu-macos.pkg" target="_blank">
                  <Button className="w-full bg-zinc-800 text-white hover:bg-zinc-700 font-semibold mb-4 border border-zinc-700">
                    <Download className="mr-2 h-4 w-4" /> Download .pkg
                </Button>
              </Link>

              <div className="bg-black/50 rounded-lg p-3 border border-zinc-800/50">
                <code className="text-sm text-zinc-300 font-mono flex items-center justify-between">
                  <span>brew install aayu</span>
                </code>
              </div>
            </div>
          </div>

          {/* Linux Card */}
          <div className="group relative rounded-2xl border border-zinc-800 bg-zinc-900/50 p-8 hover:bg-zinc-900 transition-colors">
            <div className="absolute inset-0 bg-gradient-to-b from-red-500/5 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div className="relative">
              <div className="h-12 w-12 rounded-xl bg-zinc-800 flex items-center justify-center mb-6 text-white group-hover:scale-110 group-hover:bg-red-500 transition-all">
                <Terminal size={24} />
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">Linux</h3>
              <p className="text-zinc-400 mb-6 min-h-[48px]">Ubuntu, Debian, Fedora, Arch. Statically linked binaries.</p>
              
              <Link href="/releases/aayu-linux.tar.gz" target="_blank">
                  <Button className="w-full bg-zinc-800 text-white hover:bg-zinc-700 font-semibold mb-4 border border-zinc-700">
                    <Download className="mr-2 h-4 w-4" /> Download .tar.gz
                </Button>
              </Link>

              <div className="bg-black/50 rounded-lg p-3 border border-zinc-800/50">
                <code className="text-sm text-zinc-300 font-mono flex items-center justify-between">
                  <span>curl -sL https://aayu.run | bash</span>
                </code>
              </div>
            </div>
          </div>
        </div>

        {/* Source Code Section */}
        <div className="rounded-2xl border border-zinc-800 bg-zinc-900/30 p-8 md:p-12 flex flex-col md:flex-row items-center justify-between gap-8 mb-20">
          <div>
            <h2 className="text-3xl font-bold text-white mb-4">Build from Source</h2>
            <p className="text-zinc-400 max-w-2xl mb-6">
              AAYU is fully open-source and built with Python (compiler) and C (runtime). You can easily build the latest edge version directly from the repository.
            </p>
            <div className="flex gap-4">
              <Link href="https://github.com/Minato95-ayu/INTENT-TO-SILICON" target="_blank">
                  <Button className="bg-transparent border border-zinc-600 text-white hover:bg-zinc-800 font-semibold">
                    <Code2 className="mr-2 h-4 w-4" /> GitHub Repository
                </Button>
              </Link>
            </div>
          </div>
          <div className="w-full md:w-auto flex-shrink-0 bg-black rounded-xl p-6 border border-zinc-800 shadow-2xl">
            <div className="flex items-center gap-2 mb-4 border-b border-zinc-800 pb-4">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
              <span className="ml-2 text-xs text-zinc-500 font-mono">terminal</span>
            </div>
            <pre className="font-mono text-sm">
              <span className="text-green-400">git</span> <span className="text-zinc-300">clone /releases/aayu.exe</span><br/>
              <span className="text-green-400">cd</span> <span className="text-zinc-300">INTENT-TO-SILICON</span><br/>
              <span className="text-green-400">pip</span> <span className="text-zinc-300">install -e .</span><br/>
              <br/>
              <span className="text-zinc-500"># Run your first script</span><br/>
              <span className="text-red-400 font-bold">aayu</span> <span className="text-zinc-300">run hello.aayu</span>
            </pre>
          </div>
        </div>
        
        {/* Features Checklist */}
        <div className="grid md:grid-cols-3 gap-8 border-t border-zinc-800 pt-16">
          <div className="flex items-start gap-4">
            <div className="p-3 bg-red-500/10 rounded-lg text-red-400">
              <Cpu size={24} />
            </div>
            <div>
              <h4 className="text-lg font-bold text-white mb-2">Native C-Speed Execution</h4>
              <p className="text-zinc-400 text-sm">Compiles AAYU intent to raw C and invokes GCC under the hood for zero-overhead silicon execution.</p>
            </div>
          </div>
          <div className="flex items-start gap-4">
            <div className="p-3 bg-red-500/10 rounded-lg text-red-400">
              <Code2 size={24} />
            </div>
            <div>
              <h4 className="text-lg font-bold text-white mb-2">Zero Dependencies</h4>
              <p className="text-zinc-400 text-sm">No node_modules, no virtual environments. Built-in HTTP, File I/O, JSON parser, and Database.</p>
            </div>
          </div>
          <div className="flex items-start gap-4">
            <div className="p-3 bg-red-500/10 rounded-lg text-red-400">
              <Terminal size={24} />
            </div>
            <div>
              <h4 className="text-lg font-bold text-white mb-2">REPL & Playground</h4>
              <p className="text-zinc-400 text-sm">Use the built-in interactive shell, or try the WebAssembly playground directly in your browser.</p>
            </div>
          </div>
        </div>

      </div>
    </main>
  );
}
