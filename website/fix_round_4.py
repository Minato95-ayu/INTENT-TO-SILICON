import os

repo = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website'

def replace_exact(path_suffix, old, new):
    path = os.path.join(repo, path_suffix)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            t = f.read()
        t = t.replace(old, new)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(t)

# 1. lib/mdx.ts
replace_exact('lib/mdx.ts', 'const fullPath = path.join(DOCS_DIR, category, .mdx);', 'const fullPath = path.join(DOCS_DIR, category, ${slug}.mdx);')

# 2. app/examples/page.tsx
replace_exact('app/examples/page.tsx', 'href={https://github.com/Minato95-ayu/AAYU/tree/main/examples/\}', 'href="https://github.com/Minato95-ayu/AAYU/tree/main/examples/"')

# 3. app/brainos/page.tsx
replace_exact('app/brainos/page.tsx', 'className={ bsolute top-0 right-0 w-64 h-64 blur-[100px] rounded-full opac...', 'className="absolute top-0 right-0 w-64 h-64 blur-[100px] rounded-full opacity-20 bg-blue-500"')
# Wait the log truncated it. Let's do a substring match.
path3 = os.path.join(repo, 'app/brainos/page.tsx')
with open(path3, 'r', encoding='utf-8') as f:
    text3 = f.read()
import re
text3 = re.sub(r'className=\{\s?bsolute top-0 right-0.*?\}', 'className="absolute top-0 right-0 w-64 h-64 blur-[100px] rounded-full opacity-20 bg-blue-500"', text3)
with open(path3, 'w', encoding='utf-8') as f:
    f.write(text3)

# 4. app/docs/layout.tsx
path4 = os.path.join(repo, 'app/docs/layout.tsx')
with open(path4, 'r', encoding='utf-8') as f:
    text4 = f.read()
text4 = re.sub(r'className=\{.*?ext-sm py-1\.5.*?\}', 'className="text-sm py-1.5 px-2 rounded-md transition-colors"', text4)
with open(path4, 'w', encoding='utf-8') as f:
    f.write(text4)

# 5. app/features/compiler/page.tsx
path5 = os.path.join(repo, 'app/features/compiler/page.tsx')
with open(path5, 'r', encoding='utf-8') as f:
    text5 = f.read()
text5 = re.sub(r'className=\{h-8 w-px my-2 transition-colors \}', 'className="h-8 w-px my-2 transition-colors"', text5)
with open(path5, 'w', encoding='utf-8') as f:
    f.write(text5)

# 6. data/docs.ts
# It failed parsing export type. Let's just make it a pure object export.
path6 = os.path.join(repo, 'data/docs.ts')
with open(path6, 'w', encoding='utf-8') as f:
    f.write('''export const DOCS_NAVIGATION = [
  {
    title: "Getting Started",
    items: [
      { title: "Introduction", href: "/docs/introduction" },
      { title: "Installation", href: "/docs/installation" },
      { title: "Quick Start", href: "/docs/quick-start" }
    ]
  },
  {
    title: "Core Concepts",
    items: [
      { title: "Intent Graph", href: "/docs/intent-graph" },
      { title: "BrainOS", href: "/docs/brainos" },
      { title: "Compiler Pipeline", href: "/docs/compiler-pipeline" }
    ]
  }
];
''')

# 7. data/language-content.tsx
path7 = os.path.join(repo, 'data/language-content.tsx')
with open(path7, 'r', encoding='utf-8') as f:
    text7 = f.read()
text7 = text7.replace('{// aayu.mod\\nmodule my_app 1.0.0\\nrequire http_server >= 2.1.0}', '{"// aayu.mod\\nmodule my_app 1.0.0\\nrequire http_server >= 2.1.0"}')
# Just in case the previous replacement left it bare again
text7 = re.sub(r'\{?// aayu.mod\nmodule my_app 1\.0\.0\nrequire http_server >= 2\.1\.0\}?', '{"// aayu.mod\\nmodule my_app 1.0.0\\nrequire http_server >= 2.1.0"}', text7)
with open(path7, 'w', encoding='utf-8') as f:
    f.write(text7)

print("Fixed round 4")
