
import fs from "fs";
import path from "path";
import matter from "gray-matter";

const DOCS_DIR = path.join(process.cwd(), "content/docs");

export type DocFrontmatter = {
  title: string;
  description?: string;
  order?: number;
};

export type DocData = {
  slug: string;
  category: string;
  content: string;
  frontmatter: DocFrontmatter;
};

// Get all docs for sidebar generation and search
export function getAllDocs(): DocData[] {
  if (!fs.existsSync(DOCS_DIR)) return [];
  
  const categories = fs.readdirSync(DOCS_DIR).filter(cat => fs.statSync(path.join(DOCS_DIR, cat)).isDirectory());
  
  const allDocs: DocData[] = [];

  for (const category of categories) {
    const catPath = path.join(DOCS_DIR, category);
    const files = fs.readdirSync(catPath).filter(f => f.endsWith(".mdx"));
    
    for (const file of files) {
      const slug = file.replace(/${slug}.mdx$/, "");
      const fullPath = path.join(catPath, file);
      const fileContents = fs.readFileSync(fullPath, "utf8");
      
      const { data, content } = matter(fileContents);
      
      allDocs.push({
        slug,
        category,
        content,
        frontmatter: data as DocFrontmatter,
      });
    }
  }

  return allDocs;
}

// Get a specific doc by category and slug
export function getDocBySlug(category: string, slug: string): DocData | null {
  const fullPath = path.join(DOCS_DIR, category, `${slug}.mdx`);
  
  if (!fs.existsSync(fullPath)) return null;
  
  const fileContents = fs.readFileSync(fullPath, "utf8");
  const { data, content } = matter(fileContents);
  
  return {
    slug,
    category,
    content,
    frontmatter: data as DocFrontmatter,
  };
}

// Build Sidebar structure
export function getSidebarTree() {
  const allDocs = getAllDocs();
  
  // Group by category
  const grouped: Record<string, DocData[]> = {};
  for (const doc of allDocs) {
    if (!grouped[doc.category]) grouped[doc.category] = [];
    grouped[doc.category].push(doc);
  }
  
  // Sort inside categories
  for (const cat in grouped) {
    grouped[cat].sort((a, b) => (a.frontmatter.order || 99) - (b.frontmatter.order || 99));
  }
  
  return grouped;
}
