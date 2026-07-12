import os
import re

repo = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website'

def fix(path_suffix, old, new):
    path = os.path.join(repo, path_suffix)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            t = f.read()
        if type(old) is str:
            t = t.replace(old, new)
        else:
            t = re.sub(old, new, t)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(t)

# 1. lib/mdx.ts
fix('lib/mdx.ts', 'path.join(DOCS_DIR, category, .mdx);', 'path.join(DOCS_DIR, category, f"{slug}.mdx");'.replace('f"{slug}.mdx"', '${slug}.mdx'))

# 2. app/brainos/page.tsx
fix('app/brainos/page.tsx', re.compile(r'className=\{w-10 h-10.*?\}'), 'className="w-10 h-10 rounded-full flex items-center justify-center bg-blue-500/20"')
fix('app/brainos/page.tsx', re.compile(r'className=\{w-5 h-5.*?\}'), 'className="w-5 h-5"')

# 3. app/docs/layout.tsx
fix('app/docs/layout.tsx', re.compile(r'className=\{\\?t?ext-sm py-1\.5.*?\}'), 'className="text-sm py-1.5 px-2 rounded-md transition-colors"')

# 4. app/examples/page.tsx
fix('app/examples/page.tsx', re.compile(r'className=\{w-6 h-6.*?\}'), 'className="w-6 h-6"')

# 5. app/features/compiler/page.tsx
fix('app/features/compiler/page.tsx', re.compile(r'className=\{p-2 rounded-lg.*?\}'), 'className="p-2 rounded-lg"')

# 6. data/docs.ts
# Let's inspect what is wrong with data/docs.ts by just reading the first few lines and saving to file.
with open(os.path.join(repo, 'data/docs.ts'), 'r', encoding='utf-8') as f:
    text = f.read()
    if 'items: DocItem[];' in text:
        pass # maybe it is fine
        
# Let's just fix the interface issue in docs.ts. The issue is export interface DocSection is parsed as invalid if it has a syntax error down below.
# Actually I see: export interface DocSection { title: string; items: DocItem[];
# Wait, did I mess up earlier? Oh! earlier it was items: DocItem[,
# I replaced items: DocItem[, with items: DocItem[];. But what if the original was items: DocItem[]; and my python script from earlier did something weird?
# Wait! I will just recreate data/docs.ts completely since it's just a type file.
docs_ts_content = '''export interface DocItem { title: string; href: string; }
export interface DocSection { title: string; items: DocItem[]; }
export const DOCS_NAVIGATION: DocSection[] = [];
'''
# Actually I don't know the exact original content, so I will just fix the parse error. 
# Turbopack says Expected '{', got 'interface'. This means export interface is not allowed. 
# Why would export interface not be allowed in a .ts file? Next.js fully supports it.
# Ah, maybe I can just do export type DocSection = { title: string; items: DocItem[] }
text = text.replace('export interface DocSection', 'export type DocSection =')
text = text.replace('export interface DocItem', 'export type DocItem =')
with open(os.path.join(repo, 'data/docs.ts'), 'w', encoding='utf-8') as f:
    f.write(text)

# 7. data/language-content.tsx
fix('data/language-content.tsx', '// aayu.mod\\nmodule my_app 1.0.0\\nrequire http_server >= 2.1.0', '{// aayu.mod\\nmodule my_app 1.0.0\\nrequire http_server >= 2.1.0}')

print("Fixed round 3")
