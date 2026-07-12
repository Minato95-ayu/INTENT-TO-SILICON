import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\task.md'
if not os.path.exists(filepath):
    filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'

content = '''# AAYU v1.0 Roadmap

## 🚀 Week 1: Developer Platform (Current Focus)
- [ ] Intent Engine Portal (/intent-engine)
- [ ] Architecture Explorer (/architecture)
- [ ] Examples Gallery (/examples)
- [ ] Playground Backend Integration (Connect UI to AST/Pipeline)

## 🚀 Week 2: Intelligence & BrainOS
- [ ] BrainOS A2 (Cost, Security, Alts, Multi-domain)
- [ ] BrainOS A3 (DB schema, Docker, CI/CD, Tests gen)
- [ ] Intent Engine (NLP, Knowledge Graph)

## 🚀 Week 3: Tools & Release
- [ ] VS Code Extension
- [ ] CLI Polish
- [ ] Release Candidate
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated task.md for Week 1-3.")
