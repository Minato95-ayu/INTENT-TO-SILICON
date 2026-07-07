import os

filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'

content = '''# AAYU Developer Operating System Tasks

## 🚀 The Killer Features (In Progress)
- [ ] **Interactive Homepage Hero (/)**
- [ ] **Live BrainOS Demo (/brainos/live)**
- [ ] **Deep Architecture Explorer (/architecture)**

## 🛠️ Deepening the Core Portals
- [ ] **Advanced Playground Update** (10 tabs, simulated deterministic data)
- [ ] **Download Center & VS Code Realism** (Enforce Authenticity Rule)
- [ ] **The Big 3 Identities** (Solidify AAYU, BrainOS, Intent Engine portals)
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated task.md")
