import Link from 'next/link';

export const metadata = {
  title: 'Benchmarks | AAYU',
  description: 'Twenty distinct correctness-checked AAYU core workload benchmarks.',
};

const rows = [
  ['Integer addition accumulator', 10000, '49995000', 73.546, 70.314, 199.249],
  ['Integer subtraction countdown', 10000, '0', 74.215, 70.876, 155.731],
  ['Integer multiply-accumulate', 10000, '149985000', 76.679, 74.669, 91.06],
  ['Integer divide-accumulate', 10000, '24995000', 112.868, 87.982, 163.001],
  ['Float half-step accumulation', 10000, '5000', 75.452, 70.692, 77.032],
  ['Float multiply-accumulate', 10000, '24997500', 73.279, 70.933, 77.946],
  ['Less-than true branch', 10000, '5000', 72.851, 71.212, 77.565],
  ['Greater-than true branch', 10000, '4999', 72.784, 72.227, 77.527],
  ['Equality branch', 10000, '1', 73.867, 70.723, 78.43],
  ['Inequality branch', 10000, '9999', 74.745, 71.805, 78.093],
  ['Less-or-equal branch', 10000, '5001', 72.496, 71.005, 76.236],
  ['Greater-or-equal branch', 10000, '5000', 73.431, 70.292, 77.896],
  ['Nested loop counter', 10000, '10000', 76.886, 70.722, 80.723],
  ['Nested loop weighted sum', 10000, '495000', 73.169, 69.788, 81.36],
  ['Mixed multiply and subtract', 10000, '49995000', 73.878, 72.859, 99.137],
  ['Multiply then divide', 10000, '249975000', 74.592, 70.753, 82.061],
  ['Descending sum', 10000, '50005000', 75.985, 72.07, 86.114],
  ['Variable copy and accumulate', 10000, '49995000', 73.45, 69.887, 99.145],
  ['Nested conditional branches', 10000, '19999', 74.717, 72.385, 78.386],
  ['Comparison loop boundary', 10000, '50005000', 71.639, 70.375, 77.727],
] as const;

export default function BenchmarksPage() {
  return (
    <main className="min-h-screen bg-black px-4 py-24 text-white">
      <div className="mx-auto max-w-6xl">
        <header className="mb-10">
          <h1 className="mb-5 text-4xl font-bold md:text-5xl">AAYU core workload matrix</h1>
          <p className="max-w-3xl text-lg leading-7 text-zinc-400">
            Twenty distinct benchmark programs from the currently supported AAYU core subset, all run at N=10,000. Every case checks its output. These timings include launching the VM process and loading bytecode; compilation is excluded.
          </p>
        </header>

        <div className="mb-8 rounded-xl border border-white/10 bg-zinc-900 p-6 text-sm leading-6 text-zinc-300">
          <strong className="text-white">Recorded environment:</strong> Windows 10.0.26300, Intel64 Family 6 Model 142, 8 logical processors, x64, Rust VM crate v0.3.1. One warm-up, 11 measured runs per case. Process startup dominates these short workloads; use them as a correctness-checked workload catalog, not instruction-level VM throughput or a language shootout.
        </div>

        <div className="overflow-x-auto rounded-xl border border-white/10">
          <table className="w-full border-collapse text-left text-sm">
            <thead className="bg-zinc-900 text-zinc-300">
              <tr>{['Workload', 'Input size', 'Expected output', 'Median ms', 'Min ms', 'Max ms'].map((label) => <th key={label} className="px-4 py-3">{label}</th>)}</tr>
            </thead>
            <tbody>
              {rows.map(([workload, n, expected, median, min, max], index) => (
                <tr key={`${workload}-${n}`} className="border-t border-white/5 odd:bg-white/[0.02]">
                  <td className="px-4 py-3">{String(index + 1).padStart(2, '0')} · {workload}</td>
                  <td className="px-4 py-3 font-mono">{n.toLocaleString()}</td>
                  <td className="px-4 py-3 font-mono">{expected}</td>
                  <td className="px-4 py-3 font-mono text-cyan-300">{median.toFixed(3)}</td>
                  <td className="px-4 py-3 font-mono text-zinc-400">{min.toFixed(3)}</td>
                  <td className="px-4 py-3 font-mono text-zinc-400">{max.toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <p className="mt-6 text-sm leading-6 text-zinc-400">
          Reproduce with <code>powershell -ExecutionPolicy Bypass -File benchmarks/run_workload_matrix.ps1</code>. The script regenerates the report on your machine; timings will vary. See the <Link className="text-cyan-300 underline" href="https://github.com/Minato95-ayu/INTENT-TO-SILICON/blob/main/benchmarks/BENCHMARK_MATRIX_RESULTS.md">full recorded artifact</Link> and the <Link className="text-cyan-300 underline" href="https://github.com/Minato95-ayu/INTENT-TO-SILICON/blob/main/benchmarks/run_workload_matrix.ps1">runner source</Link>.
        </p>
      </div>
    </main>
  );
}
