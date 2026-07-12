"""
=============================================================================
FILE: create_skeletons.py
PURPOSE: Generates project skeleton templates
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles generates project skeleton templates.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os

base_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app'
directories = ['language', 'examples', 'learn', 'privacy', 'terms']

for d in directories:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)
    with open(os.path.join(base_dir, d, 'page.tsx'), 'w', encoding='utf-8') as f:
        f.write(f'''
export default function {d.capitalize()}Page() {{
  return (
    <main className="min-h-screen bg-black text-white pt-24 pb-20 px-4">
      <div className="container mx-auto max-w-5xl">
        <h1 className="text-4xl font-bold mb-8 capitalize">{d} Portal</h1>
        <p className="text-zinc-400">Content for {d} is currently being assembled from the AAYU compiler source.</p>
      </div>
    </main>
  );
}}
''')

print("Created skeleton directories to prevent 404s.")
