import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\task.md'
if not os.path.exists(filepath):
    filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'

content = '''# Developer Operating System - Vercel/Linear Quality Upgrade

## ✅ Priority 1 — Homepage (Sabse pehle)
- [ ] Hero me Live Project Generator ("Describe your app -> Build")
- [ ] "Build" animation
- [ ] Human Thought -> Intent Engine -> BrainOS -> AAYU -> Production pipeline
- [ ] Live architecture preview
- [ ] Real examples
- [ ] Zero fake stats

## ✅ Priority 2 — Playground
- [ ] Split screen IDE
- [ ] Live tabs: Source Code, Tokens, AST, Semantic, Optimizer, Bytecode, Runtime, Console, BrainOS Review

## ✅ Priority 3 — Documentation
- [ ] Breadcrumb, Search (Ctrl+K), Copy Button
- [ ] Edit on GitHub, Previous / Next
- [ ] Examples, Common Errors, Best Practices, Interactive diagrams

## ✅ Priority 4 — Download Center
- [ ] Stable, Preview, Nightly, Source, VS Code Extension
- [ ] Release Notes, Checksums, Installation, Verification, Troubleshooting
- [ ] Strictly enforce "Coming in v1.0" for missing binaries

## ✅ Priority 5 — Architecture Explorer
- [ ] Interactive zoomable graph (Lexer to Runtime)
- [ ] Side panel with Purpose, Source files, Examples, Output, Documentation

## ➕ Additional Portals
- [ ] Developer Dashboard (Projects, Jobs, Logs)
- [ ] Learn Portal (Roadmap: Beginner -> Syntax -> BrainOS)
- [ ] Examples Gallery (Real templates with Architecture, Source Code)
- [ ] Remove Fake Benchmarks (Enforce Authenticity Rule)
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Created new task list based on user's priority order.")
