"""
=============================================================================
FILE: update_cli_docs.py
PURPOSE: Updates CLI documentation
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles updates cli documentation.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os
import json

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\data\docs.ts'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

cli_docs = """
  {
    title: "Toolchain & CLI",
    items: [
      {
        slug: "cli",
        title: "CLI Reference",
        introduction: "The AAYU CLI is the single entry point for all development operations. It includes the compiler, formatter, linter, and BrainOS interface.",
        syntax: "aayu <command> [options]",
        examples: [
          {
            code: "aayu init my_app",
            explanation: "Scaffolds a new AAYU project with the standard directory structure."
          },
          {
            code: "aayu run main.aayu",
            explanation: "Compiles and immediately executes the script via the VM."
          },
          {
            code: "aayu build src/",
            explanation: "Compiles the source directory into an optimized production binary."
          },
          {
            code: "aayu fmt .",
            explanation: "Formats all AAYU code in the current directory."
          },
          {
            code: "aayu lint",
            explanation: "Runs static analysis and Intent graph validation."
          },
          {
            code: "aayu package install",
            explanation: "Resolves and installs dependencies from AAYU Registry."
          },
          {
            code: "aayu doctor",
            explanation: "Checks environment setup, dependencies, and memory constraints."
          },
          {
            code: "aayu brainos analyze",
            explanation: "Forces the BrainOS engine to output architectural tradeoffs for the current project."
          }
        ],
        bestPractices: [
          "Use 'aayu doctor' whenever you encounter weird environment errors.",
          "Run 'aayu fmt' before committing code to maintain a clean codebase."
        ],
        commonErrors: [
          {
            error: "Error: No BrainOS knowledge base found.",
            fix: "Ensure you are running AAYU inside an initialized project (aayu init) or that the global KB path is set."
          }
        ]
      }
    ]
  }
"""

# Insert the CLI section before the last element (which is Architecture Components)
if "];" in content:
    content = content.replace("];", ",\n" + cli_docs + "\n];")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected CLI docs into docs.ts")
