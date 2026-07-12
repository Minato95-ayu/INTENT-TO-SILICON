import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\task.md'
if not os.path.exists(filepath):
    filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'

content = '''# AAYU v1.0 Milestones

## 🥇 Milestone A: BrainOS MVP (Highest Priority)
- [ ] Decision Engine
- [ ] Recommendation Engine
- [ ] Tradeoff Engine
- [ ] Architecture Generator
- [ ] Project Scaffold Generator
- [ ] Tests & Documentation

## 🥈 Milestone B: Website Production Ready
- [ ] Homepage, BrainOS Portal, Playground polish
- [ ] Real Docs & Examples
- [ ] Download Center strict authenticity

## 🥉 Milestone C: Intent Engine Production Ready
- [ ] Offline NLP & Knowledge Graph
- [ ] Domain Packs & Engineering Rules
- [ ] Clarification Engine & API Generator

## 🏅 Milestone D: Developer Tools
- [ ] VS Code Extension (LSP)
- [ ] CLI, Formatter, Linter

## 🏆 Milestone E: AAYU v1.0 Release Candidate
- [ ] Tests, CI/CD, README, Deployments
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated task.md with Milestones A-E.")
