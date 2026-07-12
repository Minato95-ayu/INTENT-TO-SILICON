import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\task.md'
if not os.path.exists(filepath):
    filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'

content = '''# Developer Operating System - V2 Architecture

## ✅ Sprint 1: Top 5 Core Experiences

### 1. Homepage (Developer OS)
- [ ] Hero: Live BrainOS Generator
- [ ] Install, Playground, Docs, Examples quick links
- [ ] Interactive Compiler Pipeline overview
- [ ] Recent Releases & Docs Search
- [ ] Examples Grid preview

### 2. Documentation Engine (MDX)
- [ ] Install \
ext-mdx-remote\ and \gray-matter\
- [ ] Create \content/docs\ folder structure
- [ ] Build MDX parser and auto-generated Sidebar
- [ ] Build real Search (Ctrl+K) over MDX files
- [ ] Map shared components (CodeBlock, Playground, Pipeline, Diagram)

### 3. Playground
- [ ] Split-Screen Editor (Tokens, AST, IR, Architecture, Bytecode, Runtime, Console, BrainOS Review)
- [ ] Buttons: Run, Build, Format, Lint, Download, Share

### 4. BrainOS Portal
- [ ] Interactive Flow diagram (Human Thought -> Intent -> Knowledge -> Decision -> Tradeoff -> Architecture -> Planner -> Code -> Compiler -> Runtime)
- [ ] Clickable nodes with explanations

### 5. Download Center
- [ ] Channels: Stable, Nightly, Preview, Source
- [ ] Artifacts: CLI, VSIX, Source Code, Checksums (SHA256)
- [ ] Guides: Installation, Troubleshooting, Requirements, Release Notes
- [ ] Authenticity: "Coming in v1.0" badges
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated task.md for V2 Architecture.")
