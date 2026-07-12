 
import { getDocItem, documentationData } from "@/data/docs";
import { notFound } from "next/navigation";
import { Copy } from "lucide-react";
import Link from "next/link";

export default async function DocPage({ params }: { params: Promise<{ slug: string }> }) {
  const resolvedParams = await params;
  const doc = getDocItem(resolvedParams.slug);
  
  if (!doc) {
    notFound();
  }

  // Find prev/next links
  let prev = null;
  let next = null;
  const flatDocs = documentationData.flatMap(section => section.items);
  const currentIndex = flatDocs.findIndex(item => item.slug === resolvedParams.slug);
  
  if (currentIndex > 0) prev = flatDocs[currentIndex - 1];
  if (currentIndex < flatDocs.length - 1) next = flatDocs[currentIndex + 1];

  return (
    <div className="max-w-4xl pb-20">
      <h1 className="text-4xl font-extrabold tracking-tight mb-4">{doc.title}</h1>
      <p className="text-xl text-zinc-400 mb-10 leading-relaxed">{doc.introduction}</p>

      {/* Syntax Section */}
      {doc.syntax && (
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4 flex items-center gap-2 border-b border-white/10 pb-2">
            Syntax
          </h2>
          <div className="relative group rounded-xl bg-zinc-900 border border-white/10 overflow-hidden">
            <div className="absolute right-4 top-4 opacity-0 group-hover:opacity-100 transition-opacity">
              <button className="text-zinc-400 hover:text-white bg-black/50 p-2 rounded-md">
                <Copy className="h-4 w-4" />
              </button>
            </div>
            <pre className="p-6 overflow-x-auto text-sm font-mono text-zinc-300">
              <code>{doc.syntax}</code>
            </pre>
          </div>
        </section>
      )}

      {/* Examples Section */}
      {doc.examples && doc.examples.length > 0 && (
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4 border-b border-white/10 pb-2">Examples</h2>
          <div className="space-y-8">
            {doc.examples.map((ex, idx) => (
              <div key={idx} className="space-y-3">
                {ex.explanation && <p className="text-zinc-300">{ex.explanation}</p>}
                <div className="rounded-xl bg-black border border-white/10 overflow-hidden">
                  <div className="bg-zinc-900/50 px-4 py-2 text-xs font-mono text-zinc-500 border-b border-white/10">Input</div>
                  <pre className="p-4 overflow-x-auto text-sm font-mono text-blue-300">
                    <code>{ex.code}</code>
                  </pre>
                  {ex.output && (
                    <>
                      <div className="bg-zinc-900/50 px-4 py-2 text-xs font-mono text-zinc-500 border-y border-white/10">Output</div>
                      <pre className="p-4 overflow-x-auto text-sm font-mono text-green-400">
                        <code>{ex.output}</code>
                      </pre>
                    </>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Best Practices */}
      {doc.bestPractices && doc.bestPractices.length > 0 && (
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4 border-b border-white/10 pb-2 text-green-400">Best Practices</h2>
          <ul className="list-disc list-inside space-y-2 text-zinc-300">
            {doc.bestPractices.map((bp, idx) => (
              <li key={idx} className="leading-relaxed">{bp}</li>
            ))}
          </ul>
        </section>
      )}

      {/* Common Errors */}
      {doc.commonErrors && doc.commonErrors.length > 0 && (
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4 border-b border-white/10 pb-2 text-red-400">Common Errors</h2>
          <div className="space-y-4">
            {doc.commonErrors.map((ce, idx) => (
              <div key={idx} className="bg-red-500/10 border border-red-500/20 rounded-lg p-4">
                <p className="font-mono text-sm text-red-400 mb-2">{ce.error}</p>
                <p className="text-sm text-zinc-300 flex items-start gap-2">
                  <span className="text-green-400">💡 Fix:</span> {ce.fix}
                </p>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Reference */}
      {doc.reference && (
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4 border-b border-white/10 pb-2">Reference</h2>
          <p className="text-zinc-300 leading-relaxed">{doc.reference}</p>
        </section>
      )}

      {/* Navigation */}
      <div className="mt-16 pt-8 border-t border-white/10 flex items-center justify-between">
        {prev ? (
          <Link href={`/docs/${prev.slug}`} className="group flex flex-col gap-1">
            <span className="text-sm text-zinc-500 group-hover:text-zinc-400">← Previous</span>
            <span className="text-lg font-medium text-blue-400 group-hover:text-blue-300 transition-colors">{prev.title}</span>
          </Link>
        ) : <div />}
        
        {next && (
          <Link href={`/docs/${next.slug}`} className="group flex flex-col gap-1 text-right">
            <span className="text-sm text-zinc-500 group-hover:text-zinc-400">Next →</span>
            <span className="text-lg font-medium text-blue-400 group-hover:text-blue-300 transition-colors">{next.title}</span>
          </Link>
        )}
      </div>
    </div>
  );
}
