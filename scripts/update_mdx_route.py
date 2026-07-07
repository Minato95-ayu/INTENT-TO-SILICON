import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\docs\[...slug]\page.tsx'

content = '''
import { MDXRemote } from "next-mdx-remote/rsc";
import { getDocBySlug } from "@/lib/mdx";
import { notFound } from "next/navigation";
import { CodeBlock, ErrorBlock, PipelineDiagram, PageNav } from "@/components/docs/DocsComponents";
import { AlertTriangle } from "lucide-react";

// The custom components we pass into MDX
const components = {
  CodeBlock,
  ErrorBlock,
  PipelineDiagram,
  PageNav,
  // We can also override standard HTML elements if we want to style them
  h1: (props: any) => <h1 className="text-4xl font-extrabold mb-6" {...props} />,
  h2: (props: any) => <h2 className="text-2xl font-bold mt-12 mb-4 border-b border-white/10 pb-2" {...props} />,
  p: (props: any) => <p className="text-zinc-400 leading-relaxed mb-6" {...props} />,
  code: (props: any) => <code className="bg-white/10 text-blue-300 px-1.5 py-0.5 rounded font-mono text-sm" {...props} />
};

export default function DocPage({ params }: { params: { slug: string[] } }) {
  if (params.slug.length < 2) {
    notFound();
  }

  const category = params.slug[0];
  const slug = params.slug[1];
  
  const doc = getDocBySlug(category, slug);

  if (!doc) {
    // Fallback UI for pages that haven't been written in Markdown yet
    return (
      <>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-yellow-500/10 border border-yellow-500/20 text-yellow-500 text-xs font-bold mb-6">
          <AlertTriangle className="w-4 h-4" /> Documentation in Progress
        </div>
        <h1 className="text-4xl font-extrabold mb-4 capitalize">{slug.replace("-", " ")}</h1>
        <p className="text-zinc-400">
          This page is currently being drafted by the AAYU team and will be available in the upcoming v1.0 release.
        </p>
        <div className="mt-12">
          <PipelineDiagram stages={["Drafting", "Review", "Publishing"]} />
        </div>
      </>
    );
  }

  return (
    <>
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold mb-4">{doc.frontmatter.title}</h1>
        {doc.frontmatter.description && (
          <p className="text-xl text-zinc-400">{doc.frontmatter.description}</p>
        )}
      </div>
      
      {/* Render the MDX Content */}
      <MDXRemote source={doc.content} components={components} />
    </>
  );
}
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated dynamic route to use next-mdx-remote.")
