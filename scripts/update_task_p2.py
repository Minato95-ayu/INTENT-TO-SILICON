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

﻿import os

task_path = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'
with open(task_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('[/] Phase 2: Playground & FastAPI Backend', '[x] Phase 2: Playground & FastAPI Backend')
content = content.replace('[ ] Create FastAPI pi/main.py', '[x] Create FastAPI pi/main.py')
content = content.replace('[ ] Connect Next.js playground to API', '[x] Connect Next.js playground to API')
content = content.replace('[ ] Phase 3: BrainOS Real Intelligence', '[/] Phase 3: BrainOS Real Intelligence')

with open(task_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated task.md for Phase 2")
