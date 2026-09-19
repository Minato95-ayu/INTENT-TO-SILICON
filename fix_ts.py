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

with open("website/app/roadmap/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the array definition
content = content.replace("const phases = [", "const phases: Phase[] = [")

with open("website/app/roadmap/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("roadmap/page.tsx fixed TypeScript error")
