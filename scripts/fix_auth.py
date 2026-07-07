import os
import re

# 1. Update page.tsx
p1 = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\page.tsx'
with open(p1, 'r', encoding='utf-8') as f:
    c1 = f.read()

c1 = c1.replace('curl -fsSL aayu.dev | bash', 'git clone https://github.com/Minato95-ayu/AAYU.git')
# Add "Simulation" badge to playground
c1 = c1.replace('<span className="text-sm font-bold text-zinc-300">Interactive Playground</span>',
                '<span className="text-sm font-bold text-zinc-300">Interactive Playground</span><span className="ml-2 text-[10px] font-bold text-yellow-500 bg-yellow-500/10 border border-yellow-500/20 px-1.5 py-0.5 rounded">Simulation</span>')

with open(p1, 'w', encoding='utf-8') as f:
    f.write(c1)


# 2. Update download/page.tsx
p2 = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\download\page.tsx'
with open(p2, 'r', encoding='utf-8') as f:
    c2 = f.read()

c2 = c2.replace('curl -fsSL https://aayu.dev/install-nightly.sh | bash', 'git clone -b nightly https://github.com/Minato95-ayu/AAYU.git')

with open(p2, 'w', encoding='utf-8') as f:
    f.write(c2)


# 3. Update installation.mdx
p3 = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\content\docs\getting-started\installation.mdx'
with open(p3, 'r', encoding='utf-8') as f:
    c3 = f.read()

c3 = c3.replace('curl -fsSL https://aayu.dev/install.sh | bash', 'git clone https://github.com/Minato95-ayu/AAYU.git')
c3 = c3.replace('https://github.com/aayu/aayu.git', 'https://github.com/Minato95-ayu/AAYU.git')

with open(p3, 'w', encoding='utf-8') as f:
    f.write(c3)

print("Authenticity fixes applied.")
