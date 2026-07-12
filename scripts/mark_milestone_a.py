import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\task.md'
if not os.path.exists(filepath):
    filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Specifically checking off the BrainOS MVP tasks under Milestone A
content = content.replace('## 🥇 Milestone A: BrainOS MVP (Highest Priority)\n- [ ] Decision Engine\n- [ ] Recommendation Engine\n- [ ] Tradeoff Engine\n- [ ] Architecture Generator\n- [ ] Project Scaffold Generator\n- [ ] Tests & Documentation',
                          '## 🥇 Milestone A: BrainOS MVP (Highest Priority)\n- [x] Decision Engine\n- [x] Recommendation Engine\n- [x] Tradeoff Engine\n- [x] Architecture Generator\n- [x] Project Scaffold Generator\n- [x] Tests & Documentation')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Checked off BrainOS MVP tasks.")
