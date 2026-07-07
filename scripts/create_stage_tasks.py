import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\task.md'
if not os.path.exists(filepath):
    filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'

content = '''# AAYU v1.0 Roadmap

## 🚀 Stage 1: Website (In Progress - Needs Real Compiler Hookup)
- [x] Landing Page
- [x] Documentation
- [ ] Playground (Real Backend Connection)
- [x] Download Center
- [x] Examples
- [x] Architecture Explorer
- [x] BrainOS Portal
- [x] Intent Engine Portal

## 🚀 Stage 2: BrainOS Intelligence (Current Focus)
- [ ] Cost Engine
- [ ] Security Review
- [ ] Performance Review
- [ ] Architecture Review
- [ ] Multi-domain reasoning

## 🚀 Stage 3: Intent Engine
- [ ] Offline NLP, Intent IR, Knowledge Graph

## 🚀 Stage 4: Developer Tools
- [ ] VS Code Extension, Language Server, CLI

## 🚀 Stage 5: Release
- [ ] README, Benchmarks, CI/CD, Installers
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated task.md for Stage 1-5.")
