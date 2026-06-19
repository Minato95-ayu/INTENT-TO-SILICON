import fs from "fs";
import path from "path";
import matter from "gray-matter";
import { MDXRemote } from "next-mdx-remote/rsc";

export async function generateStaticParams() {
  const docsDirectory = path.join(process.cwd(), "docs");
  const filenames = fs.readdirSync(docsDirectory);

  return filenames.map((filename) => ({
    slug: filename.replace(".mdx", ""),
  }));
}

function getDocContent(slug: string) {
  const fullPath = path.join(process.cwd(), "docs", `${slug}.mdx`);
  if (!fs.existsSync(fullPath)) return null;
  const fileContents = fs.readFileSync(fullPath, "utf8");
  const { content, data } = matter(fileContents);
  return { content, frontmatter: data };
}

export default async function DocPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const doc = getDocContent(slug);

  if (!doc) {
    return (
      <div className="prose">
        <h1>404 - Document Not Found</h1>
        <p>The document `{slug}` could not be found.</p>
      </div>
    );
  }

  return (
    <article className="prose prose-invert max-w-3xl">
      <MDXRemote source={doc.content} />
    </article>
  );
}
