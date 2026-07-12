import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\task.md'
if not os.path.exists(filepath):
    filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'

content = '''# Developer Operating System - Sprint 2 Execution

## ✅ Phase A — Trust & Authenticity Audit
- [ ] Ensure real GitHub links (Minato95-ayu/AAYU)
- [ ] Remove fake curl aayu.dev/install.sh everywhere
- [ ] Add "Simulation" badge to Playground/BrainOS
- [ ] Add "Planned" to VS Code extension
- [ ] No fake stats, benchmarks, or release counts

## ✅ Phase B — Information Architecture
- [ ] Homepage: Organize strictly into 3 pillars (AAYU Language, BrainOS, Intent Engine) with clear features under each

## ✅ Phase C — Real Documentation
- [ ] Build consistent template (Overview, Why, Syntax, Example, Output, Common Errors, Best Practices, Related Topics)
- [ ] Write 12 core MDX pages

## ✅ Phase D & E — Cross-linking & Learning Path
- [ ] Inject cross-links (Compiler -> Playground -> Architecture Explorer)
- [ ] Implement guided roadmap in Docs
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Created Phase A-E tasks.")
