import Link from 'next/link';
import { BarChart3, CircleCheck, Cpu } from 'lucide-react';

export default function ReportsPage() {
  return (
    <main className="min-h-screen bg-[#050505] px-4 pb-24 pt-28 text-white">
      <div className="mx-auto max-w-4xl">
        <header className="mb-10">
          <p className="mb-3 flex items-center gap-2 text-sm text-cyan-300"><BarChart3 className="h-4 w-4" /> Benchmark report</p>
          <h1 className="mb-4 text-4xl font-bold md:text-5xl">Twenty checked workload measurements</h1>
          <p className="max-w-3xl text-zinc-400">Twenty distinct AAYU core workload patterns were run at N=10,000. The runner checks expected results before recording timings and repeats each case five times.</p>
        </header>
        <div className="mb-8 grid gap-4 sm:grid-cols-2">
          <section className="rounded-xl border border-white/10 bg-[#0a0a0a] p-6">
            <h2 className="mb-3 flex items-center gap-2 font-semibold"><CircleCheck className="h-5 w-5 text-emerald-300" /> Correctness checks</h2>
            <p className="text-sm leading-6 text-zinc-400">Every matrix case has a deterministic expected output. The runner checks it on warm-up and on every timed run. The report lists expected values and timing ranges.</p>
          </section>
          <section className="rounded-xl border border-white/10 bg-[#0a0a0a] p-6">
            <h2 className="mb-3 flex items-center gap-2 font-semibold"><Cpu className="h-5 w-5 text-cyan-300" /> What the time includes</h2>
            <p className="text-sm leading-6 text-zinc-400">Wall-clock process launch and bytecode loading are included. Compilation is excluded. These short runs are dominated by process startup, so the page makes no instruction-level speed claim.</p>
          </section>
        </div>
        <Link href="/benchmarks" className="inline-flex rounded-lg bg-cyan-300 px-5 py-3 font-semibold text-black hover:bg-cyan-200">Open all 20 results →</Link>
        <p className="mt-6 text-sm text-zinc-500">Reproduce with <code>benchmarks/run_workload_matrix.ps1</code>. The original end-to-end and hand-built microkernel results are also recorded in the repository benchmark artifact, with their scope explained there.</p>
      </div>
    </main>
  );
}
