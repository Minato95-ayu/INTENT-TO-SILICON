"""
=============================================================================
FILE: append_docs.py
PURPOSE: Appends documentation files
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles appends documentation files.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import json
import os
import re

file_path = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\data\docs.ts'

# The topics to add
categories = {
    "Language Features": ["Variables", "Modules", "Packages", "Interfaces", "Extensions", "Generics", "Type System"],
    "Internals": ["Compiler", "Bytecode", "Runtime"],
    "Tooling": ["Standard Library", "CLI", "Formatter", "Linter", "Package Manager"],
    "Ecosystem": ["BrainOS", "Intent Engine", "Architecture"],
    "Resources": ["Examples", "FAQ", "Contributing"]
}

# we'll use regex to append to the array.
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# build new sections
new_sections = ""
for category, items in categories.items():
    section_str = f'  {{\n    title: "{category}",\n    items: [\n'
    for item in items:
        slug = item.lower().replace(' ', '-')
        section_str += f'''      {{
        slug: "{slug}",
        title: "{item}",
        introduction: "Documentation for {item} is currently being written.",
        examples: [],
        bestPractices: [],
        commonErrors: []
      }},\n'''
    section_str += '    ]\n  },\n'

# insert before the last ];
content = content.replace('];\n\nexport function', f',\n{new_sections}];\n\nexport function')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added missing sections to docs.ts")
