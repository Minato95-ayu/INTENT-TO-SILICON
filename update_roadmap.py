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

# Replace 'status: "in-progress"' with 'status: "completed"' for the first 5
replacements = [
    ('id: "A",\n    title: "Language Core",\n    status: "in-progress"', 'id: "A",\n    title: "Language Core",\n    status: "completed"'),
    ('id: "B",\n    title: "Native HTTP Runtime",\n    status: "in-progress"', 'id: "B",\n    title: "Native HTTP Runtime",\n    status: "completed"'),
    ('id: "C",\n    title: "Native Storage Runtime",\n    status: "in-progress"', 'id: "C",\n    title: "Native Storage Runtime",\n    status: "completed"'),
    ('id: "CLI",\n    title: "CLI & Tooling",\n    status: "in-progress"', 'id: "CLI",\n    title: "CLI & Tooling",\n    status: "completed"'),
    ('id: "STD",\n    title: "Standard Library",\n    status: "in-progress"', 'id: "STD",\n    title: "Standard Library",\n    status: "completed"')
]

for old, new in replacements:
    content = content.replace(old, new)

with open("website/app/roadmap/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated roadmap page")
