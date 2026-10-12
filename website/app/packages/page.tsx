import Link from 'next/link';
import { Package } from 'lucide-react';

const modules = ['ai.aayu', 'crypto.aayu', 'db.aayu', 'fs.aayu', 'http.aayu', 'ledger.aayu', 'math.aayu', 'server.aayu', 'ui.aayu'];

export default function PackagesPage() {
  return (
    <main className="min-h-screen pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-5xl text-center">
        <Package className="w-16 h-16 text-blue-500 mx-auto mb-6" />
        <h1 className="text-5xl font-bold mb-6">AAYU Standard-Library Sources</h1>
        <p className="text-xl text-zinc-400 mb-12">These AAYU source modules are present under <code>std/</code>. Presence in the repository does not guarantee complete runtime integration or production readiness; check each module before using it.</p>
        <ul className="grid md:grid-cols-3 sm:grid-cols-2 gap-4 text-left">
          {modules.map((module) => (
            <li key={module} className="bg-[#050505] border border-white/10 p-5 rounded-xl font-mono text-cyan-300">std/{module}</li>
          ))}
        </ul>
        <p className="mt-10 text-zinc-400">The current VM CLI does not provide a package-registry command. See <Link className="text-cyan-400 underline" href="https://github.com/Minato95-ayu/INTENT-TO-SILICON/blob/main/KNOWN_LIMITATIONS.md">known limitations</Link>.</p>
      </div>
    </main>
  );
}
