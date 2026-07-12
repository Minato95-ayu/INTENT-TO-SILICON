 

import { notFound } from "next/navigation";
import { ChevronRight, ChevronLeft } from "lucide-react";
import Link from "next/link";
import { getLanguageDocContent, getAllLanguageSlugs } from "@/data/language-content";

export async function generateStaticParams() {
  const slugs = getAllLanguageSlugs();
  return slugs.map((slug) => ({ slug }));
}

export default async function LanguageDocPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const content = getLanguageDocContent(slug);

  if (!content) {
    notFound();
  }

  return (
    <div className="max-w-4xl mx-auto pb-20">
      <div className="mb-8">
        <div className="flex items-center text-sm text-zinc-500 mb-4">
          <Link href="/language" className="hover:text-white transition-colors">Language</Link>
          <ChevronRight className="h-4 w-4 mx-1" />
          <span className="text-zinc-300">{content.title}</span>
        </div>
        <h1 className="text-4xl font-extrabold tracking-tight mb-4">{content.title}</h1>
        <p className="text-xl text-zinc-400 leading-relaxed">{content.description}</p>
      </div>

      <div className="prose prose-invert prose-blue max-w-none">
        {content.body}
      </div>

      <div className="mt-16 pt-8 border-t border-white/10 flex items-center justify-between">
        {content.prev ? (
          <Link href={`/language/${content.prev.slug}`} className="group flex flex-col items-start gap-1">
            <span className="text-xs text-zinc-500 uppercase tracking-wider group-hover:text-zinc-400">Previous</span>
            <span className="text-blue-400 group-hover:text-blue-300 font-medium flex items-center gap-2">
              <ChevronLeft className="h-4 w-4" /> {content.prev.title}
            </span>
          </Link>
        ) : <div />}

        {content.next ? (
          <Link href={`/language/${content.next.slug}`} className="group flex flex-col items-end gap-1">
            <span className="text-xs text-zinc-500 uppercase tracking-wider group-hover:text-zinc-400">Next</span>
            <span className="text-blue-400 group-hover:text-blue-300 font-medium flex items-center gap-2">
              {content.next.title} <ChevronRight className="h-4 w-4" />
            </span>
          </Link>
        ) : <div />}
      </div>
    </div>
  );
}
