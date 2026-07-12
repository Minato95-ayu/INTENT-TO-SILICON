import os
import re

def fix_file(filepath, replacements):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for old, new in replacements:
            # We'll use regex to handle any corrupted whitespace
            if type(old) is str:
                content = content.replace(old, new)
            else:
                content = re.sub(old, new, content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filepath}")
    except Exception as e:
        print(f"Error {filepath}: {e}")

repo = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website'

fix_file(os.path.join(repo, 'lib', 'mdx.ts'), [
    (r'\$\{slug\}\.mdx\)', '${slug}.mdx)'),
    (r'path\.join\(DOCS_DIR, category, \$\{slug\}\.mdx\);', 'path.join(DOCS_DIR, category, f"{slug}.mdx");'.replace('f"{slug}.mdx"', '${slug}.mdx'))
])

fix_file(os.path.join(repo, 'data', 'language-content.tsx'), [
    (r'\{enum Result<T, E>', 'enum Result<T, E>'),
    (r'enum Result<T, E>', '{"enum Result<T, E>"}')
])

fix_file(os.path.join(repo, 'app', 'brainos', 'live', 'page.tsx'), [
    (re.compile(r'className=\{.*?ransition-all duration-700.*?\}'), 'className="transition-all duration-700"')
])

fix_file(os.path.join(repo, 'app', 'brainos', 'page.tsx'), [
    (re.compile(r'className=\{.*?lex items-center gap-4 p-4 rounded-xl cursor-pointer transition.*?\}'), 'className="flex items-center gap-4 p-4 rounded-xl cursor-pointer transition-all"')
])

fix_file(os.path.join(repo, 'app', 'docs', 'layout.tsx'), [
    (re.compile(r'className=\{\\ md:block w-full.*?\}'), 'className="hidden md:block w-full md:w-64 lg:w-72 border-r border-white/10 bg-[#0a0a0a]"')
])

fix_file(os.path.join(repo, 'app', 'examples', 'page.tsx'), [
    (re.compile(r'className=\{w-12 h-12 rounded-xl.*?\}'), 'className="w-12 h-12 rounded-xl border flex items-center justify-center"')
])

fix_file(os.path.join(repo, 'app', 'features', 'compiler', 'page.tsx'), [
    (re.compile(r'className=\{w-64 p-4 rounded-xl border transition-all.*?\}'), 'className="w-64 p-4 rounded-xl border transition-all duration-300 flex items-center"')
])

fix_file(os.path.join(repo, 'app', 'showcase', 'page.tsx'), [
    (re.compile(r'className=\{px-2 py-0\.5 text-xs font-bold uppercase tracking-wider.*?\}'), 'className="px-2 py-0.5 text-xs font-bold uppercase tracking-wider"')
])

fix_file(os.path.join(repo, 'data', 'docs.ts'), [
    (r'items: DocItem\[;', 'items: DocItem[];')
])

fix_file(os.path.join(repo, 'app', 'download', 'page.tsx'), [
    (r', Github } from "lucide-react";', '} from "lucide-react";'),
    (r'<Github ', '<Code2 ')
])

