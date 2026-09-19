# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import re

with open("website/app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add download button in hero section near GitHub
hero_buttons = '''              <Link href="https://github.com/Minato95-ayu/INTENT-TO-SILICON" target="_blank">
                <Button className="h-full px-6 bg-white text-black hover:bg-zinc-200 font-bold rounded-xl gap-2">
                  <GitBranch className="w-4 h-4" /> GitHub
                  <ExternalLink className="w-3 h-3 ml-1 opacity-50" />
                </Button>
              </Link>'''
new_hero_buttons = '''              <Link href="/download">
                <Button className="h-full px-6 bg-cyan-500 text-black hover:bg-cyan-400 font-bold rounded-xl gap-2">
                  <Download className="w-4 h-4" /> Download AAYU
                </Button>
              </Link>
              <Link href="https://github.com/Minato95-ayu/INTENT-TO-SILICON" target="_blank">
                <Button className="h-full px-6 bg-white text-black hover:bg-zinc-200 font-bold rounded-xl gap-2">
                  <GitBranch className="w-4 h-4" /> GitHub
                  <ExternalLink className="w-3 h-3 ml-1 opacity-50" />
                </Button>
              </Link>'''

content = content.replace(hero_buttons, new_hero_buttons)

# Write back
with open("website/app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated page.tsx")
