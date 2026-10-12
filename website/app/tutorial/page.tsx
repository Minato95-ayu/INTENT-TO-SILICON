import Link from 'next/link';
import { chapters } from '@/lib/tutorial-data';

export default function TutorialPage() {
  return (
    <main className="min-h-screen bg-black px-4 pb-24 pt-32 text-white">
      <div className="mx-auto max-w-6xl">
        <header className="mb-12 max-w-3xl">
          <p className="mb-3 text-sm font-semibold uppercase tracking-widest text-cyan-300">Verified core course · 6 lessons</p>
          <h1 className="mb-5 text-5xl font-extrabold tracking-tight md:text-7xl">Learn AAYU by running it</h1>
          <p className="text-lg leading-8 text-zinc-400">
            A beginner path through the language subset exercised by the repository regressions: values, arithmetic, loops, conditions, and a small complete program. Each lesson links to checked-in source. The test harness checks program output; it does not certify features outside these examples.
          </p>
        </header>

        <div className="mb-10 rounded-xl border border-amber-500/30 bg-amber-500/5 p-5 text-sm leading-6 text-amber-100">
          This course covers the verified core subset. HTTP/SQL apps, functions, async, AI/ML, UI interaction, and package publishing are not taught as working AAYU features here. See <Link className="underline" href="/docs/1-getting-started/1-installation">installation</Link> and the repository <Link className="underline" href="https://github.com/Minato95-ayu/INTENT-TO-SILICON/blob/main/KNOWN_LIMITATIONS.md">known limitations</Link>.
        </div>

        <section aria-label="Course lessons" className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {chapters.map((chapter) => (
            <Link key={chapter.slug} href={`/tutorial/${chapter.slug}`} className="group rounded-xl border border-zinc-800 bg-zinc-950 p-6 transition hover:border-cyan-500/40 hover:bg-zinc-900">
              <div className="mb-4 text-sm font-mono text-cyan-300">LESSON {String(chapter.num).padStart(2, '0')} · VERIFIED SOURCE</div>
              <h2 className="mb-3 text-xl font-bold group-hover:text-cyan-100">{chapter.title}</h2>
              <p className="text-sm leading-6 text-zinc-400">{chapter.description}</p>
              <p className="mt-5 text-sm text-cyan-300">Open lesson →</p>
            </Link>
          ))}
        </section>
      </div>
    </main>
  );
}
