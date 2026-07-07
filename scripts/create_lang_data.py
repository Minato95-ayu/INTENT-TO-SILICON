"""
=============================================================================
FILE: create_lang_data.py
PURPOSE: Generates language data structures
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles generates language data structures.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os

base_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website'

language_data = '''
export const languageNavData = [
  {
    title: "Getting Started",
    items: [
      { slug: "overview", title: "Overview" },
      { slug: "why-aayu", title: "Why AAYU" },
      { slug: "installation", title: "Installation" }
    ]
  },
  {
    title: "Language Guide",
    items: [
      { slug: "syntax", title: "Syntax" },
      { slug: "variables", title: "Variables" },
      { slug: "functions", title: "Functions" },
      { slug: "modules", title: "Modules & Packages" },
      { slug: "interfaces", title: "Interfaces" },
      { slug: "extensions", title: "Extensions & Traits" },
      { slug: "generics", title: "Generics" },
      { slug: "type-system", title: "Type System" }
    ]
  },
  {
    title: "Internals",
    items: [
      { slug: "compiler", title: "Compiler Pipeline" },
      { slug: "runtime", title: "Runtime & VM" },
      { slug: "bytecode", title: "Bytecode Architecture" },
      { slug: "optimizer", title: "Optimizer" },
      { slug: "reflection", title: "Reflection" }
    ]
  },
  {
    title: "Tooling",
    items: [
      { slug: "cli", title: "CLI Reference" },
      { slug: "package-manager", title: "Package Manager" },
      { slug: "formatter", title: "Formatter" },
      { slug: "linter", title: "Linter" },
      { slug: "debugger", title: "Debugger" },
      { slug: "vscode", title: "VS Code Extension" }
    ]
  },
  {
    title: "Resources",
    items: [
      { slug: "faq", title: "FAQ" }
    ]
  }
];
'''

with open(os.path.join(base_dir, 'data', 'language.ts'), 'w', encoding='utf-8') as f:
    f.write(language_data)

print("Created language.ts data file.")
