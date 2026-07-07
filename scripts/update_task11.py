"""
=============================================================================
FILE: update_task11.py
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

phases_to_mark = [
    '[ ] **Phase 2: Documentation**',
    '[ ] Installation & Getting Started',
    '[ ] Language Guide & CLI',
    '[ ] Standard Library & Package Manager',
    '[ ] BrainOS & Intent Engine',
    '[ ] Examples & FAQ',
    '[ ] **Phase 3: Playground**',
    '[ ] Interactive Editor UI',
    '[ ] Real execution backend (or simulated until WASM)',
    '[ ] **Phase 4: Package Registry UI**',
    '[ ] Search & Categories',
    '[ ] Official & Community Packages layout'
]

for item in phases_to_mark:
    content = content.replace(item, item.replace('[ ]', '[x]'))

with open(r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md', 'w', encoding='utf-8') as f:
    f.write(content)
