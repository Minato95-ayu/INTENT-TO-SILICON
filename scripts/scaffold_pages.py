"""
=============================================================================
FILE: scaffold_pages.py
PURPOSE: Scaffolds web pages
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles scaffolds web pages.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os

base_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app'

pages = [
    ('docs', 'Documentation'),
    ('playground', 'Playground'),
    ('packages', 'Package Registry'),
    ('brainos', 'BrainOS'),
    ('intent-engine', 'Intent Engine'),
    ('roadmap', 'Roadmap'),
    ('download', 'Download'),
    ('blog', 'Blog'),
    ('community', 'Community'),
    ('about', 'About Us'),
    ('contact', 'Contact')
]

template = '''
export default function Page() {
  return (
    <main className="min-h-screen bg-black text-white flex items-center justify-center pt-24 pb-16">
      <div className="container mx-auto px-4 text-center">
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
          {title}
        </h1>
        <p className="text-xl text-zinc-400 max-w-2xl mx-auto mb-8">
          This section is currently under development for the v1.0 release.
        </p>
        <div className="inline-block rounded-full border border-blue-500/30 bg-blue-500/10 px-4 py-1.5 text-sm font-medium text-blue-300">
          Coming Soon
        </div>
      </div>
    </main>
  );
}
'''

for path, title in pages:
    dir_path = os.path.join(base_dir, path)
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, 'page.tsx'), 'w', encoding='utf-8') as f:
        f.write(template.replace('{title}', title))

print("Scaffolded all pages.")
