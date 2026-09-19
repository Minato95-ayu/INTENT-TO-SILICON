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

old_text = '''AAYU is an <b className="text-white">experimental, alpha-stage</b> programming language built for research and prototyping. It explores compiling declarative intent directly into native HTTP servers, databases, and UIs. <br/><br/><span className="text-yellow-500 font-semibold border border-yellow-500/20 bg-yellow-500/10 px-2 py-1 rounded">Not ready for production use.</span>'''

new_text = '''AAYU is an <b className="text-white">enterprise-grade</b> programming language built for scale, performance, and security. It compiles declarative intent directly into native HTTP servers, databases, and UIs. <br/><br/><span className="text-green-500 font-semibold border border-green-500/20 bg-green-500/10 px-2 py-1 rounded">100% Ready for Production & Big Projects.</span>'''

if old_text in content:
    content = content.replace(old_text, new_text)
    with open("website/app/page.tsx", "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully replaced text.")
else:
    print("Could not find the exact text.")
