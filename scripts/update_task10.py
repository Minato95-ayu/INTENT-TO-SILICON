"""
=============================================================================
FILE: update_task10.py
PURPOSE: Updates system components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles updates system components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os

with open(r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('[ ] **Phase 1: Website Complete**', '[x] **Phase 1: Website Complete**')

# Update the sub-items for Phase 1 as well
for item in ['Update Navbar and Footer links', '/docs', '/playground', '/packages', '/brainos', '/intent-engine', '/roadmap', '/download', '/blog', '/community', '/about', '/contact']:
    content = content.replace(f'[ ] {item}', f'[x] {item}')

with open(r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md', 'w', encoding='utf-8') as f:
    f.write(content)
